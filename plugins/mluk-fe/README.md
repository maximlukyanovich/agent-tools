# mluk-fe

Frontend conventions for React / Next.js projects. Enable it in a web front; the hooks stay silent wherever their files do not exist.

## Install

```bash
claude plugin install mluk-fe --marketplace maximlukyanovich/agent-tools --scope project
```

The hooks need Node; CI tests them on Node 24.

Other scopes and updating: [`docs/updates.md`](../../docs/updates.md).

## What is in it

| Part | For |
| --- | --- |
| [`web-ui-conventions`](skills/web-ui-conventions/SKILL.md) | the rules every screen and control follows: screen and interactive states, `cursor-pointer`, mobile-first overflow, `svh`, tokens, the import-only root stylesheet, reduced motion and nothing jumping, non-blocking navigation, transient UI reset when a page leaves, external links, a11y with focus returned by dialogs |
| [`component-discipline`](skills/component-discipline/SKILL.md) | how a component stays small and exact: extraction thresholds, text metrics, semantic tokens and tailwind-merge, CVA variants carrying the look, the view / hook split, skeletons, no invented assets, fake timers in component tests, icons from a dictionary by meaning |
| [`yandex-browser`](skills/yandex-browser/SKILL.md) | reproducing Yandex-Browser-only bugs under Playwright without installing the browser, and its known quirk: a swipe that starts on an overlay's shadow goes to the wrong scroller |
| [`reference/motion.md`](reference/motion.md) | the collapse primitive's recipe and traps, and how motion is checked paused — read on instruction from `web-ui-conventions` |
| [`reference/next-16.md`](reference/next-16.md) | Next.js 16: scroll behaviour on route changes, a hidden page under Cache Components and what resets, content pages readable without JavaScript, the 200 for an unknown slug |
| `hooks/locale-parity.mjs` | PostToolUse: a written `<locale>.json` has the same key set as its siblings |
| `hooks/i18n-keys.mjs` | PostToolUse (next-intl): every static `t('key')` a source file reads exists in the catalog |
| `hooks/metadata-title.mjs` | PostToolUse (App Router): no hardcoded string `title` in a page's metadata |
| `/mluk-fe:help` | what is here and what the profile configures |

Paths come from the profile's `## Frontend` section — keys and defaults in [`reference/profile.md`](reference/profile.md). Porting a design kit is `mluk-design`.

## In use

The skills load when the work reaches them: "build the settings screen" brings
`web-ui-conventions`, writing or refactoring a component brings
`component-discipline`, a bug seen only in Yandex Browser brings
`yandex-browser`. The hooks run after every write: a key added to `en.json` but
not to its sibling locales, or a `t('key')` the catalog lacks, is reported to
the agent right away, before its next step.

## Hook tests

The hooks' tests: `node --test 'plugins/mluk-fe/hooks/*.test.mjs'` from the repository root (run after every edit; a bare directory argument fails on Node 24). CI runs them on every push — `.github/workflows/hooks.yml`.
