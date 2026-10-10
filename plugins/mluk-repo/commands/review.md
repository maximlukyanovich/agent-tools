---
description: Review the current branch — or a named branch or worktree, or a specific PR — against the base branch, and return findings sorted by severity with a file:line anchor each. Keeps a pass ledger so a repeat run reviews only what changed. Read-only apart from the ledger; edits only with the fix argument.
argument-hint: '[<PR#> | <branch> | <worktree-path>] [<sha>..<sha>] [<severity>+] [full] [fix]'
---

# /mluk-repo:review

Review a pull request or the work on a branch (committed and uncommitted) —
the current one, or one named, typically living in a worktree — against the
profile's `base branch`, through the library rubric plus the project lenses in
`## Review`.

**Read-only by default**: no commits, no code edits, no `gh` mutations. The one
file it writes is its own ledger (below). Code edits only with `fix`; posting to
a PR only on an explicit yes at the end.

**Run it in a fresh session**, not the one that wrote the code. The authoring
session remembers its own reasons and tends to confirm them. Everything a review
needs from the past is in the ledger, not in the conversation. The fresh
session may sit in the main tree: a branch in a worktree is reached by name.

## Arguments

Positional, optional, any order — recognised by shape: a bare number is a PR;
`<sha>..<sha>` is an explicit commit range; `blocker+` / `major+` / `minor+`
narrows what is written out in full; `full` ignores the ledger's delta and
reviews the whole target; `fix` applies the narrow list of deterministic fixes
after the report, confirmed. A path is a worktree folder; any other word that
names a local branch (`git rev-parse --verify refs/heads/<word>`) is that
branch.

## The tree under review

A named branch, or a worktree folder, is reviewed **where it is checked out**:
`git worktree list --porcelain` gives its folder, and from then on every git
command is `git -C <folder> …`, every file is read from that folder, and
`validate` runs there. The ledger stays the repository's — at the profile's
`ledger` path in the main tree. A named branch checked out nowhere is reviewed
from git alone (`git diff origin/<base>...<branch>`, files via
`git show <branch>:<path>`), and the header says that `validate` did not run.

No argument and the current branch is the base: look for the work instead of
stopping — the worktrees whose branch is ahead of the base
(`git rev-list --count origin/<base>..<branch>`). Exactly one → review it and
name it in the header; several → ask which; none → nothing to review.

## The ledger

One file per target at the profile's `ledger` (default `docs/local/reviews/`,
which must be gitignored). Named by the first of: the task key in the branch
name, the PR number (`pr-<n>`), the branch slug. A PR that appears later is
added to `Aliases:`; the file is not renamed.

```
# Review ledger — <key>
Aliases: PR #12, feat/<slug>
Trajectory: P1 a1b2c3d 0/2/5/5 changes · P2 e4f5a6b 0/0/1/2 ready
## Open
- R3 minor bug src/api/client.ts:114 — error body lost when it is not JSON
## Pass 2 — <date> — head e4f5a6b · base a1b2c3d · delta — ready to merge
- R9 minor fix-critique src/api/client.ts:83 — helper duplicated in connect.ts — open
```

Finding ids `R<n>` never change between passes. Status is one of `open`,
`fixed`, `deferred (<reason>)`, `false-positive (<mechanism>)`, `disputed`.
Only `Trajectory` and `Open` are read by default; pass sections are appended,
never rewritten.

## Scope control

- A diff under ~25 files and ~2000 lines is reviewed inline. Past either,
  delegate to subagents **cut by file group**, each with its slice of the diff
  and the whole rubric but **not the ledger**; cap at 4–6. A subagent returns
  findings (`severity | tag | file:line | what | one-line fix | anchor`), never
  diff.
- Synthesis stays in the main thread: deduplicate, catch cross-slice problems
  (a field changed here, its test asserting the old shape there), normalise
  severities.
- Never read a file in full speculatively; open one only when a finding needs
  its context.

## Steps

1. **Parse arguments; read the profile** (`base branch`, `validate`,
   `## Review` with `ledger`, `design source` and `consumers`, `## Docs` for
   the contract log and techdebt file).

2. **Find the ledger and set the target.** `HEAD` below is the head of the
   tree under review.
   - The ledger's last head equals `HEAD` and no `full` → there is nothing new:
     print the recorded verdict and the open findings, and stop.
   - The last head is an ancestor of `HEAD` → the target is the delta
     `<last head>..HEAD`.
   - No ledger, or `full` → the whole target as below. An explicit range
     overrides both.

3. **Get the diff.** PR: `gh pr view <n> --json title,body,state,isDraft,
   headRefName,baseRefName` and `gh pr diff <n>`. Branch: `git fetch origin
   <base> --quiet`, `git diff origin/<base>...HEAD --stat`, `git status
   --porcelain`, `git diff`, `git ls-files --others --exclude-standard` —
   untracked files are the easiest thing to miss — all in the tree under
   review. `HEAD` on the base branch, no PR and no worktree ahead of it →
   nothing to review. Run the profile's `validate` once, in that tree.

4. **Frame the scope** in one line from the branch name, PR text and commit
   subjects: a whole task or a slice? What a slice leaves out is not a missing
   feature — at most "expected in a follow-up". If this session edited files in
   the diff, say so in the header and recommend a fresh session.

5. **Run the rubric, blind.** Do not open the ledger's findings yet — reading a
   previous verdict first anchors this one. General lenses: `bug` (unhandled
   branches, `None` assumptions, boundary cases, a missing transaction; for
   async code and stateful hooks, walk the lifecycle transitions — A→B mid-event,
   A→none→A — and a peer that misbehaves, such as a 200 that closes at once),
   `perf` (N+1, a per-row query, a full scan on a hot path, a client-only fetch
   on an SEO surface), `dup` (a rule written inline next to the shared
   implementation), `test` (a behaviour change with no test in the same commit is its own
   `major`, unless it is genuinely untestable and the commit says why; a test
   passing by coincidence), `shared` (a change to a shared function, hook or
   component that alters behaviour for an existing caller — walk every call
   site; an extension that is not backward-compatible and did not migrate its
   callers is `major`), `convention` (placement, style drift), `docs` (behaviour or
   contract changed, document did not; a type's doc comment contradicted by the
   code; a compromise as a `TODO` instead of a techdebt entry), `security` (a
   secret in the diff, a token logged, an auth shortcut widened, an object
   lookup not scoped to the requesting user, user content interpolated without
   bound), `contract` (a field renamed or retyped without a note in the contract
   log), `language` (a user-facing string in the wrong language). Project
   lenses from `## Review` carry the same weight. A finding names **every** place
   with the same mechanism, not only the first one found. UI in the diff is
   checked against the profile's `design source` (read only). A contract change
   — a field, an endpoint, a payload's shape or timing — is followed into each
   `consumers` repository's call sites (its clone from the local profile's
   `## Siblings`); a consumer that now misreads it is a
   finding here.

6. **Try to refute each `blocker` / `major`** in the code before keeping it — a
   guard elsewhere, a caller that never passes the bad input. What survives is
   reported; what does not is dropped or demoted with the reason. Every claim
   about a library's behaviour — in a finding or under "what is good" — is
   checked in its source or by a probe outside the repository, not assumed; a
   comment or test name that promises a behaviour needs a case that would fail
   without it.

7. **Reconcile with the ledger.** Now read it, and tag every finding:
   `new` (code after the last reviewed head), `missed` (older code, never raised
   — keeps its honest severity, marked "missed in pass N"), `escalated` (a
   deferred finding raised higher — only with a named new cause, otherwise it
   keeps its old severity), `fix-critique` (targets a fix a previous pass asked
   for). A recorded false positive is not raised again without a new mechanism.

8. **Assemble the report.** It always opens with the same block, on every
   pass, zeros included — the owner compares passes by it (labels in the
   chat's language):

   ```
   **Review `<target>`, pass <N>.** <range>, <commits>, <files / lines>; uncommitted: <yes / no>; focus: <…>
   Trajectory: P1 <head> <b/m/m/n> <verdict> → P2 <head> <b/m/m/n> <verdict>

   | blocker | major | minor | nit |
   |---|---|---|---|
   | <n> | <n> | <n> | <n> |

   **Verdict: <blocked / changes requested / ready to merge>.**
   ```

   The verdict is derived mechanically from the table. Then the findings,
   grouped by severity — each with tag, class, `file:line`, what is wrong, the
   anchor, a one-line fix
   — then "what is good" if there is anything honest to say, then open
   questions for the owner. When a finding's class has come up before — in
   earlier passes of this ledger, in other ledgers, or in several places of
   this diff — add one line proposing the rule in the project's repository that
   would prevent it during the work (kickoff step 8). Propose a check first — a
   lint rule, a test, a hook — and a line in AGENTS.md or a skill only when the
   rule cannot be checked. **Stop and ask** what a further pass should add
   when this is pass 3+ with no new commits, when findings grew while the delta
   is small, or when `escalated` plus `fix-critique` are over half the findings.

9. **Append the pass to the ledger** — without asking; it is gitignored and
   holds only the review's own memory. Update statuses the owner stated.

10. **Post to the PR** only for a PR target, only after printing, only on an
    explicit yes: `gh pr comment <n> --body-file <tmp outside the repo>`.

11. **`fix`** — confirmed, and limited to: unused imports and variables this
    diff introduced; a user-facing string in the wrong language where the
    surrounding code is unambiguous; a broken relative link with an unambiguous
    target; trailing whitespace in files the diff touches. Never: migrations,
    model or serializer shapes, permission logic, validators, test expectations,
    anything named in the profile's blast-radius list, structural refactoring.
    After fixing, run `validate` and close with one line.

## Hard rules

- Nothing but the ledger is written during analysis.
- `blocker` / `major` need `file:line` **and** a reproducible scenario, a named
  mechanism, or a quoted rule. Vague findings are `nit`. Zero blockers is a
  legitimate result — do not inflate.
- Verdicts are stable: the same commits get the same verdict. A change is
  explained by its class — new commits, a missed finding, a stated escalation
  cause, a withdrawn finding with its mechanism.
- What `validate`, the linter or a git hook catches is one finding ("the gate is
  red"), not a scattering, and not repeated as judgement.
- Requirements are not invented; a suspected gap is "possible gap — check
  against the task".
