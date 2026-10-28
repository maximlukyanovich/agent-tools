#!/usr/bin/env python3
"""PreToolUse guard for Bash: sorts every command that reaches a configured server.

    read            → allow (no prompt), so the prompts that remain are rare enough to be read
    change          → ask, with the command in the prompt
    irreversible    → deny: the owner runs it (skill server-ops, §4) — unless the command carries
                      SRV_OWNER_APPROVED=1 AND the owner's latest typed message explicitly lets the
                      agent run it; then ask, with the warning in the prompt
    ssh/scp/rsync to a configured host outside srv → deny

Inert when ~/.config/mluk-ops/servers.json lists no servers, and for any Bash command that does not
touch one. When unsure, a command is classified as the stricter class — the rules are in
lib/ops_classify.py. Checks: hooks/test_guard.py.
"""
from __future__ import annotations

import json
import re
import shlex
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'lib'))
import ops_config  # noqa: E402
from ops_classify import APPROVAL_MARKER, CHANGE, READ, READ_COMMANDS, classify_call  # noqa: E402

CONSENT = re.compile(
    r'(выполни|выполняй|запусти|запускай|разрешаю|можешь\s+(сам\s+)?(это\s+)?(выполн|запуст)|'
    r'сам\s+(выполни|запусти)|go ahead and run|you may run|run it yourself)', re.IGNORECASE)


def srv_calls(command: str) -> list[list[str]] | None:
    """Argument lists of every srv call in the command, or None if a part of it is not srv.

    Local segments made of harmless filters (`| grep`, `| tail`) are allowed around srv; anything
    else next to it makes the whole command fall back to the normal permission flow.
    """
    lex = shlex.shlex(command, posix=True, punctuation_chars=';&|')
    lex.whitespace_split = True
    try:
        parts = list(lex)
    except ValueError:
        return None
    calls = []
    local_ok = True
    segments: list[list[str]] = [[]]
    for tok in parts:
        if tok in (';', '&&', '||', '|', '&', ';;', '|&'):
            segments.append([])
        else:
            segments[-1].append(tok)
    for seg in segments:
        seg = [t for t in seg if not re.match(r'^\w+=', t)] if seg else seg
        if not seg:
            continue
        if seg[0].rsplit('/', 1)[-1] == 'srv':
            calls.append(seg[1:])
        elif not (seg[0] in READ_COMMANDS and seg[0] not in ('cd',)):
            local_ok = False
    if not calls:
        return []
    return calls if local_ok else None


def latest_human_message(transcript_path: str | None) -> str:
    """Text of the owner's latest typed message. Empty when unknown — the check then fails closed."""
    if not transcript_path:
        return ''
    text = ''
    try:
        with open(transcript_path, encoding='utf-8') as fh:
            for line in fh:
                try:
                    row = json.loads(line)
                except ValueError:
                    continue
                if row.get('type') != 'user' or row.get('isMeta'):
                    continue
                origin = row.get('origin') or {}
                content = (row.get('message') or {}).get('content')
                if isinstance(content, list):
                    if any(b.get('type') == 'tool_result' for b in content if isinstance(b, dict)):
                        continue
                    body = ' '.join(b.get('text', '') for b in content if isinstance(b, dict))
                else:
                    body = content or ''
                if origin.get('kind', 'human') == 'human' and body.strip():
                    text = body
    except OSError:
        return ''
    return text


def decide(command: str, config: dict, transcript_path: str | None) -> tuple[str, str] | None:
    """(permissionDecision, reason), or None to leave the command to the normal permission flow."""
    servers = config['servers']
    if not servers:
        return None
    markers = ops_config.host_markers(config)
    calls = srv_calls(command)

    if not calls:
        uses_transport = re.search(r'(^|[\s;&|(])(ssh|scp|sftp|rsync|sshfs)(?=\s|$)', command)
        if uses_transport and any(m in command for m in markers):
            return 'deny', ('Прямой ssh/scp/rsync на сервер проекта запрещён: используйте srv '
                            '(навык server-ops) — он пишет журнал и проходит проверку.')
        if calls is None and re.search(r'(^|/)srv\s', command):
            return 'ask', 'Команда srv вместе с другими командами — проверьте её целиком.'
        return None

    worst, why, shown = READ, '', []
    for args in calls:
        if not args or args[0] in ('--list', '-h', '--help'):
            continue
        name, rest = args[0], args[1:]
        if name not in servers:
            return 'deny', f'srv: сервер {name!r} не настроен ({ops_config.CONFIG_PATH}).'
        cls, reason = classify_call(rest)
        shown.append(f'{name}: {" ".join(rest)}')
        if cls > worst or not why:
            worst, why = cls, reason

    detail = '\n'.join(shown)
    if worst == READ:
        return 'allow', f'Только чтение: {detail}'
    if worst == CHANGE:
        return 'ask', f'Изменение на сервере ({why}):\n{detail}\nСверьте с превью в чате: что меняется и как откатить.'
    approved = APPROVAL_MARKER in command and CONSENT.search(latest_human_message(transcript_path))
    if approved:
        return 'ask', (f'⚠ НЕОБРАТИМО — {why}. Владелец разрешил выполнение агенту в последнем сообщении.\n'
                       f'{detail}\nПроверьте команду и бэкап, прежде чем подтверждать.')
    return 'deny', (f'⚠ НЕОБРАТИМО — {why}. Агент такие команды не выполняет: передайте её владельцу '
                    f'в формате server-ops §4 (команда, что пропадёт, бэкап, проверка после).\n{detail}')


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except ValueError:
        return 0
    if event.get('tool_name') != 'Bash':
        return 0
    command = (event.get('tool_input') or {}).get('command', '')
    result = decide(command, ops_config.load(), event.get('transcript_path'))
    if result is None:
        return 0
    decision, reason = result
    print(json.dumps({'hookSpecificOutput': {
        'hookEventName': 'PreToolUse',
        'permissionDecision': decision,
        'permissionDecisionReason': reason,
    }}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
