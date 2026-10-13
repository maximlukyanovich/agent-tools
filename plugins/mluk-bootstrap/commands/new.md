---
description: Create a project in an empty folder — stack recipe, generator with every option explicit, pinned environment, git, first commit and remote on a go-ahead — before /mluk-bootstrap:setup.
argument-hint: '[<stack>]'
disable-model-invocation: true
---

# /mluk-bootstrap:new

Create the project itself in an empty folder, so that `/mluk-bootstrap:setup`
has a repository to inventory. Runs once, before `setup`, never after it.

**Writes files** in the current folder only. The commit, the remote and the
push each wait for their own yes.

## Steps

The order is fixed. Steps are not reordered or skipped.

1. **Check the folder** in one call: `ls -A`, and `git rev-parse --verify HEAD`
   when `.git/` exists. Only service entries are allowed — `.claude/`, `.git/`
   without commits, editor folders (`.idea/`, `.vscode/`, `.zed/`) and OS
   litter (`.DS_Store`). Anything else — a manifest, sources, a commit,
   `README.md`, `AGENTS.md`, `CLAUDE.md` — means the project exists: stop and
   end with `/mluk-bootstrap:setup` in a code block, or `/mluk-bootstrap:audit`
   when a harness is already there.

2. **Ask the stack** — `$1` when given, otherwise one question. Load the
   `mluk-repo:kickoff` skill first; its questionnaire rules apply here and in
   step 4. The options are the recipes in
   `${CLAUDE_PLUGIN_ROOT}/reference/scaffold/` — one file per stack, named
   after it — plus "another stack".

3. **Read the recipe** — `${CLAUDE_PLUGIN_ROOT}/reference/scaffold/<stack>.md`,
   that one file, its `Scaffold` section. No recipe for the stack → ask which
   generator and which parameters; never invent them.

4. **Ask the recipe's questions** in one round, each with the recommendation
   the recipe marks, plus the closing "anything to add?".

5. **Run the generator** into the current folder, with every option the recipe
   lists passed explicitly: a generator's "accept defaults" flag may take the
   saved preferences of its earlier runs instead. Its own git is off — the
   commit is step 8, not the generator's. A mode that empties a non-empty
   folder is never used: it deletes `.claude/`.

6. **Pin the environment** as the recipe says — runtime version, package
   manager, lockfile — and run its install check.

7. **Initialise git**: `git init -b main`, unless `.git/` exists. The branch
   chain is a `setup` question; `main` is only where it starts.

8. **The first commit — ask in this session, commit on a yes.** Before it:
   - add `.claude/settings.local.json` to `.gitignore` — the plugin was
     installed before git existed, and nothing ignores that file yet;
   - read `git config user.email`. Empty → ask on whose behalf the project is
     committed (the `mluk-repo:github-accounts` skill) and set `user.name` and
     `user.email` in this repository's config, never copied from a
     neighbouring repository;
   - stage explicit paths from `git status --porcelain`, never `git add -A`;
   - write the message in the default preset of Q6 in
     `${CLAUDE_PLUGIN_ROOT}/reference/questions.md`, without a scope or an
     issue — `:tada: chore: Scaffold the app with <generator> <version>`. Show
     it with the question "does this format suit you?" and a note that `setup`
     sets the project's commit rules and can reword this commit until it is
     pushed.

9. **The remote — ask, act on a yes.** Either:
   - the URL of an existing repository: `git ls-remote <url>` must list no refs
     — a repository created with a README rejects the first push — then
     `git remote add origin <url>`; or
   - a new repository through `gh repo create`, on its own yes: `gh auth status`
     first (the `mluk-repo:github-accounts` skill — never `gh auth switch`),
     then the flags read from `gh repo create --help`, passed explicitly —
     owner and name, visibility, no README, licence or `.gitignore` — and
     `origin` in the URL form that skill names for the account.

   The push is a separate yes: `git push -u origin main`. After it the first
   commit's message is final.

10. **End** with the next step, for a fresh session:

    ```
    /mluk-bootstrap:setup
    ```

## Hard rules

- **The current folder only.** Nothing is written, installed or initialised
  outside it.
- **No `AGENTS.md` or `CLAUDE.md` from this command.** They are `setup`'s job,
  and a generator refuses a folder that already holds them. What the generator
  writes stays as it wrote it.
- **No force.** No overwrite mode, no `--force`, no force push.
- **Commit, remote, repository creation, push** — each on its own yes in the
  current turn.
- **Never invent a generator option.** What the recipe does not list and the
  owner did not answer is asked.
