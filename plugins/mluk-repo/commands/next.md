---
description: Recommend what to take next — from the roadmap, local notes, open issues and PRs, and the branch chain. Offers a roadmap status patch, written only on confirmation.
argument-hint: '[<focus>]'
---

# /mluk-repo:next

Answer one question: **what do we do next?** The answer is one recommended
task with the reason, then what else is ready, what waits and on whom, and the
housekeeping the repository needs before or alongside it.

There is no tracker. The plan lives in the repository's own documents (the
profile's roadmap, the notes its brief sources name, GitHub issues) and its
state lives in git and in open pull requests. The recommendation needs both: a
roadmap says what comes next, git says what is already half done.

**Read-only, with one exception:** a roadmap status patch, written only after
the owner confirms it. Nothing is committed, pushed, opened or started.

## Steps

1. **Scope.** `$1` is a free-text focus — an area, a section, a theme
   (`backend`, `deploy`, `player`). With a focus, every section of the report
   keeps only what relates to it, and says what the focus left out in one
   line. Without one, the whole queue.

2. **Read the profile** — `.claude/project-profile.md` and this clone's
   `project-profile.local.md` if present: `## Docs` (`roadmap`, `techdebt`,
   `contract log`), `## Task` (`brief sources`), `## Repository` (`base
   branch`, `chain`, `upstream`). A roadmap in a sibling repository is read
   from the clone the local `## Siblings` names, else through
   `gh api repos/<owner>/<repo>/contents/<path>`. No profile → say so, offer
   `/mluk-bootstrap:setup`, and work with `AGENTS.md` and `docs/`.

3. **Read the plan.**
   - **The roadmap's queue** — the part that orders work: a priority table, a
     numbered list, a "next" section with statuses. Read its own conventions
     too (status markers, where finished work moves), the open questions it
     marks, and the decisions it says are waiting for someone.
   - **Notes** the `brief sources` name under `docs/local/` — the newest
     first. A note that names next steps is a source; one that contradicts
     the roadmap is a finding, not an override.
   - **Open GitHub issues** — `gh issue list --state open`.
   - **Techdebt** entries with a priority high enough to compete with work.

4. **Read the delivery state** in one Bash call where possible:

   ```bash
   git fetch -q; git branch --show-current; git status --porcelain | head
   git for-each-ref --format='%(refname:short)' refs/heads \
     | while read b; do n=$(git rev-list --count origin/<base>..$b 2>/dev/null); [ "${n:-0}" -gt 0 ] && echo "$b $n"; done
   git branch --merged origin/<base> | grep -v -E '^\*|<protected branches>'
   gh pr list --state open --json number,title,headRefName,baseRefName,isDraft,reviewDecision,statusCheckRollup
   ```

   For each adjacent pair in `chain` after the base (`develop → staging`,
   `staging → main`): `git rev-list --count origin/<next>..origin/<prev>` —
   work waiting for promotion. With an `upstream` in the profile, read the
   state of the pull request into it; never act on it.

5. **Work out, per candidate:**
   - **Started** — an open PR or a branch with unmerged commits. Finishing it
     goes before anything new.
   - **Blocked**, and by what — the roadmap's order, a question it marks
     open, a decision it says waits for a named person, a dependency the text
     names. Say where the block comes from. A dependency is what a document
     or git says, never a guess: a task with none is "no dependency
     recorded", not "unblocked".
   - **Status drift** — work merged into the base while the roadmap still
     lists it as planned or in progress; a roadmap row for a branch that no
     longer exists; a note that disagrees with the roadmap.

6. **Rank the ready candidates:** started work first, then the roadmap's
   order, then how much each one unblocks, then the smaller one. Name the
   tie-break used.

7. **Report**, in the conversation's language (the profile's `## Languages`
   `conversation`, else Russian); identifiers and quotes stay verbatim:
   - **Recommended** — one task, where it comes from (roadmap row, issue,
     note), one paragraph on why it goes before the runner-up.
   - **Also ready** — one line each, with the reason it ranks lower.
   - **Waiting** — one line each: what, and on what or whom.
   - **Housekeeping** — PRs ready to merge, work waiting for promotion with
     the ready line (`/mluk-repo:promote <target>`), merged branches not yet
     deleted, status drift.
   - **Decisions for the owner** — named as decisions, not ranked as work.

8. **Offer the roadmap patch** when step 5 found drift: the exact edit, in
   the roadmap's own conventions (its status markers, its rule for where
   finished work goes). Apply it with the editing tools only after the owner
   says yes. A roadmap in a sibling with no local clone gets the patch shown,
   not applied. Never commit it — that is `/mluk-repo:commit`, in the
   repository that owns the roadmap.

9. **End** with the next command in a code block, ready to copy:

   ```
   /mluk-repo:task <a one-line brief of the recommended task>
   ```

## Hard rules

- The only write is a confirmed roadmap patch. No commit, push, PR, merge,
  branch or issue change; the task is started by the owner with `task`.
- One recommendation, stated as one. A list of "you could" is the question
  handed back.
- The plan comes from the documents, the issues and git — not from memory of
  earlier sessions. What a document does not say is reported as missing.
- Never re-estimate or re-prioritise silently: a ranking that goes against
  the roadmap's order says so and why.
