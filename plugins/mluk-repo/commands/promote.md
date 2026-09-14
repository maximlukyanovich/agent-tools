---
description: Advance the current work along the profile's branch chain up to the target, one pull request per boundary — sync, PR, CI, merge — confirming at every boundary. Never touches upstream.
argument-hint: '[<target-branch>]'
---

# /mluk-repo:promote

Walk the chain from `## Repository` (`chain`, default `feature/* → develop →
main`) up to `<target>`. Every boundary that still has unpromoted commits is
one `/mluk-repo:create-pr merge` hop, preceded by a sync of the target into the
source when the target moved. A single hop to the next branch is the same as
`/mluk-repo:create-pr merge`; this command exists for several.

**Writes to git and GitHub**, each action on confirmation.

## Steps

1. **Resolve the target.** Given → must be a branch in the chain, else stop
   with the chain printed. Not given → the next branch after the current one.
   Print `current → target`.

2. **Pre-flight** as in `create-pr`: clean tree, correct remote alias and `gh`
   account, `upstream` out of scope, `validate` green when the first source is
   the working branch.

3. **Build the segments** — the chain prefix ending at the target:
   `feat/x → develop`, then `develop → main`. Already at or past the target →
   say so and finish.

4. **Walk each segment**, in order:

   - **Refresh and diff** — `git fetch origin <src> <dst> --prune`, then the
     commit list and `--stat` of `origin/<dst>..<src-ref>` (`<src-ref>` is the
     local branch for the first segment, `origin/<src>` after). Empty → skip
     the segment with a one-line note. Flag migrations, dependencies, runtime
     keys, blast-radius paths for the PR body.
   - **Sync when the target moved** — if `origin/<dst>` has commits not in
     `<src>`, run the `sync` procedure into `<src>` first (merge, conflicts
     stop the run, post-merge checks). A protected source (`develop`) is never
     pushed directly: its sync PR is the same hop.
   - **Push the source** — feature branches and `develop` only when ahead, on
     confirmation. A source of `main` ahead of origin is an error: a protected
     branch was edited by hand.
   - **PR + CI + merge** — the `create-pr` steps 3–6 with `<dst>` as target.
     For a `develop → main` hop the body aggregates since the last promotion.
     For the production branch **re-confirm separately**, even when the run
     started with it as the argument.
   - **Pull the merged target locally** with `--ff-only`; a failure stops the
     run.

   Red CI stops the run; the remaining segments do not execute.

5. **Wrap up**: segments merged, segments skipped, PR URLs, `git log --oneline
   -5` of the target, the `git-safety` reminder line, and a checkout back to
   the branch the owner started on.

## Hard rules

- Confirm before every `git push` and every `gh pr merge`. One yes at the start
  is not authorisation for the chain.
- Protected branches advance only through `gh pr merge`. Never a direct push,
  never `--force`, `--admin`, `--no-verify`, never a squash the profile did
  not ask for.
- `upstream` is never pushed to or targeted, even when convenient.
- This command does not commit. A dirty tree → `/mluk-repo:commit` first.
- Never go further than `<target>`.
