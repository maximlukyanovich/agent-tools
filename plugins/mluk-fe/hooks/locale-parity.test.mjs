import { execFileSync } from 'node:child_process'
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { fileURLToPath } from 'node:url'
import assert from 'node:assert/strict'
import { afterEach, beforeEach, describe, it } from 'node:test'

const HOOK = fileURLToPath(new URL('./locale-parity.mjs', import.meta.url))

let projectDir

function run(payload) {
  try {
    execFileSync('node', [HOOK], {
      input: JSON.stringify(payload),
      env: { ...process.env, CLAUDE_PROJECT_DIR: projectDir },
      encoding: 'utf8',
      stdio: ['pipe', 'pipe', 'pipe'],
    })
    return { code: 0, stderr: '' }
  } catch (error) {
    return { code: error.status ?? 1, stderr: String(error.stderr ?? '') }
  }
}

function writeLocale(locale, json) {
  const dir = join(projectDir, 'messages')
  mkdirSync(dir, { recursive: true })
  writeFileSync(join(dir, `${locale}.json`), JSON.stringify(json, null, 2))
}

beforeEach(() => {
  projectDir = mkdtempSync(join(tmpdir(), 'hook-locale-parity-'))
})

afterEach(() => {
  rmSync(projectDir, { recursive: true, force: true })
})

describe('check_locale_parity hook', () => {
  it('exits 0 when the edited file is not a locale catalogue', () => {
    const result = run({ tool_name: 'Write', tool_input: { file_path: 'src/foo.ts' } })
    assert.equal(result.code, 0)
  })

  it('exits 0 on a non-Write/Edit tool', () => {
    const result = run({ tool_name: 'Bash', tool_input: { command: 'ls' } })
    assert.equal(result.code, 0)
  })

  it('exits 0 when ru matches en', () => {
    writeLocale('en', { greeting: 'Hi', errors: { generic: 'Oops' } })
    writeLocale('ru', { greeting: 'Привет', errors: { generic: 'Ой' } })
    const result = run({ tool_name: 'Write', tool_input: { file_path: 'messages/ru.json' } })
    assert.equal(result.code, 0)
    assert.equal(result.stderr, '')
  })

  it('exits 2 when ru is missing keys present in en', () => {
    writeLocale('en', { greeting: 'Hi', actions: { save: 'Save' } })
    writeLocale('ru', { greeting: 'Привет' })
    const result = run({ tool_name: 'Write', tool_input: { file_path: 'messages/ru.json' } })
    assert.equal(result.code, 2)
    assert.ok(result.stderr.includes('missing keys present in en.json'))
    assert.ok(result.stderr.includes('actions.save'))
  })

  it('reports extra keys in ru that en does not have', () => {
    writeLocale('en', { greeting: 'Hi' })
    writeLocale('ru', { greeting: 'Привет', stale: 'leftover' })
    const result = run({ tool_name: 'Write', tool_input: { file_path: 'messages/ru.json' } })
    assert.equal(result.code, 2)
    assert.ok(result.stderr.includes('missing keys present in ru.json'))
    assert.ok(result.stderr.includes('stale'))
  })

  it('exits 2 when en gains keys ru does not yet cover', () => {
    writeLocale('en', { greeting: 'Hi', actions: { save: 'Save' } })
    writeLocale('ru', { greeting: 'Привет' })
    const result = run({ tool_name: 'Write', tool_input: { file_path: 'messages/en.json' } })
    assert.equal(result.code, 2)
    assert.ok(result.stderr.includes('ru.json: missing keys present in en.json'))
    assert.ok(result.stderr.includes('actions.save'))
  })
})

describe('locale-parity with a project profile', () => {
  function writeProfile(frontend) {
    mkdirSync(join(projectDir, '.claude'), { recursive: true })
    writeFileSync(
      join(projectDir, '.claude', 'project-profile.md'),
      `# Project profile\n\n## Frontend\n\n${frontend}\n\n## Copy\n\n- messages: \`ignored\`\n`,
    )
  }

  it('reads the catalog directory from `## Frontend`', () => {
    writeProfile('- messages: `i18n/catalogs` — flat, one file per locale')
    mkdirSync(join(projectDir, 'i18n', 'catalogs'), { recursive: true })
    writeFileSync(join(projectDir, 'i18n', 'catalogs', 'en.json'), JSON.stringify({ a: 1, b: 2 }))
    writeFileSync(join(projectDir, 'i18n', 'catalogs', 'ru.json'), JSON.stringify({ a: 1 }))
    const result = run({ tool_name: 'Edit', tool_input: { file_path: 'i18n/catalogs/ru.json' } })
    assert.equal(result.code, 2)
    assert.ok(result.stderr.includes('i18n/catalogs/ru.json: missing keys present in en.json: b'))
  })

  it('stays silent when the profile switches it off', () => {
    writeProfile('- hooks off: `locale-parity`, `metadata-title` — reason')
    writeLocale('en', { greeting: 'Hi', extra: 'x' })
    writeLocale('ru', { greeting: 'Привет' })
    const result = run({ tool_name: 'Write', tool_input: { file_path: 'messages/ru.json' } })
    assert.equal(result.code, 0)
  })
})
