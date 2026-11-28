# Collapse and appearance: the recipe

Read by `web-ui-conventions` rule 7 before building or changing the project's collapse primitive, or a block that shows and hides its content, and before checking any motion in a browser. Figures below were measured in Chromium 146.

## The collapse primitive

One component in the project's shared UI, used for every expand / collapse — full text, details, an answer, "more". Not an instant height change, not a `line-clamp` toggle.

- The box is a one-row grid whose row moves `0fr ↔ 1fr`; the content inside has `min-height: 0` and clips (`overflow: hidden`) only while closed or moving, so focus rings and shadows are not cut when open.
- Content that is closed and not peeking is `inert` — out of the tab order and the accessibility tree.
- The end of the movement is set by `transitionend` **and** by a timer of the transition's length: a project that zeroes durations under reduced motion starts no transition, so `transitionend` never fires, and the timer ends a plain fade in its place as well.

## Traps

- **Both ends of the row in one form.** `0fr ↔ 1fr` and `minmax(L, 0fr) ↔ minmax(L, 1fr)` interpolate; ends of different forms — `minmax(L, 0fr) ↔ 1fr`, `0fr ↔ minmax(L, 1fr)`, an `fr` against `auto` — do not, and the row jumps at the halfway point.
- **A peek is held by the box, not by the content's `min-height`.** A closed block that shows its first lines through `min-height` on the content stands still until the row's share passes that height — with a 100 px peek of 300 px, the first third of the time. Give the box a bottom padding of the peek height and the content the same negative bottom margin: it moves from the first frame.
- **A fade at the edge is a mask on the box.** On the content, the mask's percentages count from the full text, not from what is visible. The mask stop is animated through a registered custom property (`@property`); an unregistered one changes in one step.

## Appearance without jumps

An element that appears or disappears with a state — a button, a hint, a badge in a row — keeps its place reserved in advance or stays where it is and changes its look; the container's height is the same before and after. A block does not expand by itself from an action inside it. Entry and exit are short transitions — entry on the project's "fast" motion token, exit shorter still — not instant and not sluggish.

## Checking the motion

A sample taken on a timer shows where the element stands at that moment, not how it got there: two samples on either side of a jump look like a smooth step. So a motion is checked paused, not timed: take the element's `getAnimations()`, pause each, set `currentTime` to fractions of the duration (¼, ½, ¾) and read `getBoundingClientRect().height` — it grows steadily, with no jump at the middle and no flat start. A jump is checked the same way: the container's height before and after the state change.
