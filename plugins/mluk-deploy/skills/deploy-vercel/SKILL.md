---
name: deploy-vercel
description: How a Next.js front of a personal project is deployed on Vercel — one project per long-lived environment, production branch and previews, function region, env vars per environment, custom domains with Cloudflare as DNS only, gating a staging site, and the Hobby-plan limits. Use when creating or changing a Vercel project, its env vars or domains.
---

# deploy-vercel

## Projects and branches

- **One Vercel project per long-lived environment** (`<project>-staging`, `<project>-production`),
  each with its own Production Branch (`staging`, `main`) and its own env vars and domain. Pull
  requests get preview deployments inside the project they target.
- **The production project is created when production is set up**, not earlier. The apex domain is
  not attached to anything before that.
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

The Hobby plan cannot password-protect a production URL. A staging project's own production domain is
public, so staging is gated in the app:
- basic auth in the proxy/middleware, driven by env vars and off when they are absent;
- the same check in route handlers that the middleware matcher skips (`/api/*`). Otherwise the API
  proxy stays open behind the password page.

## Plan limits

Hobby is for non-commercial use only. A project that takes money moves to Pro before production opens.
Check the function duration limit against the slowest proxied request (set `maxDuration` on that route
handler).
