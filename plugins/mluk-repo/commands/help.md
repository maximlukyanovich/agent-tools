---
description: What mluk-repo can do — the workflow commands, their usual order, the profile sections they read, and the skills they lean on.
argument-hint: '[<language code>]'
---

# /mluk-repo:help

Introduce this plugin. **Read-only.**

Language: the conversation's, unless `$1` gives a code.

## Steps

1. **List the commands from their frontmatter.** Read `description` and
   `argument-hint` out of every file in `${CLAUDE_PLUGIN_ROOT}/commands/`. Use
   that path verbatim — never search the filesystem for the plugin. Mark the
   mutating ones: `commit`, `create-pr`, `promote`, `sync`; `update-docs`
   writes after confirmation; `review` writes only its gitignored ledger, code only with `fix`.

2. **Show the usual order:** `start` → `task` → work → `commit` → `review` →
   `sync` when the base moved → `create-pr` or `promote`; `update-docs` before
   a commit that changed behaviour.

3. **Say what the profile must contain** — `## Repository` for every command,
   `## Checks` for `start`, `## Task` for `task`, `## Review` for `review`,
   `## Docs` for `update-docs` — and point at
   `${CLAUDE_PLUGIN_ROOT}/reference/profile.md` for keys and defaults.

4. **Name the skills** — `commit-conventions`, `pr-conventions`,
   `github-accounts`, `git-safety`, `yandex-browser` — one line each.

5. **Say what is present here** — is there a profile, which sections it has,
   which local overrides exist in `.claude/commands/`. One line each.

## Hard rules

- **Never search the filesystem for the plugin.** Its files are at
  `${CLAUDE_PLUGIN_ROOT}` — use that path verbatim.
- Read-only. No file is written, no `gh` call changes anything.
- The command list comes from frontmatter, not from memory.
- Keep it short.
