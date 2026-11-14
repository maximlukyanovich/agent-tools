# Final check

Run it and show the result. Anything unchecked is reported, not quietly skipped.

- [ ] `AGENTS.md` exists, covers the seven sections, and does not contradict
      the code.
- [ ] `CLAUDE.md` imports it and duplicates not a single line of it.
- [ ] `.claude/project-profile.md` exists with every section an enabled plugin
      reads; no section copies what a command answers. A project with a
      testing skill names it in `## Task` as `testing skill`.
- [ ] The settings file Q11 chose declares in `extraKnownMarketplaces` every
      marketplace `enabledPlugins` names — `mluk-agent-tools` (GitHub source,
      `autoUpdate`, and `ref` when Q11 pinned a release),
      `claude-plugins-official` when its plugins are enabled —
      enables the Q11 set and sets empty attribution.
- [ ] `.claude/commands/<prefix>-start.md` (`start.md` with `none`) comes from `templates/start/` with the
      current version line, one variant left and every placeholder filled; it
      only installs and hands over. With Node, `scripts/agent-plugins.mjs` and
      its `lib/` are beside it and their test passes in the project's run.
      `## Checks` has the plugin row, `.claude/COMMANDS.md` its row,
      README the «Agent tooling» paragraph.
- [ ] `.claude/COMMANDS.md` carries the `Harness:` line with this plugin's
      `MAJOR.MINOR` and the date of this setup or audit.
- [ ] `.claude/COMMANDS.md` carries `Command prefix:`, and every local command
      is named `<prefix>-<verb>`; with `none`, no name is a built-in command
      or a bundled skill (`reference/layout.md` → Command names).
- [ ] `AGENTS.md` §6 has the line on a prompt offered to the developer, with a
      worktree prompt's entering, leaving and entering again.
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
      the full gate runs once per branch, or in CI by `full gate`
      (`mluk-repo`, `reference/commands.md`, "The gate"); `hub files` lists
      the files whose related tests are most of the suite.
- [ ] The gate is fast: one of several parts picks them by their content
      since the last green run, not by the branch's diff — a part whose
      content is unchanged is skipped, its fingerprint taken before and after
      its checks and recorded only when the two match, and `--all` runs
      everything. A part's content is everything its tool reads — its own
      globs, the files they import, the files they read from disk (tests read
      the stylesheets and the static assets). A path leaves a part only by a
      probe named in a comment beside the rule — a command
      (`tsc --listFilesOnly`) or a way to look (a search for imports and disk
      reads in the part's files) — never by the tool's `include` or ignore
      configuration; in doubt the path stays, since a missing path is a false
      green. The test runner runs in parallel only where the tests share
      no outside state — a Redis-backed config, a cache or a database the dev
      stack also uses — the linter keeps a cache when no rule needs type
      information, the type-check is incremental. CI runs without these
      caches.
- [ ] A heavy local run leaves the machine usable. Outside CI the test
      runner and the gate run below normal priority (`nice`,
      `os.setPriority`, inherited by the workers), and the worker count is
      the runner's default, a machine's own from an ignored local file; CI
      runs on defaults. Whether runs also queue is the developer's answer,
      not the agent's guess: asked whether runs go slow or red when sessions
      on one machine overlap, a yes adds a lock around the step that takes
      every core — the test runner over the whole suite, alone or inside
      the gate — `/tmp/heavy-run.lock` in every project, so the machine runs
      one at a time and a waiting run says so: a kernel lock that its
      process's exit drops (`flock`), never a marker file; without `flock`
      the run goes unqueued and says so. A run filtered to some files and
      the single-threaded parts — lint, type-check, format — take no lock:
      queued, they would leave cores idle. Holding the lock, the step does
      not start while something else keeps most of the cores busy: their
      share over a few seconds against the project's threshold, which a
      machine may override — not the load average, which lags a minute and
      still counts a run that just ended. The step then names the busiest
      processes and exits with a code of its own, not red's, unless a flag
      passed down from the gate says to run anyway. A no leaves the lock as
      advice to the developer, not a finding. Observed on one machine:
      three sessions' runs at once each took about as long as three single
      runs add up to, and all went red.
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
- [ ] GitHub's `delete_branch_on_merge` matches the profile's `delete branch`
      — on only with `platform` — and no branch of the chain but the last is
      exposed to it.
- [ ] `/mluk-repo:start` runs and prints a green table — or rows with concrete
      actions.

Then report: what was created, what was changed, what was left out and why, and
which questions are still open.
