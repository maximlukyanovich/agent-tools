# mluk-design

For projects that are built against a design kit. Enable it only there.

## Install

```bash
claude plugin install mluk-design --marketplace maximlukyanovich/agent-tools --scope project
```

Other scopes and updating: [`docs/updates.md`](../../docs/updates.md).

## Skills

| Skill | For |
| --- | --- |
| [`design-decisions`](skills/design-decisions/SKILL.md) | how new design is drawn for the owner's decision: an inventory of the kit and the app first, component variants beside whole concepts, one element per question, every frame looked at before publishing |
| [`design-port`](skills/design-port/SKILL.md) | how a kit is ported: the source read at write time, kit classes worn by a matching third-party primitive, the stretched-link card, real data over demo data, and what to do when the kit itself is wrong |

`/mluk-design:help` introduces the plugin and checks whether the project names a design source.

Project specifics — which kit, its artifact URLs, the paths — stay in the project.

## In use

Nothing to invoke: with the plugin on, a request like "build the pricing
section from the kit" loads `design-port`, and the agent reads the kit's source
as it writes instead of recalling it; "draw variants of the settings screen"
loads `design-decisions`.
