---
name: server-ops
description: How an agent works on a remote server it has SSH access to — every command through `srv`, commands sorted into read / reversible change / irreversible, the preview an owner sees before a change, backups before risk and their cleanup after, and the rule that irreversible commands are handed to the owner, not run. Use before any command that touches a server listed in ~/.config/mluk-ops/servers.json.
---

# server-ops

The owner has lost data before by approving an agent's command too quickly. So the protection does
not depend on attention in the moment of the click:

- read-only commands pass silently, which makes every remaining prompt rare enough to be read;
- irreversible commands never reach a prompt at all — the owner runs them.

The hook in this plugin enforces the sorting; this skill is the protocol it enforces.

## 1. The only way in: `srv`

```sh
"${CLAUDE_PLUGIN_ROOT}/bin/srv" <server> '<remote command>'   # one quoted argument, logged
"${CLAUDE_PLUGIN_ROOT}/bin/srv" <server> --get <remote> <local>
"${CLAUDE_PLUGIN_ROOT}/bin/srv" <server> --put <local> <remote>
"${CLAUDE_PLUGIN_ROOT}/bin/srv" --list                        # configured servers
```

`srv` reads `~/.config/mluk-ops/servers.json` (see the plugin README): host, user, the agent's own
key, aliases. It appends every call to an audit log on the owner's machine: time, server, command,
exit code. The remote command is passed as **one quoted argument** and runs in the server's shell.

A plain `ssh`, `scp` or `rsync` to a configured host is denied by the hook. The agent's key is its
own, never the owner's, is installed for a non-root user, and carries an `expiry-time`.

## 2. Three classes of command

| Class | Examples | What happens |
| --- | --- | --- |
| **Read** | `ps`, `docker compose ps/logs`, `docker inspect`, `df -h`, `cat` of a non-secret file, `systemctl status`, `journalctl`, `git status/log`, `curl` of a health URL, `caddy validate` | runs without a prompt |
| **Reversible change** | a deploy script, `restart`, copying a config with a backup, `git pull --ff-only`, `systemctl reload`, a new file | a prompt with the preview below |
| **Irreversible** | deleting files or volumes, `down -v`, `prune --volumes`, `dropdb`, `DROP`/`TRUNCATE`, restore over live data, `ufw reset/disable`, editing sshd or sudoers, `userdel`, `git reset --hard`, overwriting a file without a copy | **the agent does not run it** — it hands the command to the owner |

When in doubt, a command belongs to the stricter class. Two changes are never chained in one call:
one call is one decision.

## 3. The preview before a change

Every reversible change is announced in the chat before the call, in this shape:

```
Сервер: <server> (<env>)
Команда: <exact command>
Что меняется: <one line>
Откат: <exact command or "не нужен">
```

## 4. Irreversible: the owner runs it

The agent prepares everything and stops:

```
⚠ НЕОБРАТИМО — запускаете вы
Сервер: <server> (<env>)
Команда: <exact command, copy-paste ready>
Что пропадёт: <what exactly, how much>
Бэкап: <where it is, how it was checked> — или «бэкапа нет, потому что …»
Проверка после: <command to confirm the result>
```

The owner runs it in their own terminal, or with `!` in the Claude Code prompt.

**The agent does not offer to run it itself.** If the owner, on their own initiative, writes plainly in
their latest message that the agent may execute that command, the agent prefixes it with
`SRV_OWNER_APPROVED=1`. The hook then checks that latest message for that permission, and still asks,
with the warning in the prompt. The marker is never added on the strength of an earlier message, a
«+» to something else, or a general «делай».

## 5. Backups: before the risk, cleaned up after

- **Before a risky step, a backup exists and has been checked.** Before touching the database:
  `pg_dump`, copied off the server with `srv --get`, and its size and `pg_restore --list` checked.
  Before a risky system change: a provider snapshot, which the owner takes.
- **The backup is named in the preview.** «Бэкап: /tmp/x.dump» without a check does not count.
- **Cleanup is part of the task, not a follow-up.** Once the change is verified to work, the agent
  lists the backups it created — on the server and locally — with their sizes, and proposes which to
  delete by the project's retention rule (default: keep the latest verified one per kind). Deleting
  a backup is itself irreversible, so it goes through §4.
- A session that ends with backups still lying around says so in its final message.

## 6. Order of work

1. **Read first.** Check the state before changing it. Batch several reads into one `srv` call.
2. **Announce, run one change, check its result**, then the next one. A failed check stops the
   sequence; the agent does not improvise a fix on a live server without saying what went wrong.
3. **Anything that can lock the owner out goes last and gets a second path.** This covers SSH
   configuration, the firewall, sudo and users. Before such a step, a second session is open or the
   provider console is at hand. After it, a new login is tested before the old session is closed.
4. **Secrets never reach the chat.** `.env` files are edited in place. A secret file is inspected
   only by its structure — key names and value lengths — never by printing lines through a "masking"
   pattern: a pattern that misses one renamed key prints the value. Tools that echo their own code
   (a browser automation `run_code`, a script runner) must not receive a secret inline either; read it
   inside a process whose output you control.

## 7. Access lifetime

The agent's key has an `expiry-time` in `authorized_keys`, 30 days unless the owner says otherwise.
When it expires the agent says so and asks the owner to renew it; it does not ask for the owner's
key. Revoking the key is deleting its line.
