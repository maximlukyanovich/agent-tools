# The review rubric

Read by `/mluk-repo:review` at its step 5 and by every `review-group` agent
it starts, which reads this file itself rather than getting it in its
prompt. The project's lenses from the profile's `## Review` carry the same
weight as these.

## General lenses

- `bug` — unhandled branches, `None` assumptions, boundary cases, a missing
  transaction. Empty is not unset: `0`, `""`, `[]` and a missing key each
  take their own branch. A repeat — a double click, a retried job or
  webhook — does not repeat a side effect. For async code and stateful
  hooks, walk the lifecycle transitions — A→B mid-event, A→none→A — and a
  peer that misbehaves, such as a 200 that closes at once. In UI, an element
  holding the focus that leaves the page outside a modal's focus scope with
  nowhere named for the focus to go, which the plan's state table names
  (`kickoff`): the browser drops it to `<body>` — a `nit`, `minor` only when
  a keyboard user loses their place in a flow under way.
- `perf` — N+1, a per-row query, a full scan on a hot path, a client-only
  fetch on an SEO surface.
- `dup` — a rule written inline next to the shared implementation.
- `test` — graded by `proof.md`, "In review": a risk-class break with no
  test, a removed or weakened guard, or a document claiming a test that does
  not assert the decision is `major`; the same gap in code the branch did
  not touch or claim is `minor` at most and goes to techdebt; a test of the
  look is a `nit` to remove.
- `shared` — a change to a shared function, hook or component that alters
  behaviour for an existing caller: walk every call site; an extension that
  is not backward-compatible and did not migrate its callers is `major`.
  Pairs that must agree — read and write, display and submit, list and
  detail, create, edit and copy, every entry point to one action: a changed
  rule is checked in each. A new path beside an old one does everything the
  old did besides its main effect — signals and hooks, a cache or derived
  state reset, implicit validation, hints and required marks in the UI; a
  write past the model (`update`, a bulk operation) is the usual case.
- `convention` — placement, style drift.
- `docs` — behaviour or contract changed, document did not; a type's doc
  comment contradicted by the code; a compromise as a `TODO` instead of a
  techdebt entry. New text — a log line, an error, UI copy — is true in
  every outcome: success, partial failure, timeout, the flag off.
- `security` — a secret in the diff, a token logged, an auth shortcut
  widened, an object lookup not scoped to the requesting user, user content
  interpolated without bound, a surface that changes data — a button, a list
  action, an endpoint — still usable by an account that may only read its
  page: each new one is walked as the least-privileged account that can
  open it.
- `contract` — a field renamed or retyped without a note in the contract log.
- `language` — a user-facing string in the wrong language.

## Across the lenses

- A finding names **every** place with the same mechanism, not only the
  first one found.
- UI in the diff is checked against the profile's `design source` (read
  only).
- A contract change — a field, an endpoint, a payload's shape or timing — is
  followed into each `consumers` repository's call sites (its clone from the
  local profile's `## Siblings`, read at its remote head by
  `reference/profile.md`); a consumer that now misreads it is a
  finding here.
