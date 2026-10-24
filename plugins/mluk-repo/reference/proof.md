# What proves a change

Read by `kickoff` (step 7), `fix` and `review` (the `test` lens), so the rule
is written once.

## Tests by risk

A test is the proof where a mistake is costly and quiet. A change in a risk
class ships with its test in the same commit, and the test fails without the
change:

- money — a price, a charge, a refund, a balance;
- data written or deleted, and what decides which rows;
- permissions and access — who may see or change what;
- a merge of records or accounts;
- what lets a confirmation through, or blocks it;
- logic that branches on its input — a parser, a rule, a validator.

Any other behaviour — the focus, an announcement, the look, a transition
between screens — is checked live (a browser, a request), and the check is
recorded in the commit body or the report; or one end-to-end story covers it.
It needs no test of its own per transition. A risk-class change that
genuinely cannot be tested says why in the commit body.

## A test that must go red on the old code

A test that may pass by coincidence — it leans on the focus, timing, a fake or
a mock, an async step — is run once against the code it replaces and must go
red there: a test that also passes on the old code proves nothing. A plain
input → output test needs no such run. It is one run per such test, not a
batch over every finding.

## One read of the diff before the commit

The defects a change brings come from what else it does, not from the case it
was made for, and no revert finds them. So before the commit the slice's or
the round's own diff is read once, with one question: what else does each
change do — in which states, for which users of the element (mouse, keyboard,
screen reader, another order of events)? A precedent is copied whole, not one
attribute of it.

- A doubt in the reasoning — "if…", "probably…", "fine anyway" — becomes a
  row of the state table, a check or a line in the report; it is never
  dropped.
- A changed sentence is reread whole. A changed rule, name or fact is
  searched for by its key terms across the docs, the harness and the tests —
  root-level test files included — and every copy changes in the same commit.
