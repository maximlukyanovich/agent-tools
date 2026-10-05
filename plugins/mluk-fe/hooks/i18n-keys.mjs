#!/usr/bin/env node
// PostToolUse hook `i18n-keys` (next-intl): every static translation key a source file reads must
// exist in the locale catalog. Fires on `<source>/**/*.{ts,tsx}` (the keys of that file) and on
// `<messages>/<locale>.json` (every key read anywhere under `<source>`). A missing key exits 2 with
// `file:line ns.key`, so a renamed or moved key is caught before a page renders MISSING_MESSAGE.
//
// Scope: `const t = useTranslations('Ns')` / `getTranslations('Ns')` /
// `getTranslations({ …namespace: 'Ns' })` bind a translator variable to a namespace from that line
// on (a later declaration of the same name rebinds it — one file, several components). Only
// `t('literal')` calls are checked; template literals and `t.rich` / `t.raw` are skipped.
import { readdir, readFile } from 'node:fs/promises'
import { join, relative, resolve } from 'node:path'

import { escapePath, fail, readFrontendConfig, readWriteToolInput } from './_lib.mjs'

const MAX_SHOWN = 8

const DECLARATION =
  /\b(?:const|let)\s+(\w+)\s*=\s*(?:await\s+)?(?:useTranslations|getTranslations)\(\s*(?:'([\w.]+)'|\{[^}]*?namespace:\s*'([\w.]+)'[^}]*\})\s*\)/g

function hasKey(catalog, path) {
  let node = catalog
  for (const part of path.split('.')) {
    if (!node || typeof node !== 'object' || !(part in node)) return false
    node = node[part]
  }
  return true
}

/** `[{ line, key }]` for every static key the file reads, resolved to `ns.key`. */
function collectKeys(source) {
  const bound = new Map()
  const found = []
  source.split('\n').forEach((text, index) => {
    for (const m of text.matchAll(DECLARATION)) bound.set(m[1], m[2] ?? m[3])
    for (const [name, ns] of bound) {
      const call = new RegExp(`(?<![\\w.])${name}\\(\\s*'([\\w.]+)'`, 'g')
      for (const m of text.matchAll(call)) found.push({ line: index + 1, key: `${ns}.${m[1]}` })
    }
  })
  return found
}

async function loadCatalog(path) {
  try {
    return JSON.parse(await readFile(path, 'utf8'))
  } catch {
    return null
  }
}

async function* sourceFiles(dir) {
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    const path = join(dir, entry.name)
    if (entry.isDirectory()) yield* sourceFiles(path)
    else if (/\.(ts|tsx)$/.test(entry.name) && !/\.test\./.test(entry.name)) yield path
  }
}

function report(missing) {
  const shown = missing.slice(0, MAX_SHOWN).map((m) => `  ${m.file}:${m.line} ${m.key}`)
  const tail = missing.length > MAX_SHOWN ? `\n  (+${missing.length - MAX_SHOWN} more)` : ''
  fail(`[mluk-fe:i18n-keys] translation keys missing from the catalog:\n${shown.join('\n')}${tail}`)
}

const input = await readWriteToolInput()
if (!input) process.exit(0)

const config = await readFrontendConfig(input.projectDir)
if (config.off.has('i18n-keys')) process.exit(0)

const messagesRoot = resolve(input.projectDir, config.messages)
const catalogEdit = new RegExp(`^${escapePath(config.messages)}/([a-zA-Z-]+)\\.json$`).test(
  input.relative,
)
const sourceEdit =
  new RegExp(`^${escapePath(config.source)}/.*\\.(ts|tsx)$`).test(input.relative) &&
  !/\.test\./.test(input.relative)
if (!catalogEdit && !sourceEdit) process.exit(0)

// The catalog to check against: the one just edited, else the default locale, else the first one.
let catalog = null
if (catalogEdit) catalog = await loadCatalog(input.absolute)
else {
  if (config.defaultLocale)
    catalog = await loadCatalog(join(messagesRoot, `${config.defaultLocale}.json`))
  if (!catalog) {
    try {
      const first = (await readdir(messagesRoot)).filter((f) => f.endsWith('.json')).sort()[0]
      if (first) catalog = await loadCatalog(join(messagesRoot, first))
    } catch {
      // no catalogs — nothing to check
    }
  }
}
if (!catalog) process.exit(0)

const files = []
if (sourceEdit) files.push(input.absolute)
else {
  try {
    for await (const file of sourceFiles(resolve(input.projectDir, config.source))) files.push(file)
  } catch {
    process.exit(0)
  }
}

const missing = []
for (const file of files) {
  let source
  try {
    source = await readFile(file, 'utf8')
  } catch {
    continue
  }
  const rel = relative(input.projectDir, file).split('\\').join('/')
  for (const { line, key } of collectKeys(source)) {
    if (!hasKey(catalog, key)) missing.push({ file: rel, line, key })
  }
}

if (missing.length) report(missing)
process.exit(0)
