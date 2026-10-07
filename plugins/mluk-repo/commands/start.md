---
description: Onboard the developer — an overview from the project's own documents, the command and skill index, and a live check of everything the profile's Checks section lists. Read-only.
argument-hint: '[<language>]'
---

# /mluk-repo:start

One-screen onboarding for the repository, built from what the repository
already says about itself. **Strictly read-only**: no file writes, no
installs, no commits, no container or server lifecycle changes. The first
command of a fresh session, before `task` or `promote`.

Language: `$1`, else the profile's `## Languages` conversation language, else
Russian. Paths, command names, identifiers, code and quotes from project
documents are never translated.

## Steps

1. **Read the sources**, selectively: `AGENTS.md` (sections 1, 2, 4, 5, 6),
   `.claude/COMMANDS.md`, `.claude/project-profile.md` (`## Repository`,
   `## Checks`, `## Docs`) and this clone's `project-profile.local.md` if
   present, `docs/README.md` if present. No profile → say so and offer
   `/mluk-bootstrap:setup`; continue with what `AGENTS.md` gives.

2. **Run the checks** from `## Checks` in one Bash call where possible, plus
   the git baseline:

   ```bash
   git branch --show-current; git status --porcelain | head
   git log --oneline -5
   git rev-list --left-right --count origin/<base>...HEAD 2>/dev/null
   git remote -v; gh auth status 2>&1 | head -3
   ```

   Record `ok` / `missing` / `warn` / `info` per row and the one-line fix the
   profile gives. **Do not start the dev server or the containers** — the
   owner runs them; a missing one is a `✗` with "ask the owner to run …". The
   validate command is an `info` row and is not run. Check the remote alias
   against `remote account` (`github-accounts` skill).

3. **Print the summary** — each section at most four lines, identifiers
   verbatim: product and phase (from `AGENTS.md` §1), stack and layout (§2–3),
   things that bite (§6), documents (`## Docs`: where technical and product
   docs live, where the contract log and roadmap are, that `docs/local/` is
   personal), git (`## Repository`: remote, chain, commit preset — a key
   the local file overrides is marked `(local)`), commands
   (the library ones from the enabled plugins as this session lists them —
   `enabledPlugins` in `.claude/settings.json` says which; the project's own
   and its overrides from `.claude/COMMANDS.md`; one line each, mutating
   ones marked), skills (project ones by name; library ones by plugin).

4. **Print the status table** — one row per check: check, `✓` / `✗` / `⚠`,
   action. Every non-`✓` row carries a concrete command, not advice.

5. **Show where the work stands**: branch, ahead/behind the base, the last
   commit subjects. A `docs/local/` note with open items is mentioned by name
   and count, never quoted.

## Hard rules

- Read-only; nothing started, stopped, installed or written.
- The command list comes from the enabled plugins and `.claude/COMMANDS.md`,
  not from memory; library commands are never read from a copy in the project.
- Missing profile sections are reported as rows to fill, not guessed.
