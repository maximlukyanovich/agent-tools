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

Built for, and used on:

- **GitHub with `gh`, no issue tracker.** The workflow commands open pull
  requests with `gh`; a task starts from a description in chat, not from a
  ticket.
- **A React / Next.js front** — App Router, Tailwind, next-intl — deployed on
  Vercel.
- **A backend in Docker Compose on a VPS** behind Caddy, deployed by GitHub
  Actions. The first one was Django + Celery + Postgres + Redis; the scheme
  does not depend on Django.
- **A site built against a design kit**, and **client-facing copy in Russian**.

Each plugin is enabled separately, so a project takes only what fits.
`mluk-bootstrap` and `mluk-repo` are stack-agnostic. A different forge (GitLab,
Bitbucket) or a tracker-driven process is not covered by `mluk-repo`; the rest
still applies.

## Requirements

- Claude Code.
- `git`, and `gh` signed in — for `mluk-repo`.
- Node — for the `mluk-fe` hooks; CI tests them on Node 24.
- Python 3 and `ssh` — for `mluk-ops`; CI tests its guard on Python 3.12.

## Quick start

```bash
claude plugin marketplace add maximlukyanovich/agent-tools
claude plugin install mluk-bootstrap@mluk-agent-tools --scope user
```

Then, in your repository, run `/mluk-bootstrap:setup`. It looks at the code,
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

## Plugins

| Plugin | Kind | What it does |
| --- | --- | --- |
| `mluk-bootstrap` | generator + audit | Initialise or audit a repository's agent harness: `AGENTS.md`, the project profile, skills, hooks, docs. Carries the `layers` model. |
| `mluk-repo` | library | The repository workflow: `commit`, `create-pr`, `promote`, `review`, `sync`, `start`, `next`, `task`, `update-docs`, and the `kickoff` method — how a task is started. Reads `.claude/project-profile.md`. |
| `mluk-design` | library | `design-port` — how a design kit is ported. Enabled where a kit exists. |
| `mluk-fe` | library + hooks | Frontend conventions for React / Next.js: `web-ui-conventions`, `component-discipline`, and PostToolUse hooks for locale parity, translation keys and metadata titles. Reads the profile's `## Frontend`. Enabled in a web front. |
| `mluk-deploy` | library | How projects are deployed: `deploy-vps`, `deploy-vercel`, `domain-dns`. Skills and a `help` command. |
| `mluk-ops` | library + hook | Safe agent access to servers: `srv` with an audit log, a guard hook, the `server-ops` protocol. Enabled only where the agent works on a server. |
| `mluk-ru` | library | Business Russian: the principles of client-facing and legal copy, the self-check, the checklist, and `review` for a text. |

## Two kinds of plugin

**A generator** runs once and writes files into the project. What it produces
becomes the project's own code: edited locally, never updated from here.
`mluk-bootstrap:setup` is a generator — `AGENTS.md`, the profile and domain
skills are about one repository.

**A library** keeps its commands and skills here and is invoked from any
project. The project contributes only a profile. `mluk-repo` and `mluk-ru` are
libraries: the procedure is identical everywhere, the differences (base branch,
validate command, commit preset, glossary) are data.

| | Generator | Library |
| --- | --- | --- |
| Appears in the project | `AGENTS.md`, domain skills, hooks, the profile | profile lines only |
| Commands come from | the project | the plugin |
| Updating the method | not updated; it is project code now | `claude plugin update` |

**Library base, local override.** `/mluk-repo:commit` is the default in every
project. A project that genuinely needs a different procedure — not different
parameters — writes its own `.claude/commands/commit.md`; the two coexist under
different names. The test: if the difference fits in a profile line, it is the
library. If the procedure differs, it is a local command. `mluk-bootstrap:audit`
reports local commands that merely duplicate the library.

## Method here, project there

**Here — the method.** How a task is started and planned, how a commit and a PR
are shaped, how a review is scoped, how Russian copy is phrased, templates for
`AGENTS.md` and skills.

**In the project — the profile and the domain.** Branch chain, validate command,
commit preset, design-system id, doc map, glossary; domain skills (design
fidelity for this kit, module placement for this tree); hooks.

The rule of thumb: if a rule survives a change of project, it belongs here. If
it names concrete paths, ids or a design system, it belongs to the project.

### Precedence

Every command and skill here reads the project profile before it acts and treats
it as authoritative. Strongest first:

1. What the developer says in the current session.
2. This clone's overrides — `.claude/project-profile.local.md`, gitignored: a
   fork's trunk, the paths of sibling checkouts. Single keys, same headings.
3. The project profile — `.claude/project-profile.md`.
4. The project's own `AGENTS.md` and skills.
5. The defaults in this repository.

A plugin never dictates a branch name or a commit format: it ships a default,
reads the profile, and asks when the profile is silent.

## Command naming

Claude Code prefixes a plugin's commands with the plugin name and a colon —
`/mluk-repo:commit`. The prefix lives in the **plugin name**; the command name
stays a short verb. Never a colon in a filename, never the plugin name repeated
inside a command name. Plugin names are fixed once: renaming one changes every
command it ships and every document quoting them.

| Plugin | Commands |
| --- | --- |
| `mluk-bootstrap` | `:setup`, `:audit`, `:help` |
| `mluk-repo` | `:commit`, `:create-pr`, `:promote`, `:review`, `:sync`, `:start`, `:next`, `:task`, `:update-docs`, `:help` |
| `mluk-ru` | `:review`, `:help` |
| `mluk-fe` | `:help` |
| `mluk-design` | `:help` |
| `mluk-deploy` | `:help` |
| `mluk-ops` | `:help` |

## Layout

```
.claude-plugin/marketplace.json   the catalogue
plugins/<name>/
  .claude-plugin/plugin.json      manifest
  commands/*.md                   procedures a human invokes
  skills/<name>/SKILL.md          knowledge the agent loads by itself
  reference/*.md                  read one file at a time, on instruction
  README.md                       for people, links to the skill
```

`commands/` is the older of the two plugin formats; Claude Code now prefers
skills with `disable-model-invocation`; the layout migrates in one move when
it does.

## Contributing

Issues and pull requests are welcome — a rule that misfired in your project, a
trap worth naming, a fix.

- Plugin texts, commits and pull requests are in English (the business-Russian
  skill is the one exception: its subject is Russian).
- A rule that names your project's paths, ids or design system belongs in your
  project's profile, not here.
- Before opening a pull request, run the checks in
  [`AGENTS.md`](AGENTS.md) §3, and run the changed command or skill once in a
  real repository — say in the pull request where and how. To try a plugin
  straight from a checkout, without installing: `claude --plugin-dir
  <checkout>/plugins`.

## License

[MIT](LICENSE).
