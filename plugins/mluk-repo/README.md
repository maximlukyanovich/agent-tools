# mluk-repo

The repository workflow for GitHub projects, as a library: the
procedure lives here, the project supplies `.claude/project-profile.md`.

## Install

```bash
claude plugin install mluk-repo --marketplace maximlukyanovich/agent-tools --scope project
```

Other scopes and updating: [Quick start](../../README.md#quick-start).

## Commands

| Command | Mutating | What it does |
| --- | --- | --- |
| `/mluk-repo:start` | no | Onboarding: overview from the project's own documents, how to run it, every enabled plugin's commands, and a live check of the plugins and what the profile lists. |
| `/mluk-repo:next` | roadmap patch after confirmation | What to take next: one recommendation from the roadmap, local notes, open issues and PRs and the branch chain; what waits and on whom; housekeeping. Ends with the `task` line. |
| `/mluk-repo:task` | no | Kickoff: brief → branch decision (or a worktree) → flavour → exploration → questions → plan. No code. |
| `/mluk-repo:review` | ledger only (`fix` opt-in) | Review the branch against the base — the current one, a named branch or worktree — or a PR, findings by severity; a pass ledger makes a repeat run review only what changed. Run it in a fresh session. |
| `/mluk-repo:sync` | yes | Merge the base branch into the current one, run the profile's post-merge checks, report what landed. |
| `/mluk-repo:update-docs` | after confirmation | Measure drift since the last docs update, classify, propose patches by the profile's doc map. |
| `/mluk-repo:commit` | yes | Stage explicitly, check what changed, draft by the preset, commit. Never pushes. |
| `/mluk-repo:create-pr` | yes | PR texts by `pr-conventions` → push → `gh pr create` → optionally merge after green CI. |
| `/mluk-repo:promote` | yes | Walk the profile's chain; each boundary is `sync` + `create-pr` + merge, confirmed. |
| `/mluk-repo:handoff` | a local note, only when a block runs long | The next session's prompt at a phase boundary — the review after a task's commit, the fixes, the plan's next step or the promote after a review, the next task after a merge — from git and the ledger. `commit`, `review`, `create-pr` and `promote` call it at their end. |
| `/mluk-repo:help` | no | This plugin's surface. |

`/promote` to the next branch is the same as `/create-pr merge`; `promote`
exists for walking more than one boundary.

## Profile

Every command reads `## Repository` first; `start`, `next`, `task`, `review`,
`update-docs` also read `## Checks`, `## Task`, `## Review`, `## Docs`. Keys
and defaults: `reference/profile.md`. When the profile is silent the command
asks and offers to write the answer into the profile.

`commit`, `review`, `promote` and `handoff` also act on a branch in a
worktree, named by folder or branch: `reference/commands.md`.

## Agents

- `review-group` — reviews one file group of a large diff for `review`;
  read-only, on the session's model, returns finding lines only.

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
  rules, the decisions table, slices, approval, and proposing a project rule
  when a problem recurs. `/mluk-repo:task` runs it.

## Local overrides

A project may ship a local `/commit`, `/promote`, … when its procedure differs.
The two coexist; the local one is what the owner types. Parameters never
justify an override — they go to the profile.
