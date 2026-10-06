---
description: Audit an existing agent harness against the layer model — drift, duplication, local commands that copy the library, a profile with missing sections — and report in priority order. Read-only.
argument-hint: ''
---

# /mluk-bootstrap:audit

The harness exists; the job is to find the gaps, not to rewrite it.
**Read-only** until a change is approved, and then one group at a time.

## What to check

1. **Document against code.** Do the commands named in `AGENTS.md` exist —
   locally or in an enabled plugin? Does the described architecture match the
   tree? Are the enforcement mechanisms it names actually wired up? A
   linter plugin in the dev-dependencies (`eslint-plugin-boundaries`, an
   import-order or a11y plugin) that the linter config never loads is a rule
   the project believes it has — check each against the config, and the prose
   that cites it against what the rule actually forbids. **Prose
   that contradicts the code is stale prose, and it is worse than no prose** —
   it looks like a source of truth without being one.

2. **Duplication.** The same rule in `AGENTS.md`, `CLAUDE.md`, a project skill
   and a library skill — collapse to one place plus links. The library is the
   source for anything that survives a change of project.

3. **Local commands that copy the library.** For every `.claude/commands/*.md`
   whose name matches a `mluk-repo` command (`commit`, `create-pr`, `promote`,
   `review`, `sync`, `start`, `task`, `update-docs`): does its procedure differ,
   or only its parameters? Parameters → propose moving them into the profile
   and deleting the local file. A genuine procedural difference → keep, and
   check it is documented as an override in `.claude/COMMANDS.md`.

4. **The profile.** Does `.claude/project-profile.md` exist and carry the
   sections the enabled plugins read (`${CLAUDE_PLUGIN_ROOT}/reference/
   project-profile.md`)? A missing section makes the library ask the same
   question every session. A copied fact (a list an API answers) is a second
   truth going stale.

5. **A rule on the wrong layer.** A paragraph of prose about something a linter
   rule expresses — move it down. A hook that needs contextual judgement — move
   it up into a skill.

6. **Dead artefacts.** Commands and skills nobody uses, hooks with steady false
   positives, links to files that no longer exist.

7. **Where the gate runs.** Is a git hook running the whole validate command —
   minutes per push, soon bypassed? The library's `commit` and `create-pr` run
   it. Does lint-staged run the formatter after the linter's fixes? The wrong
   order leaves linter edits unformatted while the hook passes, and the gate
   fails a commit later.

8. **Gaps.** Layers from the model that are absent. Absence is allowed — but it
   must be deliberate and written down, with the conditions that would fill it.

9. **Secret hygiene.** Are the generated MCP config and the environment file
   ignored? Did a token leak into a committed file, into history, or into
   `settings.json` permission entries?

10. **Cross-agent availability.** Do the rules live in `AGENTS.md` rather than
   only in a vendor file? Are the skill symlinks present and unbroken, and
   pointing the right way? Is every marketplace named in `enabledPlugins`
   declared in the project's own `extraKnownMarketplaces`? One known only to
   the author's user settings works on the author's machine and nowhere else.
   A declared marketplace in a private repository is still out of reach for a
   collaborator without read access: compare the project's collaborators
   (`gh api repos/<project>/collaborators --jq '.[].login'`) with the
   marketplace's, and report each one missing. Until they have it, deleting a
   local command that copies the library leaves them with no command at all.

11. **True in every clone.** Read the committed harness as a collaborator's
   clone sees it, not the author's. Remote names used to identify a repository
   (`origin is <owner>/…`, "never touch upstream" where upstream is someone's
   own repository), a fork's trunk written as the project's base branch,
   filesystem paths to sibling checkouts (`../web`) — each is true on one disk
   and false on the next. The fix is a slug in committed text and the clone's
   specifics in the gitignored `project-profile.local.md`.

12. **Rules that are not project-specific.** Rules in this project's
    `AGENTS.md` or skills that name no concrete path or id and would hold in any
    project — list them, one line each. Where they go is the owner's decision.

## Report

A table: finding → layer → severity → proposed action. Rules that are not
project-specific as a separate short list. Questions to the owner follow the
questionnaire rules of `mluk-repo`'s `kickoff` skill, a closing "anything to
add?" included. Apply changes after confirmation, one group at a time,
never all at once.

## Hard rules

- **Read-only by default.** Findings first, edits after approval.
- **Do not rewrite a working harness to match a template.** A deliberate
  deviation is a finding only if it is undocumented.
- **Deleting an artefact is proposed, never done silently** — a command that
  looks unused may be someone's weekly ritual.
- **Only the project's files are edited.** An installed plugin is never
  edited from here.
