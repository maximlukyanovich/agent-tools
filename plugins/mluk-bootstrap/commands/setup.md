---
description: Set up a repository's agent harness — inventory, questions, plan, then create AGENTS.md, the project profile, settings, skills, hooks and docs. Library commands come from mluk-repo, not from here.
argument-hint: '[<language>]'
---

# /mluk-bootstrap:setup

Create the agent harness for this repository. Stack-agnostic.

**Writes files.** Nothing is created before the plan is approved, and nothing is
committed at all.

## Steps

The order is fixed. Steps are not reordered or skipped.

1. **Inventory the repository.** Everything visible from code, config and git
   history is **not** a question. What exists already: `AGENTS.md`, `.claude/`,
   other agents' config, a `project-profile.md`. The stack and its quality
   commands, from the manifest files. Branches, remotes, the account alias the
   remote uses (`git@github.com:` is the personal key, `git@github-work:` the
   work one — see the `github-accounts` skill in `mluk-repo`), commit style,
   git hooks. Documentation and local notes. Integrations: MCP examples,
   environment templates.

   Decide the mode from what you found: nothing or fragments → set up; a harness
   already there → say so and offer `/mluk-bootstrap:audit` instead.

2. **Ask what the code cannot answer.** One or two batches, never one question
   per turn, every question with a default marked as the recommendation. The
   questionnaire rules are in the `kickoff` skill of `mluk-repo`; the list is in
   `${CLAUDE_PLUGIN_ROOT}/reference/questions.md` — ten questions, and the
   most valuable is "what has already gone wrong here", because without it the
   hook set comes out speculative. Wait for the answers.

3. **Show the plan**: which files will be created, which changed, which left
   alone, and which library commands the project will use as they are. Wait
   for confirmation.

4. **Create.** Layout and the two traps that cost a rewrite:
   `${CLAUDE_PLUGIN_ROOT}/reference/layout.md`. Skeletons:
   `${CLAUDE_PLUGIN_ROOT}/reference/templates.md`. The profile:
   `${CLAUDE_PLUGIN_ROOT}/reference/project-profile.md`. Which layer each rule
   belongs on: the `layers` skill.

   Order: `AGENTS.md` first — everything else references it — then `CLAUDE.md`,
   the profile, `settings.json` (declare the `mluk-agent-tools` marketplace in
   `extraKnownMarketplaces` and enable `mluk-repo@mluk-agent-tools`, plus
   `mluk-design` where there is a design kit, `mluk-fe` in a web front,
   `mluk-deploy` where the project deploys, `mluk-ops` where the agent works on
   a server; `mluk-ru` is user-scoped and needs nothing here), skills, hooks,
   MCP, docs. Plugins are installed with `--scope project`.

   **Local commands are the exception, not the rule.** `commit`, `create-pr`,
   `promote`, `review`, `sync`, `start`, `task`, `update-docs` exist in
   `mluk-repo` and read the profile. Write a local `.claude/commands/<name>.md`
   only when the answer to a question showed that the *procedure* differs —
   and say in the plan which library command it overrides and why.

5. **Run the final check** from `${CLAUDE_PLUGIN_ROOT}/reference/checklist.md`
   and report what is green and what is not.

6. **Report**: created, changed, deliberately left out and why, still open.

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
- **Personal projects only.** A repository under the work tree gets the work
  library's bootstrap, not this one.
