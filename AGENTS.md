# Agent instructions

Canonical guidance for this repository. It ships tooling that teaches other
repositories to have a harness, so it has one of its own. `docs/design.md`
explains the model — generator versus library, the profile, precedence,
naming. This file holds only the rules for working on the repository itself.

## 1. Working agreements

- **Nothing is pushed without an explicit instruction on the current turn.**
  Permission does not carry over. Commits are fine once the owner has said what
  to commit; pushing needs its own "+".
- **Changes go through a branch and a pull request into `main`.** The library
  is public and other people install it, so `main` is what they get; a pull
  request leaves a diff to read before it lands. A trivial fix — a typo, a
  broken link — may land on `main` directly; inside a plugin it still raises
  the patch version. No force push.
- **Before a new branch, the open pull requests touching the same files** —
  `gh pr list --json number,headRefName,files`. An overlap is merged first,
  or the work goes onto that branch; two branches editing one file book a
  conflict in advance.
- **Plugin files are addressed through `${CLAUDE_PLUGIN_ROOT}`** inside plugin
  texts, never found by searching the filesystem. An installed plugin is a
  copy under `~/.claude/plugins/cache/`, even when the marketplace is
  registered from this checkout; `${CLAUDE_PLUGIN_ROOT}` points there.
- **An edit here is not live** until it lands on `main` with its plugin's
  `version` raised: a project that declares the marketplace with
  `autoUpdate` gets it up to ten minutes after an interactive session's
  first message, by hand `claude plugin update <plugin>@mluk-agent-tools`
  (per installed scope); `/reload-plugins` applies it to an open session.
  While writing a plugin, test it straight from the checkout with
  `claude --plugin-dir …/agent-tools/plugins`.
- **A change raises the `version` of every plugin it touches**, in its
  `plugin.json`; a change to the plugin's README alone needs none. Major when
  a project must act or it breaks — a profile format, a new required plugin,
  a removed command; minor for a new rule, command or template section; patch
  for wording or a fix that keeps the behaviour. Claude Code replaces an
  installed plugin only when its version differs from the installed one, so
  a change without a raise reaches nobody, the owner included. The catalogue
  carries no `version`: `plugin.json` wins over it, and a second copy drifts.
- **A merged batch is released** on the owner's word, like a push: an
  annotated tag `vYYYY.MM.DD` on the batch's merge commit into `main` — that
  commit's date, `git log -1 --format=%cs <merge>`; `.2`, `.3` for a second
  and third batch that day — and a GitHub release whose notes put
  `scripts/release_notes.py` — the plugin versions and what a project must
  do — above the merged pull requests:

  ```bash
  git tag -a <tag> -m <tag> <merge> && git push origin <tag>
  gh release create <tag> --verify-tag --title <tag> \
    --notes "$(python3 scripts/release_notes.py <previous tag> <tag>)" \
    --generate-notes --notes-start-tag <previous tag>
  ```

  Release immutability is on: a released tag cannot be moved or deleted, so a
  wrong release is corrected by the next tag. The date says which release a
  project runs; a plugin's version says whether the project must act.
- **Library base, local override.** A project keeps a local command only when
  its procedure differs from the library's, not when a parameter does. The
  parameter goes to the profile.
- **The method lives here; project specifics live in the project profile.** A
  rule that names a concrete path, id or design system does not belong in a
  plugin. A rule that survives a change of project does not belong in a project.
- **No workspace specifics.** The plugins work in any clone of any project:
  nothing in a plugin names the author's machine, paths, sibling repositories,
  other tool libraries or personal habits of working with this one. The
  README may point a reader to the sibling library that fits their project
  better.
- **One fact, one place.** The skill is the source; README links to it and does
  not restate it.
- **A change corrects every text it makes untrue, in the same commit** —
  README, `AGENTS.md`, `CONTRIBUTING.md`, `docs/design.md`, a plugin's README
  and `help`. Before committing, search the repository for the statements the
  change touches. "One fact, one place" keeps the copies few; this keeps the
  ones left true.
- **A tool's behaviour is stated only after a check.** What a plugin text says
  Claude Code, git, Compose or any other tool does — which file a value comes
  from, what a flag or a scope changes, which entry wins a merge — is checked
  first: a probe in a scratch directory, the tool's documentation (Context7)
  or its source, never memory or inference. A claim that holds for some
  options names them; a reason that names no property ("that copy lacks what
  the declaration carries") was not checked.

## 2. Conventions

- **Language.** Everything committed is English — plugin texts, README, commit
  messages, this file. The one exception is `plugins/mluk-ru/skills/
  business-russian/SKILL.md` with its `plugins/mluk-ru/reference/legal.md`:
  their rules and examples are Russian, because the subject is Russian.
- **Commits.** `:gitmoji: type(scope): Subject`, blank line, body as `- ` bullets
  explaining why, each bullet on one line, no hard wrap. Scope is the plugin
  name without the prefix (`bootstrap`, `repo`, `ru`) or `readme` / `catalog`
  for the repository level. No agent attribution of any kind.
- **No real project is named** — a client's or the owner's own — in plugin
  texts, examples, commit messages, pull requests or issues: not its name,
  issue keys, paths, recognisable domain terms or quotes from it. A lesson
  from a live project is described as "observed on a live project", without
  saying which.
- **Command names** are short verbs; the plugin name is the prefix, added by the
  harness with a colon. Never a colon in a filename.
- **Plugin names are fixed once.**
- **Descriptions are the loading mechanism.** A skill's `description` decides
  when the agent loads it; a command's decides what completion shows. Both are
  written narrowly and both are paid for in every session — except a
  command only a human runs, such as `help`, which carries
  `disable-model-invocation: true` and stays out of the model's context.
- **`model:` goes on agents, not on commands or skills.** A command's
  override lasts one turn, and the next turn re-reads the whole history
  without cache; a subagent starts with an empty context, so its model is
  where the choice pays.
- **A command ends with its next step** as a code block ready to copy;
  alternatives are separate blocks. So does a step that stops early and sends
  the owner to another command — a dirty tree to the commit: the command is
  also given as a block, with the worktree or branch argument the work needs.
  Naming it inside a sentence is fine; what the stop must not lack is the
  block. A step answered in the same session — a yes to a commit, a choice
  between closing steps — stays a question.

## 3. Checks before a pull request

Two workflows gate every pull request and `main`. `Check` runs
`scripts/check.py`; run it locally before pushing, after `git fetch` —
`python3 scripts/check.py`. It compares versions against `origin/main`, or the
`--base` you pass, and stops when that ref is missing. It checks:

- every `commands/*.md` has frontmatter with `description` and `argument-hint`;
- every `skills/*/SKILL.md` has `name` and `description`, every
  `agents/*.md` has `name`, `description` and `tools`;
- every file reference inside a plugin resolves — a relative link to a file that
  exists, or a `${CLAUDE_PLUGIN_ROOT}` path;
- `marketplace.json` lists every plugin under `plugins/`, and each `plugin.json`
  name matches its catalogue entry;
- every plugin hook points at a script that exists, in `command` or `args`;
- every Python script compiles;
- it warns, without failing, about a plugin text above 10 KB — any `*.md`
  under `plugins/` but a README: splitting it is a decision, not drift;
- every `plugin.json` has a `version` of the form `MAJOR.MINOR.PATCH`, the
  catalogue has none, and a plugin whose files changed, its README aside, has
  a version above the base's.

`Plugin tests` runs the hooks' and the start template's tests. Before opening
a pull request, its author checks by hand:

- a changed hook or template passes its tests — `node --test 'plugins/mluk-fe/hooks/*.test.mjs'`,
  `python3 plugins/mluk-ops/hooks/test_guard.py`,
  `node --test 'plugins/mluk-bootstrap/templates/start/lib/*.test.mjs'`; the `Plugin tests`
  workflow runs the same on every push;
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
  agents/*.md                     subagents a command delegates to
  reference/*.md                  read one file at a time, on instruction
  templates/<name>/               files setup copies into a project as they are
  README.md                       for people, links to the skill
scripts/check.py                  the pull-request gate, run by CI
scripts/release_notes.py          a release's notes: plugin versions, action needed
.github/workflows/check.yml       runs the gate
.github/workflows/hooks.yml       runs the hooks' and the start template's tests
```

`commands/` is the older of the two plugin formats; Claude Code now prefers
skills with `disable-model-invocation`; the layout migrates in one move when
it does.
