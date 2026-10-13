# Scaffold recipe: Next.js

`/mluk-bootstrap:new` reads **Scaffold**; `/mluk-bootstrap:setup` reads **For
the harness**. Each reads its own section only.

## Scaffold

Verified with create-next-app 16.4.0 (Next 16.4.0, React 19.3.0, pnpm 11.6.0).
First run `pnpm dlx create-next-app@latest --version`; on another version,
compare its `--help` with the flags below before running — a new option is a
question to the owner, not a silent default.

**The folder name becomes the package name.** npm rules apply: lower case, no
spaces, URL-safe characters, no leading dot or underscore. Check it first; a
name that breaks them stops the command — the owner renames the folder and
starts again.

**Questions**, one round:

| Question | Recommended | Flags |
| --- | --- | --- |
| Cache Components | on — the Next 16 model; its traps are below, under For the harness | `--cache-components` / `--no-cache-components` |
| Agent feedback | off — an experimental `next.config` flag the project gains nothing from | `--no-agent-feedback` / `--agent-feedback` |

Under `--yes` both are on, and `--help` does not say so; Cache Components also
writes `partialPrefetching: true`. src/ and the React Compiler are off.

**Command** — every option explicit, because `--yes` takes the preferences
saved by earlier runs (`~/.config/create-next-app-nodejs`) before the defaults:

```bash
pnpm create next-app@latest . --ts --tailwind --eslint --app --no-src-dir \
  --no-react-compiler --import-alias "@/*" --use-pnpm --agents-md --no-api \
  --no-empty --no-rspack --disable-git --yes \
  <Cache Components flag> <agent feedback flag>
```

Without `--disable-git` the generator commits "Initial commit from Create Next
App" itself. It tolerates `.claude/`, `.git/`, `.idea/`, `.vscode/` and
`.gitignore`, and refuses a folder holding `AGENTS.md`, `CLAUDE.md` or
`README.md`.

**Environment:**

- `.nvmrc` — the major of `node --version`; `engines.node` in `package.json` —
  `"<major>.x"`.
- `packageManager` in `package.json` and `pnpm-workspace.yaml` with
  `allowBuilds` — written by the generator; check both are there.
- `pnpm install --frozen-lockfile` passes, with no `ERR_PNPM_IGNORED_BUILDS`.

## For the harness

- **The generator's block in `AGENTS.md`** — `<!-- BEGIN:nextjs-agent-rules -->`
  … `<!-- END:nextjs-agent-rules -->` — stays as it is; the harness sections
  are written around it. Removed, it comes back: `next dev` started by an
  agent appends it to the end of the file. The generator writes no
  `CLAUDE.md`.
- **Next 16 renamed middleware**: `middleware.ts` is `proxy.ts`, next to
  `app/`, exporting `proxy`.
- **With Cache Components** `await params` is runtime data. With locales, the
  locale comes from `next/root-params` — a getter named after the root
  segment, `await lang()` — not from `params`; each root parameter needs at
  least one value in `generateStaticParams`, or the build fails.
- **pnpm `allowBuilds`**: `AGENTS.md` §2 carries the line `templates.md`
  describes; the entries go to the generator's `pnpm-workspace.yaml`.
- **Type-check is `next typegen && tsc --noEmit`.** The generated
  `app/layout.tsx` uses the global `LayoutProps`, which `next typegen` writes;
  a bare `tsc` on a clean clone fails with TS2304. The profile's validate
  command runs the pair.
