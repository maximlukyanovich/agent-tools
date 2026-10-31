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
(`acme/web` → `docs/product/`); `../web` is true only on
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
| `base branch` | the branch after `feature/*` in `chain` | all |
| `chain` | asked once; the chain the project's documents already name is offered first as recommended, else `feature/* → develop → main`; the answer is written down | `promote`, `create-pr`, `next` |
| `protected` | every branch of `chain` after `feature/*` — never pushed directly | `commit`, `create-pr`, `promote` |
| `upstream` | none; if named, never pushed to, never targeted by a PR | `promote`, `create-pr`, `next` |
| `validate` | asked (e.g. `pnpm validate`, `make test`) | `commit`, `create-pr`, `sync`, `review` |
| `targeted checks` | none — table "path class → command"; a step runs the rows of the paths it changed, and a path no row covers runs `validate` | `commit`, `fix`, `sync` |
| `commit preset` | `gitmoji-conventional` | `commit` |
| `commit confirm` | `ask` — stage and show the draft, commit on go-ahead; `auto` — the invocation is the authorisation | `commit` |
| `worktree folder` | `../<repo>-<slug>` — beside the repository, so the main tree's linters, tests and type-check never pick it up | `task` |
| `amend unpushed` | `yes` — a fix goes into the unpushed commit it corrects, by `git-safety` "Amending"; `no` — every fix and every review round is a new commit | `commit`, `fix` |
| `merge method` | `merge` (no squash, no rebase) | `create-pr`, `promote` |
| `delete branch` | `merge` — who deletes the remote feature branch after a merge: `ask` — the command asks; `merge` — the merge does (`yes` is its older spelling); `platform` — GitHub's automatic deletion. The local branch goes on confirmation, safe form only | `create-pr` |
| `pr language` | `en` | `create-pr`, `promote` |
| `post-merge checks` | none — commands to run after a `sync` (e.g. `makemigrations --check`) | `sync` |

How the two gate keys work together is `reference/commands.md`, "The gate".
A `targeted checks` command really narrows: the linter and the formatter on
`<files>` (the row's changed paths), the type-check, the tests related to
`<files>` (`vitest related <files> --run`, one app's tests with `--keepdb`).
A filter that silently runs the whole suite is not one — run it once before
writing it down. Shared configuration — the lockfile, the linter's,
type-checker's or test runner's config, the test setup — gets no row: a
change there reaches every file, so it runs `validate`.

## Docs

| Key | Default | Read by |
| --- | --- | --- |
| `technical` | `AGENTS.md`, `CLAUDE.md`, `docs/README.md` | `update-docs`, `start` |
| `product` | none — path, or `owner/repo` + path for a sibling, with its language | `update-docs`, `review`, `task` |
| `contract log` | none — where front↔back contract gaps are recorded; a sibling by slug | `update-docs`, `review` |
| `roadmap` | none — a sibling by slug when it lives there | `update-docs`, `next` |
| `techdebt` | none — where compromises are recorded instead of `TODO` comments | `update-docs`, `review`, `next` |
| `map` | table: change category → target document | `update-docs` |

## Task

| Key | Default | Read by |
| --- | --- | --- |
| `flavours` | none — `name → skill(s) to load` (e.g. `ui → task-ui`, `api → task-api`, `authoring → django-conventions`) | `task` |
| `brief sources` | inline, `docs/local/` note, GitHub issue | `task`, `next` |
| `branch prefix` | `feat|fix|refactor|chore|docs|perf/<kebab-slug>` off the base branch | `task` |
| `blast radius` | none — operations that must be named in every plan (e.g. anything that orphans live sessions) | `task` |
| `testing skill` | none — the project's skill that holds proof by risk and the state lists; `task` loads it before the plan, and without it `reference/proof.md` | `task` |

## Checks

A list, one per line: `label — command — fix when not ok`. `start` runs them
read-only and prints the table. Typical rows: the agent plugins installed
(the report the project's `/start` runs), dev server on its port, containers
up, `.env` present, migrations applied, `gh auth status`, working tree clean.
The validate command is shown as `info` and not run. A fix says how, as a
command — not who runs it.

Who may start and stop the dev server or the stack is a habit of one machine,
so it lives only in the local file:

| Key | Default | Read by |
| --- | --- | --- |
| `agent starts` | none — the agent starts and stops nothing and names the fix for the developer; else the list it may run itself (`dev server`, `stack`) | any step that needs one running — a browser check, tests inside the stack |

`start` starts nothing either way.

## Review

Project lenses added to the library rubric, one per line with the anchor that
makes a finding `major`: a security path (an auth shortcut that must not
widen), a data-loss path (an operation that re-creates rows with new ids), a
contract clients rely on, a language rule for user-facing strings.

| Key | Default | Read by |
| --- | --- | --- |
| `ledger` | `docs/local/reviews/` — must be gitignored; one file per reviewed target | `review`, `create-pr` |
| `design source` | none — where the visual design lives (a Design System artifact URL, a kit path); read, never written | `review` |
| `consumers` | none — sibling repositories (by slug) that consume this one's contract | `review` |

## Sources of truth

Where the answer to a question lives, in priority order, and what to do when two
of them disagree (the default: show the owner the conflict, never pick one
silently). One line per source: the code and the schema it publishes, product
docs (by slug when in a sibling), the design source (a durable link or id),
the design's per-screen statuses when the project keeps them (a durable link
and which page or status means ready), third-party library docs (the docs tool
before memory). `task` reads the design source and the statuses from here when
the task has UI.

## Languages

| Key | Default | Read by |
| --- | --- | --- |
| `committed` | English — code, comments, commits, PRs, technical docs | `commit`, `create-pr`, `update-docs` |
| `user-facing` | none — the language of strings a user reads, and where they live | `review` |
| `conversation` | Russian | `start`, `task` |

## The command index

`.claude/COMMANDS.md` — not a profile section, a sibling file: the project's
own commands and every override of a library command with its reason, one row
each. It does not copy the library's commands — each plugin's `help` lists
them. `start` prints it; its template is in `mluk-bootstrap`'s
`reference/templates.md`.
