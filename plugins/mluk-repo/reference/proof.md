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
- logic that branches on its input — a parser, a rule, a validator;
- what breaks where nobody looks:
  - the request a page assembles — a field's name, a hidden fingerprint, the
    form a checkbox or a button belongs to, a `formaction`;
  - what lets a key, a tap or a submit reach an action — above all one that
    deletes or charges;
  - a contract of shared code other screens lean on — a lock taken and
    released, a queue that moves, a global flag reset, a fallback that never
    leaves the user stuck;
  - a path the local check cannot reach — the exchange with a provider, a
    slow or failing network, a first visit, reduced motion, touch.

  The whole class holds on one condition, on any screen: the break costs
  data, access, a merge or a payment, or leaves the user stuck. A break of
  the look alone is outside it.

Any other behaviour — the focus, an announcement, the look, a transition
between screens — is checked live (a browser, a request), and the check is
recorded in the commit body or the report; or one end-to-end story covers it.
It needs no test of its own per transition. A risk-class change that
genuinely cannot be tested says why in the commit body.

A test that holds a convention of the project's code — the module graph, the
language of messages, the number of queries as the data grows — is a
deterministic check, like a lint rule: this rule neither asks for it nor
removes it, and it lives as long as the convention does.

## What a test asserts

The decision: the request sent, the handler called, the code or the status
returned, a guarding attribute (`inert`, `form=`). Not a class, the layout or
a text, and not what a mock was told to return. Markup that assembles the
next request is a decision, not the look.

## An existing test

An audit of the tests removes a test that proves nothing, and one whose break
the live check of the change itself would show — a break of the look alone
among them. A test of a break that happens silently, or somewhere else, stays,
even where a new change would not have required it.

## In review

The `test` lens of `review` grades by this file:

- **`major`** — no test where this file asks for one: a risk-class change
  without its test in the same commit, unless it genuinely cannot be tested
  and the commit says why; a deleted or weakened test that guarded such a
  break; a document or a comment that calls a behaviour tested when its test
  does not assert the decision. An item of the last class whose break meets
  none of its condition is not a finding.
- **`minor` at most** — the same gap in code the branch did not change or
  delete and made no claim about; its place is the techdebt file.
- **Any other behaviour change** — a recorded live check needs no test, and a
  missing one is a `nit` at most; with neither a test nor a recorded check it
  is a `minor`.
- **`nit`, "remove"** — a test that asserts the look: a class, the layout, a
  text.
- **A finding** — a test that passes by coincidence, or may, and was never run
  against the code it replaces (below).

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
