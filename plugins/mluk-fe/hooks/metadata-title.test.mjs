import { execFileSync } from 'node:child_process'
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import assert from 'node:assert/strict'
import { afterEach, beforeEach, describe, it } from 'node:test'

const HOOK = fileURLToPath(new URL('./metadata-title.mjs', import.meta.url))

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

function writeSource(relative, content) {
  const absolute = join(projectDir, relative)
  mkdirSync(dirname(absolute), { recursive: true })
  writeFileSync(absolute, content)
  return relative
}

beforeEach(() => {
  projectDir = mkdtempSync(join(tmpdir(), 'hook-metadata-title-'))
})

afterEach(() => {
  rmSync(projectDir, { recursive: true, force: true })
})

describe('check_metadata_title hook', () => {
  it('exits 0 for files outside the app route tree', () => {
    const file = writeSource('src/modules/foo.tsx', "export const metadata = { title: 'Acme' };\n")
    const result = run({ tool_name: 'Write', tool_input: { file_path: file } })
    assert.equal(result.code, 0)
  })

  it('exits 0 when the title is built via getTranslations', () => {
    const file = writeSource(
      'src/app/[locale]/catalog/page.tsx',
      [
        "import type { Metadata } from 'next';",
        '',
        'export async function generateMetadata(): Promise<Metadata> {',
        "  const t = await getTranslations({ locale: 'ru', namespace: 'Catalog' });",
        "  return { title: t('title') };",
        '}',
      ]
        .join('\n')
        .concat('\n'),
    )
    const result = run({ tool_name: 'Write', tool_input: { file_path: file } })
    assert.equal(result.code, 0)
    assert.equal(result.stderr, '')
  })

  it('exits 2 on `export const metadata: Metadata = { title: "X" }`', () => {
    const file = writeSource(
      'src/app/[locale]/catalog/page.tsx',
      [
        "import type { Metadata } from 'next';",
        '',
        "export const metadata: Metadata = { title: 'Catalog — Quest Bot' };",
        '',
        'export default function Page() { return null; }',
      ]
        .join('\n')
        .concat('\n'),
    )
    const result = run({ tool_name: 'Write', tool_input: { file_path: file } })
    assert.equal(result.code, 2)
    assert.ok(result.stderr.includes('metadata-title'))
    assert.ok(result.stderr.includes('src/app/[locale]/catalog/page.tsx:'))
  })

  it('exits 2 on a hardcoded literal returned from generateMetadata', () => {
    const file = writeSource(
      'src/app/[locale]/saves/page.tsx',
      [
        "import type { Metadata } from 'next';",
        '',
        'export async function generateMetadata(): Promise<Metadata> {',
        "  return { title: 'Saves' };",
        '}',
      ]
        .join('\n')
        .concat('\n'),
    )
    const result = run({ tool_name: 'Write', tool_input: { file_path: file } })
    assert.equal(result.code, 2)
    assert.ok(result.stderr.includes('metadata-title'))
  })

  it('does not flag unrelated `title:` keys outside metadata blocks', () => {
    const file = writeSource(
      'src/app/[locale]/catalog/page.tsx',
      [
        "function Icon({ title }: { title: string }) { return <svg title='Logo' />; }",
        '',
        'export default function Page() { return null; }',
      ]
        .join('\n')
        .concat('\n'),
    )
    const result = run({ tool_name: 'Write', tool_input: { file_path: file } })
    assert.equal(result.code, 0)
  })
})

describe('metadata-title with a project profile', () => {
  it('reads the app root from `## Frontend` (a project without src/)', () => {
    writeSource('.claude/project-profile.md', '## Frontend\n\n- app: `app`\n')
    const file = writeSource(
      'app/[locale]/page.tsx',
      "export const metadata: Metadata = {\n  title: 'Home',\n}\n",
    )
    const result = run({ tool_name: 'Write', tool_input: { file_path: file } })
    assert.equal(result.code, 2)
    assert.ok(result.stderr.includes('app/[locale]/page.tsx:2'))
  })
})
