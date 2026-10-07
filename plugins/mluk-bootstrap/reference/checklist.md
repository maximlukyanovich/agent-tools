# Final check

Run it and show the result. Anything unchecked is reported, not quietly skipped.

- [ ] `AGENTS.md` exists, covers the seven sections, and does not contradict
      the code.
- [ ] `CLAUDE.md` imports it and duplicates not a single line of it.
- [ ] `.claude/project-profile.md` exists with every section an enabled plugin
      reads; no section copies what a command answers.
- [ ] `.claude/settings.json` declares `mluk-agent-tools` in
      `extraKnownMarketplaces` (GitHub source), enables
      `mluk-repo@mluk-agent-tools` (and `mluk-design` / `mluk-fe` /
      `mluk-deploy` / `mluk-ops` where they apply) and sets empty attribution.
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
      validate command that runs them — the same one the profile names.
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
      `../path`; no remote name standing for a repository; a fork's trunk and
      local paths only in the gitignored `project-profile.local.md`.
- [ ] Every collaborator of the project can read the marketplace repository.
- [ ] `/mluk-repo:start` runs and prints a green table — or rows with concrete
      actions.

Then report: what was created, what was changed, what was left out and why, and
which questions are still open.
