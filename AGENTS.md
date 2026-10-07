# Agent instructions

Canonical guidance for this repository. It ships tooling that teaches other
repositories to have a harness, so it has one of its own. README.md explains the
model — generator versus library, the profile, precedence, naming. This file
holds only the rules for working on the repository itself.

## 1. Working agreements

- **Nothing is pushed without an explicit instruction on the current turn.**
  Permission does not carry over. Commits are fine once the owner has said what
  to commit; pushing needs its own "+".
- **Changes go through a branch and a pull request into `main`.** The library
  is public and other people install it, so `main` is what they get; a pull
  request leaves a diff to read before it lands. A trivial fix — a typo, a
  broken link — may land on `main` directly. No force push.
- **Plugin files are addressed through `${CLAUDE_PLUGIN_ROOT}`** inside plugin
  texts, never found by searching the filesystem. An installed plugin is a
  copy under `~/.claude/plugins/cache/`, even when the marketplace is
  registered from this checkout; `${CLAUDE_PLUGIN_ROOT}` points there.
- **An edit here is not live.** After changing a plugin run
  `claude plugin update <plugin>@mluk-agent-tools` (per installed scope) and
  restart the session. While writing a plugin, test it straight from the
  checkout with `claude --plugin-dir …/agent-tools/plugins`.
- **Library base, local override.** A project keeps a local command only when
  its procedure differs from the library's, not when a parameter does. The
  parameter goes to the profile.
- **The method lives here; project specifics live in the project profile.** A
  rule that names a concrete path, id or design system does not belong in a
  plugin. A rule that survives a change of project does not belong in a project.
- **No workspace specifics.** The plugins work in any clone of any project:
  nothing here names the author's machine, paths, sibling repositories, other
  tool libraries or personal habits of working with this one.
- **One fact, one place.** The skill is the source; README links to it and does
  not restate it.

## 2. Conventions

- **Language.** Everything committed is English — plugin texts, README, commit
  messages, this file. The one exception is `plugins/mluk-ru/skills/
  business-russian/SKILL.md`: its rules and examples are Russian, because the
  subject is Russian.
- **Commits.** `:gitmoji: type(scope): Subject`, blank line, body as `- ` bullets
  explaining why, each bullet on one line, no hard wrap. Scope is the plugin
  name without the prefix (`bootstrap`, `repo`, `ru`) or `readme` / `catalog`
  for the repository level. No agent attribution of any kind.
- **Command names** are short verbs; the plugin name is the prefix, added by the
  harness with a colon. Never a colon in a filename.
- **Plugin names are fixed once.**
- **Descriptions are the loading mechanism.** A skill's `description` decides
  when the agent loads it; a command's decides what completion shows. Both are
  written narrowly and both are paid for in every session.

## 3. Checks before a commit

The only automated gate is the `Hook tests` workflow. Before committing, the author checks by hand:

- every `commands/*.md` has frontmatter with `description` and `argument-hint`;
- every `skills/*/SKILL.md` has `name` and `description`;
- every file reference inside a plugin resolves — a relative link to a file that
  exists, or a `${CLAUDE_PLUGIN_ROOT}` path;
- `marketplace.json` lists every plugin under `plugins/`, and each `plugin.json`
  name matches its catalogue entry;
- a changed hook passes its tests — `node --test 'plugins/mluk-fe/hooks/*.test.mjs'`,
  `python3 plugins/mluk-ops/hooks/test_guard.py`; the `Hook tests` workflow runs the same on
  every push;
- the changed command or skill was run once, in a real repository, after
  `claude plugin update` (or via `--plugin-dir`), and did what its text says.

The last item is not optional. A command that has never been executed is a
draft.

## 4. Layout

```
.claude-plugin/marketplace.json   the catalogue
plugins/<name>/
  .claude-plugin/plugin.json      manifest
  commands/*.md                   procedures a human invokes
  skills/<name>/SKILL.md          knowledge the agent loads by itself
  reference/*.md                  read one file at a time, on instruction
  README.md                       for people, links to the skill
```
