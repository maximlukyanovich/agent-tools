import { execFileSync } from 'node:child_process'
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import assert from 'node:assert/strict'
import { afterEach, beforeEach, describe, it } from 'node:test'

const HOOK = fileURLToPath(new URL('./i18n-keys.mjs', import.meta.url))

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

function write(relativePath, content) {
  const path = join(projectDir, relativePath)
  mkdirSync(dirname(path), { recursive: true })
  writeFileSync(path, content)
}

const edit = (file_path) => ({ tool_name: 'Edit', tool_input: { file_path } })

const CATALOG = {
  Account: { title: 'Профиль', account: { logout: 'Выйти' } },
  Story: { favorite: 'В избранное' },
  Saves: { played: 'играли' },
}

beforeEach(() => {
  projectDir = mkdtempSync(join(tmpdir(), 'hook-i18n-keys-'))
  write('messages/ru.json', JSON.stringify(CATALOG))
  write('messages/en.json', JSON.stringify(CATALOG))
})

afterEach(() => {
  rmSync(projectDir, { recursive: true, force: true })
})

describe('check_i18n_keys', () => {
  it('passes a source file whose keys exist', () => {
    write('src/ok.tsx', `const t = useTranslations('Account')\nt('title')\nt('account.logout')\n`)
    assert.equal(run(edit('src/ok.tsx')).code, 0)
  })

  it('flags a key the catalog does not have, with file:line', () => {
    write('src/menu.tsx', `const ta = useTranslations('Account')\n<span>{ta('logout')}</span>\n`)
    const result = run(edit('src/menu.tsx'))
    assert.equal(result.code, 2)
    assert.ok(result.stderr.includes('src/menu.tsx:2 Account.logout'))
  })

  it('rebinds a translator name per declaration (several components in one file)', () => {
    write(
      'src/two.tsx',
      [
        "function A() { const t = useTranslations('Story'); return t('favorite') }",
        "function B() { const t = useTranslations('Saves'); return t('played') }",
      ].join('\n'),
    )
    assert.equal(run(edit('src/two.tsx')).code, 0)
  })

  it('understands getTranslations with a namespace option and skips template keys', () => {
    write(
      'src/page.tsx',
      "const t = await getTranslations({ locale, namespace: 'Story' })\nt('favorite')\nt(`${mode}.title`)\n",
    )
    assert.equal(run(edit('src/page.tsx')).code, 0)
  })

  it('scans every source file when a catalog is edited', () => {
    write('src/a/deep.tsx', `const t = useTranslations('Saves')\nt('missing')\n`)
    const result = run(edit('messages/ru.json'))
    assert.equal(result.code, 2)
    assert.ok(result.stderr.includes('src/a/deep.tsx:2 Saves.missing'))
  })

  it('stays silent outside its scope', () => {
    write('README.md', '# x')
    assert.equal(run(edit('README.md')).code, 0)
    assert.equal(run({ tool_name: 'Read', tool_input: { file_path: 'src/ok.tsx' } }).code, 0)
  })
})
