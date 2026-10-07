---
description: What mluk-design can do — the design-port skill, when it applies, and where this project's profile names its design source.
argument-hint: '[<language code>]'
---

# /mluk-design:help

Introduce this plugin. **Read-only.**

Language: the conversation's, unless `$1` gives a code.

## Steps

1. **Name the skills from their frontmatter.** Read `name` and `description` out of every
   `${CLAUDE_PLUGIN_ROOT}/skills/*/SKILL.md`, one line each. Use that path verbatim — never search
   the filesystem for the plugin.

2. **State the method in a few lines:** the kit's source is read at write time, never recalled;
   its look is ported exactly while its demo code is not copied; a deviation is agreed for one spot
   and offered back to the kit; when the kit itself is wrong, the owner decides.

3. **Say what is present here** — the design source the profile names (`## Sources of truth`, and
   `design source` under `## Review` in `.claude/project-profile.md`), or that there is none, in
   which case the plugin should not be enabled in this project.

4. **Point at the neighbours:** screen-level rules and component discipline are `mluk-fe`; the
   review lens for design deviations is `mluk-repo:review`.

## Hard rules

- **Never search the filesystem for the plugin.** Its files are at `${CLAUDE_PLUGIN_ROOT}` — use
  that path verbatim.
- The skill list comes from frontmatter, not from memory.
- Read-only. Keep it short.
