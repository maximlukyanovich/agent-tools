#!/usr/bin/env python3
"""Checks for bin/srv — run by hand after every edit: python3 lib/test_srv.py

srv runs as a subprocess against a temporary server list, with a fake ssh and scp first in PATH that
only record their arguments: nothing here reaches a server.
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

SRV = Path(__file__).resolve().parent.parent / 'bin' / 'srv'
FAKE = '#!/bin/sh\nprintf "%s\\n" "$(basename "$0") $*" >> "$SRV_TEST_CALLS"\n'
results = []


def check(name, ok, detail=''):
    results.append(ok)
    if not ok:
        print(f'FAIL {name}: {detail}')


def run(tmp: Path, argv: list[str], approved: bool = False, shell: str | None = None):
    """(exit code, stderr, transport calls, last audit record) of one srv call."""
    calls = tmp / 'calls'
    calls.unlink(missing_ok=True)
    env = {k: v for k, v in os.environ.items() if k != 'SRV_OWNER_APPROVED'}
    env.update(PATH=f'{tmp / "bin"}{os.pathsep}{env["PATH"]}', MLUK_OPS_CONFIG=str(tmp / 'servers.json'),
               SRV_TEST_CALLS=str(calls))
    if approved:
        env['SRV_OWNER_APPROVED'] = '1'
    cmd = ['sh', '-c', shell] if shell else [str(SRV), *argv]
    done = subprocess.run(cmd, env=env, capture_output=True, text=True)
    sent = calls.read_text().splitlines() if calls.exists() else []
    log = (tmp / 'audit.log').read_text().splitlines()
    return done.returncode, done.stderr, sent, json.loads(log[-1]) if log else {}


def main() -> int:
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        (tmp / 'bin').mkdir()
        for tool in ('ssh', 'scp'):
            (tmp / 'bin' / tool).write_text(FAKE)
            (tmp / 'bin' / tool).chmod(0o755)
        (tmp / 'servers.json').write_text(json.dumps({
            'audit_log': str(tmp / 'audit.log'),
            'servers': {'box': {'host': '203.0.113.7', 'user': 'deploy'}}}))

        code, err, sent, rec = run(tmp, ['box', 'rm -rf /srv/old'])
        check('irreversible without the marker is refused', code == 3 and not sent, (code, sent))
        check('the refusal names the reason', 'НЕОБРАТИМО — удаление файлов' in err, err)
        check('the refusal is logged', rec.get('refused') == 'удаление файлов' and rec.get('exit') == 3, rec)

        code, err, sent, rec = run(tmp, ['box', 'docker compose -f x.yml down -v'])
        check('down -v without the marker is refused', code == 3 and not sent, (code, sent))

        code, err, sent, rec = run(tmp, ['box', 'rm -rf /srv/old'], approved=True)
        check('irreversible with the marker runs',
              code == 0 and len(sent) == 1 and sent[0].endswith('rm -rf /srv/old'), (code, sent))
        check('the marker is logged', rec.get('owner_approved') is True and 'refused' not in rec, rec)

        code, err, sent, rec = run(tmp, ['box', 'uptime'])
        check('a read runs', code == 0 and len(sent) == 1 and sent[0].startswith('ssh '), (code, sent))
        check('a read is logged without refused', rec.get('command') == 'uptime' and 'refused' not in rec, rec)

        code, err, sent, rec = run(tmp, ['box', 'sudo systemctl reload caddy'])
        check('a change runs: the hook asks about it, not srv', code == 0 and len(sent) == 1, (code, sent))

        code, err, sent, rec = run(tmp, ['box', '--put', './site.caddy', '/tmp/site.caddy'])
        check('--put runs', code == 0 and len(sent) == 1 and sent[0].startswith('scp '), (code, sent))

        code, err, sent, rec = run(tmp, ['box', '--get', '/tmp/db.dump', './db.dump'])
        check('--get runs', code == 0 and len(sent) == 1 and sent[0].startswith('scp '), (code, sent))

        code, err, sent, rec = run(tmp, [], shell=f"echo \"{SRV} box 'rm -rf /x'\" | sh")
        check('an indirect call through sh without the marker is refused', code == 3 and not sent, (code, sent))

        code, err, sent, rec = run(
            tmp, [], shell=f"python3 -c \"import os; os._exit(os.system('{SRV} box rm -rf /y') >> 8)\"")
        check('an indirect call through python3 -c without the marker is refused', code == 3 and not sent,
              (code, sent))

    print(f'{sum(results)}/{len(results)} ok')
    return 0 if all(results) else 1


if __name__ == '__main__':
    sys.exit(main())
