#!/usr/bin/env python3
"""PreToolUse guard for Bash: sorts every command that reaches a configured server.

    read            → allow (no prompt), so the prompts that remain are rare enough to be read
    change          → ask, with the command in the prompt
    irreversible    → deny: the owner runs it (skill server-ops, §4) — unless the command carries
                      SRV_OWNER_APPROVED=1 AND the owner's latest typed message explicitly lets the
                      agent run it; then ask, with the warning in the prompt
    ssh/scp/rsync to a configured host outside srv → deny

Inert when ~/.config/mluk-ops/servers.json lists no servers, and for any Bash command that does not
touch one. When unsure, a command is classified as the stricter class. Checks: hooks/test_guard.py.
"""
from __future__ import annotations

import json
import re
import shlex
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'lib'))
import ops_config  # noqa: E402

READ, CHANGE, IRREVERSIBLE = 0, 1, 2
APPROVAL_MARKER = 'SRV_OWNER_APPROVED=1'

# Destructive whatever the context. (pattern, what is lost)
IRREVERSIBLE_PATTERNS = [
    (r'(^|[\s;&|(])(sudo\s+)?rm\s', 'удаление файлов'),
    (r'\b(shred|wipefs|mkfs(\.\w+)?|fdisk|sfdisk|parted)\b', 'операции с диском'),
    (r'\bdd\b[^|;&]*\bof=', 'запись поверх устройства или файла'),
    (r'\btruncate\b', 'обрезка файла или таблицы'),
    (r'\bfind\b[^|;&]*(-delete|-exec(dir)?\s+rm)', 'удаление найденных файлов'),
    (r'\bdocker\s+(volume\s+(rm|prune)|system\s+prune|container\s+prune|rm\s+(-\w*\s+)*-\w*v)',
     'тома или данные Docker'),
    (r'\bdocker[\s-]compose\b[^|;&]*\bdown\b[^|;&]*(\s--volumes\b|\s-\w*v\w*\b)', 'тома стека (down -v)'),
    (r'\b(dropdb|dropuser)\b', 'база данных'),
    (r'(?i)\b(drop\s+(table|database|schema|role|user|extension)|truncate\s+table|delete\s+from)\b',
     'данные в базе (SQL)'),
    (r'\bpg_restore\b[^|;&]*(\s--clean\b|\s-\w*c\w*\b)', 'восстановление поверх живых данных'),
    (r'(?i)\b(flushall|flushdb)\b', 'данные Redis'),
    (r'manage\.py\s+(flush|reset_db|sqlflush)\b|manage\.py\s+migrate\s+\S+\s+(zero|\d{4})\b',
     'данные или схема Django'),
    (r'\bufw\s+(reset|disable|delete|deny|reject)\b', 'правила firewall'),
    (r'\b(userdel|deluser|groupdel|chpasswd)\b|\bpasswd\b|\busermod\s+[^|;&]*-L\b', 'пользователи и пароли'),
    (r'\biptables\s+-(F|X|P)\b', 'правила iptables'),
    (r'\bsystemctl\s+(disable|mask|stop)\s+(ssh|sshd)\b', 'доступ по SSH'),
    (r'\b(reboot|shutdown|poweroff|halt)\b', 'перезагрузка или выключение сервера'),
    (r'\bgit\s+(reset\s+--hard|clean\s+-\w*f|checkout\s+--\s|restore\s|stash\s+(drop|clear)|branch\s+-D)',
     'незакоммиченные изменения в git'),
    (r'\bgit\s+push\b[^|;&]*(\s--force\b|\s-f\b)', 'история в удалённом git'),
    (r'\bsed\s+(-\w*\s+)*-i(\s|$)', 'правка файла без резервной копии (sed -i без суффикса)'),
    (r'(?<![>&0-9])>(?!>)\s*(?!/dev/null|&|/tmp/)[^\s>]', 'перезапись файла (>)'),
]

# Paths whose change can lock the owner out. A read of them is fine; anything else is irreversible.
ACCESS_PATHS = r'(sshd_config|authorized_keys|/etc/sudoers|sudoers\.d|/etc/ssh/)'
# A read of these still asks: the protocol keeps secrets out of the chat.
SECRET_PATHS = r'((^|/)\.env(\.[\w-]+)?$|id_(rsa|ed25519|ecdsa)|\.pem$|\.key$|/etc/shadow|htpasswd|/etc/caddy/auth)'

READ_COMMANDS = {
    'ls', 'cat', 'head', 'tail', 'less', 'more', 'grep', 'egrep', 'fgrep', 'zgrep', 'wc', 'sort', 'uniq',
    'cut', 'tr', 'column', 'jq', 'df', 'du', 'free', 'uptime', 'whoami', 'id', 'hostname', 'hostnamectl',
    'date', 'uname', 'ps', 'pgrep', 'ss', 'lsblk', 'stat', 'file', 'readlink', 'realpath', 'echo',
    'printf', 'test', 'which', 'type', 'journalctl', 'tree', 'dig', 'nslookup', 'host', 'getent',
    'groups', 'pwd', 'true', 'lsof', 'nproc', 'lscpu', 'timedatectl', 'sha256sum', 'md5sum', 'zcat',
    'cd', 'basename', 'dirname', 'nl', 'diff', 'cmp', 'last', 'w', 'who', 'apt-cache',
}
READ_SUBCOMMANDS = {
    'systemctl': {'status', 'is-active', 'is-enabled', 'is-failed', 'list-units', 'list-timers', 'cat', 'show'},
    'git': {'status', 'log', 'diff', 'show', 'rev-parse', 'describe', 'ls-files', 'shortlog'},
    'caddy': {'validate', 'version', 'list-modules', 'adapt'},
    'ufw': {'status'},
    'certbot': {'certificates'},
    'apt': {'list', 'policy', 'show'},
}
DOCKER_READ = {'ps', 'images', 'inspect', 'logs', 'info', 'version', 'top', 'port', 'history'}
DOCKER_GROUP_READ = {'volume': {'ls', 'inspect'}, 'network': {'ls', 'inspect'}, 'image': {'ls', 'inspect', 'history'},
                     'container': {'ls', 'inspect', 'logs', 'top', 'port'}, 'system': {'df', 'info'}}
COMPOSE_READ = {'ps', 'logs', 'config', 'images', 'top', 'ls', 'version', 'port'}
COMPOSE_FLAGS_WITH_VALUE = {'-f', '--file', '-p', '--project-name', '--env-file', '--profile', '--project-directory'}
CONSENT = re.compile(
    r'(выполни|выполняй|запусти|запускай|разрешаю|можешь\s+(сам\s+)?(это\s+)?(выполн|запуст)|'
    r'сам\s+(выполни|запусти)|go ahead and run|you may run|run it yourself)', re.IGNORECASE)
SEGMENT_SPLIT = re.compile(r'&&|\|\||;|\||\n')


def tokens_of(text: str) -> list[str]:
    try:
        return shlex.split(text)
    except ValueError:
        return text.split()


def strip_prefixes(tokens: list[str]) -> list[str]:
    while tokens and (tokens[0] in ('sudo', 'command', 'time', 'nice') or re.match(r'^\w+=', tokens[0])
                      or (tokens[0].startswith('-') and tokens[0] in ('-n', '-E', '-u'))):
        tokens = tokens[1:]
    return tokens


def is_read_segment(segment: str) -> bool:
    tokens = strip_prefixes(tokens_of(segment.strip()))
    if not tokens:
        return True
    cmd, args = tokens[0].rsplit('/', 1)[-1], tokens[1:]
    if cmd in READ_COMMANDS:
        return not any(re.search(SECRET_PATHS, a) for a in args)
    if cmd in READ_SUBCOMMANDS:
        sub = next((a for a in args if not a.startswith('-')), '')
        if cmd == 'git' and sub == 'branch':
            return not any(a in ('-d', '-D', '-m', '-M', '--delete') for a in args)
        if cmd == 'git' and sub == 'remote':
            return len(args) == 1 or args[1:] == ['-v']
        return sub in READ_SUBCOMMANDS[cmd]
    if cmd == 'crontab':
        return args == ['-l']
    if cmd == 'dpkg':
        return bool(args) and args[0] in ('-l', '-s', '-L')
    if cmd == 'sed':
        return '-n' in args and not any(a.startswith('-i') for a in args)
    if cmd == 'find':
        return not any(a in ('-delete', '-exec', '-execdir', '-ok', '-fprint', '-fprintf', '-fls') for a in args)
    if cmd == 'curl':
        writes = ('-d', '--data', '--data-raw', '--data-binary', '--data-urlencode', '-F', '--form', '-T',
                  '--upload-file', '-o', '--output', '-O', '--remote-name')
        if any(a in writes or a.startswith(('--data', '-d')) and a != '-D' for a in args):
            return False
        for flag in ('-X', '--request'):
            if flag in args:
                i = args.index(flag)
                if i + 1 >= len(args) or args[i + 1].upper() not in ('GET', 'HEAD'):
                    return False
        return True
    if cmd == 'openssl':
        return bool(args) and args[0] in ('x509', 's_client', 'version')
    if cmd in ('docker', 'docker-compose'):
        rest = args if cmd == 'docker' else ['compose', *args]
        if not rest:
            return False
        if rest[0] == 'compose':
            i, rest = 0, rest[1:]
            while i < len(rest) and rest[i].startswith('-'):
                i += 2 if rest[i] in COMPOSE_FLAGS_WITH_VALUE else 1
            return i < len(rest) and rest[i] in COMPOSE_READ
        if rest[0] in DOCKER_GROUP_READ:
            return len(rest) > 1 and rest[1] in DOCKER_GROUP_READ[rest[0]]
        if rest[0] == 'stats':
            return '--no-stream' in rest
        return rest[0] in DOCKER_READ
    return False


def classify_remote(remote: str) -> tuple[int, str]:
    """(class, reason) for a command that will run on the server."""
    for pattern, lost in IRREVERSIBLE_PATTERNS:
        if re.search(pattern, remote):
            return IRREVERSIBLE, lost
    if re.search(r'\$\(|`|<\(', remote):
        return CHANGE, 'подстановка команд — классифицировать нельзя'
    if '>' in re.sub(r'\d?>\s*/dev/null|\d>&\d', '', remote):
        return CHANGE, 'запись в файл'
    segments = [s for s in SEGMENT_SPLIT.split(remote) if s.strip()]
    reads = [is_read_segment(s) for s in segments]
    if all(reads):
        return READ, 'только чтение'
    if re.search(ACCESS_PATHS, remote):
        return IRREVERSIBLE, 'доступ к серверу (ssh, sudo, authorized_keys)'
    if any(re.search(SECRET_PATHS, t) for s in segments for t in tokens_of(s)):
        return CHANGE, 'затрагивает секреты'
    return CHANGE, 'изменение на сервере'


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
        if rest[:1] == ['--get']:
            cls, reason = READ, 'скачивание файла'
            if any(re.search(SECRET_PATHS, a) for a in rest[1:2]):
                cls, reason = CHANGE, 'скачивание секрета'
        elif rest[:1] == ['--put']:
            cls, reason = CHANGE, 'загрузка файла на сервер (может перезаписать)'
        else:
            cls, reason = classify_remote(' '.join(rest))
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
