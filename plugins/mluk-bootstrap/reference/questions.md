# Phase 1: the questions

Rules: ask in batches through the questionnaire tool, never one per turn; every
question carries a default marked as the recommendation; never ask what the
inventory already answered. **If an answer changes no file, the question is
redundant.** The questionnaire rules themselves are in the `mluk-repo:kickoff`
skill, loaded before the first question.

**Rounds.** Four questions a round, the closing one included
(`mluk-repo:kickoff`). Q9 and Q10 are not asked, so eleven come down to nine:

1. Q1, Q2, Q3, and Q8 as the closing question;
2. Q4, Q5, Q6, Q7 — without UI there is no Q4, Q11 takes its place and there
   is no third round;
3. Q11 alone — the plugin set follows from the answers to Q4 and Q7.

A question the inventory answered fully drops out; the rest keep their order.

**Q1. The repository's role and current phase.** What the product is, in a
paragraph; who the repository's clients are; whether there are sibling
repositories (backend, legacy, design bundle); whether there is a phase in which
production code must not be written yet. *Never derivable — always ask.*

**Q2. Boundaries and architecture.** How the code is laid out, what may import
what, what is forbidden. Default for a new project: two layers — domain modules
plus a shared layer, each module's public API through a single entry file. If
boundaries are already visible in the tree, state them and ask for confirmation
rather than asking from scratch.

**Q3. What "verified" means.** Which command is the full gate (the profile's
`validate`), and which narrow commands check a change between edits and in a
commit — the linter on the changed files, the type-check, the tests related to
them (`targeted checks`, each tried once to see that it narrows). Whether a
manual step is required — a browser check through the Playwright tool against
the running dev server, a real request, a migration. Separately: which changes
need a test — the default is `mluk-repo`'s `reference/proof.md` (money, data
written or deleted, access, merges, what lets a confirmation through,
branching logic, a costly break where nobody looks), with a recorded live
check for the rest. How the dev server and the stack start goes to `AGENTS.md` §2 and
the fixes in `## Checks`, as commands. Who starts them — the developer or the
agent — is a habit of one machine, not a project rule: the answer goes to the
gitignored `project-profile.local.md` (`agent starts`), and without it the
agent starts and stops nothing.

**Q4. Source of design** — only if the repository has UI. A Claude Design
project (DesignSync, needs the project id), Figma, screenshots plus prose, or
none. Affects the design-fidelity skill, the profile's `## Sources of truth`,
and the MCP set.

**Q5. Git: remote, account, chain.** GitHub with `gh`. Which account alias the
remote uses (`git@github.com:` personal, `git@github-work:` work — the wrong one
shows up as "Repository not found" on push). Chain default `feature/* →
develop → main`; a `staging` stage by answer. Where a PR goes by default, what is
protected from direct pushes, whether an `upstream` exists that must never be
touched. All of it lands in the profile's `## Repository`.

**Q6. Commit convention.** Default `gitmoji-conventional` — `:gitmoji:
type(scope): Subject`, body one bullet per point. Alternative `topic-prose` —
`Topic: description` with a prose body and a closing `Tests:` line. Ask whether
there is machine enforcement (commitlint, husky) or only agreement, and whether
`commit` should stage with confirmation or treat the invocation as
authorisation. Both presets are described in the `mluk-repo:commit-conventions`
skill. *Always asked, even when the history follows one format: it shows a
habit, not whether that is a rule, and says nothing about how `commit` stages.
The format it follows becomes the recommended option.*

**Q7. Languages.** Three independent answers: the language of code,
identifiers, commits and PRs — English; the language of committed
documentation; the language the agent speaks in chat — Russian by default. And
separately, the language of strings the end user sees — the single most common
place a fresh session gets it wrong.

**Q8. What has already gone wrong.** Which mistakes the agent or the developer
made repeatedly here. Each answer is a candidate for a hook (if
machine-checkable) or a skill (if it needs understanding). Without this question
the hook set comes out speculative. *Asked as round 1's closing question — "What
has already gone wrong here, or anything else to add?" — with the options
"nothing yet, all covered" and "yes, I will describe it in chat".*

**Q9. External access.** Which MCP servers and CLIs exist or are needed: library
docs (Context7), design (DesignSync, Figma), browser (Playwright). Whether there
are tokens and where they live. *Not asked: the plan states the set derived
from the inventory, Q3 and Q4 as an assumption the owner can overturn.*

**Q10. Local notes.** Does the developer keep local material — plans, excerpts,
handoffs, a copy journal — and where should it live. Default `docs/local/`,
fully gitignored except its own README. *Not asked: the plan states
`docs/local/` as an assumption the owner can overturn.*

**Q11. Plugins, and where they are recorded.** The set follows from the
inventory and the answers — confirm it as a multi-select, do not ask from
scratch: `mluk-bootstrap` and `mluk-repo` always (already installed),
`mluk-fe` in a web front, `mluk-design` where there is a design kit,
`mluk-deploy` where the project deploys, `mluk-ops` where the agent works on a
server, `mluk-ru` where the project has Russian texts for people. The file:
`.claude/settings.json` by default, committed, so every clone gets the set;
`.claude/settings.local.json` when the project's rules keep AI settings out of
git. Which release of the library: follow `main` — every raised version
arrives through `autoUpdate`, the default for one developer — or pin the
latest release tag, so a team moves between releases by a reviewed settings
change.

There is no question about a tracker or time tracking. A task brief comes inline, from a `docs/local/` note, or from a GitHub
issue when one exists.
