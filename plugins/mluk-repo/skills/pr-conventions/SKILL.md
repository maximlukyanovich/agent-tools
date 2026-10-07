---
name: pr-conventions
description: The shape of a pull request title and body in GitHub projects — plain conventional title without gitmoji, the body sections, the test plan as checkboxes, no hard wrap, English, and the habit of reading the last merged PRs first. Use when drafting, editing or reviewing a PR title or description.
---

# pr-conventions

A PR is read in the GitHub UI by the owner, later by whoever bisects history.
It is written for both.

## Before drafting

Read the last few merged PRs — they are the source of truth when this skill
and practice diverge:

```bash
gh pr list --state merged --limit 5 --json number,title,body
```

Match their tone and structure. A PR text drifts less than a command file.

## Title

- Plain text, one line, ≤ 70 characters, no markdown, no trailing period.
- **Conventional style without gitmoji** — `feat(story): Add the story detail
  page`, `fix(api): Keep body-less responses from failing a request`. Commits
  carry gitmoji; PR titles stay plain for the GitHub UI. In a `topic-prose`
  repository the title uses that repository's `Topic: description` form.
- An imperative summary when the change does not fit one type.

## Body

Omit any section that does not apply; never leave a placeholder.

```markdown
## Summary

One to three bullets on why the change exists and the user-visible outcome. No file paths here.

## Changes

Bullets grouped by area where it helps (**API**, **UI**, **Models**, **Docs**, **Tests**). Each bullet is a behavioural change, not a list of touched files; a key file is named inline only when it adds value.

## Migrations & deploy notes

Only when the diff has migrations, new dependencies, new runtime config keys, or anything requiring action on deploy — name what has to happen in which order.

## Test plan

- [x] `pnpm validate` green (typecheck, lint, format, tests)
- [x] Verified in the browser: <which flows, light/dark, narrow/wide>
- [ ] <what the reviewer still has to check>

## Risks / follow-ups

Only when there are real ones — data-loss paths, feature flags, deferred items, a techdebt entry.
```

- **The test plan is a checkbox list** (`- [x]` done, `- [ ]` pending), never
  plain bullets — the owner ticks it in the UI.
- **No hard wrap.** Each bullet and paragraph is one line; GitHub wraps.
- For a `develop → main` promotion the body aggregates what accumulated since
  the last promotion instead of restating every commit.

## Tone

English, neutral, technical. Past tense or present perfect for what changed,
imperative for the title. No filler ("This PR adds…"). Write what changed
semantically, not the diff line by line.

## Forbidden

`Co-Authored-By`, agent attribution, person names, links to chat or personal
notes, a tracker id that does not exist. A GitHub issue is referenced only
when one exists (`Closes #42`).
