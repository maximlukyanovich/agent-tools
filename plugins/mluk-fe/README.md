# mluk-fe

Frontend conventions for React / Next.js projects. Enable it in a web front; the hooks stay silent wherever their files do not exist.

| Part | For |
| --- | --- |
| [`web-ui-conventions`](skills/web-ui-conventions/SKILL.md) | the rules every screen and control follows: screen and interactive states, `cursor-pointer`, mobile-first overflow, `svh`, tokens, the import-only root stylesheet, reduced motion, non-blocking navigation, a11y |
| [`component-discipline`](skills/component-discipline/SKILL.md) | how a component stays small and exact: extraction thresholds, text metrics, semantic tokens and tailwind-merge, CVA variants, the view / hook split, skeletons, no invented assets, fake timers in component tests |
| `hooks/locale-parity.mjs` | PostToolUse: a written `<locale>.json` has the same key set as its siblings |
| `hooks/i18n-keys.mjs` | PostToolUse (next-intl): every static `t('key')` a source file reads exists in the catalog |
| `hooks/metadata-title.mjs` | PostToolUse (App Router): no hardcoded string `title` in a page's metadata |
| `/mluk-fe:help` | what is here and what the profile configures |

Paths come from the profile's `## Frontend` section — keys and defaults in [`reference/profile.md`](reference/profile.md). Porting a design kit is `mluk-design`.

The hooks' tests: `node --test 'plugins/mluk-fe/hooks/*.test.mjs'` from the repository root (run after every edit; a bare directory argument fails on Node 24). CI runs them on every push — `.github/workflows/hooks.yml`.
