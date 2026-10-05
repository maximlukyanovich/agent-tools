---
name: kickoff
description: How a piece of work is started and planned — plan mode, exploration, the questionnaire rules (a marked recommendation first, at most four questions a round, a closing "anything to add" always in the first round, later only when new input is plausible), the decisions table, slices, approval before code, separate commits on an explicit go-ahead, and proposing a project rule when a problem recurs. Use when starting any task that needs a plan, when about to ask the owner questions, and when the same kind of mistake shows up again. Not for trivial edits.
---

# kickoff

A task starts with a plan the owner has approved, not with code. The plan is
built from what the code says, from questions the code cannot answer, and from
the owner's decisions — recorded, not remembered.

## When it applies

Any task whose answer is not obvious from one file: a feature, an integration,
a refactor across modules, a workflow change. A typo, a one-line fix or a
rename does not need this.

## How to do it

1. **Enter plan mode** before reading widely. In plan mode the only file that
   changes is the plan file.

2. **Explore before asking.** Everything visible from code, config, git history
   and the design source is not a question. Use exploration subagents for broad
   sweeps (one per area, at most three in parallel); read the critical files
   yourself afterwards. Verify library versions and APIs through the docs tool
   rather than memory.

3. **Ask what the code cannot answer** — with the questionnaire tool, not as
   prose in chat:
   - **The recommendation goes first and is marked** `(Recommended)`. Every
     other option carries a one-line trade-off, so the owner can choose without
     asking back.
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
   execution order with the files each touches, assumptions the owner can
   overturn, open questions, and verification (how the result is proven — tests,
   a browser check, a curl).
   The plan is written in the language of the chat — the owner reads it in the
   approval dialog. Identifiers, paths and class names stay as they are;
   committed text (commits, PR bodies, code comments) keeps the repository's
   language.

6. **Ask for approval** through the plan-approval mechanism, not with a
   question in chat. The owner may return the plan with comments: apply them,
   ask for approval again.

7. **After approval**: code in slices, validate after each, verify in the real
   environment, and commit each slice separately — only on an explicit
   go-ahead, never pushed without its own.
   When the work is a queue of small tasks, each one ends at the base branch:
   its PR is merged there after green CI on the owner's go-ahead. Promotion up
   the branch chain (to staging, to production) happens in batches, only when
   the owner asks for it — not once per task.

8. **A problem that recurs** — the same class of mistake met again by a
   review, a check, a hook or the owner (a test missing for new behaviour, a
   gate failing the same way) — gets a one-line proposal of the rule that would
   have prevented it while working, in the project's repository: AGENTS.md, a
   project skill, a lint rule, a hook. A deterministic check beats a prose
   rule; one sighting is not yet a pattern.

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
section before approval is requested. Each slice ends with the validate command
green and a real check (browser, request, test) the plan named. Every commit was
preceded by an explicit go-ahead in that turn.
