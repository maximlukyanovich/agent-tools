---
description: Audit an existing agent harness against the layer model — drift, duplication, local commands that copy the library, a profile with missing sections, the efficiency journal, on a yes the test suite by risk — and report in priority order. Read-only until a change is approved.
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
   it looks like a source of truth without being one. Does `AGENTS.md` say
   how the project runs — install, dev server, the stack — as commands that
   work from the repository root? Missing, prose without commands, or a rule
   about who starts them (that habit belongs in the clone's
   `project-profile.local.md`) is a finding: `/mluk-repo:start` prints that
   section for a newcomer.

2. **Duplication.** The same rule in `AGENTS.md`, `CLAUDE.md`, a project skill
   and a library skill — collapse to one place plus links. The library is the
   source for anything that survives a change of project.

3. **Local commands that copy the library.** For every `.claude/commands/*.md`
   whose name matches a `mluk-repo` command (`commit`, `create-pr`, `promote`,
   `review`, `sync`, `start`, `next`, `task`, `update-docs`): does its procedure differ,
   or only its parameters? Parameters → propose moving them into the profile
   and deleting the local file. A genuine procedural difference → keep, and
   check it is documented as an override in `.claude/COMMANDS.md`. An index
   that lists library commands is a copy going stale — propose replacing the
   rows with a pointer to the plugins' `help`. The project's `/start` from
   the template is not such a copy; §14 checks it.

4. **The profile.** Does `.claude/project-profile.md` exist and carry the
   sections the enabled plugins read (`${CLAUDE_PLUGIN_ROOT}/reference/
   project-profile.md`)? A missing section makes the library ask the same
   question every session. A copied fact (a list an API answers) is a second
   truth going stale. A project skill that holds proof by risk or the state
   lists, while `## Task` has no `testing skill`, is a finding: propose the
   key, since `/mluk-repo:task` otherwise plans from `proof.md` alone.

5. **A rule on the wrong layer.** A paragraph of prose about something a linter
   rule expresses — move it down. A hook that needs contextual judgement — move
   it up into a skill.

6. **Dead artefacts.** Commands and skills nobody uses, hooks with steady false
   positives, links to files that no longer exist.

7. **Where the gate runs.** Is a git hook running the whole validate command —
   minutes per push, soon bypassed? The library runs the full gate once per
   tree, in the review and before the push, and the targeted checks between
   edits and in a commit: does every code path have a `targeted checks` row
   whose command narrows, and does a gate of several parts skip a part whose
   content is unchanged — and does every path a part excludes name its probe,
   by the checklist's "The gate is fast"
   (`${CLAUDE_PLUGIN_ROOT}/reference/checklist.md`)? Does lint-staged run the formatter after the linter's
   fixes? The wrong order leaves linter edits unformatted while the hook
   passes, and the gate fails a commit later. Does GitHub's
   `delete_branch_on_merge` agree with the profile's `delete branch` — on
   with `platform`, off otherwise (`yes` reads as `merge`) — and is no branch
   of the chain but the last exposed to it, neither protected nor the
   default? A mismatch or an exposed branch is a finding with a question to
   the owner, never an edit; the facts go into the report.

8. **Gaps.** Layers from the model that are absent. Absence is allowed — but it
   must be deliberate and written down, with the conditions that would fill it.

9. **Secret hygiene.** Are the generated MCP config and the environment file
   ignored? Did a token leak into a committed file, into history, or into
   `settings.json` permission entries?

10. **Cross-agent availability.** Do the rules live in `AGENTS.md` rather
   than only in a vendor file? Are the skill symlinks present and unbroken, and
   pointing the right way? Is every marketplace named in `enabledPlugins`
   declared in the project's own `extraKnownMarketplaces`,
   `claude-plugins-official` included? One known only to the author's user
   settings works on the author's machine and nowhere else. When
   `mluk-agent-tools`'s `source` pins a `ref`: does it name an existing tag,
   and is a newer one out — the first line of
   `git ls-remote --tags --refs --sort=-v:refname https://github.com/maximlukyanovich/agent-tools 'v*'`?
   A newer tag is reported with its release, never moved here — moving is the
   project's own reviewed change. And does `~/.claude/settings.json` declare
   `mluk-agent-tools` too? That declaration wins, so the pin does not hold on
   this machine — report it with the entry to delete. A source without `ref`
   follows `main`, and nothing is asked.
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

13. **A fresh clone installs.** Does `pnpm install --frozen-lockfile` pass in a
    fresh clone — not in the author's tree, where a warm `node_modules` hides a
    build script missing from `allowBuilds`? Under pnpm 11 that gap fails the
    deploy's install and nothing earlier.

14. **A fresh clone gets its plugins.** Is there a `.claude/commands/start.md`
    from `${CLAUDE_PLUGIN_ROOT}/templates/start/`? Without it a collaborator's
    clone has the plugins turned on and no command to install them. Does its
    version line match the template's — and, with Node, the one in
    `scripts/agent-plugins.mjs` and its `lib/`? Compare with `diff` against
    the template, not by reading both. Is it still thin — it installs and
    hands over to `/mluk-repo:start`, with no overview or checks copied in?
    Are the `## Checks` row, the `.claude/COMMANDS.md` row and the README's
    «Agent tooling» there? A version behind → propose copying the template
    again, with the project's placeholders kept.

15. **The efficiency journal.** Do `docs/local/efficiency-remarks.md` and its
    line in `AGENTS.md` §6 exist? Then read the rows not yet marked analysed
    and group them by cause:
    - a cause in this project — a rule, a skill, a hook, a profile key, a
      check that does not narrow — is a finding of this audit, with its edit;
    - a cause in a library plugin goes into **one** issue draft for that
      library's repository (its `plugin.json` `repository`), the whole
      audit's worth: the mechanism and the proposed change, with no project
      name, task key, path or quote — the library's issues are public. The
      draft is shown verbatim and filed with `gh issue create` only on an
      explicit yes. When the session's instructions name another route for
      library proposals, the draft goes there instead.

    The analysed rows get the audit's date in their last column.

16. **Tests by risk.** Asked as a step of its own, with its price — it reads
    every test and spends a second reviewer, so the question names the
    suite's size and an estimate. On a yes, against `mluk-repo`'s
    `reference/proof.md` ("Tests by risk", "An existing test"):
    - **Every test sorted** A — proves nothing; B — its break shows in the
      live check of a change; C — it breaks silently or somewhere else. A and
      B go on the removal list. A second, independent reviewer — a subagent
      that never receives the first pass's sorting — goes over that list
      with one question per test: would whoever makes the change see this
      break? Observed on a live project: the second pass found mistakes of
      the first.
    - **What a test costs to keep** — the git history of each test file
      (`git log --follow --oneline`): a test edited along with its code in
      most commits is the expensive one.
    - **What the suite costs to run** — a test class inheriting a working
      `TestCase` that reruns its parent's tests, a slow password hasher left
      on in tests. Observed: these alone took a backend suite from 84 s to
      39 s.
    - **Gaps** — code in a risk class with no test is the report's first
      level, the rest the second.
    - **A defect found** becomes its own task in the roadmap, not an edit
      inside the audit.
    - **A researcher's claim** — "these tests send paid requests" — is proven
      by a run (a spy, a counter) before it enters the plan. Observed: one
      such claim was refuted by a spy that counted zero requests.

## Report

A table: finding → layer → severity → proposed action. Rules that are not
project-specific as a separate short list. Before asking the owner, load the
`mluk-repo:kickoff` skill — its questionnaire rules apply, a closing "anything
to add?" included. Apply changes after confirmation, one group at a time,
never all at once.

End with the next step in a code block. Changes applied → the project's commit
command (`/mluk-repo:commit` or its local override), to run in this session —
it runs `/mluk-repo:handoff` after. Nothing applied → the first proposed
change, as a prompt that applies it.

## Hard rules

- **Read-only by default.** Findings first, edits after approval.
- **Do not rewrite a working harness to match a template.** A deliberate
  deviation is a finding only if it is undocumented.
- **Deleting an artefact is proposed, never done silently** — a command that
  looks unused may be someone's weekly ritual.
- **Only the project's files are edited.** An installed plugin is never
  edited from here.
