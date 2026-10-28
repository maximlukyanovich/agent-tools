#!/usr/bin/env python3
"""The pull-request gate for this repository — the mechanical part of AGENTS.md §3.

Checks what a reviewer should never have to read for:
  - every command has frontmatter with `description` and `argument-hint`;
  - every skill has frontmatter with `name` and `description`, every agent `name`, `description`
    and `tools`;
  - every `${CLAUDE_PLUGIN_ROOT}/…` path and every relative Markdown link resolves;
  - marketplace.json lists every plugin under plugins/, sources exist, names match plugin.json;
  - every plugin hook points at a script that exists, in its `command` or its `args`;
  - every Python script compiles;
  - every plugin.json has a MAJOR.MINOR.PATCH `version` and the catalogue has none; a plugin whose
    files differ from the merge base with --base, its README aside, has a version above the one at
    --base's tip.

The sections are the work-agent-tools gate's, kept in pairs; it differs in three: no plugin here
keeps a CHANGES.md, so there is no section for one; commands here carry `argument-hint`; plugins
here ship agents.

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


def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    return {k.strip(): v.strip() for k, v in
            (line.split(":", 1) for line in m.group(1).splitlines() if ":" in line and not line.startswith(" "))}


def prose(text):
    """Markdown with code removed: a path inside backticks or a fence is an example, not a link."""
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", text)


PLUGIN_ROOT_REF = re.compile(r"\$\{CLAUDE_PLUGIN_ROOT\}/([A-Za-z0-9_./-]+)")

# ---------------------------------------------------------------- frontmatter
REQUIRED = {"commands/*.md": ("description", "argument-hint"),
            "skills/*/SKILL.md": ("name", "description"),
            "agents/*.md": ("name", "description", "tools")}
for pattern, keys in REQUIRED.items():
    kind = pattern.split("/")[0].rstrip("s")
    for path in sorted(PLUGINS.glob(f"*/{pattern}")):
        fm = frontmatter(path)
        for key in keys:
            if fm is None or not fm.get(key):
                fail(path, f"{kind} without `{key}` in frontmatter")

# ---------------------------------------------------------------- references
for md in sorted(PLUGINS.rglob("*.md")) + [ROOT / "README.md", ROOT / "AGENTS.md"]:
    raw = md.read_text(encoding="utf-8")
    plugin = next((p for p in md.parents if p.parent == PLUGINS), None)
    # Plugin-root paths are checked even inside code: that is where commands write them.
    for ref in PLUGIN_ROOT_REF.findall(raw):
        if plugin is None:
            continue
        if not (plugin / ref.rstrip(".")).exists():
            fail(md, f"${{CLAUDE_PLUGIN_ROOT}}/{ref} does not exist in {plugin.name}")
    for target in re.findall(r"\]\(([^)\s]+)\)", prose(raw)):
        # A URL, an anchor or a placeholder in an example — `[PR #1](…)` — is not a file link.
        if re.match(r"[a-z]+:|#", target) or not re.search(r"[A-Za-z0-9]", target):
            continue
        if not (md.parent / target.split("#")[0]).exists():
            fail(md, f"link to {target} does not resolve")


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

# ---------------------------------------------------------------- plugin hooks
# A hook names its script in `command` or, with an interpreter there, in `args`.
for hooks in sorted(PLUGINS.glob("*/hooks/hooks.json")):
    plugin = hooks.parent.parent
    try:
        config = json.loads(hooks.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        fail(hooks, f"does not parse: {e}")
        continue
    for groups in config.get("hooks", {}).values():
        for group in groups:
            for hook in group.get("hooks", []):
                for part in [hook.get("command", ""), *hook.get("args", [])]:
                    for ref in PLUGIN_ROOT_REF.findall(part):
                        if not (plugin / ref).exists():
                            fail(hooks, f"${{CLAUDE_PLUGIN_ROOT}}/{ref} does not exist in {plugin.name}")

# ---------------------------------------------------------------- scripts
for script in sorted(ROOT.rglob("*.py")):
    if "__pycache__" in script.parts:
        continue
    try:
        compile(script.read_text(encoding="utf-8"), str(script), "exec")
    except SyntaxError as e:
        fail(script, f"does not compile: line {e.lineno}: {e.msg}")

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
