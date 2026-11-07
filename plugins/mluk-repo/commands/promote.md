---
description: Advance the work along the branch chain, one pull request per boundary, and check what it deploys.
argument-hint: '[<worktree | branch>] [<target-branch>]'
---

# /mluk-repo:promote

Walk the chain from `## Repository` (`chain`; without one, asked as
`${CLAUDE_PLUGIN_ROOT}/reference/profile.md` says) up to `<target>`. Every boundary that still has unpromoted commits is
one `/mluk-repo:create-pr merge` hop, preceded by a sync of the target into the
source when the target moved. A single hop to the next branch is
`/mluk-repo:create-pr merge` with the environment's check after it; this
command exists for several, and for that check.

**Writes to git and GitHub**, each action on confirmation.

## Steps

1. **Resolve the source and the target.** A branch of the chain after its
   first element is the target; a folder, or a branch outside the chain, is
   the source, resolved by `${CLAUDE_PLUGIN_ROOT}/reference/commands.md` —
   every step then runs in its tree. No source → the current branch; no
   target → the next branch after the source; anything else → stop with the
   chain printed. Print `source → target`.

2. **Pre-flight** as in `create-pr`: clean tree, correct remote alias and `gh`
   account, `upstream` out of scope, and when the first source is the working
   branch the gate: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/gate_record.py" check <tree> --base <base>`
   (`--small` for a small change) says `skip`, or the full `validate` is
   green and recorded the same way (`record full <tree>`). With `full gate:
   ci`, no local run — the question with a reason, or nothing, and the merge
   waits for green checks.

3. **Build the segments** — the chain prefix ending at the target:
   the working branch → the first protected branch, then each hop between
   protected branches. Already at or past the target → say so, run step 4's
   **Check the environment** on the target after `git fetch origin <target>`,
   then step 5.

4. **Walk each segment**, in order:

   - **Refresh and diff** — `git fetch origin <dst> --prune`, `<src>` too
     after the first segment (a merged feature branch may be gone from
     origin, and fetching it fails), then the commit list and `--stat` of
     `origin/<dst>..<src-ref>` (`<src-ref>` is the local branch for the first
     segment, `origin/<src>` after). Empty, or `<src-ref>` is the
     `headRefOid` of a merged PR (`gh pr list --head <src> --base <dst>
     --state merged --json headRefOid`) — a squash leaves the commits outside
     `<dst>` — → a one-line note and straight to **Check the environment**: a
     rerun after a stop comes this way. Flag migrations, dependencies, runtime
     keys, blast-radius paths for the PR body.
   - **Sync when the target moved** — if `origin/<dst>` has commits not in
     `<src>`, run the `sync` procedure into `<src>` first (merge, conflicts
     stop the run, post-merge checks). A protected source (an intermediate branch of
     the chain) is never pushed directly: its sync PR is the same hop.
   - **Show the texts** — the `create-pr` step 3 with `<dst>` as target. For a
     hop between protected branches the body aggregates since the last
     promotion.
   - **Push the source** — a feature branch only when ahead, on confirmation.
     A protected source ahead of origin is an error: a protected branch was
     edited by hand.
   - **PR + CI + merge** — the `create-pr` steps 5–6 with `<dst>` as target.
     For the production branch **re-confirm separately**, even when the run
     started with it as the argument.
   - **Pull the merged target locally** with `--ff-only`; a failure stops the
     run.
   - **Check the environment** when `environments` has a row for `<dst>`;
     with none, go on. Wait for `ready`, its `<sha>` being
     `git rev-parse origin/<dst>`, the way "Waiting for checks" in
     `${CLAUDE_PLUGIN_ROOT}/reference/commands.md` waits: bounded by the row's
     `limit`, errors in sight. The limit ran out → `not deployed`, with
     `ready`'s last output; exit 126 or 127, the command never ran → `not run`.
     Then run its `checks` yourself, before any checklist reaches the owner;
     one that cannot run — a tool or an access is missing — is `not run` too.

   Red CI, `not deployed`, `not run` or a failed check stops the run, the
   failure first in the report; the remaining segments do not execute.

5. **Wrap up**, after a stop too: segments merged, segments skipped, PR URLs,
   each environment's checks and, with a row, the checklist of only what needs
   a person — what the range changed that its `checks` cannot reach —
   `git log --oneline -5` of the target, the `git-safety` reminder line, a
   checkout back to the branch the owner started on, then run
   `/mluk-repo:handoff` yourself, without asking. A stop on an environment says
   the merge is done and the environment unproved, and skips the handoff, whose
   first rows would offer the next task. Its block is
   `/mluk-repo:promote <the branch it stopped on>`, whose rerun checks that
   environment again and goes no further — a rerun to `<target>` would start
   past it — with `/mluk-repo:promote <target>` named for after; after a
   failed check, `/mluk-repo:task <what failed>` comes first.

## Hard rules

- Confirm before every `git push` and every `gh pr merge`. One yes at the start
  is not authorisation for the chain.
- Protected branches advance only through `gh pr merge`. Never a direct push,
  never `--force`, `--admin`, `--no-verify`, never a squash the profile did
  not ask for.
- `upstream` is never pushed to or targeted, even when convenient.
- This command does not commit. A dirty tree → `/mluk-repo:commit` first.
- Never go further than `<target>`.
- A check on an environment, `ready` included, only reads, on production too:
  nothing created, no sign-in completed, no form sent but the request that
  opens the provider's window.
