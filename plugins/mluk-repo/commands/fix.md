---
description: Fix the open findings of a review pass — read the ledger, the plan and each finding's anchor, make the narrow fix with its proof, read the round's diff once for side effects, then hand over to commit. Edits code; never commits by itself.
argument-hint: '[<worktree | branch>] [R<n> …]'
---

# /mluk-repo:fix

One round of fixes for the findings a review left in its ledger. A round
costs in proportion to its findings — a document or a one-line fix takes
minutes, a round on a small task about twenty to thirty — and what turns it
into hours is the measures added on top of the fixes, not the fixes. So the
round makes the narrow fix for every finding it takes, proves each by its
risk, and asks before anything that costs more.

**Edits code** in the target's tree. Never commits, pushes or posts:
`/mluk-repo:commit` makes the commit, on its own go-ahead. Run it in a fresh
session, as the review's handoff prints it.

## Arguments

A leading folder or local branch is the work to fix, by
`${CLAUDE_PLUGIN_ROOT}/reference/commands.md`; none → the session's tree.
Ids (`R3 R7`) choose the findings; none → every open `blocker` and `major`
plus the `fix-now` ones. The rest are named in the report as left open.

## Steps

1. **Read the state** — the profile (`targeted checks`, `validate`, `## Docs`
   `techdebt`, `## Review` `ledger`), the ledger's `Open` and its last pass,
   the plan found as `handoff` finds it. Only the chosen findings' lines.

2. **Read by anchor** — each finding's `file:line`, its callers and the test
   beside it, not the module in full.

3. **Set the scope before the first edit** — a short list in the chat: each
   id, the narrow fix, the proof it will carry. Ask, in one question with the
   cost in minutes, before:
   - a structural fix — moving logic out, moving tests, a new convention. The
     default is the narrow fix, with the structural alternative recorded in
     the `techdebt` file; the structure goes ahead only on a yes;
   - a long measure — agents critiquing the plan or the delta, a batch of
     reverts, a repeated full gate or build;
   - a parser, a protocol or a format of its own where the code already uses
     a library for the job — the library is the answer.

   A round that will plainly take longer than its findings suggest says so
   here, with why.

4. **Fix one finding at a time.** The narrow change. A mechanism the fix
   introduces covers every site of its class, not only the sites the finding
   named. A fix that changes state starts from its transition rows
   (`kickoff`). Each fix takes its proof by
   `${CLAUDE_PLUGIN_ROOT}/reference/proof.md`, and the targeted checks of the
   paths it changed run after it (`reference/commands.md`, "The gate") —
   not the full gate.

5. **Read the round's diff once** for what else each change does
   (`reference/proof.md`, "One read of the diff before the commit"); a doubt
   becomes a row, a check or a report line.

6. **Close every finding taken.** One that cannot be closed in the round — it
   waits on an answer, a key, another team — is named with its reason; none
   drops out silently.

7. **Report** — one table, then the checks that ran and what they did not
   exercise:

   | Finding | Change | Proof | Left |
   | --- | --- | --- | --- |
   | R3 | `client.ts:114` keeps a text body | `client.test.ts` "non-JSON error", red on the old code | — |

   Then run `/mluk-repo:commit` for the same target yourself, through the
   Skill tool: it asks for its go-ahead, places the round in the review-fix
   commit (`git-safety`, "Amending") and hands the review over.

## Hard rules

- Only the chosen findings. A defect met on the way is a line in the report,
  not a silent extra fix.
- No commit, push or PR here, and the ledger is not edited: statuses change
  through the next review or the owner's word.
- Never weaken a test or a check to make a fix pass.
- A measure that costs more than the fix is asked about, with its price —
  never added by default.
