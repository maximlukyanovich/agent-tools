---
description: Merge the base branch (or a given one) into the current branch, run the profile's post-merge checks, and report only what the base shipped that this branch re-implements or conflicts with.
argument-hint: '[<source-branch>]'
---

# /mluk-repo:sync

Bring the base branch into the current feature branch. Reads `## Repository`
for `base branch`, `validate`, `post-merge checks`.

**Writes to git** (a merge commit). Token-efficient by design: this is not an
inventory of the codebase.

## Steps

1. **Pre-flight.** Dirty tree → refuse and offer `/mluk-repo:commit`; do not
   stash for the owner. Current branch is the source, or is protected → refuse.
   `git fetch origin <source> --quiet`.

2. **Merge.** `git merge origin/<source> --no-edit` — merge, not rebase, not
   squash; history is preserved. Conflicts → stop; the owner resolves, or the
   agent resolves only with the owner's decision per hunk. "Already up to
   date" → say so in one line and exit.

3. **Post-merge checks.** The profile's `post-merge checks` first (a second
   migration head, a lockfile drift, a generated file out of date) — report a
   hit as the top finding with the fix, and do not apply the fix yourself.
   Then `validate`; failures are shown and stop the report.

4. **Capture the boundary.**

   ```bash
   OUR_TIP=$(git rev-parse HEAD^1); SRC_TIP=$(git rev-parse HEAD^2)
   BASE=$(git merge-base "$OUR_TIP" "$SRC_TIP")
   git diff --name-only --diff-filter=AM "$BASE".."$SRC_TIP"   # what the base shipped
   git diff --name-only "$BASE".."$OUR_TIP"                   # what our branch changed
   ```

   Filter mentally: comment edits, renames without semantics and formatting
   are skipped. Look at the shared surface the project names (shared modules,
   `AGENTS.md`, the profile) — a changed rule may invalidate how our branch was
   written.

5. **Cross-check with cheap heuristics** — a name match, a behaviour match, a
   field computed in two places, a literal the base just turned into a config
   key. Open a file in full **only** on a hit.

6. **Report actionable deltas only**, at most ~8, each ≤ 4 lines:
   `base now provides: … / our branch has: file:line / suggested swap: … /
   blast radius: local | crosses N files | unclear`. Nothing found → one line.

## Hard rules

- Do not silently replace shared code; propose the swap, the owner decides.
- Do not run a migration merge or a lockfile regeneration yourself; report.
- Do not chase the usage graph of the base's new entity.
- Do not commit anything beyond the merge commit git created.
