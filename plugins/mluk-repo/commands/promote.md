---
description: Advance the work along the branch chain, one pull request per boundary, and check what it deploys.
argument-hint: '[<worktree | branch>] [<target-branch>]'
---

# /mluk-repo:promote

Walk the chain from `## Repository` (`chain`; without one, asked as
`${CLAUDE_PLUGIN_ROOT}/reference/profile.md` says) up to `<target>`. Every boundary that still has unpromoted commits is
one `/mluk-repo:create-pr merge` hop, preceded by a sync of the target into the
source when the target moved. A single hop to the next branch is the same as
`/mluk-repo:create-pr merge`; this command exists for several.

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
   protected branches. Already at or past the target →
   say so and finish.

4. **Walk each segment**, in order:

   - **Refresh and diff** — `git fetch origin <src> <dst> --prune`, then the
     commit list and `--stat` of `origin/<dst>..<src-ref>` (`<src-ref>` is the
     local branch for the first segment, `origin/<src>` after). Empty → skip
     the segment with a one-line note. Flag migrations, dependencies, runtime
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
     with none, go on. Wait for `ready` the way "Waiting for checks" in
     `${CLAUDE_PLUGIN_ROOT}/reference/commands.md` waits: bounded, errors in
     sight. The limit ran out → `not deployed`. Then run its `checks`
     yourself, before any checklist reaches the owner.

   Red CI, `not deployed` or a failed check stops the run, the failure first
   in the report; the remaining segments do not execute.

5. **Wrap up**: segments merged, segments skipped, PR URLs, each environment's
   checks and the checklist of only what needs a person, `git log --oneline
   -5` of the target, the `git-safety` reminder line, a checkout back to the
   branch the owner started on, then run `/mluk-repo:handoff` yourself,
   without asking.

## Hard rules

- Confirm before every `git push` and every `gh pr merge`. One yes at the start
  is not authorisation for the chain.
- Protected branches advance only through `gh pr merge`. Never a direct push,
  never `--force`, `--admin`, `--no-verify`, never a squash the profile did
  not ask for.
- `upstream` is never pushed to or targeted, even when convenient.
- This command does not commit. A dirty tree → `/mluk-repo:commit` first.
- Never go further than `<target>`.
- A check on an environment only reads, on production too: no form sent, no
  sign-in completed, nothing created.
