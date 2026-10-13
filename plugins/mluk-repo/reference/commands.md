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
