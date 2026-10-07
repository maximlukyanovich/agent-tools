---
description: What mluk-deploy can do — the deployment skills (VPS, Vercel, DNS), when each one applies, and which deployment files this project has.
argument-hint: '[<language code>]'
---

# /mluk-deploy:help

Introduce this plugin. **Read-only.**

Language: the conversation's, unless `$1` gives a code.

## Steps

1. **Name the skills from their frontmatter.** Read `name` and `description` out of every
   `${CLAUDE_PLUGIN_ROOT}/skills/*/SKILL.md`, one line each, with when it applies. Use that path
   verbatim — never search the filesystem for the plugin.

2. **Say what the plugin is not.** Knowledge only: no hooks, and no command besides this one. The
   concrete files — compose, scripts, Caddy sites, workflows, the runbook — live in the project;
   the skills carry the reasoning and the traps.

3. **Say what is present here**, one line each: a deployment runbook (the profile's `## Docs` map
   row for deployment, else `docs/deploy.md`), deploy workflows under `.github/workflows/`, a
   `vercel.json`, compose files for a server. Name the skill each one belongs to.

4. **Point at the neighbour:** work on the live server itself is `mluk-ops` — its `server-ops`
   skill and the `srv` guard.

## Hard rules

- **Never search the filesystem for the plugin.** Its files are at `${CLAUDE_PLUGIN_ROOT}` — use
  that path verbatim.
- The skill list comes from frontmatter, not from memory.
- Read-only. Keep it short.
