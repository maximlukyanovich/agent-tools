---
name: component-discipline
description: How a React component is written so that it stays small and exact — when to extract and when not to, text metrics (size + line-height + tracking), promoting repeated literals to semantic tokens and registering them with tailwind-merge, the shadcn CVA variant convention, the view / hook split, section-shaped skeletons with aria-busy, not inventing assets the design left out, and fake timers in component tests. Use when writing, refactoring or reviewing a component. Porting a kit's look is mluk-design:design-port; screen-level rules are web-ui-conventions.
---

# Component discipline

What keeps a component small and exact. The kit's look is ported by `mluk-design:design-port`; the states every screen and control must have are in `web-ui-conventions`. This skill does not repeat either. Project specifics — the token file, the primitives folder, example components — live in the project's own skill or `AGENTS.md`.

## How to do it

1. **Extract repetition, not everything.** The line sits around two real occurrences plus an expected third.
   - Extract: 2+ identical JSX trees → a sub-component; 2+ identical logic blocks → a helper, or a hook when it touches state; markup with behaviour (keyboard, ARIA, focus) → a named component even at one use, the name documents intent; a value used 3+ times → a named constant.
   - Keep inline: a one-off block of 10–30 lines (a sub-component with four pass-through props reads worse), a one-time transform (`items.filter(…).map(…)` needs no `getActiveItems`), an abstraction that saves 2–3 lines but adds a file, anything justified only by a future that has not come.
   - Utilities follow the same rule: no `utils/` dumping ground, a file named for its purpose; start in the same file, promote to the module, then to shared code only when a second caller appears.

2. **Text metrics are size + line-height + tracking.** Adjacent text of one size but different line-heights does not align; buttons and inputs grow with line-height. Text the design does not wrap gets an explicit height (`h-N`, `leading-none`, `leading-[Npx]`); text it wraps gets the designed line-height, never the browser default; tracking is copied exactly for caps and small sizes.

3. **A literal that repeats becomes a semantic token.** `text-[17px]`, `tracking-[0.08em]`, `leading-[1.1]` used twice are promoted to named tokens in the theme and consumed as utilities (`text-display`, `tracking-caps`). A name never collides with a framework default (`tracking-tight` → `tracking-display`) — overriding a default changes every use in the project. Grep the diff for `\[\d+px\]` and `\[-?0\.\d+em\]` before committing.

4. **A custom utility group is registered with tailwind-merge.** `cn()` built on plain `twMerge` does not know a new group: a custom font size such as `text-display` is read as a colour, and `cn('text-display', 'text-muted')` silently drops one of them. When the first custom group lands, switch `cn()` to `extendTailwindMerge` with that group in the same commit. A project that only redefines the framework's own scale names (`--text-sm`) does not need it.

5. **Primitive variants follow the shadcn CVA convention.** Variants are declared with `cva`, the prop typed as `VariantProps<typeof xVariants>`, and call sites pass plain string literals (`variant="outline" size="sm"`). A local `as const` map is fine for a discriminator reused across many call sites; named-const indirection is not retrofitted onto every primitive.

6. **A component with state splits into view and hook.** When a component owns a query, a mutation, form state or 2+ derived values, they move into a sibling `use-x.ts` that returns one object; the component stays a declarative tree. A single render without state stays one file.

7. **Pending UI is a section-shaped skeleton.** One wrapper next to the composite mirrors the loaded layout 1:1 and carries `aria-busy="true"` on its outer element — a stable target for assistive tech and tests. Not for a one-line inline loader, a button's spinner, an error / empty / not-found branch, a modal or a toast.

8. **What the design left out is asked for, not invented.** A custom icon is used verbatim, never swapped for a library look-alike; an empty icon slot, missing copy or a missing image is a question. A value the design shows as static but is really data (a count, a rating, a version) is wired to its source or raised as an open question; user-facing copy goes through the translation catalogs.

9. **A state from another DOM layer is checked in the rendered HTML.** A headless library's `data-*` attribute and a CSS pseudo-class are not interchangeable; a guessed selector is a rule that silently never applies.

10. **A component test drives its timers.** A component that waits on a timer before it is usable — a reveal, a stagger, a debounce, a delayed hint — is tested on fake timers (`vi.useFakeTimers()` in `beforeEach`, real ones back in `afterEach`), and the test moves time itself with `act(() => vi.runOnlyPendingTimers())` before it acts. `waitFor` on a real timer races its own timeout: the test passes alone and fails one run in a few under a loaded suite. Check that the test still fails when the timer never fires.

## How not to do it

- A `components/Helpers.tsx` with six single-use wrappers.
- A row of text that aligns in the design and not on the page because two line-heights differ.
- `text-[15px]` in four components, or a custom `text-*` group added without touching `cn()`.
- A primitive whose variants are a `const VARIANTS = { OUTLINE: 'outline' }` map imported everywhere.
- A 300-line component with two queries, a form and the markup in one function.
- A "Loading…" paragraph where the loaded page is a grid of cards.
- A `lucide` icon "close enough" to the custom SVG in the design.
- A component test that clicks after `await waitFor(…)` on a real reveal timer — green locally, red once in four runs in CI.

## How it is verified

Before committing: the diff has no repeated literal outside the tokens; every new custom utility group is in `cn()`; each component with a query or a mutation has its hook; pending states render a skeleton with `aria-busy="true"`; and the component is checked in a real browser against the design — text boxes measured, not eyeballed.
