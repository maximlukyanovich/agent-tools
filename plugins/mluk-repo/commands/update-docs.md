---
description: Measure how far the code drifted from the last documentation update, classify the changes, and propose targeted patches by the profile's doc map — including docs in a sibling repository. Writes after confirmation, commits nothing.
argument-hint: '[<base-ref>]'
---

# /mluk-repo:update-docs

Bring documentation back in line with the code after substantive changes.
On demand, not on every commit. Reads `## Docs` (`technical`, `product`,
`contract log`, `roadmap`, `techdebt`, `map`).

**Writes after confirmation.** Never commits — documentation ships in the
same commit as the code, through `/mluk-repo:commit`.

## Steps

1. **Resolve the baseline** — `$1` verbatim, else the last commit that touched
   the technical docs:

   ```bash
   git log -1 --format='%H %ad %s' --date=short -- <technical doc paths>
   ```

   State it: `<sha> — "<subject>" (<date>)`.

2. **Collect the drift** — `git diff <base>..HEAD --stat` and `--name-only`
   over source, config and harness paths, excluding the doc paths themselves;
   `git log <base>..HEAD --oneline`; and the doc side too, so already-done
   work is not proposed again. Read file diffs selectively. No drift → one
   line, stop.

3. **Classify each change** with one dominant category — architecture,
   contract (what clients see), data model, behaviour (what the user sees),
   convention, techdebt (a deliberate compromise), minor (no doc needed).
   Flag ambiguous ones for the owner.

4. **Pick the targets** from the profile's `map`. Rules that bind:
   - A behaviour or contract change that reaches a client is a **product-doc**
     change and a **contract-log** entry, named with the repository when the
     product docs live in a sibling. A sibling is named by slug in the profile;
     its clone on this machine comes from the local profile's `## Siblings`.
   - A compromise goes to the techdebt file with reason and priority, not into
     a `TODO` comment.
   - Reuse an existing document; never leave an empty stub.
   - Any status or scope change is reflected in the roadmap even when nothing
     else changes.
   - Do not invent a source, an endpoint or a rationale to make a document look
     complete; unverified is said to be unverified.

5. **Output**: a classification table (file group → category → target → what
   diverged, repository marked), targeted patch fragments per document (what
   to remove, what to add, in which section), a separate block for owner
   decisions (new techdebt entries, contract gaps, open questions — each with
   context, options, recommendation).

6. **Apply after confirmation** with the editing tools. Patches to a sibling
   repository are applied there only when the owner says so — it has its own
   branch and its own commit preset.

## Hard rules

- No writes before confirmation; no commits at all.
- Compact report, ordered by impact, contract divergences first.
