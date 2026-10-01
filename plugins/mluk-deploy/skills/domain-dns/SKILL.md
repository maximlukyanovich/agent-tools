---
name: domain-dns
description: Moving a domain's authoritative DNS to Cloudflare without breaking the mail the registrar hosts — export and diff the zone, MX/SPF/DKIM/DMARC as DNS only, CAA and DNSSEC before the nameserver switch, which records to proxy — plus naming environments on subdomains and separating transactional and marketing mail. Use when adding or moving a domain, its DNS records or mail.
---

# domain-dns

## Moving the zone to Cloudflare

The registrar may stay the registrar; only the nameservers move. Nothing is switched blind.

1. **Export the current zone** from the registrar and keep the file: it is the rollback point.
2. **Add the domain in Cloudflare** and compare its imported records line by line with the export.
   The automatic import misses records.
3. **Mail records stay exactly as exported and DNS only:**
   - MX;
   - SPF (`TXT v=spf1 …`);
   - DKIM (`TXT` or `CNAME` under `*._domainkey`);
   - DMARC (`_dmarc`, start with `p=none; rua=mailto:…`);
   - autodiscover and autoconfig.

   Take the values from the export, never from memory or a provider's generic docs.
4. **CAA.** If present, it must allow every CA in use: `letsencrypt.org` for Caddy and Vercel, plus
   Cloudflare's CAs if its edge certificates are used. Or have no CAA at all.
5. **DNSSEC.** Turn it off at the registrar before the switch and wait out the DS record's TTL. A DS
   pointing at the old nameservers makes the domain stop resolving. Re-enable it in Cloudflare after.
6. **Lower TTLs a day ahead**, then switch the nameservers at the registrar.
7. **Verify:**
   - `dig MX/TXT/CNAME` against `1.1.1.1` and `8.8.8.8`;
   - a mail sent to and from a mailbox on the domain;
   - every site and its certificate.

## Proxied or DNS only

| Record | Mode | Why |
| --- | --- | --- |
| Mail (MX, SPF, DKIM, DMARC, autodiscover) | DNS only | mail cannot go through the proxy |
| Vercel (apex, `www`, `staging`) | DNS only | Vercel is a CDN already; the proxy breaks its certificates |
| API on a VPS | DNS only **while any request can exceed 100 s** | Cloudflare cuts proxied requests at 100 s (524) on non-Enterprise plans |
| API on a VPS, all requests fast | Proxied, SSL **Full (strict)** | never Flexible: redirect loops and broken CSRF |

With the API proxied, the origin can additionally accept only Cloudflare's IP ranges.

## Naming

- **Environments are flat subdomains:** `api.example.com`, `api-staging.example.com`,
  `staging.example.com`. Cloudflare's free Universal SSL covers one level only, so
  `api.staging.example.com` gets no edge certificate.
- **A new environment can start before the zone moves.** An `A` record at the registrar's DNS plus
  Let's Encrypt on the origin works. The record is imported with the zone later.

## Mail roles

- **People** (hello@, support@) use the registrar's mailbox or a workspace.
- **Transactional** (sign-up codes, password reset) uses a transactional provider (Resend, Postmark)
  over SMTP from a subdomain (`no-reply@notify.example.com`), with its own SPF/DKIM/DMARC. It is
  never the people's mailbox SMTP. Staging catches mail in Mailpit instead.
- **Marketing** uses a separate service and a separate subdomain (`news.example.com`), so its
  reputation cannot hurt the transactional one.
