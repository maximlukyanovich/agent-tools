# Final check

Run it and show the result. Anything unchecked is reported, not quietly skipped.

- [ ] `AGENTS.md` exists, covers the seven sections, and does not contradict
      the code.
- [ ] `CLAUDE.md` imports it and duplicates not a single line of it.
- [ ] `.claude/project-profile.md` exists with every section an enabled plugin
      reads; no section copies what a command answers.
- [ ] The settings file Q11 chose declares in `extraKnownMarketplaces` every
      marketplace `enabledPlugins` names — `mluk-agent-tools` (GitHub source,
      `autoUpdate`), `claude-plugins-official` when its plugins are enabled —
      enables the Q11 set and sets empty attribution.
- [ ] `.claude/commands/start.md` comes from `templates/start/` with the
      current version line, one variant left and every placeholder filled; it
      only installs and hands over. With Node, `scripts/agent-plugins.mjs` and
      its `lib/` are beside it and their test passes in the project's run.
      `## Checks` has the plugin row, `.claude/COMMANDS.md` the `/start` row,
      README the «Agent tooling» paragraph.
- [ ] `AGENTS.md` §2 says how the project runs as commands from the
      repository root — install, dev server, the stack — and not who runs them.
- [ ] Skills: real directories under `.claude/skills/`, working symlinks in
      `.agents/skills/`, each with a precise `description`, none restating a
      library skill.
- [ ] Local commands: only overrides whose procedure differs from the library,
      each naming what it overrides and why; the index is in
      `.claude/COMMANDS.md` and does not copy the library's commands;
      nothing inside `commands/` is not a command.
- [ ] Hooks: each silent outside its area, each with a test, all wired into
      `settings.json`.
- [ ] Deterministic layer: linter, formatter, types, tests, git hooks, and one
      validate command that runs them — the same one the profile names. The
      profile's `targeted checks` give each code path a row whose command
      really narrows — the linter on the changed files, the type-check, the
      tests related to them — tried once, so edits and commits run those and
      the full gate runs once per tree (`mluk-repo`, `reference/commands.md`,
      "The gate").
- [ ] The gate is fast: one of several parts picks them by their content
      since the last green run, not by the branch's diff — a part whose
      content is unchanged is skipped, its fingerprint taken before and after
      its checks and recorded only when the two match, and `--all` runs
      everything; the test runner runs in parallel only where the tests share
      no outside state — a Redis-backed config, a cache or a database the dev
      stack also uses — the linter keeps a cache when no rule needs type
      information, the type-check is incremental. CI runs without these
      caches.
- [ ] Git hooks stay fast: no hook runs the whole validate command — minutes
      per push get bypassed. `commit` and `create-pr` run it instead. lint-staged
      runs the linter's fixes first and the formatter last, or the linter's
      edits land unformatted while the hook reports success.
- [ ] A fresh clone installs: with pnpm 11, `allowBuilds` lists every
      dependency build script with its reason, `AGENTS.md` §2 says a new one
      needs an entry, and `pnpm install --frozen-lockfile` passes.
- [ ] MCP: the example in git, the generated file and `.env` ignored,
      generation works.
- [ ] `docs/README.md` and `docs/local/README.md` exist; `docs/local/` is fully
      ignored except its README.
- [ ] No harness file contains a secret, an absolute path, or a person's name.
- [ ] Committed text holds in every clone: sibling repositories by slug, not
      `../path`; no remote name standing for a repository; a fork's trunk,
      local paths and who starts the dev server or the stack
      (`agent starts`) only in the gitignored `project-profile.local.md`.
- [ ] Every collaborator of the project can read the marketplace repository.
- [ ] `/mluk-repo:start` runs and prints a green table — or rows with concrete
      actions.

Then report: what was created, what was changed, what was left out and why, and
which questions are still open.
