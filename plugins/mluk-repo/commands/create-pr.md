---
description: Draft the PR title and body by pr-conventions, then on confirmation push the branch and open the PR into the base branch with gh; with merge, wait for green CI and merge. Confirms before each git/gh action.
argument-hint: '[<target-branch>] [merge]'
---

# /mluk-repo:create-pr

One hop: the current branch into its target through a pull request. Reads
`## Repository` for `base branch`, `chain`, `protected`, `upstream`,
`validate`, `merge method`, `delete branch`, `pr language`, `remote account`.

**Writes to git and GitHub**, each step on confirmation. Without `merge` it
stops after printing the PR URL.

## Arguments

- `<target-branch>` — the PR base. Default: the next branch in the chain
  (`feature/* → develop`, `develop → main`, or `staging` when the chain has it).
- `merge` — after the PR is open, wait for CI and merge.

## Steps

1. **Pre-flight.**
   - `git branch --show-current`. The current branch is protected and no
     target was given → stop; protected branches advance through
     `/mluk-repo:promote`.
   - `git status --porcelain`. Dirty → show the diff and offer
     `/mluk-repo:commit`. Do not commit or stash on the owner's behalf.
   - `git remote -v`, `gh auth status`. The remote alias must match the
     profile's `remote account` and `gh`'s active account must own the
     repository (`github-accounts` skill); otherwise stop and say so. An
     `upstream` remote is out of scope — a PR must target `origin`.
   - The gate: `git rev-parse HEAD^{tree}` equals `$(git rev-parse
     --git-dir)/validated-tree` → `commit` already ran the full `validate` on
     exactly this tree; say so and skip. Otherwise run the profile's
     `validate` — red → stop and show; green → record the tree the same way.
     Only a full run is recorded, never a targeted one.
   - Behaviour, domain or scope changed and the docs did not → offer
     `/mluk-repo:update-docs` before pushing.

2. **Show what moves.**

   ```bash
   git fetch origin <target> --quiet
   git log --no-merges origin/<target>..HEAD --pretty=format:'%h %s'
   git diff --stat origin/<target>...HEAD
   ```

   Empty → nothing to PR; stop. Flag what the PR body must mention:
   migrations, new dependencies, new runtime config keys, anything in the
   profile's blast-radius list.

3. **Draft the texts** by the `pr-conventions` skill — read the last merged PRs
   first. Print title and body in chat.

4. **Push** — on confirmation, only if the local branch is ahead of
   `origin/<branch>`: `git push -u origin <branch>`.

5. **Open or reuse the PR.**

   ```bash
   gh pr list --head <branch> --base <target> --json number,url,state,title
   ```

   - None → on confirmation `gh pr create --base <target> --head <branch>
     --title "<title>" --body "$(cat <<'EOF' … EOF)"`. Verify the PR targets
     `origin`, not a fork parent; if `gh` picked the parent, stop.
   - Open → reuse; new commits attach. Regenerate title/body only on explicit
     confirmation via `gh pr edit`.
   - Closed, not merged → ask: reopen or create anew.

   Print the URL. **No `merge` → stop here.**

6. **With `merge`.**
   - Read the review ledger for this branch (profile `ledger`, see
     `/mluk-repo:review`). No pass on the current head, or `major`+ findings
     still `open` → print that and merge only on an explicit yes. Merging
     without a review stays possible; it should not be accidental.
   - `gh pr checks <n>`. Pending → offer `gh pr checks <n> --watch` or coming
     back later; no sleep loops. Red → stop, print the failing checks, suggest
     `gh run view <run-id> --log-failed`; no retry, no bypass. No CI configured
     → say so and state when `validate` last ran.
   - Re-confirm, then `gh pr merge <n> --<merge method>` plus
     `--delete-branch` when the profile says so. Never `--squash` unless the
     profile's method is squash; never `--admin`. Verify with
     `gh pr view <n> --json state,mergedAt`.
   - `git fetch origin <target> --quiet && git checkout <target> && git pull
     --ff-only origin <target>`. A failed fast-forward is a desync for a human.
   - Offer to delete the local feature branch with `git branch -d` (safe form
     only); on "keep", return to it.
   - **The branch lives in a worktree** (`git worktree list` shows it in
     another folder): the target is checked out in the main tree, and git
     refuses to check it out a second time — so neither `git checkout <target>`
     nor `--delete-branch` (which checks it out too) works from the worktree.
     Merge without `--delete-branch`, then, from the main tree and each on
     confirmation: pull the target there (`--ff-only`), `git worktree remove
     <folder>`, `git branch -d <branch>`, and, when the profile deletes
     branches, `git push origin --delete <branch>`. Offer this cleanup by
     default — a merged worktree left behind is clutter nobody asked for.

7. **Wrap up**: PR URL and status (`opened` / `merged` / `pending CI`), and the
   `git-safety` reminder line.

## Hard rules

- Confirm before each `git push`, `gh pr create`, `gh pr merge`. One yes is not
  a blanket.
- Never push directly to a protected branch; never touch `upstream`.
- Never `--force`, `--no-verify`, `--admin`; never a squash the profile did
  not ask for.
- PR text in the profile's `pr language` (English by default), no attribution.
