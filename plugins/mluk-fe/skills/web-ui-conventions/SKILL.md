---
name: web-ui-conventions
description: The UI rules every screen of a React / Next.js web project follows from the first commit — the full set of screen states, interactive states with cursor-pointer on clickable non-links, mobile-first overflow, svh instead of vh for full-screen sections, design tokens instead of literals, a root stylesheet that is only an import list, reduced motion, navigation that never freezes, accessibility as the floor. Use when building or reviewing any screen or interactive element. Not for porting a kit's look — that is mluk-design:design-port.
---

# Web UI conventions

Cheaper to bake in than to retrofit. Each rule below was paid for on a live project; the project's `AGENTS.md` carries only what is specific to it (its token file, its area stylesheets) and links here.

## How to do it

1. **Every data-driven screen has all its states:** default, loading, empty, error (server errors included). Loading is a skeleton shaped like the content, not a spinner or "Loading…"; empty and error are answers with their own copy, not pending states. In the App Router each segment that fetches has `loading.tsx`, `error.tsx` and, where it applies, `not-found.tsx`. A mutation reports its outcome with a toast; a destructive action is confirmed in a dialog. Not only screens load: an image, an upload, a retry, a reconnect, a route the router kept alive and shows again, an item being created — each shows something until it arrives and while it is slow, never a blank area. When the design does not draw that state, it is a question for the designer, with a placeholder from existing primitives named in the task report.

2. **Every interactive element has all its states:** hover, focus-visible, active, disabled, loading where it waits — plus enter / exit transitions where they help — and works from the keyboard. **Every clickable element that is not a link gets `cursor-pointer`** — buttons, chips, toggles, custom controls; utility frameworks and headless primitives do not set it. Anchors already have it; text inputs keep the text cursor; `disabled:cursor-not-allowed` is the mirror case. **What hangs on hover or focus must survive a touch:** a phone keeps `:hover` on the tapped element until the next tap elsewhere, and a tap focuses a button without being keyboard focus — so a hover that pauses a timer, opens a menu or reveals controls sits under `@media (hover: hover) and (pointer: fine)`, and a focus that does the same uses `:focus-visible` (`:has(:focus-visible)` on a container), not `:focus` / `:focus-within`. A hold that must work under a finger is marked from pointer events (down until up or cancel, anywhere), not left to `:active`.

3. **Mobile first.** Base styles are the phone; `sm:` / `md:` / `lg:` layer up. Overflow is handled on purpose: `truncate` or a line clamp for one-line text, `break-words` (or `break-all` for unbroken strings) for user content, `shrink-0` on what must not compress. When one template cannot serve both, propose distinct phone and desktop layouts instead of squeezing one.

4. **Full-screen and pinned sections use `svh`, not `vh`.** `100vh` jumps on mobile as the browser bars show and hide, and clips content under them. `svh` (`min-h-svh`, `h-[100svh]`) is the stable small viewport; `dvh` only when the box must follow the bars; `lvh` only when the largest height is intended. Sticky content is offset by the header height from a variable, not a literal.

5. **Tokens, not literals.** Colours, type sizes, spacing, radii, shadows come from the design tokens (`@theme` / CSS variables) and the utilities built on them — never a hardcoded hex or px in a component. A value missing from the tokens is a question to the owner (extend the tokens, or accept the nearest with a recorded delta), not an inline literal. Conditional classes are composed with `cn()`.

6. **The root stylesheet is only an import list.** Framework layers first, then the per-area stylesheets, then the site tokens last. Styles go into an imported file, never into the root itself: Turbopack does not hot-reload an edit to the root stylesheet, while an imported file reloads at once — and a newly added `@import` needs a dev-server restart.

7. **Motion is gated.** Every animation respects `prefers-reduced-motion` — reduced means instant or a plain fade, not a shorter version of the same movement. Animate `transform` and `opacity`; batch pointer-driven work in `requestAnimationFrame`; stop loops that are off screen. Swapped text (a scene, a locale switch) fades instead of jumping.

8. **Navigation never freezes on the old screen.** A client navigation shows its loading state at once — `loading.tsx`, Suspense boundaries, `useTransition` — instead of waiting for the server render. The first load (SSR, a deep link) is the exception.

9. **Accessibility is the floor, not the ceiling.** Semantic elements, a label for every control, a visible focus ring, sufficient contrast, `aria-*` where semantics fall short. The framework's a11y lint plugin is the minimum.

## How not to do it

- A screen that shows a spinner for loading and nothing for empty or error.
- A custom `div` button with `onClick` and no `cursor-pointer`, no focus ring, no keyboard handler.
- A countdown paused by `:hover` or `:focus-within`: on a phone the tap that answered it freezes it for good.
- `h-screen` / `100vh` on a hero that must fill a phone.
- `text-[17px]` or `#c9a46a` in a component because "it is only used here".
- A new rule appended to the root stylesheet, then a reload that shows nothing.
- An animation that ignores reduced motion, or a navigation that sits on the previous page while the next one renders.

## How it is verified

Open the screen in a real browser at phone width and at desktop width, in both themes, with reduced motion on: every state is reachable (throttle the network for loading; break the request for error; an empty account for empty), every control is reachable by keyboard and shows focus, a tap under touch emulation leaves no hover-only behaviour switched on, nothing overflows its box, and a client navigation shows its skeleton immediately.
