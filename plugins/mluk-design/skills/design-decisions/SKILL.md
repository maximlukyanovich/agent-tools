---
name: design-decisions
description: How new design is drawn on a canvas for the owner's decision — an inventory of the kit and the app first, a primitives page for a new module, component variants beside whole concepts, one element per numbered question, every frame looked at before publishing, and the owner's answers turned into redraws. Use before drawing a frame or variant on a Design canvas, before publishing one, and when the owner answers design questions. Porting a decided design is design-port.
license: MIT
metadata:
  author: Maxim Lukyanovich
  source: https://github.com/maximlukyanovich/agent-tools
---

# Design decisions on a canvas

A round of variants is how new design reaches the owner's decision. The
canvases and the kit are those the profile's `## Sources of truth` names;
the project names its question prefix and the alphabet of its letters
there too. How a decided design reaches the code is `design-port`. Each
step below was missed on a live project and cost the owner a round.

## Before the first frame

1. **Inventory first.** List what the kit already has for every element the
   screens need — its stylesheet and its component code — and what the app
   has in its shared components and modules. Menus, fields, tags, switches,
   checks, confirms, search, accordions come from there, as they are or with
   a modifier. Only what neither has gets a new class under the kit's
   prefix, marked as a kit candidate.
2. **A new module starts with a primitives page.** Every element its screens
   need, with variants taken from the kit and from the app's code, then new
   ones styled after them. The owner approves the primitives; the screens
   are drawn on them.
3. **One implementation per component.** When the kit and the code render
   the same element differently, that is not a choice between A and B: show
   one component with the divergence and propose the unified one, its looks
   as variants of it (tone, background, size). Variants that differ barely
   to the eye are not a choice either; field backgrounds follow one rule
   across a screen.

## Drawing a round

4. **Component variants beside whole concepts, in the first round.** Every
   page with concepts gets its details set: each element the concepts are
   built from — on a new screen and in every kit block the screen touches —
   as its own question, variants as columns, states as rows. Every
   interactive element says what a press opens. The owner then combines a
   concept with any component variant; without the set they can only take a
   concept whole.
5. **A behaviour variant is drawn inside the screen where it happens.** A
   question about what happens — a dialog after a button, a limit reached, a
   banner over the content — is a whole screen in its real context: the
   screen already on a canvas, in the changed state, not cells of fragments
   on a page of their own. Several frames of one question go in the order of
   the action (view → press → result), and the sticky names the order.
   Buttons and labels come from the existing screens, never a new one beside
   them. Cells stay for the details set of step 4.
6. **One question, one element.** A question number is one element or one
   case, its letters the alternatives for it: two things to decide (an
   item's details and a reply form) are two numbers, never A for one and B
   for the other — list them before the round. One group per question,
   titled "<number> · question"; its frames "<number> · A · what is shown ·
   device", a context frame "<number> · what is shown"; one sticky with what
   to decide and the recommendation at the end of the group's first row. No
   step numbers, no labels of your own; a frame of no question has a plain
   title. The next free number is on the canvas's contents page.

## Before publishing

7. **Look at every changed frame** after its last edit: render it from the
   canvas's own frame parameters, never from a list of your own, and look at
   the picture. A kit class out of its context — a flex rule in a column, an
   absolute menu — breaks a frame whose code looks right.
8. **Check the copy.** Text written for a frame is text for people: it
   passes `mluk-ru:business-russian` (or the project's language skill)
   before publishing, as text in code does.
9. **Check the set.** Each new or touched element of each concept page has
   its row of variants (step 4); each question frame's title starts with its
   number and a letter (step 6); each new class is checked against the
   kit's list (step 1) and its name by the stylesheet search in "Writing
   to the kit" (`design-port`); each question group has its sticky in the
   canvas's index — a note id outside the canvas's format is dropped
   without an error, by `${CLAUDE_PLUGIN_ROOT}/reference/artifact-sandbox.md`.

## Answering the owner

10. **The table to approve is grouped by canvas page** — a heading per page
    with its link, the question rows under it — so the owner knows where
    each frame is.
11. **An answer with a change is not a decision.** Sort every item into
    decided as is, decided with a text change, and needs a redraw. Text
    changes go into the frames at once; each redraw gets new variants — with
    component variants — published in the same turn, and stays an open
    question. Never report that nothing is open while a redraw remains.
12. **A decided question leaves the page on review**: the chosen variant
    goes into the kit by "Writing to the kit" in `design-port`, into its
    module's page and a row into the archive by "The source" there; a
    page whose questions are all decided is deleted.

## How not to do it

- Publishing a page of concepts without its details set.
- Drawing a behaviour question as fragment cells instead of the screen.
- Two things to decide under one number, or a numbering of your own.
- Redrawing a menu, a field or a switch the kit already has.
- Publishing a frame that was not looked at after its last edit.

## How it is verified

Every published concept page has its details set, every question group its
title, letters and sticky in the canvas's index, every changed frame was
looked at after its last edit, and the owner's table lists the open
questions by page.
