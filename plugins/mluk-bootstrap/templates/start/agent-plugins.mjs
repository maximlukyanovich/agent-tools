// The Claude Code plugins `.claude/settings.json` declares that this machine has not installed for
// this checkout. Committed settings turn a plugin on for everyone but do not download it: Claude
// Code registers a declared marketplace once the folder is trusted, and each collaborator installs
// the plugins once. The `/start` command runs this first.
//
// Template: mluk-bootstrap start v1 — copied by /mluk-bootstrap:setup into a folder one level below
// the repository root, with lib/ beside it; /mluk-bootstrap:audit compares the version. Node 20.11+.
//
//   node scripts/agent-plugins.mjs             report; exits 1 when a declared plugin is missing
//   node scripts/agent-plugins.mjs --install   install the missing plugins whose marketplace this
//                                              machine knows
//
// Plugins are installed at local scope: the settings already turn them on, and a project-scope
// install rewrites the committed settings.json (key order, formatting). Marketplaces are not added
// from here — a local declaration would lack the committed `autoUpdate`; trusting the folder
// registers them as declared. A session that is already open loads new plugins after
// `/reload-plugins`.
import { execFileSync, spawnSync } from 'node:child_process'
import { readFileSync } from 'node:fs'
import path from 'node:path'

import {
  declaredPlugins,
  gitRoot,
  marketplaceOf,
  pluginGaps,
  realpath,
} from './lib/agent-plugins.mjs'

const root = path.resolve(import.meta.dirname, '..')
const install = process.argv.slice(2).includes('--install')

/** A `claude` subcommand's JSON output, or `null` when Claude Code is not on PATH. */
function claudeJson(args) {
  try {
    return JSON.parse(execFileSync('claude', args, { cwd: root, encoding: 'utf8' }))
  } catch (error) {
    if (error.code === 'ENOENT') return null
    throw error
  }
}

function claude(args) {
  console.log(`\n$ claude ${args.join(' ')}`)
  return spawnSync('claude', args, { cwd: root, stdio: 'inherit' }).status === 0
}

const settings = JSON.parse(readFileSync(path.join(root, '.claude', 'settings.json'), 'utf8'))
const installed = claudeJson(['plugin', 'list', '--json'])
if (installed === null) {
  console.log('Claude Code is not on PATH — the plugins in .claude/settings.json are for it alone.')
  process.exit(0)
}
const known = claudeJson(['plugin', 'marketplace', 'list', '--json'])

// An install is recorded for the folder it ran in — a worktree's own path when run there — and
// counts in every checkout of the same repository, as Claude Code reads it.
const roots = new Map()
const rootOf = (dir) => {
  if (!roots.has(dir)) roots.set(dir, gitRoot(dir))
  return roots.get(dir)
}
const { missing, turnedOff, marketplaces } = pluginGaps({
  settings,
  installed: installed.map((plugin) => ({
    ...plugin,
    projectPath: plugin.projectPath && realpath(plugin.projectPath),
    gitRoot: plugin.projectPath ? rootOf(plugin.projectPath) : null,
  })),
  known,
  projectPath: realpath(root),
  gitRoot: rootOf(root),
})

for (const id of turnedOff) console.log(`Turned off here, left alone: ${id}`)
if (!missing.length) {
  console.log(
    `Claude Code plugins: all ${declaredPlugins(settings).length} that .claude/settings.json declares are installed.`,
  )
  process.exit(0)
}
console.log(`Missing for this checkout:\n${missing.map((id) => `  ${id}`).join('\n')}`)
for (const { name, declared } of marketplaces) {
  console.log(
    declared
      ? `Unknown marketplace: ${name} — start Claude Code at the repository root and trust the folder; that registers it`
      : `Unknown marketplace: ${name} — declare it under extraKnownMarketplaces in .claude/settings.json`,
  )
}
if (!install) {
  console.log('\nInstall them: node scripts/agent-plugins.mjs --install')
  process.exit(1)
}

const unknown = new Set(marketplaces.map(({ name }) => name))
const failed = missing.filter(
  (id) => unknown.has(marketplaceOf(id)) || !claude(['plugin', 'install', id, '--scope', 'local']),
)
if (failed.length) {
  console.error(`\nNot installed:\n${failed.map((id) => `  ${id}`).join('\n')}`)
  process.exit(1)
}
console.log('\nInstalled. A session that is already open loads them after /reload-plugins.')
