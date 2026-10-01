#!/usr/bin/env python3
"""Checks for guard.py — run by hand after every edit: python3 hooks/test_guard.py"""
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import guard  # noqa: E402

CONFIG = {'servers': {'box': {'host': '203.0.113.7', 'user': 'deploy', 'aliases': ['api.example.test']}}}
SRV = '/home/u/.claude/plugins/cache/x/mluk-ops/bin/srv'


def transcript(*messages):
    fh = tempfile.NamedTemporaryFile('w', suffix='.jsonl', delete=False)
    for m in messages:
        fh.write(json.dumps({'type': 'user', 'origin': {'kind': 'human'},
                             'message': {'role': 'user', 'content': [{'type': 'text', 'text': m}]}}) + '\n')
    fh.write(json.dumps({'type': 'user', 'message': {'content': [{'type': 'tool_result', 'content': 'x'}]}}) + '\n')
    fh.close()
    return fh.name


CASES = [
    # (command, expected decision, transcript messages)
    ('ls -la', None, ()),
    ('git status', None, ()),
    ('curl -s https://api.example.test/health/', None, ()),
    (f"{SRV} box 'docker compose -f docker-compose.server.yml ps'", 'allow', ()),
    (f"{SRV} box 'docker compose -f x.yml logs --tail 50 api | grep ERROR'", 'allow', ()),
    (f"{SRV} box 'df -h && free -m && uptime'", 'allow', ()),
    (f"{SRV} box 'cat /srv/app/.env'", 'ask', ()),
    (f"{SRV} box 'cat ~/.ssh/authorized_keys'", 'allow', ()),
    (f"{SRV} box 'sudo systemctl status caddy'", 'allow', ()),
    (f"{SRV} box 'sudo sshd -T | grep -i permitrootlogin'", 'allow', ()),
    (f"{SRV} box 'ls /etc/ssh/sshd_config.d/ && sudo sshd -t'", 'allow', ()),
    (f"{SRV} box 'sudo sshd -D'", 'ask', ()),
    (f"{SRV} box 'curl -sS http://127.0.0.1:8001/health/'", 'allow', ()),
    (f"{SRV} box 'curl -X POST http://127.0.0.1:8001/x'", 'ask', ()),
    (f"{SRV} box 'cd /srv/app && git pull --ff-only && deploy/server/deploy.sh'", 'ask', ()),
    (f"{SRV} box 'sudo systemctl reload caddy'", 'ask', ()),
    (f"{SRV} box 'docker compose -f x.yml down'", 'ask', ()),
    (f"{SRV} box --get /tmp/db.dump ./db.dump", 'allow', ()),
    (f"{SRV} box --put ./site.caddy /tmp/site.caddy", 'ask', ()),
    (f"{SRV} box 'echo $(whoami)'", 'ask', ()),
    (f"{SRV} box 'rm -rf /srv/old'", 'deny', ()),
    (f"{SRV} box 'docker compose -f x.yml down -v'", 'deny', ()),
    (f"{SRV} box 'docker volume rm staging_postgres_data'", 'deny', ()),
    (f"{SRV} box 'docker system prune -af --volumes'", 'deny', ()),
    (f"{SRV} box 'docker compose exec -T postgres dropdb -U a a'", 'deny', ()),
    (f"{SRV} box 'psql -c \"DROP TABLE x\"'", 'deny', ()),
    (f"{SRV} box 'sudo ufw disable'", 'deny', ()),
    (f"{SRV} box 'echo PermitRootLogin no | sudo tee /etc/ssh/sshd_config.d/00-h.conf'", 'deny', ()),
    (f"{SRV} box 'sed -i s/a/b/ .env'", 'deny', ()),
    (f"{SRV} box 'sed -i.bak s/a/b/ .env'", 'ask', ()),
    (f"{SRV} box 'echo x > /etc/caddy/Caddyfile'", 'deny', ()),
    (f"{SRV} box 'echo x > /tmp/scratch'", 'ask', ()),
    (f"{SRV} box 'git reset --hard origin/main'", 'deny', ()),
    (f"{SRV} box 'sudo reboot'", 'deny', ()),
    (f"{SRV} box 'pg_restore --clean -d db /tmp/x'", 'deny', ()),
    # consent: marker alone is not enough; marker + explicit words in the latest message -> ask
    (f"SRV_OWNER_APPROVED=1 {SRV} box 'rm -rf /srv/old'", 'deny', ('+',)),
    (f"SRV_OWNER_APPROVED=1 {SRV} box 'rm -rf /srv/old'", 'deny', ('можешь выполнить', 'ок, продолжай')),
    (f"SRV_OWNER_APPROVED=1 {SRV} box 'rm -rf /srv/old'", 'ask', ('Можешь сам выполнить удаление',)),
    (f"{SRV} box 'rm -rf /srv/old'", 'deny', ('Можешь сам выполнить удаление',)),
    # direct transport to a configured host
    ('ssh deploy@203.0.113.7 uptime', 'deny', ()),
    ('scp x deploy@api.example.test:/tmp/', 'deny', ()),
    ('ssh other.host uptime', None, ()),
    ("ssh-keygen -t ed25519 -f ~/.ssh/k -C 'api.example.test'", None, ()),
    ('rsync -a ./x deploy@203.0.113.7:/tmp/', 'deny', ()),
    # srv glued to something else
    (f"{SRV} box 'uptime'; rm -rf ~/x", 'ask', ()),
    (f"{SRV} nope 'uptime'", 'deny', ()),
]


def main() -> int:
    failed = 0
    for command, expected, messages in CASES:
        path = transcript(*messages) if messages else None
        result = guard.decide(command, CONFIG, path)
        got = result[0] if result else None
        if got != expected:
            failed += 1
            print(f'FAIL {command!r}: expected {expected}, got {got} ({result[1] if result else ""})')
    assert guard.decide('ls', {'servers': {}}, None) is None
    print(f'{len(CASES) - failed}/{len(CASES)} ok')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
