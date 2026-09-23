# agent-tools

Personal Claude Code tooling for my own projects. One repository: it is both the
marketplace (`mluk-agent-tools`) and the home of the plugins.

Why it exists: the method must not live as copies in every repository. How a
task is started, how a commit and a pull request are written, how a review is
run, how Russian client copy is phrased — these are the same in every project;
only the branch chain, the validate command and the domain differ, and those
stay in the project.

This is the **personal** twin of the work library (`secl-agent-tools`). The two
never mix: work projects have Jira, GitLab and time tracking; personal projects
have GitHub with `gh`, no tracker and no timesheets. A rule earned at work goes
to the work library, a rule earned here goes here.

## Installing

On this machine the marketplace is registered from the working checkout — no
push needed, but an installed plugin is a **copy** in
`~/.claude/plugins/cache/`, so an edit reaches sessions only after a refresh:

```bash
claude plugin marketplace add /home/maximlukyanovich/private/tools/agent-tools
claude plugin install mluk-bootstrap@mluk-agent-tools --scope user
claude plugin update  mluk-bootstrap@mluk-agent-tools     # after every edit, then restart the session
```

To run a plugin straight from the checkout while writing it, without
installing: `claude --plugin-dir /home/maximlukyanovich/private/tools/agent-tools/plugins`.

On another machine, from the private repository (SSH, personal account):

```bash
/plugin marketplace add git@github.com:maximlukyanovich/agent-tools.git
/plugin marketplace update mluk-agent-tools
```

Plugins are enabled separately. `mluk-bootstrap` and `mluk-ru` are enabled at
user scope (`~/.claude/settings.json`); `mluk-repo` is enabled per personal
project in its `.claude/settings.json`, because its commands are not the way
work repositories are run:

```json
"enabledPlugins": { "mluk-repo@mluk-agent-tools": true }
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
| `mluk-bootstrap` | generator + audit | Initialise or audit a repository's agent harness: `AGENTS.md`, the project profile, skills, hooks, docs. Carries the `layers` model, the `kickoff` method — how a task is started — and `design-port` — how a design kit is ported. |
| `mluk-repo` | library | The repository workflow: `commit`, `create-pr`, `promote`, `review`, `sync`, `start`, `task`, `update-docs`. Reads `.claude/project-profile.md`. |
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
| Updating the method | not updated; it is project code now | edit here, `claude plugin update` |

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
2. The project profile — `.claude/project-profile.md`.
3. The project's own `AGENTS.md` and skills.
4. The defaults in this repository.

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
| `mluk-repo` | `:commit`, `:create-pr`, `:promote`, `:review`, `:sync`, `:start`, `:task`, `:update-docs`, `:help` |
| `mluk-ru` | `:review`, `:help` |

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
skills with `disable-model-invocation`. The layout mirrors the work library on
purpose and migrates in one move when both do.

## How this grows

The method comes out of real work. After a decision the owner makes in a
project — a convention, a rule, a way of asking — the agent proposes the
matching change here in the same session, and the owner decides. Candidates
that are not ready accumulate under `docs/local/` in the working repositories.

Planned next (iteration 2): `mluk-common` (testing and verification, no
invention, decomposition, docs discipline), `mluk-fe` (React/Next: design
fidelity, i18n with the locale-parity and translation-key hooks now living in
`quest-bot-web/.claude/hooks/`, SEO metadata, perf and motion) and `mluk-be`
(Django: conventions, testing, Celery pitfalls, API contracts). Until then the
project-level hooks and skills in the working repositories are the reference
implementations.
