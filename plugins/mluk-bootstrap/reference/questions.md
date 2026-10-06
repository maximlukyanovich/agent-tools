# Phase 1: the questions

Rules: ask in batches through the questionnaire tool, never one per turn; every
question carries a default marked as the recommendation; never ask what the
inventory already answered. **If an answer changes no file, the question is
redundant.** The questionnaire rules themselves are in the `kickoff` skill of `mluk-repo`.

**Q1. The repository's role and current phase.** What the product is, in a
paragraph; who the repository's clients are; whether there are sibling
repositories (backend, legacy, design bundle); whether there is a phase in which
production code must not be written yet. *Never derivable — always ask.*

**Q2. Boundaries and architecture.** How the code is laid out, what may import
what, what is forbidden. Default for a new project: two layers — domain modules
plus a shared layer, each module's public API through a single entry file. If
boundaries are already visible in the tree, state them and ask for confirmation
rather than asking from scratch.

**Q3. What "verified" means.** Which command must be green before a commit (the
profile's `validate`), and whether a manual step is required — a browser check
through the Playwright tool against the owner's dev server, a real request, a
migration. Separately: does every behaviour change ship with a test, or is that
incidental? Who runs the dev server and the containers — by default the owner,
and the agent never starts or stops them.

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
authorisation. Both presets are described in the `commit-conventions` skill of
`mluk-repo`.

**Q7. Languages.** Three independent answers: the language of code,
identifiers, commits and PRs — English; the language of committed
documentation; the language the agent speaks in chat — Russian by default. And
separately, the language of strings the end user sees — the single most common
place a fresh session gets it wrong.

**Q8. What has already gone wrong.** Which mistakes the agent or the developer
made repeatedly here. Each answer is a candidate for a hook (if
machine-checkable) or a skill (if it needs understanding). Without this question
the hook set comes out speculative.

**Q9. External access.** Which MCP servers and CLIs exist or are needed: library
docs (Context7), design (DesignSync, Figma), browser (Playwright). Whether there
are tokens and where they live.

**Q10. Local notes.** Does the developer keep local material — plans, excerpts,
handoffs, a copy journal — and where should it live. Default `docs/local/`,
fully gitignored except its own README.

There is no question about a tracker or time tracking. A task brief comes inline, from a `docs/local/` note, or from a GitHub
issue when one exists.
