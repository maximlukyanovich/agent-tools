---
description: Onboard the developer — an overview from the project's own documents, how to run it, the command and skill index, and a live check of the plugins and the profile's Checks. Read-only.
argument-hint: '[<language>]'
---

# /mluk-repo:start

One-screen onboarding for the repository, built from what the repository
already says about itself. **Strictly read-only**: no file writes, no
installs, no commits, no container or server lifecycle changes. The first
command of a fresh session, before `task` or `promote`; a project set up by
`mluk-bootstrap` reaches it through its own `/start`, which installs the
plugins first.

Language: `$1`, else the profile's `## Languages` conversation language, else
Russian. Paths, command names, identifiers, code and quotes from project
documents are never translated.

## Steps

1. **Read the sources**, selectively: `AGENTS.md` (sections 1, 2, 4, 5, 6),
   `.claude/COMMANDS.md`, `.claude/project-profile.md` (`## Repository`,
   `## Checks`, `## Docs`) and this clone's `project-profile.local.md` if
   present, `docs/README.md` if present. No profile → say so and offer
   `/mluk-bootstrap:setup` as a code block; continue with what `AGENTS.md`
   gives. No `.claude/commands/start.md` → a `⚠` row: a fresh clone has the
   plugins turned on and nothing to install them with; the fix is
   `/mluk-bootstrap:audit`, as a code block.

2. **Run the checks** from `## Checks` in one Bash call where possible, plus
   the git baseline:

   ```bash
   git branch --show-current; git status --porcelain | head
   git log --oneline -5
   git rev-list --left-right --count origin/<base>...HEAD 2>/dev/null
   git remote -v; gh auth status 2>&1 | head -3
   ```

   Record `ok` / `missing` / `warn` / `info` per row and the one-line fix the
   profile gives. **Nothing is started**, whatever the local profile's
   `agent starts` allows: a missing dev server or stack is a `✗` with the
   profile's fix. The validate command is an `info` row and is not
   run. Check the remote alias against `remote account` (`github-accounts`
   skill).

   **The plugins.** One `claude plugin list --json`, cut to `id`, `scope`,
   `enabled`, `projectPath`, `installPath` with `jq` or `python3` before it
   is read — never the raw list. An install counts for this checkout when
   its scope is `user` or `managed`, or its `projectPath` is this checkout or
   another checkout of the same repository (`git -C <path> rev-parse
   --path-format=absolute --git-common-dir` answers as it does here). Each
   plugin `enabledPlugins` turns on with no install that counts is a `✗` row
   with `/start` — or, when step 1 found no project `/start`, with
   `claude plugin install <id> --scope local`; a profile row for the
   plugins, when there is one, runs the same report and replaces this one.

3. **Print the summary** — each section at most four lines, identifiers
   verbatim: product and phase (from `AGENTS.md` §1), stack and layout (§2–3),
   things that bite (§6), documents (`## Docs`: where technical and product
   docs live, where the contract log and roadmap are, that `docs/local/` is
   personal), git (`## Repository`: remote, chain, commit preset — a key
   the local file overrides is marked `(local)`), commands, skills (project
   ones by name; library ones by plugin).

   Commands: the library ones from the files of each enabled plugin installed
   here — the `description` line of every `<installPath>/commands/*.md`, in
   one call (`grep -m1 '^description:'`) — since `help` carries
   `disable-model-invocation` and is missing from this session's command
   list; the project's own and its overrides from `.claude/COMMANDS.md`. One
   line each, mutating ones marked.

4. **Print how to run it** — a heading in the conversation language
   («Запуск» in Russian), then the commands from the `AGENTS.md` section that
   says how the project runs (§2 in the bootstrap template): install, dev
   server, the stack, verbatim, as code blocks ready to copy — one block per
   terminal. No such section, or one without commands → a `⚠` row with
   `/mluk-bootstrap:audit`.

5. **Print the status table** — one row per check: check, `✓` / `✗` / `⚠`,
   action. Every non-`✓` row carries a concrete command, not advice.

6. **Show where the work stands**: branch, ahead/behind the base, the last
   commit subjects. A `docs/local/` note with open items is mentioned by name
   and count, never quoted.

7. **End** with `/mluk-repo:next` in a code block, ready to copy.

## Hard rules

- Read-only; nothing started, stopped, installed or written.
- The command list comes from the enabled plugins' command files and
  `.claude/COMMANDS.md`, not from memory or this session's list; library
  commands are never read from a copy in the project.
- Missing profile sections are reported as rows to fill, not guessed.
