#!/usr/bin/env python3
"""The pull-request gate for this repository — the mechanical part of AGENTS.md §3.

Checks what a reviewer should never have to read for:
  - marketplace.json lists every plugin under plugins/, sources exist, names match plugin.json;
  - every plugin.json has a MAJOR.MINOR.PATCH `version` and the catalogue has none; a plugin whose
    files differ from the merge base with --base, its README aside, has a version above the one at
    --base's tip.

Standard library and git only, so CI needs nothing but a Python image. Exit code 1 on any finding.
Run: git fetch origin main && python3 scripts/check.py [--base <ref>]   (default origin/main)
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGINS = ROOT / "plugins"
problems = []

parser = argparse.ArgumentParser(description="The pull-request gate; see the module docstring.")
parser.add_argument("--base", default="origin/main", help="the ref versions are raised against (default origin/main)")
args = parser.parse_args()


def fail(path, message):
    problems.append(f"{path.relative_to(ROOT)}: {message}")


# ---------------------------------------------------------------- catalogue
catalogue = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
listed = {}
for entry in catalogue.get("plugins", []):
    source = (ROOT / entry["source"]).resolve()
    listed[source] = entry["name"]
    manifest = source / ".claude-plugin" / "plugin.json"
    if not manifest.exists():
        fail(ROOT / ".claude-plugin" / "marketplace.json", f"{entry['name']}: no plugin.json at {entry['source']}")
        continue
    name = json.loads(manifest.read_text(encoding="utf-8")).get("name")
    if name != entry["name"]:
        fail(manifest, f"name {name!r} differs from the catalogue entry {entry['name']!r}")
for plugin_dir in sorted(p for p in PLUGINS.iterdir() if p.is_dir()):
    if plugin_dir.resolve() not in listed:
        fail(plugin_dir, "plugin not listed in marketplace.json")

# ---------------------------------------------------------------- versions
# Claude Code replaces an installed plugin only when its version changes: a
# change without a raise reaches nobody, and nothing else would say so.
SEMVER = re.compile(r"(\d+)\.(\d+)\.(\d+)")


def git(*argv):
    return subprocess.run(["git", "-C", str(ROOT), *argv], capture_output=True, text=True)


def semver(value):
    m = SEMVER.fullmatch(value) if isinstance(value, str) else None
    return tuple(int(n) for n in m.groups()) if m else None


def shown(version):
    return ".".join(map(str, version))


for entry in catalogue.get("plugins", []):
    if "version" in entry:
        fail(ROOT / ".claude-plugin" / "marketplace.json",
             f"{entry['name']}: a `version` in the catalogue — it belongs in plugin.json alone")

versions = {}
for manifest in sorted(PLUGINS.glob("*/.claude-plugin/plugin.json")):
    version = semver(json.loads(manifest.read_text(encoding="utf-8")).get("version"))
    if version is None:
        fail(manifest, "no `version` of the form MAJOR.MINOR.PATCH")
    else:
        versions[manifest.parent.parent.name] = version

if git("rev-parse", "--verify", "--quiet", f"{args.base}^{{commit}}").returncode != 0:
    # A skipped comparison would pass the very change this section exists to stop.
    problems.append(f"versions: base {args.base} not found — git fetch origin main, or pass --base")
else:
    fork = git("merge-base", args.base, "HEAD").stdout.strip()
    changed = git("diff", "--name-only", fork, "--", "plugins/").stdout.splitlines()
    touched = {Path(p).parts[1] for p in changed
               if not (len(Path(p).parts) == 3 and Path(p).name == "README.md")}
    for plugin in sorted(touched & versions.keys()):
        before = git("show", f"{args.base}:plugins/{plugin}/.claude-plugin/plugin.json")
        if before.returncode != 0:
            continue  # new in this change: any version will do
        try:
            base_version = semver(json.loads(before.stdout).get("version")) or (0, 0, 0)
        except json.JSONDecodeError:
            base_version = (0, 0, 0)
        if versions[plugin] <= base_version:
            fail(PLUGINS / plugin / ".claude-plugin" / "plugin.json",
                 f"{plugin} changed since {args.base}, but its version {shown(versions[plugin])} "
                 f"is not above {shown(base_version)} there")

if problems:
    print("\n".join(problems))
    print(f"\n{len(problems)} problem(s)")
    sys.exit(1)
print("all checks passed")
