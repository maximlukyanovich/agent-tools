---
name: design-port
description: How a design kit (a component library with markup + CSS, e.g. a Design System artifact) is ported into a codebase — reading the source at write time, wearing kit classes on a third-party primitive whose DOM already matches, the stretched-link recipe for cards that hold buttons, real data versus demo data, what to do when the kit itself is wrong, and writing a new element to the kit before the code. Use when building or changing UI against a kit. Not for projects without a design source.
license: MIT
metadata:
  author: Maxim Lukyanovich
  source: https://github.com/maximlukyanovich/agent-tools
---

# Porting a design kit

The kit is the source of truth for the **look**: classes, tokens, markup, states,
copy. The codebase is the source of truth for the **engineering**: rendering
model, data, i18n, accessibility, performance. A port matches the first exactly
and never copies the second from a demo.

## The source

- **The design system is the only source** — tokens, components with live
  cards, the prototype built into its bundle. A Design canvas over it holds a
  copy, refreshed after the system changes; a port reads the system. The
  one exception is the project's list of components its code does better
  ("Code ahead of the kit" below).
- **Canvas pages go by status, not by date.** A module's page holds only the
  canon, and only it is ported; a page on review holds open questions with
  variants side by side and a recommendation; an archive keeps what was
  decided.
- **A decision has one number everywhere** — the canvas, its index, the
  decisions log. A port that follows one names it in a comment.

## How to do it

1. **Read the source at write time, not from memory.** The stylesheet AND the
   component code of the thing being ported, every time — a plan written from an
   earlier read goes stale the moment the owner touches the kit. An artifact's
   files are read with the Artifact tool (`read` with `path` or `paths`); keep
   local copies in the project's gitignored notes folder (`out_dir`), named
   so the linter skips them; a scratch directory does not survive a pause.

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

5. **Tell devices apart by how they are used, not by how wide they are.**
   Whatever depends on an input method — keyboard-shortcut hints, hover-only
   reveals, drag handles — is gated by the input media features (`hover`,
   `pointer`, `any-hover`, `any-pointer`), not by the viewport width: a narrow
   window can have a keyboard and a mouse, a wide tablet may have neither.
   Width decides layout; input decides affordances. Something that merely
   doubles as a shortcut but carries meaning of its own (a numbered list, an
   ordinal) is content and stays on every device.

6. **When the kit is wrong, say so — do not reproduce it silently.** A
   specificity slip, a measurement taken from the wrong ancestor, a token that
   exists in the kit's tokens file but not in the project: fix the effect in the
   port with a comment naming the kit's flaw, tell the owner, and propose the fix
   for the kit in the same session. A visible deviation from the design still
   needs the owner's explicit agreement — one place, one decision, no precedent.
   The kit's side of it is "Writing to the kit" below.

7. **Verify against the design, not against the code compiling.** Open the
   page, measure what the kit specifies (sizes, offsets, colours, states, both
   themes, the narrow viewport, reduced motion) and compare numbers, then look at
   the screenshot. Before the first number, check that
   `window.devicePixelRatio` is 1: the browser keeps a zoom level per host,
   and every size read at another scale is off by its factor. Not 1 → open
   the same server under another host (`127.0.0.1` for `localhost`) and
   measure nothing fractional until it reads 1. Observed on a live project:
   `localhost` opened at 80%, borders measured 1.25 px, and device-metrics
   emulation did not reset the zoom. A dev server may not pick up a newly created stylesheet added
   through an import, or an edit to the global stylesheet — when the served rule
   demonstrably differs from the file, ask the owner to restart it before
   debugging the CSS.

8. **Compose kit classes from whole strings.** A modifier glued to its base in a
   template literal with a leading space (`` `base${on ? ' base--mod' : ''}` ``)
   does not survive `prettier-plugin-tailwindcss`: it trims the space on every
   format, the two classes fuse into one unknown name, and a fix made by hand
   comes undone at the next format. Pick from complete strings
   (`on ? 'base base--mod' : 'base'`) or join through the project's `cn()` /
   `clsx`.

9. **The kit's look lands in the project's primitives, not at call sites.**
   A kit element that looks unlike its primitive is fixed in the primitive's
   variant, by `mluk-fe:component-discipline`, rule 5. Icons follow the
   project's dictionary by meaning (rule 11 there) on the canvas too — the
   kit or the frame generator uses the same names, so design and code do not
   drift.

## Writing to the kit

When the session can write to the design source, apply an agreed change
there yourself instead of only describing it — the owner approves the exact
list of files and values first. Before writing to an artifact, read
`${CLAUDE_PLUGIN_ROOT}/reference/artifact-sandbox.md`.

- **What goes this way:** a fix, a decided deviation, an accepted proposal
  folded into the canon, a decisions note — and a new element.
- **An element neither the kit nor a canvas has goes into the kit first** —
  its styles, its component's README, its preview — in one write, then into
  the code verbatim; never assembled from utilities in the code with the
  kit "later". The owner decides its look: for each new element ask whether
  to draw variants (`design-decisions`) or write it to the kit at once, the
  recommendation marked — at once for one whose look follows from the kit's
  tokens and neighbours. "At once" skips the round, not the kit. The
  exception is a one-off web addition with no component (a page
  transition): the web stylesheet, marked web-only, with a proposal for the
  kit.
- **A new class name only after a search of the kit's stylesheet** for the
  exact name and its prefix, modifiers included: a taken name gets another
  (`.status-row` when `.status` exists). After the write, check live both
  the new page and the components where the name already appeared. Observed
  on a live project: a new rule reused a badge's class name and overrode it
  across the published kit.
- **Code ahead of the kit, or behind it.** A project may keep a list of
  components its code does better than the kit — one entry per owner's
  word. Those come from the code; the rest are ported from the kit as is,
  and the agent proposes moving the improvement into the kit. A kit updated
  on purpose while the code shows the old look is not a deviation: the code
  follows the kit. When it is unclear which is intended, compare the dates
  (the kit's decisions log, the commit) and look for the owner's decision;
  still unclear — show both with their dates, never pick silently.

## How not to do it

- Approximating "by eye" or from a summary of the kit.
- Wrapping a library component in a hand-rolled copy of its DOM to reach the
  kit's classes.
- Putting a `<button>` inside the card's `<a>` "with stopPropagation".
- Shipping the demo's assumptions (short copy, images everywhere) as layout
  facts.
- Treating an agreed deviation in one spot as licence to deviate elsewhere.
- Hiding keyboard or hover affordances below a breakpoint and calling it
  "mobile".
- Building a class list in a template literal that relies on a space inside
  the literal.
- Building an element the kit lacks from utilities in the code, to move it
  into the kit later.
- Writing a class into the kit without searching the stylesheet for its
  name.

## How it is verified

Every kit value the port depends on can be pointed to in the kit source that was
read in the same session. The rendered page measures to those values in both
themes and at a phone width, at a device pixel ratio of 1. Web-only additions are marked in the stylesheet.
Kit flaws found on the way are listed for the owner, with the fix proposed for
the kit.
