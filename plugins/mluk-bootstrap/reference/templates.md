# Templates

Skeletons only. Every example inside a skill or command is written for **this**
project's domain — carrying someone else's examples over is an anti-pattern.

## AGENTS.md

Seven sections, in this order. Anything a linter already enforces is marked
`[lint]` and not explained twice. Anything the library already states (commit
format, PR shape, git safety, the kickoff method) is a one-line pointer to the
plugin skill, not a restatement.

```markdown
# Agent instructions

## 1. Project        what it is, which surfaces, sibling repositories, current phase
## 2. Commands       install, dev, the stack — commands run from the root, how not who; the gate, tests, build
## 3. Architecture   layers table: path, responsibility, what it may import
## 4. Conventions    languages, branches, commits (preset name → skill), styling, copy
## 5. Sources of truth   priority order, design source, what to do on conflict
## 6. Working agreements  the rules that are not machine-checkable
## 7. Agent tooling   enabled plugins, local overrides, project skills, checks, hooks
```

Rules that keep it cheap: no rule appears twice; anything expressible as lint
configuration is a one-line reference, not a paragraph; the absence of a layer
is recorded deliberately, with its reason.

With pnpm 11, §2 says next to how a dependency is added that one with a build
script — direct or transitive — needs an `allowBuilds` entry in
`pnpm-workspace.yaml`. A missing entry fails the install with
`ERR_PNPM_IGNORED_BUILDS`, but only a clean one: a warm `node_modules` hides
it, and the first to see it is the deploy. The file's header gives each entry
its reason and says to prove a new dependency with
`pnpm install --frozen-lockfile` in a fresh clone.

## CLAUDE.md

```markdown
@AGENTS.md

# CLAUDE.md

Project rules live in AGENTS.md, imported above. This file holds only what is
specific to Claude Code and written nowhere else — deleting it must not lose a
single project rule.
```

## SKILL.md

```markdown
---
name: <name>
description: <what it covers, and when it applies — the sentence that decides loading>
---

# <name>

## When it applies
## How to do it
## How not to do it
## How it is verified
```

The `description` is the whole loading mechanism. Vague means either never
loaded or always loaded.

## A local command (override)

Written only when the procedure differs from the library command of the same
job. The first paragraph names the library command it overrides and the reason.

```markdown
---
description: <one line, shown in slash-command completion>
argument-hint: '[<arg>]'
---

# /<name>

Overrides `/mluk-repo:<name>` because <the procedural difference>.

## Steps
## Hard rules      what this command must never do
```

Read-only unless stated otherwise. No implicit push, merge or PR creation;
permission applies to the current turn only.

## .claude/COMMANDS.md

```markdown
# Commands

The library plugins enabled in [`settings.json`](settings.json) bring their own
commands; each plugin's `help` lists them (`/mluk-repo:help` first). They read
[`project-profile.md`](project-profile.md) plus this clone's gitignored
`project-profile.local.md`. This file lists only what the library does not
know: the project's own commands and its overrides.

## Local

| Command | Mutating | What it does |
| --- | --- | --- |
| [`/start`](commands/start.md) | installs plugins, on a yes | First command in a fresh clone: installs the declared plugins that are missing, then runs `/mluk-repo:start` |
| [`/<local>`](commands/<local>.md) | … | … |

`/start` is local because a plugin that is not installed has no commands, so
the library cannot install itself.

## Overrides

None. A local command overrides a library one only when the procedure differs
— a parameter goes to the profile. Each override is a row here:
`/<local>` overrides `/mluk-repo:<name>` because <reason>.
```

## The project's /start

Copied, not written: `${CLAUDE_PLUGIN_ROOT}/templates/start/` — setup step 4
says how. Its version line is what `audit` compares; a project that changes the
copy records why in `.claude/COMMANDS.md`.

## README — Agent tooling

```markdown
## Agent tooling

Optional, for Claude Code: start it at the repository root and trust the
folder. That registers the plugin marketplaces `.claude/settings.json`
declares but downloads no plugin — run `/start`, which installs the missing
ones and then gives the overview. A session that is already open loads new or
updated plugins after `/reload-plugins`. Other agents read
[AGENTS.md](AGENTS.md).
```

## .mcp.json.example

Servers with `${VAR}` placeholders, committed. A generator script substitutes
values from `.env` and fails loudly on a missing one — a partially substituted
config is worse than none.

## Hook contract

A `PostToolUse` hook receives the tool call, exits **0 and silent** when the
file is outside its area, and prints an actionable message otherwise. Every hook
has a test. A hook that fires on ordinary edits gets ignored and then removed.

## docs/local/README.md

The only committed file in the personal space. It states what lives there —
plans, handoffs, excerpts, a copy journal, task notes — and one rule for the
agent: this material is context, never a source of truth, and is never quoted
into committed content.
