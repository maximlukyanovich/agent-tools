# mluk-deploy

How a project is deployed. Knowledge only: skills, no hooks; the one command is `/mluk-deploy:help`. Enable it in any
project that deploys; working on a live server additionally needs `mluk-ops`.

## Install

```bash
claude plugin install mluk-deploy --marketplace maximlukyanovich/agent-tools --scope project
```

Other scopes and updating: [Quick start](../../README.md#quick-start).

## Skills

| Skill | For |
| --- | --- |
| [`deploy-vps`](skills/deploy-vps/SKILL.md) | a Docker Compose backend on a VPS behind Caddy, deployed by GitHub Actions |
| [`deploy-vercel`](skills/deploy-vercel/SKILL.md) | a Next.js front on Vercel: projects, env vars, domains, staging gate |
| [`domain-dns`](skills/domain-dns/SKILL.md) | moving DNS to Cloudflare without breaking mail; subdomain naming; mail roles |

The concrete files live in the project (compose, scripts, Caddy sites, runbook). The skills carry the
reasoning and the traps.

## In use

Nothing to invoke: the agent loads a skill when the work reaches it. "Set up a
staging site on Vercel" brings `deploy-vercel`, "move example.com's DNS to
Cloudflare" brings `domain-dns`, "deploy the backend to a fresh VPS" brings
`deploy-vps` — and once the agent works on the server itself, `server-ops`
from `mluk-ops`.
