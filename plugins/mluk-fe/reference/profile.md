# The profile section mluk-fe reads

`.claude/project-profile.md`, section `## Frontend`. Lines are `- key: value`; backticks and a trailing ` — comment` are ignored, so a value can carry its reason. A missing key takes the default; a missing section means all defaults. The hooks read only this committed file, never the clone's `project-profile.local.md`: what they check must hold in every clone.

| Key | Default | Read by |
| --- | --- | --- |
| `messages` | `messages` — the directory of `<locale>.json` catalogs (flat or nested JSON) | `locale-parity`, `i18n-keys` |
| `default locale` | the first catalog by name — the one a source edit is checked against | `i18n-keys` |
| `source` | `src` — where `.ts` / `.tsx` files that read translations live | `i18n-keys` |
| `app` | `src/app` — the Next.js App Router root; `page.tsx` files under it are checked | `metadata-title` |
| `hooks off` | none — comma-separated hook names switched off here, with the reason after ` — ` | all hooks |

Example:

```markdown
## Frontend

- messages: `messages` — next-intl, nested JSON
- default locale: `ru`
- source: `src`
- app: `src/app`
- hooks off: none
```

A project that does not use next-intl switches `i18n-keys` off; one without the App Router switches `metadata-title` off. Write the reason after the dash — the next reader sees a decision, not an omission.
