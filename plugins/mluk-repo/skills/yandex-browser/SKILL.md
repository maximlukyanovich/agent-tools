---
name: yandex-browser
description: Reproducing and avoiding Yandex-Browser-only bugs — running Yandex Browser under Playwright without installing it (Linux package unpacked next to the session, playwright-core, touch swipes through CDP, stock Chromium of the same milestone for comparison) and its known quirk, a finger swipe that starts on an overlay's shadow, outline or rounded corner going to the wrong scroller. Use when a bug shows only in Yandex Browser, when asked to test there, or when an overlay with a shadow sits over a nested scroller.
---

# yandex-browser

Yandex Browser is a Chromium fork with its own patches, so a bug can live there
and nowhere else. It can be driven from the terminal — no phone, no owner at the
keyboard.

## Running it under Playwright

1. **Get the package, do not install it.** The index is
   `https://repo.yandex.ru/yandex-browser/deb/dists/stable/main/binary-amd64/Packages`;
   take the `Filename:` of `yandex-browser-stable` (about 190 MB), download it
   into the session's scratch directory and unpack with `dpkg-deb -x`. The
   binary is `opt/yandex/browser/yandex_browser`. No sudo; it needs the usual
   Chromium system libraries (present wherever Chrome runs). The scratch
   directory does not survive a session restart — download again.
2. **Launch it** with `chromium.launch({ executablePath, headless: true })` from
   any `playwright-core`; a project that has none can borrow a copy from
   `~/.npm/_npx/*/node_modules/`. Headless works. `chrome://version` names the
   Chromium base.
3. **Send real finger gestures.** With `hasTouch: true`, a CDP session's
   `Input.dispatchTouchEvent` (touchStart → a dozen touchMove steps → touchEnd)
   goes through the browser's own gesture pipeline. `page.touchscreen` only
   taps.
4. **Compare with stock Chromium of the same milestone** before blaming either
   side: Chrome for Testing lists a build per milestone at
   `https://googlechromelabs.github.io/chrome-for-testing/latest-versions-per-milestone-with-downloads.json`.
   If `unzip` is missing, extract with Python's `zipfile` and restore the
   executable bits.

## Finding the cause

- **Map it, do not guess.** Swipe on a grid and read `scrollTop` after each
  swipe; the dead zone's size usually names the culprit (a blur radius, a
  padding, a peek height).
- **Bisect by injected styles** — `page.addStyleTag` on the running app. No file
  in the repository changes, so it is safe beside another session.
- **Ask the compositor.** `browser.startTracing(page, { categories: ['input',
  'cc'] })` around one gesture: `Failed Hit Test` means the compositor asked the
  main thread, `Handle On Impl` right after `Hit Testing for ScrollNode` means
  it decided alone.
- **Rebuild it on a blank page** (`page.setContent`) once a suspect is found: a
  ten-line page states the rule and tells an app bug from a browser bug.
- `document.elementFromPoint` is not evidence here — it is the main thread's
  answer, and the quirks below are the compositor's.

## Known quirk: a swipe goes to the wrong scroller

Seen in 26.8 (Chromium 150); stock Chromium 146–153 does not do it.

When a finger swipe starts, Yandex Browser treats everything an element
**paints** as the element: its `box-shadow`, `outline`, `text-shadow`, and the
cut-out of a rounded corner. If that paint lies over a scroller the element is
not inside of, the swipe goes to the element's scroll chain instead of the
scroller under the finger — typically nothing moves. Stock Chromium falls back
to a main-thread hit test in such a spot.

- ✗ a bottom sheet, toolbar or floating button with a wide shadow, placed over
  or next to a nested scroll area: a band as tall as the shadow stops scrolling.
- ✓ paint the shadow on a positioned pseudo-element with
  `pointer-events: none`, sized to the border box
  (`inset` = minus the border widths, `z-index: -1`, `border-radius: inherit`).
  A hit-test-transparent layer is skipped. The look is the same up to
  anti-aliasing on rounded corners.
- ✗ `pointer-events: none` on the element with `auto` on its children — the
  shadow still counts.
- The page's own (root) scroller is not affected: a fixed header's shadow sends
  the swipe to the page, which is what was wanted.

A Chromium-based e2e suite cannot catch this; verify in Yandex Browser itself.
