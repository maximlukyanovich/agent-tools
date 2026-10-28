# mluk-ops

Safe agent access to a project's servers. Enable it only in projects where the agent works on a
server; everywhere else it is not loaded, and with no servers configured it does nothing.

The protocol is the skill [`server-ops`](skills/server-ops/SKILL.md); this file covers setup only.

## Install

```bash
claude plugin install mluk-ops --marketplace maximlukyanovich/agent-tools --scope project
```

Other scopes and updating: [Quick start](../../README.md#quick-start).

## What is in it

| Part | Role |
| --- | --- |
| `bin/srv` | the one way in: runs a command over SSH with the agent's own key and logs it; refuses an irreversible command without `SRV_OWNER_APPROVED=1`, whoever calls it |
| `hooks/guard.py` | PreToolUse on Bash: reads pass, changes ask, irreversible commands are denied and handed to the owner; plain ssh/scp/rsync to a configured host is denied |
| `skills/server-ops` | the protocol: classes, preview, owner-run irreversible commands, backups and their cleanup |
| `commands/help` | `/mluk-ops:help` — the parts, the classes, and the servers configured on this machine; never connects |

The checks: `python3 hooks/test_guard.py` for the hook and `python3 lib/test_srv.py` for `srv`, against
a fake `ssh` (run after every edit). CI runs both on every push — `.github/workflows/hooks.yml`.

## Setup on a machine

1. **The agent's key.** Separate from the owner's:

   ```sh
   ssh-keygen -t ed25519 -f ~/.ssh/<project>_agent -N '' -C '<project>-agent'
   ```

   On the server, add it to the non-root user's `authorized_keys` with an expiry:

   ```
   expiry-time="20261101" ssh-ed25519 AAAA… <project>-agent
   ```

   Revoking access is deleting that line. What the agent can do on the server is what this user
   can: no `NOPASSWD` sudo where it can be avoided, and membership in the `docker` group grants
   root-level privileges.

2. **The server list**, `~/.config/mluk-ops/servers.json`. It is per machine: one server is reached
   from several repositories.

   ```json
   {
     "audit_log": "~/.local/state/mluk-ops/audit.log",
     "servers": {
       "myapp": {
         "host": "203.0.113.7",
         "user": "deploy",
         "key": "~/.ssh/myapp_agent",
         "aliases": ["api.example.com", "api-staging.example.com"],
         "note": "staging + production"
       }
     }
   }
   ```

   `aliases` are every name the host is reached by. The hook uses them to catch a plain `ssh`.

3. **Enable the plugin** in the project's `.claude/settings.json`:

   ```json
   "enabledPlugins": { "mluk-ops@mluk-agent-tools": true }
   ```

## Known limits

- **A deny in the user's settings still wins over the hook's allow.** The hook's allow only skips the
  prompt.
- **Commands the owner runs with `!` in the prompt bypass hooks.** That is how the owner runs an
  irreversible command — through `srv` with `SRV_OWNER_APPROVED=1` in front, or `srv` refuses it.
- **The consent check reads the session transcript,** which is written asynchronously. If the latest
  message is not there yet, the check fails closed.
- **Classification is by pattern, and the unknown counts as a change.** In a command the hook sees,
  a slip past a pattern is at worst a prompt: only an allowlisted read is allowed without asking. A
  call the hook never sees — inside a script, a pipe into `sh`, `python3 -c` — gets no prompt at all.
- **`srv` refuses an irreversible command without `SRV_OWNER_APPROVED=1`**, whoever calls it — a
  script, a pipe into `sh`, `python3 -c`: exit code 3, nothing sent, the refusal in the audit log. The
  hook never sees those calls, so the owner's-consent check does not run for them.
- **This protects against an agent's mistake, not against an agent that works around it.** An agent
  can set the marker itself or reach the server another way. The boundary is the rights of the
  agent's user on the server: no `NOPASSWD` sudo where it can be avoided; membership in the `docker`
  group grants root-level privileges.
