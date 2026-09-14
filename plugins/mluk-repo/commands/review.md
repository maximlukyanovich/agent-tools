---
description: Review the current branch against the base branch, or a specific PR, and return findings sorted by severity with a file:line anchor each. Read-only; edits only with the fix argument.
argument-hint: '[<PR#>] [<severity>+] [full] [fix]'
---

# /mluk-repo:review

Review a pull request or the work on the current branch (committed and
uncommitted) against the profile's `base branch`, through the library rubric
plus the project lenses in `## Review`.

**Read-only by default**: no commits, no edits, no `gh` mutations. Edits only
with `fix`; posting to a PR only on an explicit yes at the end.

## Arguments

Positional, optional, any order — recognised by shape: a bare number is a PR;
`blocker+` / `major+` / `minor+` narrows what is written out in full; `full`
forces a complete pass instead of a delta over a target already reviewed in
this session; `fix` applies the narrow list of deterministic fixes after the
report, confirmed.

## Scope control

- A diff under ~25 files and ~2000 lines is reviewed inline. Past either,
  delegate to subagents **cut by file group**, each with its slice of the diff
  and the whole rubric; cap at 4–6. A subagent returns findings
  (`severity | tag | file:line | what | one-line fix | anchor`), never diff.
- Synthesis stays in the main thread: deduplicate, catch cross-slice problems
  (a field changed here, its test asserting the old shape there), normalise
  severities.
- Never read a file in full speculatively; open one only when a finding needs
  its context.
- A third pass over the same target → ask what new condition makes it useful
  before running.

## Steps

1. **Parse arguments; read the profile** (`base branch`, `validate`,
   `## Review`, `## Docs` for the contract log and techdebt file).

2. **Get the diff.** PR: `gh pr view <n> --json title,body,state,isDraft,
   headRefName,baseRefName` and `gh pr diff <n>`. Branch: `git fetch origin
   <base> --quiet`, `git diff origin/<base>...HEAD --stat`, `git status
   --porcelain`, `git diff`, `git ls-files --others --exclude-standard` —
   untracked files are the easiest thing to miss. `HEAD` on the base branch
   and no PR → nothing to review.

3. **Frame the scope** in one line from the branch name, PR text and commit
   subjects: a whole task or a slice? What a slice leaves out is not a missing
   feature — at most "expected in a follow-up".

4. **Run the rubric.** General lenses: `bug` (unhandled branches, `None`
   assumptions, boundary cases, a missing transaction), `perf` (N+1, a per-row
   query, a full scan on a hot path, a client-only fetch on an SEO surface),
   `dup` (a rule written inline next to the shared implementation), `test`
   (a behaviour change with no test, a test passing by coincidence),
   `convention` (commit format, placement, style drift), `docs` (behaviour or
   contract changed, document did not; a compromise as a `TODO` instead of a
   techdebt entry), `security` (a secret in the diff, a token logged, an auth
   shortcut widened, an object lookup not scoped to the requesting user,
   user content interpolated without bound), `contract` (a field renamed or
   retyped without a note in the contract log), `language` (a user-facing
   string in the wrong language). Project lenses from `## Review` are applied
   with the same weight as these.

5. **Assemble the report**: a one-line header (target, range, uncommitted
   included?, focus), the severity table (blocker / major / minor / nit), the
   verdict derived mechanically (`blocked` / `changes requested` / `ready to
   merge`), findings grouped by severity — each with tag, `file:line`, what is
   wrong, the anchor, a one-line fix — then "what is good" if there is anything
   honest to say, then open questions for the owner.

6. **Post to the PR** only for a PR target, only after printing, only on an
   explicit yes: `gh pr comment <n> --body-file <tmp outside the repo>`.

7. **`fix`** — confirmed, and limited to: unused imports and variables this
   diff introduced; a user-facing string in the wrong language where the
   surrounding code is unambiguous; a broken relative link with an unambiguous
   target; trailing whitespace in files the diff touches. Never: migrations,
   model or serializer shapes, permission logic, validators, test expectations,
   anything named in the profile's blast-radius list, structural refactoring.
   After fixing, run `validate` and close with one line.

## Hard rules

- Nothing is written during analysis.
- `blocker` / `major` need `file:line` **and** a reproducible scenario, a named
  mechanism, or a quoted rule. Vague findings are `nit`. Zero blockers is a
  legitimate result — do not inflate.
- What the validate command catches is one finding ("the suite is red"), not
  a scattering.
- Requirements are not invented; a suspected gap is "possible gap — check
  against the task".
