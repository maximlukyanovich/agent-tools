---
description: What mluk-fe can do — the two skills, the three PostToolUse hooks, and what the project profile's Frontend section configures.
argument-hint: '[<language code>]'
---

# /mluk-fe:help

Introduce this plugin. **Read-only.**

Language: the conversation's, unless `$1` gives a code.

## Steps

1. **Name the skills from their frontmatter.** Read `name` and `description` out of every
   `${CLAUDE_PLUGIN_ROOT}/skills/*/SKILL.md` — `web-ui-conventions` (the rules every screen and
   control follows) and `component-discipline` (how a component stays small and exact). One line
   each. Use that path verbatim — never search the filesystem for the plugin.

2. **Name the hooks** from `${CLAUDE_PLUGIN_ROOT}/hooks/hooks.json`: `locale-parity` (catalog key
   sets match), `i18n-keys` (every static next-intl key a file reads exists), `metadata-title` (no
   hardcoded title in App Router metadata). All run after `Write` / `Edit`, stay silent outside
   their files, and exit 2 with `file:line` on a violation — advisory, the edit is not rolled back.

3. **Say what the profile configures** — the `## Frontend` section of
   `.claude/project-profile.md` (keys in `${CLAUDE_PLUGIN_ROOT}/reference/profile.md`): the
   catalog directory, the default locale, the source and app roots, hooks switched off — and
   whether this project's profile has it.

4. **Point at the neighbours:** porting a kit's look is `mluk-design:design-port`; commit, review
   and kickoff are `mluk-repo`.

## Hard rules

- **Never search the filesystem for the plugin.** Its files are at `${CLAUDE_PLUGIN_ROOT}` — use
  that path verbatim.
- Read-only. Keep it short.
