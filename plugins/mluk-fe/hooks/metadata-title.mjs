#!/usr/bin/env node
// PostToolUse hook `metadata-title` (Next.js App Router): catch a hardcoded string title in route
// metadata — `export const metadata = { title: '…' }` and the `generateMetadata` return shape — so
// a tab title follows the active locale instead of bypassing i18n.
//
// Fires only for `<app>/**/page.tsx`. Allowed: `title: t('page.title')`, a template literal, a
// variable. Flagged: a plain quoted literal inside a metadata block.
import { readFile } from 'node:fs/promises'

import { escapePath, fail, readFrontendConfig, readWriteToolInput } from './_lib.mjs'

const MAX_HITS_SHOWN = 5

const input = await readWriteToolInput()
if (!input) process.exit(0)

const config = await readFrontendConfig(input.projectDir)
if (config.off.has('metadata-title')) process.exit(0)
if (!new RegExp(`^${escapePath(config.app)}/(.+/)?page\\.tsx$`).test(input.relative))
  process.exit(0)

let content
try {
  content = await readFile(input.absolute, 'utf8')
} catch {
  process.exit(0)
}

const hits = []
// `title:` followed by a single- or double-quoted literal. Backticks are excluded — they usually
// hold interpolated copy.
const literalTitlePattern = /title\s*:\s*['"][^'"]+['"]/g
let match
while ((match = literalTitlePattern.exec(content)) !== null) {
  // Only inside a metadata block: look back 400 characters for the identifiers. Keeps an
  // unrelated `title:` (an icon's HTML title) out.
  const before = content.slice(Math.max(0, match.index - 400), match.index)
  if (!/\b(metadata|generateMetadata|Metadata)\b/.test(before)) continue
  const lineNum = content.slice(0, match.index).split('\n').length
  hits.push(`  ${input.relative}:${lineNum}  ${match[0]}`)
  if (hits.length >= MAX_HITS_SHOWN) break
}

if (hits.length) {
  fail(
    `[mluk-fe:metadata-title] hardcoded title in metadata — use \`getTranslations\` + \`t('…title')\` so the tab title follows the locale:\n${hits.join('\n')}`,
  )
}
process.exit(0)
