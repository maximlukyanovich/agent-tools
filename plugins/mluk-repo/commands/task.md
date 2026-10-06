---
description: Kick off a task — parse the brief, decide about a branch with confirmation, load the flavour's skills from the profile, explore, ask by the kickoff method, and return a plan. No production code until the plan is approved.
argument-hint: '[<flavour>] <task description>'
---

# /mluk-repo:task

The single entry point into new work. The brief is passed inline; the
command gathers context, checks what already exists, asks what the code cannot
answer, and returns a **plan** through the `kickoff` method.

**Only plans.** Writes no production code, does not commit, does not call
`gh`. Reads `## Task` (`flavours`, `brief sources`, `branch prefix`, `blast
radius`) and `## Repository` (`base branch`).

## Arguments

An optional leading **flavour** — a name from the profile's `flavours` table
(`ui`, `api`, `authoring`, `docs`, …) — followed by the brief. A flavour
decides which skills load for the plan (`task-ui`, `task-api`, a project
skill). Not given → infer from the brief and name the choice in the plan; a
task spanning several loads all of them. A name not in the table → show the
table and ask.

No arguments → take the brief from a `docs/local/` note or a GitHub issue the
owner names, or ask. There is no tracker.

## Steps

1. **Parse.** Goal, acceptance criteria, what is explicitly out of scope, the
   flavour.

2. **Branch decision.** `git status -sb`. On the base branch → propose
   `<branch prefix>/<kebab-slug>` and create it **only on confirmation**. On a
   feature branch → ask: fork a fresh branch off here, stay and append, or
   abort. A dirty tree before any switch → show the diff, offer
   `/mluk-repo:commit` or a stash; never discard.

3. **Gather context selectively** — `AGENTS.md`, the profile, the documents
   the flavour's skill names, the product docs and contract log from `## Docs`
   for the touched area (a sibling's through the local `## Siblings`), the code the brief touches (by section, not whole
   files), the design source from `## Sources of truth` when the task has UI.
   Broad sweeps go to exploration subagents; library versions and APIs are
   verified through the docs tool, not memory.

4. **Reuse-check before designing.** Does a shared implementation already
   exist (a shared module, a validator rule, a config key, a serializer
   field)? The result is an explicit section of the plan: reused, extended,
   genuinely new and why.

5. **Ask** what the code cannot answer, by the `kickoff` questionnaire rules —
   recommendation first and marked, at most four a round, a closing "anything
   to add" only when new input is plausible.

6. **Produce the plan** by the `kickoff` shape: context, decisions table,
   architecture, slices with files and the proof each slice needs (tests,
   browser check, migration), effect on live data when `blast radius` names
   operations the plan touches — explicitly, even when "none" — documentation
   to update, assumptions, open questions.

7. **Stop and request approval** through the plan-approval mechanism.

## Hard rules

- No production code before the plan is explicitly approved; no draft files.
- No `git checkout -b` / `git switch` without confirmation.
- Never lose uncommitted work.
- Do not invent requirements, fields, semantics or library behaviour — a gap
  goes to open questions.
- Plan the smallest step that satisfies the brief, not a framework for
  imagined needs.
- For SEO surfaces, a plan that moves primary content behind a client-only
  fetch is rejected at planning time, not discovered at review.
