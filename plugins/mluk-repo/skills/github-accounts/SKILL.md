---
name: github-accounts
description: Two GitHub accounts on one machine — personal and work — selected by SSH host alias in the remote URL, never by switching gh's global account; how to recognise the wrong account ("Repository not found") and what to check before a push or gh call. Use before pushing, creating a repository or a PR, or diagnosing a push failure.
---

# github-accounts

The machine holds two GitHub identities. Which one a repository uses is decided
by its **remote URL**, and nothing else.

## How it is set up

- **Personal** → `Host github.com` in `~/.ssh/config` uses the personal key.
  Remote form: `git@github.com:<owner>/<repo>.git`.
- **Work** → `Host github-work` (same `HostName github.com`) uses the work key.
  Remote form: `git@github-work:<owner>/<repo>.git`.

A new repository needs only the right remote form — no per-repository config.
Personal projects live under the personal tree and use the default host; work
repositories on GitHub must use the alias explicitly.

## `gh` is global

`gh`'s active account is machine-wide, and `gh auth git-credential` serves only
the active account regardless of the requested username. Consequences:

- **Never switch `gh`'s active account to make a push work.** Switching it
  breaks the other workspace. Prefer SSH remotes, which do not go through `gh`.
- Before `gh repo create`, `gh pr create` or `gh pr merge`, run
  `gh auth status` and confirm the active account is the one the repository
  belongs to. If it is not, stop and tell the owner — the fix is the owner's
  call, not a silent `gh auth switch`.
- `gh api` and `gh pr view` on a public or shared repository work under either
  account; mutations do not.

## Recognising the wrong account

`remote: Repository not found` on push to a private repository almost always
means the key that authenticated has no access — the remote uses the wrong
host alias. Check `git remote -v` and `ssh -T git@github.com` /
`ssh -T git@github-work` before assuming the repository is missing.

## HTTPS fallback

Only when SSH is unavailable for a host: in that repository's local
`.git/config` set `credential.https://github.com.helper` to `store` (after
resetting the global gh-only chain with an empty value),
`credential.https://github.com.username` to the account, and
`credential.usehttppath` to `false`. Not the normal path.
