---
name: git-safety
description: What an agent never runs in git and gh, what needs an explicit go-ahead in the current turn (commit, push, PR, merge), when amending is acceptable (unpushed commits only), and how staging and secrets are handled. Use before any git or gh action that changes state.
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
- Direct pushes to protected branches (`develop`, `main`, `staging`). They
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

`--amend` is **acceptable for an unpushed commit** when the change belongs to
it — a follow-up fix to the same task, a file that should have been in it, a
wrong word in the message. Check that the commit is not on the remote
(`git log @{u}..` lists it, or `git status -sb` shows the branch ahead), say so
plainly, propose the amend, and let the owner choose between amending and a
new commit. Never amend silently, and never amend a commit that has been
pushed.

## Working tree

- A dirty tree before a switch, sync or promote is shown, and the owner is
  offered a commit or a stash. Nothing is stashed or discarded on their behalf.
- Conflicts during a merge stop the command; the owner resolves them, or the
  agent resolves them only with the owner's decision per hunk.

## Wrap-up

Every mutating command ends with what it did (`git log --oneline -N`, PR
URLs) and a one-line reminder of what it did not do — nothing was pushed,
nothing was force-pushed, no hook was bypassed.
