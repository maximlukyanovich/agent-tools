# Design

How the work is split between the plugins and the projects that use them.
Installing and using them is in the [README](../README.md).

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
| Updating the method | not updated; it is project code now | a raised version, through `autoUpdate` or `claude plugin update`; a pinned project moves its `ref` |

**No change log for the generator.** A generator that writes the process
commands into each project needs a log of what a project must carry over.
Here the process commands — `task`, `commit`, `review`, `fix`, `create-pr`,
`promote` — live in `mluk-repo` and arrive with its update; `setup` generates
only the harness: `AGENTS.md`, the profile, `CLAUDE.md`, domain skills,
`/start`, `docs/local/`. Its state is one line, `Harness:` in
`.claude/COMMANDS.md`: the `mluk-bootstrap` `MAJOR.MINOR` the harness last
matched. A minor raise is a new rule or template section — what `audit`
checks — so it is what moves the line; `/mluk-repo:start` compares it with the
installed plugin and points to `audit` when the plugin is ahead.

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
| `mluk-bootstrap` | `:new`, `:setup`, `:audit`, `:help` |
| `mluk-repo` | `:commit`, `:create-pr`, `:promote`, `:review`, `:fix`, `:sync`, `:start`, `:next`, `:task`, `:update-docs`, `:handoff`, `:help` |
| `mluk-ru` | `:review`, `:help` |
| `mluk-fe` | `:help` |
| `mluk-design` | `:help` |
| `mluk-deploy` | `:help` |
| `mluk-ops` | `:help` |

## Layers

Inside a project a rule can live on five layers — a deterministic check, an
agent hook, a document, a skill or a command — and each costs differently. The
[`layers`](../plugins/mluk-bootstrap/skills/layers/SKILL.md) skill is the
source; `mluk-bootstrap` applies it when it sets up or audits a harness.
