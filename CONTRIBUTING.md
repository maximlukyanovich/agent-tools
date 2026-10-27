# Contributing

Issues and pull requests are welcome — a rule that misfired in your project, a
trap worth naming, a fix.

- Plugin texts, commits and pull requests are in English (the business-Russian
  skill is the one exception: its subject is Russian).
- A rule that names your project's paths, ids or design system belongs in your
  project's profile, not here.
- A change to a plugin's files, its README aside, raises that plugin's
  `version` in `plugin.json` — the levels are in [`AGENTS.md`](AGENTS.md) §1.
  Without the raise the change reaches nobody.
- Before opening a pull request, run the checks in
  [`AGENTS.md`](AGENTS.md) §3, and run the changed command or skill once in a
  real repository — say in the pull request where and how. To try a plugin
  straight from a checkout, without installing: `claude --plugin-dir
  <checkout>/plugins`.

The conventions — commit format, command naming, descriptions — are in
[`AGENTS.md`](AGENTS.md) §2 and the repository layout in §4; the model behind
the plugins is in [`docs/design.md`](docs/design.md).
