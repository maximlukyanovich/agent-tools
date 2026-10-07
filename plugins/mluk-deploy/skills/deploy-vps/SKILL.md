---
name: deploy-vps
description: The deployment scheme for a backend on a single VPS — Docker Compose stack per environment behind Caddy on the host, image built on the server and tagged by commit, GitHub Actions deploy over SSH gated by a repository variable, a bootstrap script for a fresh Ubuntu host, and the traps met along the way. Use when setting up, changing or debugging a VPS deployment. For work on the live server itself, load server-ops (mluk-ops).
---

# deploy-vps

The scheme for a backend (Django/DRF + Celery + Postgres + Redis was the
first; nothing below depends on Django). The project keeps the concrete files:
- `Dockerfile`, `docker-compose.server.yml`, `deploy/server/{bootstrap,deploy,rollback}.sh`;
- the Caddy site files;
- the env templates;
- a runbook `docs/deploy.md`.

This skill is the reasoning behind them.

## Shape

```
Caddy on the host (80/443, TLS by itself) ─► 127.0.0.1:${API_PORT} ─► api (gunicorn)
   ├── static/media straight from bind-mounted var/            ├── db, cache — no published ports
   └── internal tools (/mailpit/) behind basic_auth             └── workers, scheduler
```

- **One compose project per environment**, each in its own checkout (`/srv/<project>/<env>/app/repo`)
  with its own `.env`. `COMPOSE_PROJECT_NAME` is mandatory, and the compose file refuses to start
  without it (`${VAR:?}`). Otherwise two checkouts named `repo` share containers and volumes.
- **Only the app is published, and only on 127.0.0.1.** Database and cache publish nothing.
- **`restart: unless-stopped`** on every service, or a reboot leaves the stack down.
- **The container runs as a non-root user whose uid matches the host user.** Bind-mounted `var/` then
  stays writable from both sides, and Caddy (on the host) can read static and media.
- **Migrations and `collectstatic` run in the entrypoint of the `api` service only**, behind flags.
  Workers built from the same image never run them. The image build never touches a database.
- **A `/health/` endpoint that checks the database**, used by the container healthcheck, the deploy
  script and external uptime monitoring.
- **Logs go to stdout.** `/etc/docker/daemon.json` caps them (`max-size 10m`, `max-file 3`).

## Build and rollback without a registry

The image is built on the server, tagged `:latest` and `:<commit sha>` (compose `build.tags`). A
deploy script:
1. pulls;
2. runs `up -d --build`;
3. waits for the healthcheck;
4. keeps the last three sha tags;
5. prunes week-old build cache.

Rollback is re-tagging an old sha as `:latest` and `up -d --no-build`: seconds, no rebuild.
Migrations are not reversed by it.

A registry (GHCR) becomes worth it when the build starts hurting the server or there is more than
one host. Check the Packages billing first: GHCR storage is free for now, and GitHub has announced
it will be billed.

## CI

- `tests.yml` on every PR; the deploy workflow calls it (`workflow_call`) before touching the server.
- **Deploy over SSH** (`appleboy/ssh-action`):
  - one key per environment, in GitHub Environment secrets (`SSH_HOST`, `SSH_USER`,
    `SSH_PRIVATE_KEY`, `DEPLOY_PATH`);
  - the variable `HEALTH_URL`, checked with `curl` from outside after the deploy.
- **The switch is a repository variable** (`DEPLOY_<ENV>_ENABLED == 'true'` in the job's `if`).
  Environment variables are not visible in a job-level `if`. The switch lets the workflow merge
  before the server is ready. `gh workflow disable` cannot be used for that, because a new
  workflow's first push already runs it.
- `concurrency: cancel-in-progress: false`. Cancelling mid-`up --build` leaves a half state, and
  GitHub keeps only the latest pending run anyway.
- **The production workflow starts as `workflow_dispatch` only**, until production exists.
- **The server pulls a private repository with its own read-only deploy key**, through an SSH host
  alias in `~/.ssh/config`. Pin github.com's host key after checking its published fingerprint.
- **The Actions key gets a forced command** in `authorized_keys`
  (`restrict,command="cd … && git pull … && deploy/server/deploy.sh"`): the workflow sends nothing
  meaningful, and a key leaked from GitHub can only trigger a deploy.

## Fresh host (Ubuntu LTS)

**Caddy runs from its official Docker image** (`caddy:2.x`, its own compose project, host networking,
configs from `/etc/caddy`, certificates in a volume). Its apt repository has been signed with an
expired subkey since 2024, and a stale source then breaks every `apt update`.

A bootstrap script, run once as root, safe to rerun:
- updates and `unattended-upgrades`;
- Docker from Docker's repository, with capped logs;
- `/etc/caddy` with `import /etc/caddy/sites/*.caddy` (Caddy itself comes from the image);
- a `deploy` user with root's keys, the docker group and sudo;
- `/srv/<project>`;
- UFW (22/80/443);
- a weekly `docker image/builder prune`.

The script removes known-broken apt sources **before** its first `apt-get update`, logs to a file, and
prints the failing line on an error. Test it end to end in a clean container of the same release —
including a rerun from a half-done state — before handing it to the owner.

Then, as separate steps:

1. **Test the `deploy` login from a second terminal.**
2. **Close root and password logins** in `/etc/ssh/sshd_config.d/00-hardening.conf`. The `00-` prefix
   matters: sshd keeps the first value it reads, and cloud images ship `50-cloud-init.conf` with
   `PasswordAuthentication yes`. On Ubuntu 24.04 the service is `ssh`.
3. **Add a provider firewall** (Hetzner Cloud) with the same three ports: one layer outside the
   machine.
4. **Check `authorized_keys` for keys left from before a rebuild.** Provider-attached keys survive a
   Rebuild.

## Traps

- **Caddy and `X-Forwarded-Host`.** Caddy **replaces** `X-Forwarded-*` from clients it does not trust.
  When a web front proxies the API server-side and the backend builds URLs from `X-Forwarded-Host`
  (Django `USE_X_FORWARDED_HOST`, e.g. social-login callbacks), pass it on explicitly for requests
  that carry it:

  ```
  @via_web header X-Forwarded-Host *
  handle @via_web { reverse_proxy … { header_up X-Forwarded-Host {header.X-Forwarded-Host} } }
  ```

  The backend still validates it against `ALLOWED_HOSTS`. Verify it with an echo upstream before
  trusting it.
- **Slow requests.** Anything slow inside a request needs a gunicorn `--timeout` above it. Caddy sets
  no response timeout; Cloudflare's proxy cuts at 100 s (524). See domain-dns.
- **The health endpoint and `SECURE_SSL_REDIRECT`.** The container healthcheck calls the app over
  plain HTTP on 127.0.0.1. Exempt the health path from the redirect and include `127.0.0.1` in
  `ALLOWED_HOSTS`.
- **Absolute media URLs.** `build_absolute_uri` keeps an absolute `MEDIA_URL` as is. Use it so images
  point at the host that serves them, not at the proxying web origin.
- **Object storage tokens filtered by client IP** must list the server's IPv6 range too: Linux prefers
  IPv6 when the endpoint has it, and the request then fails as if the key were wrong.
- **Hosts that are not the site still need noindex**: the API host (`X-Robots-Tag` + its own
  `robots.txt` in the proxy) and a public media bucket (a `robots.txt` object).
- **Config values that live outside the database** (e.g. django-constance on Redis) do not travel
  with a `pg_dump`. Export them separately when seeding an environment.
- **`POSTGRES_PASSWORD` only initialises a new volume.** Changing it later needs `ALTER USER`.
- **`.env` exists only on the server.** Keep an encrypted copy elsewhere (password manager or
  sops/age).
- **Rehearse before the server.** Run the server compose locally in a scratch copy, with its own
  `.env` and `COMPOSE_PROJECT_NAME`, so the owner's dev stack is untouched. Test: two deploys, then a
  rollback, then a restore of a real dump. It catches most of the above before a live host sees it.
