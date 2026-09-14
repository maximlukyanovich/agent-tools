---
description: Review a Russian client-facing, legal or documentation text against the business-russian checklist and return ✗/✓ findings with a rewrite for each. Never rewrites silently.
argument-hint: '<file path | text> [legal]'
---

# /mluk-ru:review

Run a Russian text through the `business-russian` skill and report what to
change. **Read-only**: the findings are printed in chat; the file is edited
only when the owner asks, and then finding by finding.

## Arguments

- `<file path | text>` — a path to a file (Markdown, JSON with strings, a
  template) or the text itself, pasted inline.
- `legal` — also apply the legal-text addendum and the second checklist
  (offer, agreement, terms, refund policy, FAQ).

## Steps

1. **Read the profile's `## Copy`** — canonical documents, glossary, language
   pairs, journal path. No section → proceed with the skill alone and say so.

2. **Read the text.** For a JSON catalogue, review only the human-facing
   string values. For a file that is part of a document set (an offer, a
   refund policy), open the related documents the profile names — a finding
   about a term or a promise is checked against the set, not the file alone.

3. **Run the self-check first** — the two mistakes the agent repeats (a
   dropped subject, a tautology) — then the general checklist, then the legal
   checklist when `legal` is given.

4. **Report**, in document order, one finding per item:

   ```
   <where: heading / key / paragraph>
   ✗ <the current wording>
   ✓ <the proposed wording>
   — <the principle, by number, in one line>
   ```

   A term inconsistency lists every occurrence. A finding that needs a fact
   from the code (the name of a screen, what a user actually enters) says so
   and names the file to check rather than guessing. Nothing to change → say
   so in one line.

5. **Offer the next step**: apply the rewrites (finding by finding, on
   confirmation), and record the accepted ones in the project's copy journal.
   A new kind of complaint from the owner → propose adding the principle to
   the skill in the library.

## Hard rules

- Never rewrite silently; every change is a ✗/✓ pair the owner can decline.
- Never invent a term — the glossary and the canonical documents decide;
  where they are silent, ask.
- Names of screens and artefacts come from the interface or the code, not
  from intuition.
- The owner's own phrasing is intent, not a grammar reference: a proposed
  wording may improve on it, with a note.
