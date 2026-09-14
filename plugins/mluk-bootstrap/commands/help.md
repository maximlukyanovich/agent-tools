---
description: What mluk-bootstrap can do — commands, the layer model it applies, what it creates, and the kickoff method it carries.
argument-hint: '[<language code>]'
---

# /mluk-bootstrap:help

Introduce this plugin. **Read-only.**

Language: the conversation's, unless `$1` gives a code.

## Steps

1. **List the commands from their frontmatter.** Read `description` and
   `argument-hint` out of every file in `${CLAUDE_PLUGIN_ROOT}/commands/`. Use
   that path verbatim — never search the filesystem for the plugin.

2. **Show the order:** `/mluk-bootstrap:setup` on a repository without a
   harness, `/mluk-bootstrap:audit` on one that has it. The library commands
   (`/mluk-repo:*`) are enabled by `setup` and driven by the profile.

3. **State the layer model in a few lines** — deterministic checks, hooks,
   documents, skills, commands; the cheapest layer that can catch the rule — and
   point at `${CLAUDE_PLUGIN_ROOT}/skills/layers/SKILL.md` for the rest.

4. **State the kickoff method in a few lines** — plan mode, exploration,
   questions with a marked recommendation, a decisions table, slices, approval
   before code — and point at `${CLAUDE_PLUGIN_ROOT}/skills/kickoff/SKILL.md`.

5. **Say what `/mluk-bootstrap:setup` creates**: `AGENTS.md`, `CLAUDE.md`, the
   project profile, `settings.json` with the library plugins, skills, hooks,
   docs skeleton — and what it deliberately does not create (the library
   commands).

6. **Say what is present here** — is there an `AGENTS.md`, a `.claude/`, a
   profile, are the library plugins enabled. One line each.

## Hard rules

- **Never search the filesystem for the plugin.** Its files are at
  `${CLAUDE_PLUGIN_ROOT}` — use that path verbatim.
- Read-only. No file is written, no API call changes anything.
- The command list comes from frontmatter, not from memory.
- Keep it short: this is an introduction, not the manual.
