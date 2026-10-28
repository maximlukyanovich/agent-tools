"""Shared by bin/srv and hooks/guard.py: a command bound for a server is read, change or irreversible.

What each class leads to is in hooks/guard.py; srv refuses an irreversible command on its own unless
SRV_OWNER_APPROVED=1 is in its environment. When unsure, a command is classified as the stricter
class. The reasons are Russian: they reach the owner in the hook's prompt and in srv's refusal.
Checks: hooks/test_guard.py, lib/test_srv.py.
"""
from __future__ import annotations

import re
import shlex

READ, CHANGE, IRREVERSIBLE = 0, 1, 2
APPROVAL_VAR = 'SRV_OWNER_APPROVED'
APPROVAL_MARKER = f'{APPROVAL_VAR}=1'

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
    if cmd == 'sshd':
        # -T prints the effective configuration, -t only checks it; nothing is changed.
        return bool(args) and all(a in ('-T', '-t') for a in args)
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


def classify_call(args: list[str]) -> tuple[int, str]:
    """(class, reason) for an srv call, given its arguments after the server name."""
    if args[:1] == ['--get']:
        if any(re.search(SECRET_PATHS, a) for a in args[1:2]):
            return CHANGE, 'скачивание секрета'
        return READ, 'скачивание файла'
    if args[:1] == ['--put']:
        return CHANGE, 'загрузка файла на сервер (может перезаписать)'
    return classify_remote(' '.join(args))
