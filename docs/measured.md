# Measured

Figures from live projects, which stay unnamed, taken from session
transcripts. Each section names its date and conditions; a new measurement is
added as its own section, or a dated line, rather than by rewriting an old one.

## Review against the built-in `/code-review`

`/mluk-repo:review` against the built-in `/code-review` at `high` (Claude Code
2.1.319): 14 branches of two projects, about 40 passes, recounted on
2026-11-08.

- **Full pass.** On one project's 8 branches, the built-in review found no
  `major` that `review` missed, and `review` found 7 that it missed. On the
  other's 6 branches it was 3 to 3; two of the built-in's three were failing
  end-to-end tests that a truncated gate output hid — the gate now reads red
  output whole.
- **False findings.** `review` raised one in about 40 passes, dropped before
  the report; the built-in, 9 on one project and one or two per pass in half
  of the other's.
- **Delta pass — the weak side.** `review` reads the fix round's delta and
  checks that each fix closed its finding; the built-in re-reads the whole
  branch each time, older code included. Over 6 repeat passes on fix deltas,
  `review` found nothing of its own and the built-in found 37, two of them
  `major` consequences of fixes that `review` had called ready. The rubric now
  reads every diff by three angles, one of them what a removed line held.
  2026-11-09: the passes changed on 2026-11-08, after these six; the delta
  pass has not been measured again.
- **Cost.** A full pass of `review` costs about three built-in runs — its
  price includes the gate, the refutation and the ledger; per confirmed
  finding the two are about even.

## The workflow

Who it is for: a developer alone on a project, whose work with the agent comes
down to choosing and approving the next prompt. The commands carry the rest,
and each one ends by printing the next.

- **Sessions.** On a solo project, 86 % of 149 sessions over 36 merged tasks
  started with a command or a block the agent had printed (since 2026-10-01).
- **Fixes in a fresh session.** A fix round run in the session of two reviews
  spent about three quarters of its price re-reading their context; a fresh
  session started by `handoff` does not carry it.
