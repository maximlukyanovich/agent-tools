---
description: First command in a fresh clone or session — install the Claude Code plugins this repository declares when they are missing, then hand over to /mluk-repo:start.
argument-hint: '[language]'
---

<!-- mluk-bootstrap start template v1 — copied by /mluk-bootstrap:setup; /mluk-bootstrap:audit compares the version -->

# /start

The workflow commands come from plugins declared in `.claude/settings.json`, and a plugin that is not installed has no commands — `/mluk-repo:start` cannot install itself. Trusting the folder registers the declared marketplaces but downloads no plugin. This command does that one step and hands over; the overview and the environment checks stay in the library and are never copied here.

<!-- variant: node -->
1. **Report.** Run `node scripts/agent-plugins.mjs` — read-only; it compares `enabledPlugins` with what Claude Code has installed for this checkout (an install made in the main checkout or any of its worktrees counts in all of them, as Claude Code reads it) and exits 1 when a plugin is missing.
<!-- /variant -->
<!-- variant: prose -->
1. **Report.** Read the plugins `enabledPlugins` in `.claude/settings.json` sets to `true`, and what is installed — one `claude plugin list --json`, cut to `id`, `scope`, `enabled`, `projectPath` with `jq` or `python3` before it is read. An install counts here when its scope is `user` or `managed`, when its `projectPath` is this folder, or when that path is a checkout of this repository — `git -C <path> rev-parse --path-format=absolute --git-common-dir` answers as it does here. A declared plugin with no install that counts is missing; one whose installs all have `enabled: false` is turned off here. For each missing plugin's marketplace, `claude plugin marketplace list --json` says whether this machine knows it.
<!-- /variant -->
2. **Nothing missing** → run `/mluk-repo:start $ARGUMENTS` and stop here. A plugin turned off here is a personal switch — leave it; if it is `mluk-repo` itself, say so and stop.
3. **Something missing** → show the list and ask whether to install. A plugin from a marketplace this machine does not know is not installed: one the settings declare is registered by starting Claude Code at the repository root and trusting the folder; one they do not declare goes under `extraKnownMarketplaces` first. Neither needs `claude plugin marketplace add`, and at two scopes it does harm: `--scope local` replaces the committed entry and drops its `autoUpdate`, `--scope project` rewrites the committed `settings.json`.
   <!-- variant: node -->
   - Yes → run `node scripts/agent-plugins.mjs --install`, show its output, then give the developer `/reload-plugins` and `/start` to run, in that order, each as a code block.
   <!-- /variant -->
   <!-- variant: prose -->
   - Yes → `claude plugin install <id> --scope local` for each — local, because the settings already turn the plugins on and a project-scope install rewrites the committed `settings.json`. Show the output, then give the developer `/reload-plugins` and `/start` to run, in that order, each as a code block.
   <!-- /variant -->
   - No → point to `README.md` («<getting started section>», «Agent tooling») and `AGENTS.md`, and stop.
<!-- variant: node -->
4. **No `node` on PATH** (`node: command not found`) → <what in this repository needs Node, and which version>. Point to `README.md` «<getting started section>» and stop.
<!-- /variant -->
5. **The report fails otherwise**, or Claude Code is not on PATH → show the output as it is; never install around it by hand.

Updates need no command: the marketplace is declared with `autoUpdate`, so Claude Code refreshes it and the installed plugins up to ten minutes after an interactive session's first message; an open session applies them after `/reload-plugins`.
