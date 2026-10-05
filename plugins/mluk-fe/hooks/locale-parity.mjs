#!/usr/bin/env node
// PostToolUse hook `locale-parity`: when a locale catalog `<messages>/<locale>.json` is written,
// compare its key set with every sibling catalog. A mismatch exits 2 with a short diff, so the
// next step fixes it before the commit. Nested catalogs are flattened to dotted keys.
//
// Silent when the edited file is not a catalog, or when the profile switches the hook off.
import { readdir, readFile } from 'node:fs/promises'
import { join, resolve } from 'node:path'

import { escapePath, fail, readFrontendConfig, readWriteToolInput } from './_lib.mjs'

const MAX_KEYS_SHOWN = 5

function flatKeys(obj, prefix = '') {
  const keys = []
  for (const [k, v] of Object.entries(obj)) {
    const path = prefix ? `${prefix}.${k}` : k
    if (v && typeof v === 'object' && !Array.isArray(v)) keys.push(...flatKeys(v, path))
    else keys.push(path)
  }
  return keys
}

async function loadKeys(path) {
  try {
    return new Set(flatKeys(JSON.parse(await readFile(path, 'utf8'))))
  } catch {
    return null
  }
}

function summarise(keys) {
  const head = keys.slice(0, MAX_KEYS_SHOWN).join(', ')
  const tail = keys.length > MAX_KEYS_SHOWN ? ` (+${keys.length - MAX_KEYS_SHOWN} more)` : ''
  return `${head}${tail}`
}

const input = await readWriteToolInput()
if (!input) process.exit(0)

const config = await readFrontendConfig(input.projectDir)
if (config.off.has('locale-parity')) process.exit(0)

const match = input.relative.match(
  new RegExp(`^${escapePath(config.messages)}/([a-zA-Z-]+)\\.json$`),
)
if (!match) process.exit(0)

const [, locale] = match
const messagesRoot = resolve(input.projectDir, config.messages)

const ownKeys = await loadKeys(input.absolute)
if (!ownKeys) process.exit(0)

let entries
try {
  entries = await readdir(messagesRoot, { withFileTypes: true })
} catch {
  process.exit(0)
}

const diffs = []
for (const entry of entries) {
  if (!entry.isFile()) continue
  const sibling = entry.name.match(/^([a-zA-Z-]+)\.json$/)
  if (!sibling || sibling[1] === locale) continue
  const otherKeys = await loadKeys(join(messagesRoot, entry.name))
  if (!otherKeys) continue
  const missingHere = [...otherKeys].filter((k) => !ownKeys.has(k))
  const missingThere = [...ownKeys].filter((k) => !otherKeys.has(k))
  if (missingHere.length) {
    diffs.push(
      `  ${config.messages}/${locale}.json: missing keys present in ${entry.name}: ${summarise(missingHere)}`,
    )
  }
  if (missingThere.length) {
    diffs.push(
      `  ${entry.name}: missing keys present in ${locale}.json: ${summarise(missingThere)}`,
    )
  }
}

if (diffs.length) fail(`[mluk-fe:locale-parity] locale catalog key mismatch:\n${diffs.join('\n')}`)
process.exit(0)
