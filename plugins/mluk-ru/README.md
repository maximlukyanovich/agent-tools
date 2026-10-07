# mluk-ru

Business Russian: how client-facing, legal and documentation texts are
phrased. The rules were earned on live copy — an offer, a partner
agreement, refund terms, UI strings — and are written down so the same
complaint is not made twice.

## Commands

| Command | What it does |
| --- | --- |
| `/mluk-ru:review <file\|text> [legal]` | Runs the text through the checklist and returns ✗/✓ findings with a rewrite for each; never rewrites silently. |
| `/mluk-ru:help` | What this plugin checks, how the skill is kept, what the project profile adds. |

## Skill

`skills/business-russian` — loaded by itself whenever a Russian text for
people is being written or edited: the two mistakes the agent repeats, the
principles with ✗/✓ examples, the legal-text addendum, the checklists, and the
rule for keeping the set alive. The skill is in Russian; its subject is.

## Profile

`## Copy` in `.claude/project-profile.md`: the canonical documents whose
wording is the reference, the glossary of fixed terms, language pairs that must
move together, where the copy journal lives. The skill carries the method;
the project carries its terms.
