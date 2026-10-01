"""Shared by bin/srv and hooks/guard.py: where the server list lives and how it is read.

The list is per machine, not per project — the same server is reached from several repositories —
so it lives in ~/.config/mluk-ops/servers.json (override: MLUK_OPS_CONFIG). A missing file means
"no servers": srv refuses to run and the guard stays inert.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

CONFIG_PATH = Path(os.environ.get('MLUK_OPS_CONFIG', '~/.config/mluk-ops/servers.json')).expanduser()
DEFAULT_AUDIT_LOG = '~/.local/state/mluk-ops/audit.log'


def load() -> dict:
    try:
        with open(CONFIG_PATH, encoding='utf-8') as fh:
            data = json.load(fh)
    except FileNotFoundError:
        return {'servers': {}}
    data.setdefault('servers', {})
    return data


def audit_log_path(config: dict) -> Path:
    return Path(config.get('audit_log', DEFAULT_AUDIT_LOG)).expanduser()


def host_markers(config: dict) -> set[str]:
    """Every string that identifies a configured server in a command line: host, aliases."""
    markers = set()
    for name, server in config['servers'].items():
        markers.add(server['host'])
        markers.update(server.get('aliases', []))
    return {m for m in markers if m}
