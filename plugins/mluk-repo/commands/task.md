---
description: Kick off a task — parse the brief, decide about a branch with confirmation, load the flavour's skills from the profile, explore, ask by the kickoff method, and return a plan — a short one in chat for a small change. No production code until the plan is approved.
argument-hint: '[worktree] [<flavour>] <task description>'
---

# /mluk-repo:task

The single entry point into new work. The brief is passed inline; the
command gathers context, checks what already exists, asks what the code cannot
answer, and returns a **plan** through the `kickoff` method — load that skill
first; steps 5–7 follow it.

**Only plans.** Writes no production code, does not commit, does not call
`gh`. Reads `## Task` (`flavours`, `brief sources`, `branch prefix`, `blast
radius`, `testing skill`) and `## Repository` (`base branch`).

## Arguments

An optional leading **flavour** — a name from the profile's `flavours` table
(`ui`, `api`, `authoring`, `docs`, …) — followed by the brief. A flavour
decides which skills load for the plan (`task-ui`, `task-api`, a project
skill). Not given → infer from the brief and name the choice in the plan; a
task spanning several loads all of them. A name not in the table → show the
table and ask.

A leading **`worktree`** puts the branch in a separate working tree beside
the repository instead of switching this one — for when the main tree is busy
with other work. Without it the command still offers one when step 2 finds
the tree busy; on a free tree a worktree only adds setup.

No arguments → take the brief from a `docs/local/` note or a GitHub issue the
owner names, or ask. There is no tracker.

## The change's level

The first line of the answer names it, predicted from the brief and the
exploration — there is no diff yet. Every fresh session starts by re-reading
the harness and the task, and a handoff is worth that only when the phase it
closes was large.

- **small** — prose, or a change that keeps behaviour, within the thresholds
  `/mluk-repo:handoff` measures (at most 100 lines and 5 files, prose alone
  up to 300; `${CLAUDE_PLUGIN_ROOT}/reference/change-size.md`), and in no
  risk class of the testing skill. Steps 1–4 and the testing skill as usual;
  then a short plan in chat — what changes, which files, how it is proven —
  and the owner's yes take the place of steps 5–7 and plan mode. The review
  and the merge run in this session;
- **critical** — money, access, a migration, deleted data. Its review runs
  only in a fresh session;
- **normal** — everything else, by the steps below.

The owner may raise the level at any time; the agent never lowers a critical
one. Observed on a live project: a 31-line documentation change took nine
sessions, nearly nine tenths of its cost spent on their starts.

## Steps

1. **Parse.** Goal, acceptance criteria, what is explicitly out of scope, the
   flavour.

2. **Branch decision.** A live `git status -sb` — not the status captured
   when the session started, which can be hours old. On the base branch →
   propose `<branch prefix>/<kebab-slug>` and create it **only on
   confirmation**. On a feature branch → ask: fork a fresh branch off here,
   stay and append, open a worktree, or abort. A dirty tree before any switch
   → show the diff, offer `/mluk-repo:commit` as a code block, a stash or a
   worktree; never discard.

   **A worktree** — asked for, or accepted when offered — is confirmed with
   its folder, the profile's `worktree folder`:
   - `git worktree add -b <branch> <worktree folder> <base branch>`;
   - link in what git ignores but the work reads — local notes, env files
     (one that takes the tree's own port or Compose project name is copied
     instead, see below), tool configs; list the candidates from the main
     tree's ignored files and confirm them, since a folder that is tracked
     for one file (a README) is linked entry by entry, not as a whole. A
     linked folder is a symlink, and an ignore rule ending in `/` matches
     directories only, so the link shows as untracked — add its path to
     `.git/info/exclude` (shared by every worktree, never committed) rather
     than risk committing it;
   - install dependencies in the new tree with the project's package manager;
   - a second dev server or workshop needs a free port, and a Compose stack
     its own `COMPOSE_PROJECT_NAME` beside it: under the main tree's name,
     `up` in the worktree recreates the running containers with the
     worktree's code. The port goes into the env file the dev server reads,
     the name into the `.env` beside the compose file (or the file
     `--env-file` names) — Compose takes its own variables from there, never
     from a service's `env_file:`. Either file is copied from the main tree,
     not linked, since a value written through a link lands in the main
     tree's file. What the compose file names outright is the same for both
     stacks even then, and collides or is shared: a host port, a
     `container_name`, a network or volume with its own `name:` or marked
     `external`;
   - commands act on the session's working directory, so a command run in
     the main tree sees the main tree's branch. The working session moves into
     the worktree (`EnterWorktree` with the folder's path) or addresses it
     explicitly (`git -C <folder>`, paths inside it); a command offered for
     a fresh session names the branch — `/mluk-repo:review <branch>`, and
     `commit`, `promote`, `handoff` the same way — since that session starts
     in the main tree.

   A worktree is temporary: once its branch is merged, `/mluk-repo:create-pr`
   offers to remove it; a folder deleted by hand leaves a stale entry that
   `git worktree prune` clears.

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

5. **Ask** what the code cannot answer, by the `kickoff` questionnaire rules.

6. **Produce the plan** by the `kickoff` shape — the state table included
   when state changes. Before writing it, load the skill the profile's
   `testing skill` names, whatever the flavour — without the key,
   `${CLAUDE_PLUGIN_ROOT}/reference/proof.md`: its proof by risk sets the
   plan's verification, and its state lists — a write while another is in
   flight, data out of date while a re-read runs — become rows of the state
   table. Observed on a live project: a 22-row state table held neither
   kind, and three of the first review's seven majors were rows of them.
   Then the proof each slice needs (tests, browser
   check, migration), the effect on live data when `blast radius` names
   operations the plan touches — explicitly, even when "none" — and the
   documentation to update.

7. **Stop and request approval** through the plan-approval mechanism.

## Hard rules

- No production code before the plan is explicitly approved — for a small
  change, the owner's yes to the short plan; no draft files.
- No `git checkout -b` / `git switch` without confirmation.
- Never lose uncommitted work.
- Do not invent requirements, fields, semantics or library behaviour — a gap
  goes to open questions.
- Plan the smallest step that satisfies the brief, not a framework for
  imagined needs.
- For SEO surfaces, a plan that moves primary content behind a client-only
  fetch is rejected at planning time, not discovered at review.
