---
name: kickoff
description: How a piece of work is started and planned — plan mode, the questionnaire rules, the decisions table, slices, a state table for a state change, approval before code, commits on a go-ahead, a project rule when a problem recurs. Use when starting any task that needs a plan, before asking the owner questions, and when the same mistake shows up again. Not for trivial edits.
license: MIT
metadata:
  author: Maxim Lukyanovich
  source: https://github.com/maximlukyanovich/agent-tools
---

# kickoff

A task starts with a plan the owner has approved, not with code. The plan is
built from what the code says, from questions the code cannot answer, and from
the owner's decisions — recorded, not remembered.

## When it applies

Any task whose answer is not obvious from one file: a feature, an integration,
a refactor across modules, a workflow change. A typo, a one-line fix or a
rename does not need this. `/mluk-repo:task` names the change's level first —
small, normal or critical ("The change's level" there): a small change takes
a short plan in chat and the owner's yes instead of steps 1, 3 and 6, and its
yes is the approval this skill asks for.

## How to do it

1. **Enter plan mode** before reading widely. In plan mode the only file that
   changes is the plan file.

2. **Explore before asking.** Everything visible from code, config, git history
   and the design source is not a question. Use exploration subagents for broad
   sweeps (one per area, at most three in parallel); read the critical files
   yourself afterwards. Verify library versions and APIs through the docs tool
   rather than memory. When the task builds screens from the design source,
   check each screen's design status — by the Design canvas (a module's page
   is ready, a page on review is not), by the per-screen statuses the
   profile's `## Sources of truth` names, or by the owner's word quoted with
   its date in the plan. A screen not ready goes into the last slice and a
   risk line of the plan.

3. **Ask what the code cannot answer** — with the questionnaire tool, not as
   prose in chat:
   - **The recommendation goes first and is marked** `(Recommended)`. Every
     other option carries a one-line trade-off, so the owner can choose without
     asking back.
   - **A screen with no design status found is a question** of the first
     round — where the statuses are kept, or the owner's word — and the
     answer is recorded; "no status found" is not a finding.
   - **At most four questions a round.** More than one round is fine; a wall of
     questions is not.
   - **Multi-select where choices are not exclusive** (which providers, which
     plugins, which slices).
   - **A closing "anything to add?" question ends the first round, always.** The
     owner often holds a requirement the code cannot show, and without the question
     they have to interrupt the work to add it. In later rounds ask it only when
     new input before the work starts is plausible — a design the owner may have,
     constraints only they know, material they want to attach. Its options: "no,
     all covered" and "yes, I will describe it in chat" — the latter lets the owner
     write freely and attach images in the next message. It counts toward the four.
   - **Read the answers literally.** An answer may change direction, add a
     constraint or decline; follow what it says, not what was expected.

4. **Record decisions as a table** in the plan — question → decision — so the
   plan can be re-read without the chat. Repeat the table's essence in the
   project's documentation when the plan is executed.

5. **Write the plan**: context (why this change, what prompted it), the
   decisions table, the recommended architecture (one, not a survey), slices in
   execution order with the files each touches (for a shared function,
   hook or component the plan changes: its call sites and how each keeps its
   behaviour), assumptions the owner can
   overturn, open questions, and verification (how the result is proven — tests,
   a browser check, a curl).
   A change to state — a hook's or a component's lifecycle, a store, a state
   machine, an async flow, a timer — adds three things: a **state table**
   (state × event → expected → its proof, a test or a live check by
   `${CLAUDE_PLUGIN_ROOT}/reference/proof.md`; its rows include the state
   lists of the project's testing skill — the profile's `testing skill`,
   loaded before the table is written; in UI, every element that
   leaves while it may hold the focus — a button its own press replaces, a
   row a re-read removes — with where the focus goes); **what we rely on in
   the framework**, each point with `file:line` in the library's source or
   the docs URL; and one line on **why not the structural option** — the
   change that would make the bad state impossible to express (a reset by
   key, a reducer, a discriminated union).
   When the plan describes access — who sees what, and where — the state
   table serves better as a who × where table with the states before and
   after a reset (a link reissued, rights revoked), and under it the events
   that move a person between columns mid-flow: a missed combination is an
   empty cell.
   The plan is written in the language of the chat — the owner reads it in the
   approval dialog. Identifiers, paths and class names stay as they are;
   committed text (commits, PR bodies, code comments) keeps the repository's
   language.

6. **Ask for approval** through the plan-approval mechanism, not with a
   question in chat. The owner may return the plan with comments: apply them,
   ask for approval again.

7. **After approval**: code in slices, the targeted checks of what changed
   after each edit (`${CLAUDE_PLUGIN_ROOT}/reference/commands.md`, "The
   gate"; the full gate runs once, in the review and before the push), verify
   in the real environment, and commit each slice separately — only on an
   explicit go-ahead, never pushed without its own. Inside each slice:
   - **A change carries its proof**, by
     `${CLAUDE_PLUGIN_ROOT}/reference/proof.md`: a test in the same commit
     for a change in a risk class (money, data written or deleted, access, a
     merge, what lets a confirmation through, branching logic, a costly break
     where nobody looks), a recorded
     live check for the rest, a run against the old code for a test that may
     pass by coincidence, and one read of the slice's diff before the commit.
     A test promised for "the next commit" is the gap reviews keep finding.
   - **A state change starts from its transition table** — the rows of the
     plan's state table it touches, each with its proof by the same file. The
     commit lists the rows it covers.
   - **Shared code changes only when the change is right for every consumer.**
     Walk the call sites first; a need that only one caller has stays with that
     caller.
   - **A changed statement changes everywhere.** Before committing an edit to
     a rule, a fact or a name in prose, `git grep` its key terms across the
     committed documents and the harness and fix every copy in the same
     commit — better still, keep one source and point at it. A copy left
     behind is the finding a review keeps returning to.
   - **Extending shared code is backward-compatible.** A new parameter is
     optional and its default keeps the old behaviour; existing calls keep
     their meaning. When compatibility cannot hold, every caller is migrated
     in the same change — never a shared signature that half the callers
     misread.
   - **A fix for a review finding is checked on every path through what it
     changed**, not only on the finding's scenario: each kind a shared view
     serves, each consumer of a changed contract. A fix that breaks a
     neighbour costs a whole review pass more than the check does.
   A slice ends with its next step as code blocks, one per option: the
   commit command while the slice is uncommitted; once it is committed and
   the plan goes on, continuing here after `/compact <focus>`, or the plan's
   continue prompt for a fresh session, which `/mluk-repo:handoff` prints.
   The task's last commit hands the review over through `commit` — to a
   fresh session, or here for a small change while its measured diff stays
   small; a critical change's review is never here.
   When the work is a queue of small tasks, each one ends at the base branch:
   its PR is merged there after green CI on the owner's go-ahead. Promotion up
   the branch chain (to staging, to production) happens in batches, only when
   the owner asks for it — not once per task.

8. **A problem that recurs** — the same mechanism met a second time by a
   review, a check, a hook or the owner (a test missing for new behaviour, a
   gate failing the same way) — gets a one-line proposal moving it to the
   cheapest layer that would have caught it while working: in the project's
   repository — AGENTS.md, a project skill, a lint rule, a hook — or, when
   the rule survives a change of project, in `mluk-agent-tools`. The owner
   decides where, and whether. Name the mechanism ("a fix closed one state
   of a request and left its twin"), not the incident ("the retry button in
   the feed"). A deterministic check beats a prose rule; a single sighting is
   a fix, not a rule.

## How not to do it

- Asking one question per turn, or asking what `git log` already answers.
- Presenting three architectures without a recommendation.
- Writing the plan in the commit language when the chat is in another one — the
  owner approves what they read.
- Marking the recommendation nowhere, so the owner has to guess which option
  is safe.
- Writing code "to show the idea" before the plan is approved.
- Treating one approval as permission for the whole chain of commits and
  pushes.
- Recording decisions only in chat, so the next session re-asks them.

## How it is verified

The plan file exists and has the decisions table, slices and a verification
section before approval is requested. Each slice ends with its targeted checks
green and a real check (browser, request, test) the plan named. Every commit was
preceded by an explicit go-ahead in that turn.
