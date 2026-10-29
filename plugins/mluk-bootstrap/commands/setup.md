---
description: Set up a repository's agent harness — inventory, questions, plan, then create AGENTS.md, the project profile, settings, skills, hooks and docs. Library commands come from mluk-repo, not from here.
argument-hint: '[<language>]'
---

# /mluk-bootstrap:setup

Create the agent harness for this repository. Stack-agnostic.

**Writes files.** Nothing is created before the plan is approved. The one git
write is rewording an unpushed first commit, on a yes (step 6).

## Steps

The order is fixed. Steps are not reordered or skipped.

1. **Inventory the repository.** Everything visible from code, config and git
   history is **not** a question. What exists already: `AGENTS.md`, `.claude/`,
   other agents' config, a `project-profile.md`. The stack and its quality
   commands, from the manifest files. Branches, remotes, the account alias the
   remote uses (`git@github.com:` is the personal key, `git@github-work:` the
   work one — load the `mluk-repo:github-accounts` skill), commit style,
   git hooks. Documentation and local notes. Integrations: MCP examples,
   environment templates. A history of one scaffold commit, as
   `/mluk-bootstrap:new` writes it, shows the library's default, not the
   project's style: Q6 is still asked.

   Decide the mode from what you found:
   - no manifest and only service entries (the list is step 1 of
     `${CLAUDE_PLUGIN_ROOT}/commands/new.md`) → no project yet: end with
     `/mluk-bootstrap:new` in a code block and stop;
   - no harness, or fragments of one — an `AGENTS.md` or `CLAUDE.md` holding
     only a generator's block is a fragment → set up;
   - a harness already there → say so and offer `/mluk-bootstrap:audit`
     instead, as a code block.

   With a recipe for the stack at
   `${CLAUDE_PLUGIN_ROOT}/reference/scaffold/<stack>.md`, read its `For the
   harness` section — what the generator left that the harness must respect.

2. **Ask what the code cannot answer.** Two rounds, three with UI, never one
   question per turn, every question with a default marked as the
   recommendation. Load the `mluk-repo:kickoff` skill before the first
   question — its questionnaire rules apply; `mluk-repo` is installed with this
   plugin. The list and its split into rounds are in
   `${CLAUDE_PLUGIN_ROOT}/reference/questions.md` — eleven questions, and the
   most valuable is "what has already gone wrong here", because without it the
   hook set comes out speculative. Before Q5, read the facts its branch
   deletion question carries — the setting, the default and the protected
   branches — read only; that question alone has no recommendation. Wait for
   the answers.

3. **Show the plan**: which files will be created, which changed, which left
   alone, and which library commands the project will use as they are. Wait
   for confirmation.

4. **Create.** Layout and the two traps that cost a rewrite:
   `${CLAUDE_PLUGIN_ROOT}/reference/layout.md`. Skeletons:
   `${CLAUDE_PLUGIN_ROOT}/reference/templates.md`. The profile:
   `${CLAUDE_PLUGIN_ROOT}/reference/project-profile.md`. Which layer each rule
   belongs on: the `layers` skill.

   Order: `AGENTS.md` first — everything else references it — then `CLAUDE.md`,
   the profile, settings, skills, hooks, MCP, docs — `docs/local/README.md`
   and the efficiency journal among them. A file the generator wrote
   (`AGENTS.md`, `.gitignore`) is appended to, and its block stays where it is.
   When Q3 let the agent start the dev server or the stack, that answer goes
   to this clone's `.claude/project-profile.local.md` — `## Checks`,
   `agent starts` — gitignored, so no other clone inherits it; otherwise the
   key is left out, and the agent starts nothing.

   Settings go to the file Q11 chose: every marketplace the set comes from in
   `extraKnownMarketplaces` — `mluk-agent-tools` with `autoUpdate`, and
   `claude-plugins-official` when one of its plugins is enabled (an interactive
   first start adds it on its own, a profile used only from the CLI lacks it) —
   and empty `attribution`. When Q11 pinned a release, `mluk-agent-tools`'s
   `source` carries `"ref": "<tag>"` beside `repo`, `autoUpdate` kept: the
   latest tag, the name after `refs/tags/` in the first line of
   `git ls-remote --tags --refs --sort=-v:refname https://github.com/maximlukyanovich/agent-tools 'v*'`.
   Then each plugin of the Q11 set is installed with the command a person would
   run — `claude plugin install <plugin>@mluk-agent-tools --scope project`, or
   `--scope local` for `settings.local.json` — which writes `enabledPlugins`
   itself. The plugins load in the next session. The pin holds only on a
   machine whose user settings do not declare the marketplace: when
   `~/.claude/settings.json` has a `mluk-agent-tools` entry under
   `extraKnownMarketplaces`, the report says to delete it — the project's
   settings declare it now. A pinned project's installs came from the catalogue
   this machine already knows; the next session start here fetches it from the
   tag, and `autoUpdate` moves the installs there — or
   `claude plugin update <plugin>@mluk-agent-tools --scope <scope>` right after
   that start — the report says so.

   **The project's `/start`** installs those plugins in every other clone: a
   plugin that is not installed has no commands, so the library cannot do it.
   Copy `${CLAUDE_PLUGIN_ROOT}/templates/start/` with `cp`: `start.md` to
   `.claude/commands/`, and — when the project has Node — `agent-plugins.mjs`
   with its `lib/` to `scripts/`, its test joining the project's test run.
   The scripts are never read into context; the copied `start.md` is the one
   file read, to edit it: keep the `node` variant, or
   the `prose` one without Node; drop the other's blocks and the variant
   markers, renumber, fill the `<…>` placeholders, keep the version line.
   With it go a `## Checks` row — `agent plugins — <the report> — /start` —
   a `.claude/COMMANDS.md` row saying why it is local, and the README's
   «Agent tooling» (`${CLAUDE_PLUGIN_ROOT}/reference/templates.md`).

   **Local commands are the exception, not the rule.** Besides `/start`,
   which every project gets, `commit`, `create-pr`, `promote`, `review`,
   `fix`, `sync`, `start`, `next`, `task`, `update-docs`, `handoff` exist in
   `mluk-repo` and read the profile. Write a local
   `.claude/commands/<name>.md` only when the answer to a question showed that
   the *procedure* differs — and say in the plan which library command it
   overrides and why.

5. **Run the final check** from `${CLAUDE_PLUGIN_ROOT}/reference/checklist.md`
   and report what is green and what is not.

6. **Report**: created, changed, deliberately left out and why, still open.

   When Q6 chose a format the existing first commit does not follow, and that
   commit is the only one and not pushed (`git rev-list --count HEAD` is 1;
   after `git fetch`, `git branch -r --contains HEAD` is empty), offer to
   reword it on a yes: `git commit --amend --only -m "<message>"`.

   End with the project's commit command in a code block — `/mluk-repo:commit`
   or its local override — to run in this session, because the message needs
   its context. The commit closes the setup, so it runs `/mluk-repo:handoff`
   itself; the next step goes to a fresh session, where the plugins installed
   in step 4 load.

## Hard rules

- **Never invent a missing requirement.** No stack, branch scheme, validate
  command or documentation language — ask. A placeholder is tolerable only
  while a question is open and only if it is listed in the report.
- **Never carry another project's domain over.** Examples in skills are written
  for this project.
- **No empty placeholder directories and no stub READMEs.** A directory appears
  with its first real file.
- **Nothing is committed, pushed or opened as a PR.** Not without an explicit
  instruction on the current turn.
- **One fact, one place.** Before writing a rule, check it does not already live
  in another file — including the library's skills. If it does, link to it.
- **A missing layer is a decision, not an oversight** — recorded in `AGENTS.md`
  with its reason and the conditions that would add it later.
