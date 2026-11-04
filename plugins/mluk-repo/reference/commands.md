# Rules the mluk-repo commands share

Read by the commands that point here, so each rule is written once.

## A worktree or branch argument

`commit`, `review`, `fix`, `promote` and `handoff` act on the session's own
tree unless a leading argument names other work, usually a branch living in a
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
- what one command leaves for another (`gate-record`) goes to that tree's
  git-dir, `$(git -C <tree> rev-parse --git-dir)`; the review ledger stays at
  its path in the main tree.

**A branch checked out nowhere** has no tree. `review` and `handoff` read it
from refs — `git diff origin/<base>...<branch>`, files through
`git show <branch>:<path>` — and say that the gate did not run. `commit`,
`fix` and `promote` stop and print the line that checks it out:

```
git worktree add <worktree folder> <branch>
```

**No argument, and the session's tree is on the base branch** with nothing of
its own: `review` and `handoff` look for the work instead of stopping — the
worktrees whose branch is ahead of the base (`git rev-list --count
origin/<base>..<branch>`). Exactly one → that one, named in the output;
several → ask which; none → nothing to act on.

## The gate

The full `validate` costs minutes. Run after every edit and again by every
command, it makes a fix wait longer than the fix itself. So it runs once per
branch, and the work between those runs is checked narrowly. The record
behind it is kept by the plugin's `gate_record.py`, which each command's
body calls by its full path (`${CLAUDE_PLUGIN_ROOT}/reference/gate-record.md`).
Observed on a live project: a half-hour task's merge ran the full gate again
after a review fix that had passed its targeted checks.

- **Between edits, in a commit, after a sync — the targeted checks.** For
  each changed path, the profile's `targeted checks` row that covers it; the
  union of those rows runs, and a path no row covers sends the step to the
  full `validate`. A profile without the table runs the full `validate`, as
  before. With `full gate: ci` both go to the pipeline instead: the step runs
  no `validate`, and such a commit is not recorded. Say in one line what ran
  and what was not exercised. A commit whose every path had its row, green,
  on a clean tree after the commit → `gate_record.py record targeted`. The
  paths are the whole commit's (`git show --name-only HEAD`): an amend counts
  what the commit already held, not only the round's. Several groups of one
  run are recorded after the last, with `--commits <n>`.
- **A hub file takes the tests of its areas.** The tests related to a file
  most of the code imports — the route registry, a shared config, shared
  types — are most of the suite. A change to one of the profile's `hub files`
  runs the tests of the areas whose behaviour the diff changes, by a path
  filter (`vitest run <dir>` keeps the test files whose path contains it),
  and leaves the whole suite to the branch's full gate: such a commit is not
  recorded. Observed on a live project: `related` on a route registry ran
  1749 tests beside a running dev server — timeouts and two reruns.
- **The full gate — once per branch.** `review` runs it on the head it reads,
  `create-pr` and `promote` before the push. Each first runs `gate_record.py
  check <tree> --base <base>` and skips on `skip`, saying so: the head's tree
  passed it, or a run earlier on the branch did and every commit since is
  recorded. Every green full run on a clean tree → `record full`, whichever
  command ran it. A small change (`commands/task.md`, "The change's level")
  checks with `--small`: its commits' targeted checks stand for the gate,
  and `review` runs the full gate once only when a commit is not recorded:
  it touched a hub file, or an amend ran only its own rows over a path no
  row covers. Such a path otherwise ran it in its commit, recorded `full`.
- **Where the full gate runs** — the profile's `full gate`. `local`, and no
  key: as above. `ci`: the pipeline runs it on every pull request, and its
  status decides — no command runs it on its own, a commit whose paths all
  have rows still records `targeted`, and a local run `full`; `review`
  reports the checks' status on its head (`gh pr checks`) and does not rerun
  the targeted checks — the commits ran them, and over a whole range
  "related" nears the whole suite; a head not yet pushed, or pushed with no
  pull request, rests on its commits' checks; `create-pr` and `promote` push
  without it and merge only on green checks, by `create-pr`'s merge step. A
  red check is fixed by a new commit: the commit is already on the remote.
  Before the push they offer the full gate locally as the second option,
  only with a reason — the diff touches what the targeted
  checks do not narrow (configuration, dependencies, hub files, the gate
  itself); the commits will still change (a review or a round of fixes
  ahead, an amend); `merge method` is not `squash` — with CI recommended,
  the local run's price (the gate's measured time) and its gain (an amend
  instead of a fix commit, checks that stay green). No reason, no question.
- **Beside the work, not before it.** `review` starts the full gate in the
  background (Bash with `run_in_background`) before the rubric and reads the
  result before the report.
- **Red under load is not red by code.** When only timeouts fail while the
  machine is busy — a dev server, a stack, parallel agents — rerun the failing
  files alone and report both runs and the load. Neither green nor red is
  called without the rerun: passing alone, they make the full run green for
  the record once nothing is left unrun — a gate or a runner that stopped at
  the first failure has the parts and files after it run too, and they pass.
  Any other failure keeps it red. A dev server or stack the session started
  is stopped before a test run wider than a few files; one the owner runs is
  named in the report.
