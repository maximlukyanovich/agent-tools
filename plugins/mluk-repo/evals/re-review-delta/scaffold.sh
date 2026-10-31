#!/usr/bin/env bash
# A branch reviewed once (pass 1 on its first commit), then one more commit: the repeat
# review must read only that commit. Fixed dates and author keep every sha the same.
set -euo pipefail
export GIT_AUTHOR_NAME=T GIT_AUTHOR_EMAIL=t@example.com GIT_COMMITTER_NAME=T GIT_COMMITTER_EMAIL=t@example.com
at() { export GIT_AUTHOR_DATE="2026-10-01T10:0$1:00Z" GIT_COMMITTER_DATE="2026-10-01T10:0$1:00Z"; }
git init -q -b main .
git config commit.gpgsign false
printf 'docs/local/\n.origin.git/\n' > .gitignore
mkdir -p .claude src
cat > .claude/project-profile.md <<'PROFILE'
# Project profile

## Repository

- base branch: main
- chain: feature/* → main
- validate: `python3 -m py_compile src/*.py`
- commit confirm: ask

## Review

- ledger: docs/local/reviews/
PROFILE
cat > src/cart.py <<'PY'
def total(items):
    return sum(item["price"] * item["qty"] for item in items)
PY
git add -A; at 0; git commit -q -m "Add the cart total"
git init -q --bare .origin.git
git remote add origin "$PWD/.origin.git"
git push -q origin main
git switch -q -c feat/stats
cat > src/cart.py <<'PY'
def total(items):
    return sum(item["price"] * item["qty"] for item in items)


def count(items):
    return sum(item["qty"] for item in items)
PY
git add -A; at 1; git commit -q -m "Count the items in a cart"
first=$(git rev-parse --short=7 HEAD)
cat > src/stats.py <<'PY'
from cart import count, total


def average_price(items):
    return total(items) / count(items)
PY
git add -A; at 2; git commit -q -m "Average price per item"
mkdir -p docs/local/reviews
cat > docs/local/reviews/feat-stats.md <<LEDGER
# Review ledger — feat-stats
Aliases: feat/stats
Trajectory: P1 $first 0/0/1/0 ready
## Open
## Pass 1 — 2026-10-01 — head $first · base $(git rev-parse --short=7 main) · whole — ready to merge
- R1 minor bug src/cart.py:6 — count() trusts qty to be an int — deferred (accepted: qty is validated at the form)
LEDGER
