---
name: commit-conventions
description: Commit message format for personal projects — two presets selected by the project profile, gitmoji-conventional (default) and topic-prose — the body rules (detailed, one line per bullet, why not what), and what is forbidden in any message. Use before proposing or composing any commit message, and when a commit-msg hook rejected one.
---

# commit-conventions

The profile's `commit preset` picks the format; the body rules and the
prohibitions hold for both. A repository with commitlint rejects a malformed
subject; one without accepts anything, which puts the whole burden on the
author — the history is consistent only because it was written carefully.

## Preset `gitmoji-conventional` (default)

Subject:

```
:gitmoji: type(scope): Subject
```

- **Gitmoji** in `:shortcode:` form (`:sparkles:`, `:bug:`, `:memo:`,
  `:recycle:`, `:lipstick:`, `:tada:`). Unicode emoji characters are rejected
  by commitlint.
- **Type** is a conventional-commits type: `feat`, `fix`, `refactor`, `docs`,
  `chore`, `test`, `style`, `perf`, `build`, `ci`, `revert`.
- **Scope** is lower-case, an area of the repository (`catalog`, `player`,
  `auth`, `ui`, `i18n`, `api`, `infra`).
- **Subject** is imperative mood, capitalised, no trailing period.
- No tracker id. A GitHub issue may be referenced at the end in parentheses
  when one exists — `(#42)` — and is omitted otherwise.

```
:sparkles: feat(player): Persist scene progress between sessions (#42)
:bug: fix(catalog): Restore image fallback for templates without art
:memo: docs(product): Record the cross-scene digest in AI generation
```

Body: blank line, then **`- ` bullets, one item per line**, grouped by area
when the change spans several (mock / contract / client / i18n / tests / docs).
A bullet that introduces facets ends with `:` and nests them as indented `- `
sub-bullets. The body says **why** and what changed semantically — the diff
already shows what.

## Preset `topic-prose`

Subject:

```
Topic: description
```

- **`Topic`** — the feature or domain area, capitalised: `Stories`, `Users`,
  `Story generation`. Not an app label, not a change type.
- **`description`** — lower case after the colon, no trailing period;
  imperative or a noun phrase naming the result.
- No gitmoji, no `feat:` / `fix:`, no issue ids, no scope in parentheses.

```
Stories: scope playthrough lookups to the requesting user
Users: add is_premium flag
Story generation: configurable default mode (live vs default_text)
```

Body: **explanatory prose in paragraphs**, separated by blank lines, each
paragraph on one line. A paragraph may open with a thematic lead-in ending in a
colon (`Editor:`, `Storage:`). It explains why, names incidental fixes, and
states rejected alternatives. Last line: `Tests: N cases covering …` when tests
were added or changed; when a change genuinely cannot be tested, say why
instead of omitting the line. Russian UI terms are quoted with guillemets.

## Rules for both presets

- **The header fits the limit, counted before committing.** Where commitlint
  runs, its `header-max-length` is the limit (`config-conventional` and
  `commitlint-config-gitmoji` both set 100); without one, aim under 100 anyway. The `:gitmoji:` shortcode counts as
  text — `:building_construction: ` alone takes 24 characters. Count the first
  line (`head -1 msg | wc -m`) instead of finding out from a rejected hook. A
  header that lists several changes is the usual offender: name the main one,
  the body carries the rest.
- **Every commit has a body.** A one-line subject with no body is a
  regression the owner has flagged. The body groups what changed by area and
  says why.
- **No hard wrap.** Each bullet or paragraph is one line; the tooling wraps.
- **One task, one commit.** A mixed diff is split into groups.
- **Documentation ships in the same commit** as the code that changes it.
- **English.**
- The message goes through a HEREDOC so the formatting survives shell quoting:

  ```sh
  git commit -m "$(cat <<'EOF'
  :sparkles: feat(scope): Subject

  - First bullet, on one line however long it is.
  - Second bullet.
  EOF
  )"
  ```

## Forbidden in any message

- `Co-Authored-By` trailers, "Generated with …", any agent or tool
  attribution. The harness default is suppressed with
  `attribution: { commit: "", pr: "" }` in `.claude/settings.json`; adding an
  equivalent by hand is the same violation.
- Person names.
- Links to chat, DMs or personal notes that are not in the repository.
- A language other than English.
- A subject that restates the diff (`update models.py`) instead of the change.
