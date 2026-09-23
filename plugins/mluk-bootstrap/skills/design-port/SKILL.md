---
name: design-port
description: How a design kit (a component library with markup + CSS, e.g. a Claude Design project) is ported into a codebase — reading the source at write time, wearing kit classes on a third-party primitive whose DOM already matches, the stretched-link recipe for cards that hold buttons, real data versus demo data, and what to do when the kit itself is wrong. Use when building or changing UI against a kit. Not for projects without a design source.
---

# Porting a design kit

The kit is the source of truth for the **look**: classes, tokens, markup, states,
copy. The codebase is the source of truth for the **engineering**: rendering
model, data, i18n, accessibility, performance. A port matches the first exactly
and never copies the second from a demo.

## How to do it

1. **Read the source at write time, not from memory.** The stylesheet AND the
   component code of the thing being ported, every time — a plan written from an
   earlier read goes stale the moment the owner touches the kit. When the kit
   arrives through a tool that returns files one by one, keep local copies in the
   project's gitignored notes folder, named so the linter skips them; a scratch
   directory does not survive a pause.

2. **A third-party primitive whose DOM already matches the kit wears the kit's
   classes.** Toasts, dialogs, menus from a library often render the same
   structure the kit draws. Then the library keeps what it is good at — stacking,
   timers, gestures, focus, a11y — and is switched to its unstyled mode with its
   per-part class hooks mapped onto the kit's class names; the kit's CSS goes in
   verbatim. Do not build a second component next to the library one. Two
   consequences: the library's own runtime-injected CSS loads after the
   project's, so overrides need the extra specificity of a class plus the
   library's data attribute; and a library that animates through a transform
   variable cannot take a kit keyframe on the same element — express the kit's
   entrance through the library's own enter transition.

3. **A card that is a link and holds buttons is a `div`, not an `<a>`.** Nested
   interactive content is invalid and unreachable for the keyboard. Recipe: the
   card is a positioned container with the visual styles; the link is a
   transparent hit layer over the whole card with the card's title as its
   accessible name; the content sits above the layer; the blocks that need
   hover or scrolling take pointer events themselves and hand a plain click to
   the link programmatically; buttons and toggles are ordinary siblings above
   everything. Focus ring on the container via `:has(a:focus-visible)`; tab order
   link → secondary controls → primary action.

4. **Demo data is not real data.** Kit demos carry one-sentence blurbs, six
   items, always-present images. Before shipping, feed the port the longest
   title, the emptiest record and the real count, and add the clamp, the
   fallback or the wrap the kit never needed. Mark every such addition in the
   stylesheet as web-only, next to the rule it protects.

5. **When the kit is wrong, say so — do not reproduce it silently.** A
   specificity slip, a measurement taken from the wrong ancestor, a token that
   exists in the kit's tokens file but not in the project: fix the effect in the
   port with a comment naming the kit's flaw, tell the owner, and propose the fix
   for the kit in the same session. A visible deviation from the design still
   needs the owner's explicit agreement — one place, one decision, no precedent.

6. **Verify against the design, not against the code compiling.** Open the
   page, measure what the kit specifies (sizes, offsets, colours, states, both
   themes, the narrow viewport, reduced motion) and compare numbers, then look at
   the screenshot. A dev server may not pick up a newly created stylesheet added
   through an import — when the styles are demonstrably absent from the served
   bundle, ask the owner to restart it before debugging the CSS.

## How not to do it

- Approximating "by eye" or from a summary of the kit.
- Wrapping a library component in a hand-rolled copy of its DOM to reach the
  kit's classes.
- Putting a `<button>` inside the card's `<a>` "with stopPropagation".
- Shipping the demo's assumptions (short copy, images everywhere) as layout
  facts.
- Treating an agreed deviation in one spot as licence to deviate elsewhere.

## How it is verified

Every kit value the port depends on can be pointed to in the kit source that was
read in the same session. The rendered page measures to those values in both
themes and at a phone width. Web-only additions are marked in the stylesheet.
Kit flaws found on the way are listed for the owner, with the fix proposed for
the kit.
