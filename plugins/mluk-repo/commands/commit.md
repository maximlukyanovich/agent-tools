---
description: Build a commit for the current changes — stage explicitly, run the checks of the changed paths, draft the message by the commit preset, commit. Never pushes.
argument-hint: '[<worktree | branch>] [topic or short hint]'
---

# /mluk-repo:commit

Produce a clean commit (or several) by the `commit-conventions` skill, with the
parameters from the profile's `## Repository`: `validate`, `targeted checks`,
`commit preset`, `commit confirm`.

**Writes to git.** Never pushes — that is `/mluk-repo:create-pr` or `:promote`.

A leading folder or local branch commits the work in that worktree, by
`${CLAUDE_PLUGIN_ROOT}/reference/commands.md`; every step below runs in its
tree. The rest is an optional hint about the topic. Advice, not an order: if
the diff says otherwise, pick the topic from the diff and say so in one line.

## Steps

1. **Read the profile.** No `## Repository` → ask for the validate command and
   the preset, offer to write them into the profile, then continue.

2. **Survey the working tree**, in parallel:

   ```bash
   git status -sb
   git diff --stat
   git diff --cached --stat
   git log --oneline -10
   git log @{u}.. --oneline 2>/dev/null || true
   ```

   A clean tree → say so in one line and finish. Flag secret-looking paths
   immediately (`git-safety` skill). Read `git diff` by affected area for
   substance — not whole files.

3. **Place a fix by the `git-safety` skill's "Amending" section**, which the
   profile's `amend unpushed` switches. Say in one line which commit took it.
   A pushed commit is never rewritten; the fix is a new commit.

4. **Run the checks** by `${CLAUDE_PLUGIN_ROOT}/reference/commands.md`,
   "The gate": the `targeted checks` rows of the changed paths, and the full
   `validate` only for a path no row covers or a profile without the table.
   The full gate of the range runs in the review and before the push, not
   here. The session already ran the same checks green after its last edit
   and the commit takes the whole diff → name that run and do not repeat it.
   A migration-shipping repository: a model change without its migration in
   the diff is an incomplete commit — stop.

   A check failed → **stop**. Print the error verbatim, commit nothing, do not
   fix it quietly inside this command.

5. **Plan the commits.** One task, one commit. A diff that holds several tasks
   is split into groups; a debatable split is shown and confirmed. Behaviour
   described in the project's docs changed but the document did not → say so
   and offer `/mluk-repo:update-docs` first, as a code block.

   **A changed fact is searched for before the commit.** When the diff changes
   something the repository states in words — a level, a command, a default,
   a port, a file's role — grep the old wording across the committed documents,
   the harness, code comments and env examples. Every copy is fixed in the same
   commit, or named to the owner as left on purpose (the `kickoff` rule on
   changed statements, applied at the moment it can still be caught).

   **A file that belongs to two groups** (a catalog, a changelog, a config with
   hunks from both tasks) is not a reason to merge the groups or to stash. Stage
   the earlier group's version of that file from a snapshot without touching the
   working tree:

   ```bash
   # write the earlier-task version of the file to a scratch path, then
   sha=$(git hash-object -w <scratch-path>)
   git update-index --add --cacheinfo 100644,$sha,<repo-path>
   ```

   Commit; the working tree still holds the full file, and the remaining hunks
   go into the next commit as usual. The scratch version must pass the same
   formatter as the tree (run it with the project's config), and the snapshot
   is deleted afterwards. `git add -p` is the interactive alternative and is not
   available to an agent.

6. **Draft the message** by the preset in `commit-conventions`. Always with a
   body. A round of review fixes names the ids it closes in one body line
   (`Review pass 2: R3, R7`; a later round amending the fix commit adds its
   own) — `handoff` reads it to tell a fixed range from new work.

7. **Show and commit.** `commit confirm: ask` (default) → print the file
   groups, the check results, the transition rows and their proof when the
   commit changes state (`kickoff`), and the message verbatim, and **wait for
   the go-ahead**. `commit confirm: auto` → print the same for visibility and
   proceed; stop only for the reasons below.

   ```bash
   git add <explicit paths>
   git commit -m "$(cat <<'EOF'
   <message>
   EOF
   )"
   ```

   More groups → repeat for the next one.

8. **Wrap up**: `git log --oneline -<N>` with the new commits on top, and a
   one-line reminder that nothing was pushed. If the **full** `validate` (not a
   targeted row) passed — in step 4 or the run it relied on — and the tree is
   now clean, record the tree by "The gate", so `review`, `create-pr` and
   `promote` skip a second identical run. When the commits close a task or a
   round of review fixes, run `/mluk-repo:handoff` for the same worktree or
   branch yourself, through the Skill tool, without asking — it prints the
   review to run next, in a fresh session, or here for a small change.

## When to stop and ask

- A check failed, or a model change has no migration.
- The diff contains unplanned changes: files outside the task, stray
  reformatting, build artefacts, an unexplained dependency edit.
- A path looks like a secret.
- The project's `## Task` names a blast-radius operation and the diff touches
  it without the effect being stated.

## Hard rules

- `git add` with an explicit path list only.
- Never `--no-verify`, never amend a pushed commit, never push.
- No agent attribution, English message, body always present.
- Do not edit sources just to make a check pass — a real failure is a
  separate, visible step.
