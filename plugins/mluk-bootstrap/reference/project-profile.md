# The project profile

`.claude/project-profile.md` — what the library plugins read before doing
anything. Committed: it is a project decision, not a personal setting.

It is **sectioned**, and each plugin owns its sections. `mluk-bootstrap` writes
the whole file; a library plugin installed on its own creates or appends only
its own section and never rewrites someone else's. Exact keys and defaults for
`## Repository`, `## Docs`, `## Task`, `## Checks` and `## Review` are in
`mluk-repo`'s `reference/profile.md`; `## Frontend` is read by `mluk-fe`
(keys in its `reference/profile.md`); `## Copy` is read by `mluk-ru`.

```markdown
# Project profile

Read by every library plugin before it acts. This file outranks the defaults
those plugins ship; a key in the gitignored `project-profile.local.md` outranks
it for one clone, and what the developer says in the current session outranks
both.

## Repository
Platform and CLI (GitHub, gh). Remote account alias. Base branch. Branch chain.
Upstream policy. Validate command. Commit preset and confirm mode. Merge
method. PR language.

## Docs
Where documentation lives: the technical canvas here, product docs (possibly
in a sibling repository), the contract-gap log, the roadmap. Which document
changes for which kind of change.

## Task
Task flavours and the skill each loads (e.g. `ui → task-ui`, `api → task-api`).
Where a brief comes from when not inline.

## Checks
What `start` verifies live: dev server port (owner-run), containers, env file,
migrations, gh auth. One line each with the command and the fix.

## Review
Project-specific review lenses added to the library rubric — a security check
that matters here, a data-loss path, a contract that clients rely on.

## Sources of truth
Design source (DesignSync project id, Figma file), spec, product docs — as
durable links, with priority order and what to do on conflict.

## Languages
Committed text, user-facing strings, conversation.

## Frontend
For `mluk-fe`: where the translation catalogs live and in which shape
(`messages/<locale>.json`, flat or nested), the locales, the Next.js app root
(`src/app`), and which hooks are switched off here and why.

## Copy
For `mluk-ru`: canonical documents whose wording is the reference, the
glossary of fixed terms, language pairs that must move together, where the
copy journal lives (`docs/local/copy-journal.md` by default).
```

Three rules that keep it useful:

**True in every clone.** The file is read by whoever clones the repository —
a collaborator, a fork's owner, the canonical repository's owner — so it
describes the project as its canonical repository has it: that repository's
base branch and chain, sibling repositories by `owner/repo` slug, never by
`../path`. Remote names (`origin`, `upstream`) mean different repositories in
different clones and are not used to identify one. What holds only in one
clone — a fork's trunk and its upstream, a local port, `## Siblings` with the
paths of local checkouts — goes to `.claude/project-profile.local.md`,
gitignored, same headings, overriding single keys. The mechanics are in
`mluk-repo`'s `reference/profile.md`.

**Only decisions.** Anything a command answers in one call — the list of
branches, the installed packages — is fetched, not copied. A copy becomes a
second truth that goes stale in silence.

**Deviations carry their reason.** A project that departs from the library
default records why, so the next reader sees a decision rather than a mistake.
