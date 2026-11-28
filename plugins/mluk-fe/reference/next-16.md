# Next.js 16: what the UI rules need to know

Read by `web-ui-conventions` rules 7, 8 and 10 in a project on Next.js 16. Sections 2 and 3 and the second trap of section 4 apply only with Cache Components on (`cacheComponents: true` in `next.config`). Facts below are from the docs Next ships in `node_modules/next/dist/docs/` — read that copy for the installed version when one here looks off — except those marked as read in the `react-dom` source or observed on a live project.

## 1. Smooth scrolling and route changes

Next 16 no longer switches `scroll-behavior` off during a route change (`01-app/02-guides/upgrading/version-16.md`, "Scroll Behavior Override"): with `html { scroll-behavior: smooth }` a new page scrolls to its top slowly. Put `data-scroll-behavior="smooth"` on `<html>` and Next turns smoothness off for the change, so anchors glide and a new page opens at the top at once.

## 2. A page that leaves is hidden, not unmounted

With Cache Components, Next keeps the previous page inside React's `<Activity mode="hidden">` — the DOM stays in the document under `display: none`, React state lives on, effects are cleaned up — and keeps up to three routes so (`01-app/02-guides/preserving-ui-state.md`). Back brings the page back exactly as it was left, open things included.

- **Transient UI resets in a `useLayoutEffect` cleanup** — a dropdown, a filter panel, a modal `<dialog>` opened with `showModal()`, a playing video or an iframe, a "Copied" confirmation on a timer. The cleanup runs when Activity hides the component, before the hide, so nothing stale flashes on return. Links inside a panel also close it on click through `Link`'s `onNavigate`.
- **What stops at once is stopped through the DOM in that cleanup.** A `setState` there updates a hidden tree, and React defers it to an idle render (in the `react-dom` source the update waits in `root.hiddenUpdates` on the offscreen lane); observed: a hidden modal dialog keeps the page inert — no scroll, no clicks — and a hidden iframe keeps playing until then. So the cleanup also calls `dialog.close()`, sets `iframe.src = "about:blank"`, `details.open = false`, pauses the media; the `setState` only brings the state in line.
- **"Open on this path" is not a substitute.** Keying the state to the pathname (`openOn === pathname`) reopens the panel on A → B → A, and a component in a layout is never hidden at all — it needs the reset on navigation itself.
- **What is kept on purpose is a decision**, not the default: a form draft, an expanded section, a scroll position. Name it in the task; the default for anything transient is the reset.

Check: open the element, leave by a link and by Back, return — it is closed; after Back with a modal dialog open, the new page scrolls and takes clicks; the video is silent.

## 3. Content pages show their text without JavaScript

Rule 8 makes navigations instant through Suspense, and with `partialPrefetching` Next suggests wrapping the read of `params` in `<Suspense>`. On a prerendered content page (an article, a post) that hides the text — observed: even in production it sits in a hidden `<div>` until an inline script moves it in, and without JavaScript — RSS readers, reading mode, `curl` — only the skeleton shows. For such a page:

- `export const instant = false` — the segment opts out of instant-navigation validation (`01-app/03-api-reference/03-file-conventions/02-route-segment-config/instant.md`; works only with Cache Components);
- `params` read outside Suspense; a skeleton only for data a reader without JavaScript does not need.

Check on `next build && next start`, not on dev: a Playwright context with `javaScriptEnabled: false` sees the article text.

## 4. Two traps: the status and the hidden page

- **An unknown slug answers 200.** A streamed response keeps the `200` it started with, and `notFound()` after that only adds `noindex`. The stream starts with the first `loading.tsx` or Suspense fallback that `web-ui-conventions` rule 1 asks for, or, with Cache Components, with the prerendered shell — even an empty one under `instant = false` (`01-app/03-api-reference/03-file-conventions/loading.md`, "Status codes"; `01-app/03-api-reference/04-functions/not-found.md`). A real `404` is decided before the response starts: without Cache Components, by `notFound()` that runs before any fallback renders — before the `loading.tsx` and Suspense boundaries and before an `await` that may suspend (`loading.md`, "When does streaming start?"; in 16.2, "When is the response body streamed?"); with Cache Components, by `notFound()` during prerendering; and, for a slug not known at build time, in the proxy, which checks the slug and rewrites to a not-found route or returns a `404` itself.
- **The hidden page is still in the DOM.** Ids repeat across the visible and the hidden page; observed on a live project, the visible one came first in document order, and a bare `#id` query leans on that order. In tests and scripts, scope queries to the visible page (`:visible`, a role query).
