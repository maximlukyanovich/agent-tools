// Shared helpers for the mluk-fe PostToolUse hooks.
//
// Claude Code sends a hook a JSON payload on stdin. For Write / Edit the path is
// `tool_input.file_path`; for any other tool the hooks stay silent. The project root is
// `CLAUDE_PROJECT_DIR`. Paths a hook needs come from the project profile's `## Frontend`
// section (keys in ../reference/profile.md); a missing key takes its default.

import { readFile } from 'node:fs/promises'
import { join, relative, resolve } from 'node:path'

const PROJECT_DIR = process.env.CLAUDE_PROJECT_DIR ?? process.cwd()

const DEFAULTS = {
  messages: 'messages',
  source: 'src',
  app: 'src/app',
  'default locale': null,
  'hooks off': '',
}

async function readStdin() {
  if (process.stdin.isTTY) return ''
  let buffer = ''
  process.stdin.setEncoding('utf8')
  for await (const chunk of process.stdin) buffer += chunk
  return buffer
}

/**
 * The file just written or edited, or `null` when the hook should not run (another tool, a
 * malformed payload, no path). The caller treats `null` as "exit 0".
 */
export async function readWriteToolInput() {
  const raw = await readStdin()
  if (!raw.trim()) return null
  let payload
  try {
    payload = JSON.parse(raw)
  } catch {
    return null
  }
  const toolName = payload?.tool_name
  if (toolName !== 'Write' && toolName !== 'Edit') return null
  const filePath = payload?.tool_input?.file_path
  if (typeof filePath !== 'string' || filePath.length === 0) return null
  const absolute = resolve(PROJECT_DIR, filePath)
  return {
    absolute,
    relative: relative(PROJECT_DIR, absolute).split('\\').join('/'),
    projectDir: PROJECT_DIR,
  }
}

/**
 * `## Frontend` of `.claude/project-profile.md` as `{ messages, source, app, defaultLocale,
 * off }`. Lines are `- key: value`; backticks and a trailing ` — comment` are dropped.
 */
export async function readFrontendConfig(projectDir) {
  const values = { ...DEFAULTS }
  let text = ''
  try {
    text = await readFile(join(projectDir, '.claude', 'project-profile.md'), 'utf8')
  } catch {
    // no profile — defaults
  }
  const section = text.split(/^## /m).find((part) => part.startsWith('Frontend'))
  for (const line of section?.split('\n') ?? []) {
    const match = line.match(/^- ([a-z ]+):\s*(.+)$/)
    if (!match || !(match[1] in DEFAULTS)) continue
    values[match[1]] = match[2].split(' — ')[0].replaceAll('`', '').trim()
  }
  const trim = (path) => path.replace(/^\.\//, '').replace(/\/+$/, '')
  return {
    messages: trim(values.messages),
    source: trim(values.source),
    app: trim(values.app),
    defaultLocale: values['default locale'] || null,
    off: new Set(
      values['hooks off']
        .split(',')
        .map((name) => name.trim())
        .filter(Boolean),
    ),
  }
}

/** Escape a configured path for use inside a RegExp. */
export function escapePath(path) {
  return path.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
}

/** Print one block to stderr and exit with the code that reaches the agent. */
export function fail(message) {
  process.stderr.write(`${message}\n`)
  process.exit(2)
}
