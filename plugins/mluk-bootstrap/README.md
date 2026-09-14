# mluk-bootstrap

Initialise and audit a repository's agent harness, and carry the method for
starting a task. Stack-agnostic: frontend, backend, monorepo, library, CLI.

## Commands

| Command | What it does |
| --- | --- |
| `/mluk-bootstrap:setup` | Inventories the repository, asks only what the code cannot answer, shows a plan, then creates the harness. |
| `/mluk-bootstrap:audit` | Checks an existing harness against the model — drift, duplication, local commands that merely copy the library, a profile with missing sections. Read-only. |
| `/mluk-bootstrap:help` | What this plugin can do: commands, the layer model, what it creates. Optional language argument. |

## What `setup` creates

`AGENTS.md` as the canonical document, `CLAUDE.md` as a thin vendor layer, the
project profile every library plugin reads first, `.claude/settings.json` with
the library plugins enabled, domain skills, hooks where a repeated pain
justifies one, and the `docs/**` skeleton with a gitignored `docs/local/`.

It does **not** create `commit`, `create-pr`, `promote`, `review`, `sync`,
`start`, `task` or `update-docs` commands — those come from `mluk-repo` and are
driven by the profile. A local command is written only when the project's
procedure differs from the library's.

## Skills

- `skills/layers` — the five layers a rule can live on, what each costs, and
  the anti-patterns that make a harness expensive. Loaded whenever a rule needs
  a home.
- `skills/kickoff` — how a task is started: plan mode, exploration, the
  questionnaire rules, the decisions table, slices, approval, and the habit of
  proposing a library change after an owner's decision.

## Reference

Read one at a time, not as a whole: `questions.md` (the ten asked in phase 1),
`layout.md` (target file tree, gitignore, and the two traps that cost a rewrite),
`templates.md` (skeletons), `project-profile.md` (the sectioned file the library
plugins read), `checklist.md` (the final check).
