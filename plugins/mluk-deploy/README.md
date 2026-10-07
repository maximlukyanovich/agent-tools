# mluk-deploy

How a project is deployed. Knowledge only: skills, no hooks, no commands. Enable it in any
project that deploys; working on a live server additionally needs `mluk-ops`.

| Skill | For |
| --- | --- |
| [`deploy-vps`](skills/deploy-vps/SKILL.md) | a Docker Compose backend on a VPS behind Caddy, deployed by GitHub Actions |
| [`deploy-vercel`](skills/deploy-vercel/SKILL.md) | a Next.js front on Vercel: projects, env vars, domains, staging gate |
| [`domain-dns`](skills/domain-dns/SKILL.md) | moving DNS to Cloudflare without breaking mail; subdomain naming; mail roles |

The concrete files live in the project (compose, scripts, Caddy sites, runbook). The skills carry the
reasoning and the traps.
