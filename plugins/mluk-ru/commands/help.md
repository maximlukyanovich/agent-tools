---
description: What mluk-ru can do — the review command, the principles the skill carries, and what the project profile's Copy section adds.
argument-hint: '[<language code>]'
---

# /mluk-ru:help

Introduce this plugin. **Read-only.**

Language: the conversation's, unless `$1` gives a code.

## Steps

1. **List the commands from their frontmatter.** Read `description` and
   `argument-hint` out of every file in `${CLAUDE_PLUGIN_ROOT}/commands/`. Use
   that path verbatim — never search the filesystem for the plugin.

2. **State the method in a few lines**: a clear subject and direct word order,
   full nominalisation of actions, no tautology, status-neutral headings,
   business register without metaphors; for binding texts — fixed terms,
   numerals spelled out in brackets, the obliged party named, wording checked
   against the real mechanics and across the whole document set. Point at
   `${CLAUDE_PLUGIN_ROOT}/skills/business-russian/SKILL.md`.

3. **Say what the profile adds** — the `## Copy` section of
   `.claude/project-profile.md`: canonical documents, glossary, language
   pairs, the copy journal path — and whether this project's profile has it
   (check that file, not `AGENTS.md`).

4. **Say how the set grows**: every owner complaint about wording becomes an
   entry in the project's copy journal; a principle common to projects is
   moved into the skill by the library's owner.

## Hard rules

- **Never search the filesystem for the plugin.** Its files are at
  `${CLAUDE_PLUGIN_ROOT}` — use that path verbatim.
- Read-only. Keep it short.
