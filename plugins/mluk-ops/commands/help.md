---
description: What mluk-ops can do — srv, the PreToolUse guard and its three classes, the server-ops skill, and whether this machine has servers configured. Never connects to a server.
argument-hint: '[<language code>]'
---

# /mluk-ops:help

Introduce this plugin. **Read-only, and offline:** nothing here reaches a server.

Language: the conversation's, unless `$1` gives a code.

## Steps

1. **Name the parts.** `srv` (`${CLAUDE_PLUGIN_ROOT}/bin/srv`) — the one way to a server, every
   call written to the audit log; the guard from `${CLAUDE_PLUGIN_ROOT}/hooks/hooks.json` — a
   `PreToolUse` hook on Bash; the skills, read as `name` and `description` out of every
   `${CLAUDE_PLUGIN_ROOT}/skills/*/SKILL.md`. Use those paths verbatim — never search the
   filesystem for the plugin.

2. **State the three classes in a few lines:** a read passes; a reversible change asks the owner,
   with a preview; an irreversible command is denied and handed to the owner, who runs it with `!`.
   A plain `ssh`, `scp` or `rsync` to a configured host is denied — it goes through `srv`. Point at
   `${CLAUDE_PLUGIN_ROOT}/skills/server-ops/SKILL.md` for the protocol.

3. **Say what is present on this machine:** whether `~/.config/mluk-ops/servers.json` exists, and
   the configured server names with their notes from `"${CLAUDE_PLUGIN_ROOT}/bin/srv" --list`.
   Never print a host, a user or a key path. No servers → point at the setup in
   `${CLAUDE_PLUGIN_ROOT}/README.md`.

## Hard rules

- **Never search the filesystem for the plugin.** Its files are at `${CLAUDE_PLUGIN_ROOT}` — use
  that path verbatim.
- No SSH, no `srv` call other than `--list`.
- Read-only. Keep it short.
