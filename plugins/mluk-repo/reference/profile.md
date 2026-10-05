# The profile sections mluk-repo reads

`.claude/project-profile.md`, sections `## Repository`, `## Docs`, `## Task`,
`## Checks`, `## Review`. Free-form Markdown under each heading; the keys below
are what the commands look for. A missing key takes the default; a missing
section makes the command ask once and offer to write the answer down.

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
| `product` | none — path, possibly in a sibling repo, with its language | `update-docs`, `review` |
| `contract log` | none — where front↔back contract gaps are recorded | `update-docs`, `review` |
| `roadmap` | none | `update-docs` |
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
| `consumers` | none — sibling repositories that consume this one's contract | `review` |
