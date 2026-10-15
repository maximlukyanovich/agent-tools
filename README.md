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
not covered; the plugins above still apply.

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

In an existing repository, then run `/mluk-bootstrap:setup`:

```bash
claude plugin install mluk-bootstrap@mluk-agent-tools --scope project
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
  "mluk-agent-tools": { "source": { "source": "github", "repo": "maximlukyanovich/agent-tools" } }
},
"enabledPlugins": { "mluk-repo@mluk-agent-tools": true }
```

Which plugins to enable:

| Project | Plugins |
| --- | --- |
| any repository | `mluk-bootstrap`, `mluk-repo` |
| a React / Next.js front | + `mluk-fe` |
| built against a design kit | + `mluk-design` |
| deployed on Vercel or a VPS | + `mluk-deploy` |
| the agent works on a live server | + `mluk-ops` |
| Russian texts for people | + `mluk-ru` |

An installed plugin is a copy in `~/.claude/plugins/cache/`. To pick up a new
version:

```bash
claude plugin marketplace update mluk-agent-tools
claude plugin update mluk-repo@mluk-agent-tools     # each installed plugin, then restart the session
```

## Where to start

Every plugin can introduce itself — read-only, safe to run at any time:

```bash
/mluk-bootstrap:help     what it does to a repository's harness
/mluk-repo:help          the workflow commands and the profile they read
/mluk-ru:help  en        what it checks in a Russian text, in English
```

Language follows the conversation; pass a language code to override.

## Everyday use

With `mluk-repo`, a task runs in phases, each in a fresh session, and every
command ends with the next step as a block ready to copy:

```bash
/mluk-repo:next                              what to take next: roadmap, notes, issues, open PRs
/mluk-repo:task Add a password reset form    the plan: branch, questions, slices; no code before your yes
/mluk-repo:commit                            stage, validate, message by the preset; never pushes
/mluk-repo:review                            findings by severity, each with file:line
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
| [`mluk-repo`](plugins/mluk-repo/README.md) | library | The repository workflow: `commit`, `create-pr`, `promote`, `review`, `sync`, `start`, `next`, `task`, `update-docs`, `handoff`, and the `kickoff` method — how a task is started. Reads `.claude/project-profile.md`. |
| [`mluk-design`](plugins/mluk-design/README.md) | library | `design-port` — how a design kit is ported. Enabled where a kit exists. |
| [`mluk-fe`](plugins/mluk-fe/README.md) | library + hooks | Frontend conventions for React / Next.js: `web-ui-conventions`, `component-discipline`, `yandex-browser`, and PostToolUse hooks for locale parity, translation keys and metadata titles. Reads the profile's `## Frontend`. Enabled in a web front. |
| [`mluk-deploy`](plugins/mluk-deploy/README.md) | library | How projects are deployed: `deploy-vps`, `deploy-vercel`, `domain-dns`. Skills and a `help` command. |
| [`mluk-ops`](plugins/mluk-ops/README.md) | library + hook | Safe agent access to servers: `srv` with an audit log, a guard hook, the `server-ops` protocol. Enabled only where the agent works on a server. |
| [`mluk-ru`](plugins/mluk-ru/README.md) | library | Business Russian: the principles of client-facing and legal copy, the self-check, the checklist, and `review` for a text. |

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
