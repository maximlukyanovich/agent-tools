// The Claude Code plugins `.claude/settings.json` declares, against what this machine has installed
// (`claude plugin list --json`) and which marketplaces it knows (`claude plugin marketplace list
// --json`). Tested on its own (agent-plugins.test.mjs): all of it is pure but `realpath` and
// `gitRoot`, which read the disk and are tested on folders there; calling Claude Code stays in
// scripts/agent-plugins.mjs. Template: mluk-bootstrap start v1.
import { execFileSync } from 'node:child_process'
import { realpathSync } from 'node:fs'
import path from 'node:path'

/** A folder's real path, or the folder as given when it is gone. */
export function realpath(dir) {
  try {
    return realpathSync(dir)
  } catch {
    return dir
  }
}

/**
 * The main checkout a folder belongs to — the same for each of its worktrees and subfolders — or
 * `null` outside git and for a folder that is gone. Claude Code matches install records by it.
 */
export function gitRoot(dir) {
  try {
    const commonDir = execFileSync(
      'git',
      ['rev-parse', '--path-format=absolute', '--git-common-dir'],
      { cwd: dir, encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] },
    ).trim()
    return realpath(path.dirname(commonDir))
  } catch {
    return null
  }
}

/** The plugin ids `enabledPlugins` turns on, in the order the settings list them. */
export function declaredPlugins(settings) {
  return Object.entries(settings.enabledPlugins ?? {})
    .filter(([, on]) => on === true)
    .map(([id]) => id)
}

/** The marketplace part of a `plugin@marketplace` id. */
export const marketplaceOf = (id) => id.slice(id.lastIndexOf('@') + 1)

/**
 * What a checkout at `projectPath` lacks. An install counts here the way Claude Code loads its
 * records: user-wide or managed, recorded for `projectPath` itself, or recorded for a folder with
 * the same `gitRoot` — so an install made in the main checkout or in any of its worktrees counts in
 * all of them. Each installed plugin carries the `gitRoot` of its own project path.
 *
 * - `missing` — declared plugins with no install that counts here
 * - `turnedOff` — installed here but switched off (a personal `.claude/settings.local.json`, say);
 *   reported, never reinstalled
 * - `marketplaces` — the marketplaces the missing plugins come from that this machine does not
 *   know yet, each with whether the settings declare it (trusting the folder registers those)
 */
export function pluginGaps({ settings, installed, known, projectPath, gitRoot }) {
  const here = installed.filter(
    (plugin) =>
      plugin.scope === 'user' ||
      plugin.scope === 'managed' ||
      plugin.projectPath === projectPath ||
      (gitRoot != null && plugin.gitRoot === gitRoot),
  )
  const missing = []
  const turnedOff = []
  for (const id of declaredPlugins(settings)) {
    const installs = here.filter((plugin) => plugin.id === id)
    if (!installs.length) missing.push(id)
    else if (installs.every((plugin) => plugin.enabled === false)) turnedOff.push(id)
  }

  const knownNames = new Set(known.map((marketplace) => marketplace.name))
  const marketplaces = [...new Set(missing.map(marketplaceOf))]
    .filter((name) => !knownNames.has(name))
    .map((name) => ({ name, declared: Boolean(settings.extraKnownMarketplaces?.[name]) }))

  return { missing, turnedOff, marketplaces }
}
