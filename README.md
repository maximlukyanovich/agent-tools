# agent-tools

Claude Code plugins for working on a software project with an agent: setting up
a repository's agent harness, the everyday git workflow, frontend conventions,
deployment, safe server access and business Russian copy. One author's toolkit,
grown on real projects and open to anyone — the rules are opinionated, and each
project tunes them through its own profile.

One repository: it is both the marketplace (`mluk-agent-tools`) and the home of
the plugins.

Why it exists: the method must not live as copies in every repository. How a
task is started, how a commit and a pull request are written, how a review is
run, how Russian client copy is phrased — these are the same in every project;
only the branch chain, the validate command and the domain differ, and those
stay in the project.

## Does it fit your project

Each plugin is enabled on its own, so a project takes only what fits. Some work
anywhere; the rest follow the stack they were grown on.

**Any project:**

- `mluk-bootstrap` — sets up and audits the agent harness of any repository:
  frontend, backend, monorepo, library, CLI.
- `mluk-ru` — client-facing, legal and documentation copy in Russian.
- `mluk-ops` — safe agent access to any server reached over `ssh`.

**GitHub without an issue tracker:** `mluk-repo`, the everyday workflow, opens
pull requests with `gh` and starts a task from a description in chat, not from
a ticket. A different forge (GitLab, Bitbucket) or a tracker-driven process is
not covered; the plugins above still apply. For GitLab or Jira there is
[work-agent-tools](https://github.com/maximlukyanovich/work-agent-tools), which
writes the workflow commands into the project, shaped to its forge and tracker.

**A particular stack:**

- `mluk-fe` — a React / Next.js front with Tailwind and next-intl; a hook whose
  files are missing stays silent.
- `mluk-design` — a site built against a design kit.
- `mluk-deploy` — a Next.js front on Vercel, a backend in Docker Compose on a
  VPS behind Caddy and GitHub Actions, whatever the backend is written in. Its
  `domain-dns` skill fits any domain moving to Cloudflare.

## Requirements

- Claude Code.
- `git`, and `gh` signed in — for `mluk-repo`.
- Node — for the `mluk-fe` hooks; CI tests them on Node 24.
- Python 3 and `ssh` — for `mluk-ops`; CI tests its guard on Python 3.12.

## Quick start

Once per machine — it adds the source and loads nothing into sessions:

```bash
claude plugin marketplace add maximlukyanovich/agent-tools
```

The add declares the marketplace in your user settings — skip it on a machine
that works in a project pinned to a release, see
[Pinning a release](#pinning-a-release).

In an existing repository — install, then run `setup`:

```bash
claude plugin install mluk-bootstrap@mluk-agent-tools --scope project
claude "/mluk-bootstrap:setup"
```

`mluk-repo` comes with it as a dependency. `--scope local` keeps the record in
the gitignored `.claude/settings.local.json`, for a project whose rules keep AI
settings out of git. `--scope user` works too, at a price: the plugins'
descriptions join every session on the machine, in unrelated projects as well.

From scratch, in an empty folder — `--marketplace` adds the marketplace when it
is not there yet:

```bash
mkdir my-app && cd my-app
claude plugin install mluk-bootstrap --marketplace maximlukyanovich/agent-tools --scope project && claude "/mluk-bootstrap:new"
```

`new` asks the stack, runs its generator, pins the environment, and makes the
first commit and the remote on your yes; `setup` follows in a fresh session.

`setup` looks at the code,
asks only what the code cannot answer, shows a plan and, once you approve it,
writes the harness — `AGENTS.md`, the project profile, and a
`.claude/settings.json` that enables the plugins the project needs, so every
clone gets the same tools:

```json
"extraKnownMarketplaces": {
  "mluk-agent-tools": {
    "source": { "source": "github", "repo": "maximlukyanovich/agent-tools" },
    "autoUpdate": true
  }
},
"enabledPlugins": { "mluk-repo@mluk-agent-tools": true }
```

Committed settings turn the plugins on in every clone but download nothing, so
`setup` also writes the project's `/start`: a collaborator trusts the folder,
runs it, and it installs what is missing before the overview.

Which plugins to enable:

| Project | Plugins |
| --- | --- |
| any repository | `mluk-bootstrap`, `mluk-repo` |
| a React / Next.js front | + `mluk-fe` |
| built against a design kit | + `mluk-design` |
| deployed on Vercel or a VPS | + `mluk-deploy` |
| the agent works on a live server | + `mluk-ops` |
| Russian texts for people | + `mluk-ru` |

How a new version arrives is in [Versions and updates](#versions-and-updates).

## Where to start

Every plugin can introduce itself — read-only, safe to run at any time:

```bash
/mluk-bootstrap:help     what it does to a repository's harness
/mluk-repo:help          the workflow commands and the profile they read
/mluk-ru:help  en        what it checks in a Russian text, in English
```

Language follows the conversation; pass a language code to override.

## Everyday use

With `mluk-repo`, a task runs in phases, each in a fresh session — a small
change runs whole in one — and every
command ends with the next step as a block ready to copy:

```bash
/mluk-repo:next                              what to take next: roadmap, notes, issues, open PRs
/mluk-repo:task Add a password reset form    the plan: branch, questions, slices; no code before your yes
/mluk-repo:commit                            stage, check what changed, message by the preset; never pushes
/mluk-repo:review                            findings by severity, each with file:line
/mluk-repo:fix                               one round on the open findings, then the commit on your yes
/mluk-repo:create-pr merge                   push and open the PR on your yes, merge after green CI
```

The other plugins mostly need no command: their skills load when the work
reaches them — "build the settings screen" brings `web-ui-conventions` in a
front with `mluk-fe` — and their hooks check what the agent writes. A client
letter goes through `/mluk-ru:review letter.md`.

## Plugins

| Plugin | Kind | What it does |
| --- | --- | --- |
| [`mluk-bootstrap`](plugins/mluk-bootstrap/README.md) | generator + audit | Create a project in an empty folder; initialise or audit a repository's agent harness: `AGENTS.md`, the project profile, skills, hooks, docs. Carries the `layers` model. |
| [`mluk-repo`](plugins/mluk-repo/README.md) | library | The repository workflow: `commit`, `create-pr`, `promote`, `review`, `fix`, `sync`, `start`, `next`, `task`, `update-docs`, `handoff`, and the `kickoff` method — how a task is started. Reads `.claude/project-profile.md`. |
| [`mluk-design`](plugins/mluk-design/README.md) | library | `design-port` — how a design kit is ported. Enabled where a kit exists. |
| [`mluk-fe`](plugins/mluk-fe/README.md) | library + hooks | Frontend conventions for React / Next.js: `web-ui-conventions`, `component-discipline`, `yandex-browser`, and PostToolUse hooks for locale parity, translation keys and metadata titles. Reads the profile's `## Frontend`. Enabled in a web front. |
| [`mluk-deploy`](plugins/mluk-deploy/README.md) | library | How projects are deployed: `deploy-vps`, `deploy-vercel`, `domain-dns`. Skills and a `help` command. |
| [`mluk-ops`](plugins/mluk-ops/README.md) | library + hook | Safe agent access to servers: `srv` with an audit log, a guard hook, the `server-ops` protocol. Enabled only where the agent works on a server. |
| [`mluk-ru`](plugins/mluk-ru/README.md) | library | Business Russian: the principles of client-facing and legal copy, the self-check, the checklist, and `review` for a text. |

## Versions and updates

Every plugin carries a `version` in its `plugin.json`, and `claude plugin list`
shows the one you have. A major means your project must act, a minor brings a
new rule, command or template section, a patch rewords or fixes; the rule is
in [`AGENTS.md`](AGENTS.md) §1.

An installed plugin is a copy in `~/.claude/plugins/cache/`, replaced only when
the plugin's version changes. A project set up by `setup` declares the
marketplace with `autoUpdate` and follows `main`: every raised version arrives
up to ten minutes after an interactive session's first message, and
`/reload-plugins` applies it to an open session. By hand:

```bash
claude plugin marketplace update mluk-agent-tools
claude plugin update mluk-repo@mluk-agent-tools --scope project   # each installed plugin at its scope, then /reload-plugins
```

Updating delivers the method; it never edits a project — what `setup` wrote
stays the project's, and `/mluk-bootstrap:audit` proposes the edits.
`/mluk-repo:start` says when: the `Harness:` line of `.claude/COMMANDS.md`
names the `mluk-bootstrap` version the harness last matched, and an
installed version ahead of it is a `⚠`.

### Releases

Each merged batch is released: an annotated tag `vYYYY.MM.DD` on `main` — the
merge's date, `.2` for a second batch that day — and a GitHub
[release](https://github.com/maximlukyanovich/agent-tools/releases) whose notes
list every plugin's version against the previous release, then what a project
must do — a major, a removed plugin — then the merged pull requests. The date
says which release you run; a plugin's version says whether you must act. A
released tag is never moved.

### Pinning a release

A project that follows `main` gets every raised version as it lands. A team
that moves between releases deliberately pins a tag instead — `ref` inside
`source`, `autoUpdate` kept:

```json
"extraKnownMarketplaces": {
  "mluk-agent-tools": {
    "source": { "source": "github", "repo": "maximlukyanovich/agent-tools", "ref": "vYYYY.MM.DD" },
    "autoUpdate": true
  }
}
```

The latest tag is the first line of
`git ls-remote --tags --refs --sort=-v:refname https://github.com/maximlukyanovich/agent-tools 'v*'`.
`setup` asks whether a project follows `main` or pins a release, and writes
the latest tag itself.

A pin holds on a machine under two conditions:

- **The user settings do not declare the marketplace.** The once-per-machine
  `claude plugin marketplace add` writes it into `~/.claude/settings.json`
  without `ref`, and that declaration wins: a session in the pinned project
  either registers no marketplace at all or installs the plugins from `main`.
  Skip the add on a machine that works in a pinned project — trusting the
  folder registers the marketplace from the project's settings — or delete the
  `mluk-agent-tools` entry under `extraKnownMarketplaces` in
  `~/.claude/settings.json`; a project set up by `setup` declares it in its own
  settings.
- **The plugins update in the project's own session.** The catalogue is one
  clone per machine, and a session in another project fetches it from that
  project's source. A session start in the pinned project fetches its tag
  back, and `autoUpdate` then works from it; `claude plugin update` takes the
  clone as the machine's last session left it, so after a session elsewhere it
  moves the pinned project to that source.

Moving to the next tag:

1. A pull request in the project changes `ref`; its reviewer reads the
   releases between the two tags.
2. After the merge, each developer starts an interactive session at the
   repository root: the session fetches the catalogue from the new tag.
3. The plugins follow through `autoUpdate`, up to ten minutes after that
   session's first message, and `/reload-plugins` applies them. To move at
   once, run `claude plugin update <plugin>@mluk-agent-tools --scope <scope>`
   for each installed plugin right after that start, before a session in
   another project.
4. When a release asks a project to act, `/mluk-bootstrap:audit` finds
   what to change.

Rolling back is the same move to an older tag; going back to `main` is
removing `ref`. Two commands look right and do not do it:
`claude plugin marketplace update` does not see a changed `ref` — only a
session start does — and `claude plugin marketplace add` replaces the declared
source, its `ref` included.

## How it's built

`mluk-bootstrap` generates: what `setup` writes becomes the project's own code.
The rest are libraries: the procedure stays here, and the project contributes a
profile, `.claude/project-profile.md`, that every command reads first. The
model — generator versus library, what lives here and what in the project,
precedence, command naming — is in [`docs/design.md`](docs/design.md).

## Contributing

Issues and pull requests are welcome — see [`CONTRIBUTING.md`](CONTRIBUTING.md).

## License

[MIT](LICENSE).
