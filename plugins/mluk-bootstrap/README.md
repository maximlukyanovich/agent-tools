# mluk-bootstrap

Create a project in an empty folder, then initialise and audit its agent
harness. Stack-agnostic: frontend, backend, monorepo, library, CLI; `new`
follows a recipe per stack and asks when there is none.

## Install

```bash
claude plugin install mluk-bootstrap --marketplace maximlukyanovich/agent-tools --scope project
```

Other scopes and updating: [Quick start](../../README.md#quick-start).

## Commands

| Command | What it does |
| --- | --- |
| `/mluk-bootstrap:new` | Creates a project in an empty folder: the stack's recipe, its generator with every option explicit, a pinned environment, git; the first commit and the remote on your yes. Then `setup`, in a fresh session. |
| `/mluk-bootstrap:setup` | Inventories the repository, asks only what the code cannot answer, shows a plan, then creates the harness. |
| `/mluk-bootstrap:audit` | Checks an existing harness against the model — drift, duplication, local commands that merely copy the library, a profile with missing sections. Read-only. |
| `/mluk-bootstrap:help` | What this plugin can do: commands, the layer model, what it creates. Optional language argument. |

## What `setup` creates

`AGENTS.md` as the canonical document, `CLAUDE.md` as a thin vendor layer, the
project profile every library plugin reads first, `.claude/settings.json` with
the library plugins enabled, domain skills, hooks where a repeated pain
justifies one, and the `docs/**` skeleton with a gitignored `docs/local/`.

It does **not** create `commit`, `create-pr`, `promote`, `review`, `sync`,
`start`, `next`, `task` or `update-docs` commands — those come from `mluk-repo` and are
driven by the profile. A local command is written only when the project's
procedure differs from the library's.

## Skills

- `skills/layers` — the five layers a rule can live on, what each costs, and
  the anti-patterns that make a harness expensive. Loaded whenever a rule needs
  a home.

The kickoff method (how a task is started) lives in `mluk-repo`, next to
`/mluk-repo:task` that runs it; porting a design kit lives in `mluk-design`.
`mluk-repo` is a dependency: installing this plugin installs it in the same
scope, so `new` and `setup` load its `kickoff` and `github-accounts` skills in a
fresh folder too.

## Reference

Read one at a time, not as a whole: `questions.md` (the eleven asked in phase 1),
`layout.md` (target file tree, gitignore, and the two traps that cost a rewrite),
`templates.md` (skeletons), `project-profile.md` (the sectioned file the library
plugins read), `checklist.md` (the final check), `scaffold/<stack>.md` (how
`new` runs a stack's generator, and what `setup` must respect afterwards —
`next.md` so far).
