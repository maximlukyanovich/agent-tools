# Phase 2: the target layout

```
AGENTS.md                     canonical project rules. In git. Any agent reads it
CLAUDE.md                     thin layer: @AGENTS.md plus Claude specifics. In git
.claude/
  README.md                   map of the directory: what is where, who runs it
  COMMANDS.md                 the command index — library commands and local overrides. Here, not in commands/
  project-profile.md          what the library plugins read: repository, docs, task, checks, review, sources, copy
  project-profile.local.md    this clone's overrides: a fork's trunk, local paths of siblings. Gitignored
  settings.json               shared settings: enabledPlugins, attribution, allowed MCP, hooks. In git
  settings.local.json         personal permissions. Gitignored
  commands/                   local overrides only. Command files only — no README here
  skills/                     the source of truth for project skills. In git
    README.md                 skill index — the subdirectory is not scanned, safe here
    <name>-local/             personal skills. Gitignored by suffix
  hooks/                      PostToolUse and friends. In git
    README.md                 exit-code contract, how to add one
  hooks-local/                personal checks. Gitignored except README
.agents/
  skills/<name>               symlinks to .claude/skills/<name>. Cross-agent convention
.mcp.json.example             MCP servers with ${VAR} placeholders. In git
.mcp.json                     generated. Gitignored
.env.example                  variable template. In git
.env                          real values. Gitignored
docs/
  README.md                   documentation index plus file conventions
  local/README.md             the personal space, the only committed file inside
```

Matching `.gitignore`:

```gitignore
# agent harness: share the project surface, keep the personal part local
.claude/*
!.claude/commands/
!.claude/skills/
!.claude/settings.json
!.claude/hooks/
!.claude/README.md
!.claude/COMMANDS.md
!.claude/project-profile.md
.claude/skills/*-local/
.claude/hooks-local/*
!.claude/hooks-local/README.md
.claude/settings.local.json
.mcp.json
.env

# docs/local — personal space, except its README
docs/local/*
!docs/local/README.md
```

`.claude/*` with a whitelist keeps `project-profile.local.md` out without a line
of its own. A repository whose `.gitignore` lists exclusions one by one instead
adds `.claude/project-profile.local.md` explicitly.

`settings.json` declares where the library comes from and enables it:

```json
{
  "extraKnownMarketplaces": {
    "mluk-agent-tools": {
      "source": { "source": "github", "repo": "maximlukyanovich/agent-tools" },
      "autoUpdate": true
    }
  },
  "enabledPlugins": { "mluk-repo@mluk-agent-tools": true },
  "attribution": { "commit": "", "pr": "" }
}
```

Without `extraKnownMarketplaces` the plugins resolve only on a machine whose
user settings already know the marketplace — a collaborator who clones the
repository gets "enabled but not installed" with nowhere to install from. With
it, trusting the folder makes the marketplace known; each enabled plugin is then
installed once (`claude plugin install <name>@mluk-agent-tools --scope project`).
GitHub is the one source for everyone, the author included: a library change
reaches a project once pushed to the library's `main`. The repository is
private, so a collaborator needs read access.

## Two traps that cost a rewrite

**The command index goes in `.claude/COMMANDS.md`, not in `commands/`.** Claude
Code registers **every** `.md` inside `commands/` as a slash command — including
`README.md`. It lands in the command list, is paid for in every session, and
looks like a command it is not. `.claude/` itself is not scanned, so the index
moves one floor up. `COMMANDS.md` lists the library commands the project uses
as they are, and the local overrides with the reason for each.

The limitation applies **only** to `commands/`. `skills/` is scanned for
subdirectories containing `SKILL.md`, and `hooks/` is not scanned at all — so
`skills/README.md` and `hooks/README.md` are harmless and stay next to what they
describe.

**Skills are real directories in `.claude/skills/`, and `.agents/skills/<name>`
are symlinks to them — that direction, not the reverse.** Claude Code does not
resolve symlinks when scanning `.claude/skills/`, and custom skills simply vanish
from the list. Always edit the files under `.claude/skills/`; create the link
once:

```bash
ln -s ../../.claude/skills/<name> .agents/skills/<name>
```
