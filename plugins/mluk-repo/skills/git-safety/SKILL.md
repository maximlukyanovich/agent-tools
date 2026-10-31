---
name: git-safety
description: What an agent never runs in git and gh, what needs an explicit go-ahead in the current turn (commit, push, PR, merge), when amending is acceptable (unpushed commits only), and how staging and secrets are handled. Use before any git or gh action that changes state.
license: MIT
metadata:
  author: Maxim Lukyanovich
  source: https://github.com/maximlukyanovich/agent-tools
---

# git-safety

Permission applies to the current turn. A yes given for one action does not
cover the next one.

## Needs an explicit go-ahead, every time

- `git commit` — unless the profile sets `commit confirm: auto`, in which case
  invoking the commit command is the authorisation and the draft is shown for
  visibility, not approval.
- `git push` — always, even after a commit was approved. "Commit" does not mean
  "push".
- `gh pr create`, `gh pr merge`, `gh pr edit` of someone else's text,
  `gh repo create`.
- Deleting a branch — safe form only (`git branch -d`), feature branches only,
  after a successful merge.

## Never

- `git push --force` / `--force-with-lease` to a shared branch.
- `--no-verify`, `--no-gpg-sign`, or anything that bypasses a hook or branch
  protection. A broken hook is fixed, not skipped.
- `git add -A`, `git add .`, `git add -u`. Paths are listed explicitly so the
  owner sees in chat what is staged.
- Direct pushes to the branches the profile's `protected` names. They
  advance only through a merged PR.
- Squash or rebase merges unless the profile says so. History is preserved
  with a merge commit.
- Pushing to, or opening a PR against, a repository named as `upstream` in the
  profile. Syncing with upstream is manual and human-only.
- `git branch -D`, `git checkout -- <file>` on the owner's uncommitted work,
  `git stash drop`, `git reset --hard` — discarding is never the agent's call.
- Committing or staging secrets: `.env`, `.env.*`, `*.pem`, `*.key`, `id_rsa*`,
  `docs/local/**`, anything with a token in it. A suspicious path is shown and
  left unstaged.

## Amending

**A fix to a commit not yet pushed goes into that commit** — a bug found
while the work goes on, a file that should have been in it, a wrong word in
the message. A branch merges with its history, and "fix", then "fix the fix"
tells a later reader nothing the corrected commit does not.

**Review fixes go into one fix commit.** The first round after a review is a
new commit on top of the series; every later round goes into that fix commit
while no remote holds it — amended, or folded with `--fixup` when it is not
`HEAD`. The series' own commits are not rewritten for a review fix:
spreading a round across them means blame by hunk, several reworded
messages and a rebase that stops on files more than one commit changed. The
fix commit is the one the first round made after the first reviewed head
(`git log <head>..HEAD`); when that is not plain, ask. The review's story is
in its ledger, which reads a rewritten head as `git diff <last head> HEAD`.

- Check that no remote holds it: `git branch -r --contains <sha>` prints
  nothing (for `HEAD`, `git log @{u}..` lists it).
- `HEAD` → `git commit --amend`. An older commit →
  `git commit --fixup=<sha>`, then `git rebase --autosquash <sha>~`. Before
  git 2.44 a rebase without `-i` ignores `--autosquash` and says nothing;
  there it is `GIT_SEQUENCE_EDITOR=true git rebase -i --autosquash <sha>~`.
- A rebase that stops on a conflict — a later commit changed the same lines —
  is aborted (`git rebase --abort`) and the fix becomes a new commit: a
  conflict resolved inside history the checks never see again breaks a commit.
- Reword the message when the fix changes what it says, and say in one line
  which commit took the fix. Never fold silently.
- A pushed commit is never rewritten: the fix is a new commit, and there is no
  force push.

## Working tree

- A dirty tree before a switch, sync or promote is shown, and the owner is
  offered a commit or a stash. Nothing is stashed or discarded on their behalf.
- Splitting a mixed tree into several commits happens in the index, never by
  editing the owner's files back and forth: a file shared by two tasks is staged
  from a snapshot (`git hash-object -w` + `git update-index --cacheinfo`, see
  `/mluk-repo:commit` step 5). A pre-commit hook that rewrites staged files
  (lint-staged) restores the unstaged part on its own — check `git status`
  after the commit, before the next group.
- Conflicts during a merge stop the command; the owner resolves them, or the
  agent resolves them only with the owner's decision per hunk.

## Wrap-up

Every mutating command ends with what it did (`git log --oneline -N`, PR
URLs) and a one-line reminder of what it did not do — nothing was pushed,
nothing was force-pushed, no hook was bypassed.

A commit made outside `/mluk-repo:commit` — in the working session, by a
git call — ends the way that command does: when it closes a task or a round
of review fixes, run `/mluk-repo:handoff` for the same worktree or branch
through the Skill tool, without asking, rather than end on a summary.
