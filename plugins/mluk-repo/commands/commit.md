---
description: Build a commit for the current changes — stage explicitly, run the profile's validate command, draft the message by the commit preset, commit. Never pushes.
argument-hint: '[topic or short hint]'
---

# /mluk-repo:commit

Produce a clean commit (or several) by the `commit-conventions` skill, with the
parameters from the profile's `## Repository`: `validate`, `targeted checks`,
`commit preset`, `commit confirm`.

**Writes to git.** Never pushes — that is `/mluk-repo:create-pr` or `:promote`.

The argument is an optional hint about the topic. Advice, not an order: if the
diff says otherwise, pick the topic from the diff and say so in one line.

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

3. **Decide between a new commit and an amend.** If the change belongs to the
   last commit and that commit is **unpushed** (it appears in `git log @{u}..`),
   propose `--amend`, say plainly that the commit is unpushed and the rewrite is
   safe, and let the owner choose. A pushed commit is never amended.

4. **Run the checks.** The profile's `validate` command — unless every changed
   path falls into a row of `targeted checks` (docs only, harness only, config
   only), in which case run what the row says and state what was not
   exercised. A migration-shipping repository: a model change without its
   migration in the diff is an incomplete commit — stop.

   A check failed → **stop**. Print the error verbatim, commit nothing, do not
   fix it quietly inside this command.

5. **Plan the commits.** One task, one commit. A diff that holds several tasks
   is split into groups; a debatable split is shown and confirmed. Behaviour
   described in the project's docs changed but the document did not → say so
   and offer `/mluk-repo:update-docs` first.

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
   body.

7. **Show and commit.** `commit confirm: ask` (default) → print the file
   groups, the check results and the message verbatim, and **wait for the
   go-ahead**. `commit confirm: auto` → print the same for visibility and
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
   one-line reminder that nothing was pushed. When the commits close a task or
   a round of review fixes, add the review to run next, in a fresh session:
   `/mluk-repo:review` (the ledger narrows it to the new commits). If step 4
   ran the **full** `validate` (not a targeted row) and the tree is now clean,
   record the tree it passed on: `git rev-parse HEAD^{tree} > "$(git rev-parse
   --git-dir)/validated-tree"`. `create-pr` then skips a second identical run.

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
