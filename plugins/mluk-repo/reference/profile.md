# The profile sections mluk-repo reads

`.claude/project-profile.md`, sections `## Repository`, `## Docs`, `## Task`,
`## Checks`, `## Review`, `## Sources of truth`, `## Languages`. Free-form
Markdown under each heading; the keys below are what the commands look for. A
missing key takes the default; a missing section makes the command ask once and
offer to write the answer down.

## Two files: the project and this clone

The committed profile holds what is true in **every clone** — the canonical
repository's base branch and chain, the validate command, the commit preset.
What holds only in one developer's clone goes to
`.claude/project-profile.local.md`, gitignored: a fork's own trunk and its
upstream, a local port, where the sibling repositories are checked out.

The local file has the same headings and overrides **single keys**; a key it
does not name keeps the committed value. Every command reads both before it
acts and treats the result as the profile. When a command reports a key that
came from the local file, it says so (`base: web-integration (local)`), so the
developer sees the override rather than a surprise. A command that offers to
write an answer down asks which file it belongs in: a decision for everyone →
the profile; a fact about this machine or this fork → the local file.

**Sibling repositories are named by slug, never by a filesystem path.** A
committed profile or document writes `owner/repo` plus the path inside it
(`maximlukyanovich/quest-bot-web` → `docs/product/`); `../web` is true only on
the author's disk. Where the clone lives on this machine is the local file's
`## Siblings` — one line per slug, `owner/repo: <path>`. A command that needs a
sibling's file and finds no line for it asks once for the path and offers to
record it; with no clone at all it reads the file through
`gh api repos/<owner>/<repo>/contents/<path>`.

The library hooks (`mluk-fe`) read only the committed file: what they check must
hold in every clone.

## Repository

| Key | Default | Read by |
| --- | --- | --- |
| `platform` | `github` with `gh` | all |
| `remote account` | `personal` (`git@github.com:`); `work` means `git@github-work:` | `create-pr`, `promote`, `start` |
| `base branch` | `develop` | all |
| `chain` | `feature/* → develop → main` | `promote`, `create-pr` |
| `protected` | `develop`, `main` (and `staging` if in the chain) — never pushed directly | `commit`, `create-pr`, `promote` |
| `upstream` | none; if named, never pushed to, never targeted by a PR | `promote`, `create-pr` |
| `validate` | asked (e.g. `pnpm validate`, `make test`) | `commit`, `create-pr`, `sync`, `review` |
| `targeted checks` | none — table of "changed only X → run Y or nothing" | `commit` |
| `commit preset` | `gitmoji-conventional` | `commit` |
| `commit confirm` | `ask` — stage and show the draft, commit on go-ahead; `auto` — the invocation is the authorisation | `commit` |
| `merge method` | `merge` (no squash, no rebase) | `create-pr`, `promote` |
| `delete branch` | `yes` for feature branches after merge, safe form only | `create-pr` |
| `pr language` | `en` | `create-pr`, `promote` |
| `post-merge checks` | none — commands to run after a `sync` (e.g. `makemigrations --check`) | `sync` |

## Docs

| Key | Default | Read by |
| --- | --- | --- |
| `technical` | `AGENTS.md`, `CLAUDE.md`, `docs/README.md` | `update-docs`, `start` |
| `product` | none — path, or `owner/repo` + path for a sibling, with its language | `update-docs`, `review`, `task` |
| `contract log` | none — where front↔back contract gaps are recorded; a sibling by slug | `update-docs`, `review` |
| `roadmap` | none — a sibling by slug when it lives there | `update-docs` |
| `techdebt` | none — where compromises are recorded instead of `TODO` comments | `update-docs`, `review` |
| `map` | table: change category → target document | `update-docs` |

## Task

| Key | Default | Read by |
| --- | --- | --- |
| `flavours` | none — `name → skill(s) to load` (e.g. `ui → task-ui`, `api → task-api`, `authoring → django-conventions`) | `task` |
| `brief sources` | inline, `docs/local/` note, GitHub issue | `task` |
| `branch prefix` | `feat|fix|refactor|chore|docs|perf/<kebab-slug>` off the base branch | `task` |
| `blast radius` | none — operations that must be named in every plan (e.g. anything that orphans live sessions) | `task` |

## Checks

A list, one per line: `label — command — fix when not ok`. `start` runs them
read-only and prints the table. Typical rows: dev server on its port (owner-run,
never started by the agent), containers up, `.env` present, migrations
applied, `gh auth status`, working tree clean. The validate command is shown as
`info` and not run.

## Review

Project lenses added to the library rubric, one per line with the anchor that
makes a finding `major`: a security path (an auth shortcut that must not
widen), a data-loss path (an operation that re-creates rows with new ids), a
contract clients rely on, a language rule for user-facing strings.

| Key | Default | Read by |
| --- | --- | --- |
| `ledger` | `docs/local/reviews/` — must be gitignored; one file per reviewed target | `review`, `create-pr` |
| `design source` | none — where the visual design lives (a design-system project, a kit path); read, never written | `review` |
| `consumers` | none — sibling repositories (by slug) that consume this one's contract | `review` |

## Sources of truth

Where the answer to a question lives, in priority order, and what to do when two
of them disagree (the default: show the owner the conflict, never pick one
silently). One line per source: the code and the schema it publishes, product
docs (by slug when in a sibling), the design source (a durable link or id),
third-party library docs (the docs tool before memory). `task` reads the design
source from here when the task has UI.

## Languages

| Key | Default | Read by |
| --- | --- | --- |
| `committed` | English — code, comments, commits, PRs, technical docs | `commit`, `create-pr`, `update-docs` |
| `user-facing` | none — the language of strings a user reads, and where they live | `review` |
| `conversation` | Russian | `start`, `task` |

## The command index

`.claude/COMMANDS.md` — not a profile section, a sibling file: the library
commands the project uses and every local override with its reason, one row
each. `start` prints it; its template is in `mluk-bootstrap`'s
`reference/templates.md`.
