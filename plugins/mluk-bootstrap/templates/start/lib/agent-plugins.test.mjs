import assert from 'node:assert/strict'
import { execFileSync } from 'node:child_process'
import { mkdirSync, mkdtempSync, realpathSync, rmSync, symlinkSync } from 'node:fs'
import { devNull, tmpdir } from 'node:os'
import path from 'node:path'
import { after, before, describe, it } from 'node:test'

import { declaredPlugins, gitRoot, pluginGaps, realpath } from './agent-plugins.mjs'

// Until the returned function runs, git started from this process reads neither the developer's
// global nor the system config — either may sign commits, run hooks or add ignore rules — nor the
// ignore and attributes files under $XDG_CONFIG_HOME/git/, and never looks for a repository above
// `ceiling`, wherever the temporary folder sits.
function isolateGit(ceiling) {
  const isolated = {
    GIT_CONFIG_GLOBAL: devNull,
    GIT_CONFIG_NOSYSTEM: '1',
    GIT_CONFIG_COUNT: '2',
    GIT_CONFIG_KEY_0: 'core.excludesFile',
    GIT_CONFIG_VALUE_0: devNull,
    GIT_CONFIG_KEY_1: 'core.attributesFile',
    GIT_CONFIG_VALUE_1: devNull,
    GIT_CEILING_DIRECTORIES: ceiling,
  }
  const saved = Object.fromEntries(Object.keys(isolated).map((key) => [key, process.env[key]]))
  Object.assign(process.env, isolated)
  return () => {
    for (const [key, value] of Object.entries(saved)) {
      if (value === undefined) delete process.env[key]
      else process.env[key] = value
    }
  }
}

const here = '/repo'
const settings = {
  enabledPlugins: {
    'mluk-repo@mluk-agent-tools': true,
    'context7@claude-plugins-official': true,
    'code-simplifier@claude-plugins-official': false,
  },
  extraKnownMarketplaces: {
    'mluk-agent-tools': { source: { source: 'github', repo: 'owner/agent-tools' } },
  },
}
const known = [{ name: 'mluk-agent-tools' }, { name: 'claude-plugins-official' }]

describe('declaredPlugins', () => {
  it('keeps only the plugins the settings turn on', () => {
    assert.deepEqual(declaredPlugins(settings), [
      'mluk-repo@mluk-agent-tools',
      'context7@claude-plugins-official',
    ])
  })

  it('reads settings without enabledPlugins as declaring nothing', () => {
    assert.deepEqual(declaredPlugins({}), [])
  })
})

describe('pluginGaps', () => {
  it('reports nothing when every declared plugin is installed for this checkout', () => {
    const installed = [
      { id: 'mluk-repo@mluk-agent-tools', scope: 'project', enabled: true, projectPath: here },
      {
        id: 'context7@claude-plugins-official',
        scope: 'project',
        enabled: true,
        projectPath: here,
      },
    ]
    assert.deepEqual(pluginGaps({ settings, installed, known, projectPath: here }), {
      missing: [],
      turnedOff: [],
      marketplaces: [],
    })
  })

  it('counts a user-wide or managed install, which has no project path', () => {
    const installed = [
      { id: 'mluk-repo@mluk-agent-tools', scope: 'user', enabled: true },
      { id: 'context7@claude-plugins-official', scope: 'managed', enabled: true },
    ]
    assert.deepEqual(pluginGaps({ settings, installed, known, projectPath: here }).missing, [])
  })

  it('counts an install made in a worktree in the main checkout, and the other way round', () => {
    const worktree = '/repo-worktree'
    const installed = [
      {
        id: 'mluk-repo@mluk-agent-tools',
        scope: 'local',
        enabled: true,
        projectPath: worktree,
        gitRoot: here,
      },
      {
        id: 'context7@claude-plugins-official',
        scope: 'project',
        enabled: true,
        projectPath: here,
        gitRoot: here,
      },
    ]
    for (const projectPath of [here, worktree]) {
      assert.deepEqual(
        pluginGaps({ settings, installed, known, projectPath, gitRoot: here }).missing,
        [],
      )
    }
  })

  it('does not count an install recorded for another repository', () => {
    const installed = [
      {
        id: 'mluk-repo@mluk-agent-tools',
        scope: 'project',
        enabled: true,
        projectPath: '/other',
        gitRoot: '/other',
      },
      {
        id: 'context7@claude-plugins-official',
        scope: 'local',
        enabled: true,
        projectPath: here,
        gitRoot: here,
      },
    ]
    assert.deepEqual(
      pluginGaps({ settings, installed, known, projectPath: here, gitRoot: here }).missing,
      ['mluk-repo@mluk-agent-tools'],
    )
  })

  it('does not match two folders outside git by their missing root', () => {
    const installed = [
      {
        id: 'mluk-repo@mluk-agent-tools',
        scope: 'local',
        enabled: true,
        projectPath: '/gone',
        gitRoot: null,
      },
    ]
    assert.deepEqual(
      pluginGaps({ settings, installed, known, projectPath: here, gitRoot: null }).missing,
      ['mluk-repo@mluk-agent-tools', 'context7@claude-plugins-official'],
    )
  })

  it('reports a plugin switched off here apart, not as missing', () => {
    const installed = [
      { id: 'mluk-repo@mluk-agent-tools', scope: 'project', enabled: false, projectPath: here },
      { id: 'context7@claude-plugins-official', scope: 'user', enabled: true },
    ]
    const gaps = pluginGaps({ settings, installed, known, projectPath: here })
    assert.deepEqual(gaps.missing, [])
    assert.deepEqual(gaps.turnedOff, ['mluk-repo@mluk-agent-tools'])
  })

  it('names an unknown marketplace once, and whether the settings declare it', () => {
    const gaps = pluginGaps({ settings, installed: [], known: [], projectPath: here })
    assert.deepEqual(gaps.missing, [
      'mluk-repo@mluk-agent-tools',
      'context7@claude-plugins-official',
    ])
    assert.deepEqual(gaps.marketplaces, [
      { name: 'mluk-agent-tools', declared: true },
      { name: 'claude-plugins-official', declared: false },
    ])
  })

  it('leaves out the marketplaces this machine already knows', () => {
    const gaps = pluginGaps({ settings, installed: [], known, projectPath: here })
    assert.deepEqual(gaps.marketplaces, [])
  })
})

describe('realpath', () => {
  let dir
  before(() => {
    dir = realpathSync(mkdtempSync(path.join(tmpdir(), 'agent-plugins-realpath-')))
  })
  after(() => rmSync(dir, { recursive: true, force: true }))

  it('resolves a symlink, and gives a folder that is gone back as it is', () => {
    mkdirSync(path.join(dir, 'real'))
    symlinkSync(path.join(dir, 'real'), path.join(dir, 'link'))
    assert.equal(realpath(path.join(dir, 'link')), path.join(dir, 'real'))
    assert.equal(realpath(path.join(dir, 'gone')), path.join(dir, 'gone'))
  })
})

// A repository with a subfolder and a worktree on disk: what `git rev-parse` gives each of them.
// The ceiling keeps "outside git" true when the temporary folder itself sits in a repository.
describe('gitRoot', () => {
  let main
  let worktree
  let outside
  let restoreGit
  before(() => {
    main = realpathSync(mkdtempSync(path.join(tmpdir(), 'agent-plugins-')))
    outside = realpathSync(mkdtempSync(path.join(tmpdir(), 'agent-plugins-outside-')))
    worktree = path.join(outside, 'worktree')
    restoreGit = isolateGit(path.dirname(outside))
    const git = (...args) => execFileSync('git', args, { cwd: main, stdio: 'ignore' })
    git('init', '-q')
    git(
      '-c',
      'user.name=t',
      '-c',
      'user.email=t@t',
      'commit',
      '-q',
      '--allow-empty',
      '-m',
      'fixture',
    )
    git('worktree', 'add', '-q', '-b', 'side', worktree)
    mkdirSync(path.join(main, 'sub/folder'), { recursive: true })
  })
  after(() => {
    restoreGit()
    rmSync(main, { recursive: true, force: true })
    rmSync(outside, { recursive: true, force: true })
  })

  it('names the main checkout from itself, a subfolder and a worktree', () => {
    assert.equal(gitRoot(main), main)
    assert.equal(gitRoot(path.join(main, 'sub/folder')), main)
    assert.equal(gitRoot(worktree), main)
  })

  it('is null outside git and for a folder that is gone', () => {
    assert.equal(gitRoot(outside), null)
    assert.equal(gitRoot(path.join(outside, 'gone')), null)
  })
})
