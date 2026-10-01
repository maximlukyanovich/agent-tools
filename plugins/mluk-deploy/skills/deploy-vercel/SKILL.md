---
name: deploy-vercel
description: How a Next.js front of a personal project is deployed on Vercel — one project per long-lived environment, production branch and previews, function region, env vars per environment, custom domains with Cloudflare as DNS only, gating a staging site, and the Hobby-plan limits. Use when creating or changing a Vercel project, its env vars or domains.
---

# deploy-vercel

## Projects and branches

- **One Vercel project for staging and production** (the Hobby way; Custom Environments are Pro):
  - **Production Branch = `main`**, set right after import — Vercel picks the repository's default
    branch (often `develop`) otherwise;
  - **staging is a Preview deployment of the `staging` branch**, with its own domain assigned to that
    Git branch (`staging.example.com` → Git Branch `staging`);
  - pull requests get previews in the same project and use the Preview env vars too.
- **The project needs a first deploy before a branch domain resolves.** A branch created before the
  project has no deployment until something is pushed or "Create Deployment" is run with its name.
- **Remove the automatic `<project>.vercel.app` production domain** when the project has its own
  domains. Per-deployment URLs stay; they are covered by the app's own gate and noindex header.
- **Production is gated and noindex until launch**: Production env gets only the gate and
  `ALLOW_INDEXING=false`, so a push to `main` cannot expose anything.
- **Function region `fra1`** in `vercel.json` (`{"regions": ["fra1"]}`) when the backend and the
  users are in Europe. The default is `iad1`: every server-side call would cross the Atlantic, and
  personal data would leave the EU.

## Env vars

- **Set per environment** (Production / Preview) in the project, never in git. The project keeps a
  documented `.env.example`.
- **`NEXT_PUBLIC_*` are inlined at build time.** Changing one needs a redeploy, not a restart.
- **Indexing is an explicit flag** (e.g. `NEXT_PUBLIC_ALLOW_INDEXING=true` only in production).
  Everything else serves `noindex` and a disallowing `robots.txt`.
- **A front that proxies the API server-side** (`/api/*` route handlers forwarding cookies) needs only
  the API's base URL. The browser never calls the API host, so CORS and cookie domains stay out of it.

## Domains

- The domain is added in the project, and the DNS record points at Vercel (`CNAME
  cname.vercel-dns.com` for a subdomain, Vercel's `A` for an apex).
- **Behind Cloudflare, Vercel records are DNS only** (grey cloud). Proxying Vercel through Cloudflare
  is CDN-over-CDN, and it breaks Vercel's certificate issuance and verification.
- **`www` → apex redirect** is set in the Vercel domain settings.

## Gating a staging site

The Hobby plan cannot password-protect a custom domain, so staging is gated in the app:
- **basic auth in the proxy/middleware** (Next 16 `proxy.ts`, Node runtime): a list of users as JSON in
  one env var (`{"user":"password",…}`), so each person is added or removed on their own. It is off
  when the variable is absent;
- **the gate covers `/api/*` too** (include it in the matcher and skip only i18n for it). Otherwise the
  API proxy stays open behind the password page;
- **Vercel Authentication (Deployment Protection) off**: with it on, branch domains ask for a Vercel
  login of the team, and testers outside the team cannot get in;
- **an `X-Robots-Tag: noindex, nofollow` header** from `next.config` `headers()` while indexing is off,
  on top of robots.txt and the page metadata.

## Plan limits

Hobby is for non-commercial use only. A project that takes money moves to Pro before production opens.
Check the function duration limit against the slowest proxied request (set `maxDuration` on that route
handler).
