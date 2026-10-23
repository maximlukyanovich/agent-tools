# Rules the mluk-repo commands share

Read by the commands that point here, so each rule is written once.

## A worktree or branch argument

`commit`, `review`, `promote` and `handoff` act on the session's own tree
unless a leading argument names other work, usually a branch living in a
worktree beside the repository. The word is recognised by shape:

1. **An existing folder** is that worktree; its branch is
   `git -C <folder> branch --show-current`.
2. **Otherwise a local branch** — `git rev-parse --verify --quiet
   refs/heads/<word>` — is that branch; its folder is the `worktree` line
   above `branch refs/heads/<word>` in `git worktree list --porcelain`.
3. **Neither** — the word is not this argument and goes to the command's own.

Once the tree is known:

- every git command is `git -C <tree> …` and every file is read from that
  tree; the session's working directory does not move;
- the gate — the profile's `validate`, or a `targeted checks` row — runs in
  that tree;
- what one command leaves for another (`validated-tree`) goes to that tree's
  git-dir, `$(git -C <tree> rev-parse --git-dir)`; the review ledger stays at
  its path in the main tree.

**A branch checked out nowhere** has no tree. `review` and `handoff` read it
from refs — `git diff origin/<base>...<branch>`, files through
`git show <branch>:<path>` — and say that the gate did not run. `commit` and
`promote` stop and print the line that checks it out:

```
git worktree add ../<repo>-<slug> <branch>
```

**No argument, and the session's tree is on the base branch** with nothing of
its own: `review` and `handoff` look for the work instead of stopping — the
worktrees whose branch is ahead of the base (`git rev-list --count
origin/<base>..<branch>`). Exactly one → that one, named in the output;
several → ask which; none → nothing to act on.

## The gate

The full `validate` costs minutes. Run after every edit and again by every
command, it makes a fix wait longer than the fix itself. So it runs once per
tree, and the work between those runs is checked narrowly.

- **Between edits, in a commit, after a sync — the targeted checks.** For
  each changed path, the profile's `targeted checks` row that covers it; the
  union of those rows runs, and a path no row covers sends the step to the
  full `validate`. A profile without the table runs the full `validate`, as
  before. Say in one line what ran and what was not exercised.
- **The full gate — once per tree.** `review` runs it on the head it reads,
  `create-pr` and `promote` before the push. A tree already recorded green is
  not run again: `git -C <tree> rev-parse HEAD^{tree}` equal to
  `$(git -C <tree> rev-parse --git-dir)/validated-tree` and a clean tree →
  say so and skip. Every green full run on a clean tree records it the same
  way, whichever command ran it; a targeted run never does.
- **Beside the work, not before it.** `review` starts the full gate in the
  background (Bash with `run_in_background`) before the rubric and reads the
  result before the report.
- **Red under load is not red by code.** When only timeouts fail while the
  machine is busy — a dev server, a stack, parallel agents — rerun the failing
  files alone and report both runs and the load. Neither green nor red is
  called without the rerun.
