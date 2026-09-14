# Agent instructions

Canonical guidance for this repository. It ships tooling that teaches other
repositories to have a harness, so it has one of its own. README.md explains the
model — generator versus library, the profile, precedence, naming. This file
holds only the rules for working on the repository itself.

## 1. Working agreements

- **Nothing is pushed without an explicit instruction on the current turn.**
  Permission does not carry over. Commits are fine once the owner has said what
  to commit; pushing needs its own "+".
- **`main` is the only branch.** This is a one-person library: commits land on
  `main` directly, a branch is used only when a change is experimental enough to
  want a diff first. No force push.
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
- **Personal and work stay apart.** Nothing about Jira, GitLab, worklog or a
  company standard belongs here; the work library is `secl-agent-tools`.
- **One fact, one place.** The skill is the source; README links to it and does
  not restate it.
- **A rule earned on a live project lands here in the same session**, proposed
  by the agent and accepted by the owner — not in that project's notes.

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

No automated gate. Before committing, the author checks by hand:

- every `commands/*.md` has frontmatter with `description` and `argument-hint`;
- every `skills/*/SKILL.md` has `name` and `description`;
- every file reference inside a plugin resolves — a relative link to a file that
  exists, or a `${CLAUDE_PLUGIN_ROOT}` path;
- `marketplace.json` lists every plugin under `plugins/`, and each `plugin.json`
  name matches its catalogue entry;
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
