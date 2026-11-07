#!/usr/bin/env bash
# A branch of two commits a review read and sent back with one major, and the fix for it in
# the working tree, uncommitted. The first round of review fixes is a new commit on top, not
# an amend of the reviewed commit. Fixed dates and author keep every sha the same.
set -euo pipefail
export GIT_AUTHOR_NAME=T GIT_AUTHOR_EMAIL=t@example.com GIT_COMMITTER_NAME=T GIT_COMMITTER_EMAIL=t@example.com
at() { export GIT_AUTHOR_DATE="2026-10-01T10:0$1:00Z" GIT_COMMITTER_DATE="2026-10-01T10:0$1:00Z"; }
git init -q -b main .
git config commit.gpgsign false
git config user.name T
git config user.email t@example.com
printf 'docs/local/\n.origin.git/\n' > .gitignore
mkdir -p .claude src
cat > .claude/project-profile.md <<'PROFILE'
# Project profile

## Repository

- base branch: main
- chain: feature/* → main
- validate: `python3 -m py_compile src/*.py`
- commit preset: gitmoji-conventional
- commit confirm: auto
- amend unpushed: yes

## Review

- ledger: docs/local/reviews/
PROFILE
cat > src/cart.py <<'PY'
def total(items):
    return sum(item["price"] * item["qty"] for item in items)


def count(items):
    return sum(item["qty"] for item in items)
PY
git add -A; at 0; git commit -q -m ":tada: feat(cart): Add the cart total and count"
git init -q --bare .origin.git
git remote add origin "$PWD/.origin.git"
git push -q origin main
git switch -q -c feat/stats
cat > src/labels.py <<'PY'
def label(items):
    return f"{len(items)} items"
PY
git add -A; at 1; git commit -q -m ":sparkles: feat(stats): Label the cart" -m "- The cart page names how many items it holds"
cat > src/stats.py <<'PY'
from cart import count, total


def average_price(items):
    return total(items) / count(items)
PY
git add -A; at 2; git commit -q -m ":sparkles: feat(stats): Average price per item" -m "- The cart page shows the average price of its items"
reviewed=$(git rev-parse --short=7 HEAD)
mkdir -p docs/local/reviews
cat > docs/local/reviews/feat-stats.md <<LEDGER
# Review ledger — feat-stats
Aliases: feat/stats
Trajectory: P1 $reviewed 0/1/0/0 changes
## Open
- R1 major bug src/stats.py:5 — an empty cart divides by zero
## Pass 1 — 2026-10-01 — head $reviewed · base $(git rev-parse --short=7 main) · whole — changes requested
- R1 major bug src/stats.py:5 — an empty cart divides by zero — open
LEDGER
cat > src/stats.py <<'PY'
from cart import count, total


def average_price(items):
    quantity = count(items)
    return total(items) / quantity if quantity else 0
PY
