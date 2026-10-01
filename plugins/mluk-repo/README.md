# mluk-repo

The repository workflow for personal GitHub projects, as a library: the
procedure lives here, the project supplies `.claude/project-profile.md`.

## Commands

| Command | Mutating | What it does |
| --- | --- | --- |
| `/mluk-repo:start` | no | Onboarding: overview from the project's own documents plus a live check of what the profile lists. |
| `/mluk-repo:task` | no | Kickoff: brief → branch decision → flavour → exploration → questions → plan. No code. |
| `/mluk-repo:review` | ledger only (`fix` opt-in) | Review the branch against the base, or a PR, findings by severity; a pass ledger makes a repeat run review only what changed. Run it in a fresh session. |
| `/mluk-repo:sync` | yes | Merge the base branch into the current one, run the profile's post-merge checks, report what landed. |
| `/mluk-repo:update-docs` | after confirmation | Measure drift since the last docs update, classify, propose patches by the profile's doc map. |
| `/mluk-repo:commit` | yes | Stage explicitly, validate, draft by the preset, commit. Never pushes. |
| `/mluk-repo:create-pr` | yes | PR texts by `pr-conventions` → push → `gh pr create` → optionally merge after green CI. |
| `/mluk-repo:promote` | yes | Walk the profile's chain; each boundary is `sync` + `create-pr` + merge, confirmed. |
| `/mluk-repo:help` | no | This plugin's surface. |

`/promote` to the next branch is the same as `/create-pr merge`; `promote`
exists for walking more than one boundary.

## Profile

Every command reads `## Repository` first; `start`, `task`, `review`,
`update-docs` also read `## Checks`, `## Task`, `## Review`, `## Docs`. Keys
and defaults: `reference/profile.md`. When the profile is silent the command
asks and offers to write the answer into the profile.

## Skills

- `commit-conventions` — the two presets: `gitmoji-conventional` (default) and
  `topic-prose`; the body rules; what is forbidden in a message.
- `pr-conventions` — plain conventional title, the body sections, test plan as
  checkboxes, no hard wrap, English.
- `github-accounts` — two GitHub accounts on one machine: SSH host aliases pick
  the key, `gh` is global and is not switched.
- `git-safety` — what is never run, what needs a go-ahead in the current turn,
  when `--amend` is acceptable.
- `kickoff` — how a task is started: plan mode, exploration, the questionnaire
  rules, the decisions table, slices, approval, and proposing a library change
  after an owner's decision. `/mluk-repo:task` runs it.

## Local overrides

A project may ship a local `/commit`, `/promote`, … when its procedure differs.
The two coexist; the local one is what the owner types. Parameters never
justify an override — they go to the profile.
