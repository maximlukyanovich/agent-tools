---
description: The next session's prompt at a phase boundary — after a task's commit, a review or a merge — as copyable blocks built from git and the review ledger; for a small change, the next step here. Read-only.
argument-hint: '[<worktree | branch>]'
---

# /mluk-repo:handoff

Every phase of a task — the work, its review, the fixes, the merge — runs in
its own fresh session, a small change's phases aside: a fresh session is cheaper than a long one and does not
confirm its own reasons. It needs a prompt that points at the plan, the ledger
and the branch instead of retelling them. This command prints that prompt.

**Read-only**, apart from a local note when a block runs long.

`commit` (after every commit), `review`,
`create-pr` and `promote` run it themselves at their end, through the Skill
tool, without asking; the owner may call it at any time. Called before a
commit, it prints the commit command — the nearest step — not a review.

## Arguments

A folder or a local branch — the work to hand off, by
`${CLAUDE_PLUGIN_ROOT}/reference/commands.md`. None → the session's tree.

## Steps

1. **Read the state** in one Bash call where possible: the branch and its
   head, `git status --porcelain`, `git fetch origin <base> --quiet`, whether
   the head is in `origin/<base>` (`git merge-base --is-ancestor`), the
   branch's commits (`git log --oneline origin/<base>..<branch>`). A branch
   the caller has just merged and deleted counts as merged. From the profile:
   `base branch`, `ledger`.

   **The change's level** — from the first line of `/mluk-repo:task`'s
   answer in this session, else from the plan; found nowhere — a new
   session, a compacted context — the change is normal. With commits on the
   branch, measure them:
   `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/change_size.py" <branch> --base <base>`
   (`${CLAUDE_PLUGIN_ROOT}/reference/change-size.md`). A small change whose
   measure reads `normal` becomes normal, said in one line with the
   script's reason — unless the overage is the wiring of a new isolated
   page or module (`new` in the line, `changed` beside it when there is
   wiring, by `/mluk-repo:task`'s level), which the line names instead; the
   measure never lowers a level.

2. **Read the ledger** for the branch, named as `review` names it — only
   `Trajectory`, `Open` and the last pass's head and verdict.

3. **Find the plan** — the plan file this session worked from; else the newest
   file in the plans directory (`plansDirectory` in the settings, default
   `~/.claude/plans/`) that names the branch; else leave the plan out rather
   than guess.

4. **Pick the boundary** — the first row that matches:

   | State | Blocks |
   | --- | --- |
   | Uncommitted changes | `/mluk-repo:commit <branch>` — it commits on its own go-ahead and hands off after |
   | Merged into the base | `/mluk-repo:next`. Findings are not listed: by now each has its place. Below the block, as plain text, only a gap, with the ledger path — an id still `open`, or a techdebt place whose row the file lacks |
   | Commits after the ledger's last head, or no ledger, that name no id of `Open` in their bodies, and the plan of step 3 still holds work the branch has not done | the continue prompt below for a fresh session, or `/compact <focus>` here — by the criterion below; the review waits for the task's last commit |
   | Commits after the ledger's last head, or no ledger | `/mluk-repo:review <branch> <from>..<head>` — `<from>` and `<head>` from `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/review_target.py" --ledger <ledger file> --tree <tree>`: the two shas of `delta` or `rewritten`, the merge-base with `origin/<base>` for `whole`; `none` is the next row. When `Open` holds a `blocker`, `major` or `fix-now` that no commit after the head names in its body (a fix round names the ids it closes), `/mluk-repo:fix <branch>` instead: the review waits for its commit, then reads the fixes and the new commits in one pass |
   | A pass on the head, `blocked` or `changes requested` | `/mluk-repo:fix <branch>` |
   | A pass on the head, `ready to merge`, no `fix-now` open, every techdebt row written | `/mluk-repo:promote <branch>` |
   | `ready to merge` with `fix-now` ids open, or techdebt rows to write | `/mluk-repo:fix <branch> <ids>` — its commit hands over the review of the round's delta, and that review the promote. `/mluk-repo:promote <branch>` first only on the owner's word to ship now |

   A review in the middle of a task closes the range it read, not the task.
   Before a `ready to merge` row offers promote, read the plan of step 3
   against the branch's commits: when the plan still holds work the branch
   has not done, the continue prompt takes the promote block's place, and
   promote waits for the task's end. A review after the plan's last step, or
   with no plan found, offers promote as the table says.

   The continue prompt — `<next step>` is the plan's first step the branch
   has not done, named as the plan names it:

   ```
   Continue the plan <plan path> from <next step>. Target — <branch>.
   ```

   A branch living in a worktree opens this prompt by entering the tree,
   names `EnterWorktree` and says to leave before writing to the main tree,
   then enter again, by `${CLAUDE_PLUGIN_ROOT}/reference/commands.md`, "A block
   for work in a worktree".

   **A fresh session or `/compact` for the next slice.** A fresh session
   when the plan and the task's notes hold all the next slice needs; heavy
   context — screenshots, long logs — counts for it too, since every tool
   call re-reads it. `/compact <focus>` only while the slice's decisions
   live in the conversation alone — and better: write them into the plan,
   then go fresh. The recommended block comes first.

5. **Print** each block as its own code block, with one line above it saying
   it goes to a fresh session — the words in bold, in any case and the chat's
   language: **a fresh session**, в **свежей сессии** — or, for the commit and
   for every block of a change step 1 left small, that it runs here.
   Alternatives are separate blocks, so each copies alone. The text and the
   first block name the same step, the nearest one: while a commit or another
   step of the task is ahead, the block is for it, and a review command
   follows only the task's last commit, with its head known.

## Hard rules

- **A review freezes its range.** New commits on a branch whose ledger holds
  an open `blocker`, `major` or `fix-now` do not get a review of their own:
  the next block is the fix, and the next review reads the fix and the new
  commits in one pass.
- One phase, one fresh session. A review never runs in the session that wrote
  the code, a merge never in the session that reviewed it — except for a
  change step 1 left small, whose review and merge run where it was made.
  A critical change's review is always fresh.
- `/compact` only for the next slice of an unfinished plan, by the criterion
  of step 4. At a boundary the fresh session is the cheaper option.
- Links, not retelling: paths, ids, shas. The next session reads the plan and
  the ledger itself.
- A fresh session starts in the main tree, so a command's block names the
  branch, not a worktree folder; a prompt that works in the tree enters it.
- A block longer than ~8 lines goes to `docs/local/handoff-<branch-slug>.md` —
  only when `git check-ignore` confirms that path is ignored, otherwise it is
  printed whole — and the block tells the session to read it by its absolute
  path, keeping a prompt's words on the tree. An entered session leaves to
  write this note.
- Prompt text in the chat's language; commands, paths and ids verbatim.
