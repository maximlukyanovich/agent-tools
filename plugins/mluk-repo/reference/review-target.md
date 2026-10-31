# review_target.py

Sets the target of a review pass from the ledger's last head, `HEAD` and
the arguments (`commands/review.md`, step 2). Run it; this file is its
contract.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/review_target.py" --ledger <file> \
  [--tree <dir>] [--head <rev>] [--full] [--range <a>..<b>]
```

- **Ledger** — the branch's ledger file, named as `review` names it, not
  the profile's `ledger` folder; a missing file is no ledger. Its last head is the `head <sha>` of the last
  `## Pass` header, else the last `P<n> <sha>` of `Trajectory:`.
- **Tree** — the tree under review, for `git -C`; the current directory by
  default. **Head** — `HEAD` of that tree unless given.
- **`--full`** ignores the ledger; **`--range`** outranks both.

## Output

One line on stdout, exit 0 — the mode, the diff to read, the reason:

```
target: none · head 9f8e7d6 — the ledger's last head is HEAD
target: delta · git diff e4f5a6b..9f8e7d6 — the last head is an ancestor of HEAD
target: rewritten · git diff e4f5a6b 9f8e7d6 · replaced a1b2c3d e4f5a6b — the last head is not an ancestor of HEAD
target: range · git diff a1b2c3d..9f8e7d6 — explicit range
target: whole — no ledger
```

- `none` — nothing new since the last pass.
- `delta`, `range` — the commits between the two.
- `rewritten` — the fixes went into the commits the last pass reviewed
  (`git-safety`, "Amending"), or a range's base is no longer an ancestor of
  its head: the diff between the two trees, which the reflog keeps
  resolvable; `replaced` lists the old commits the new history no longer
  holds, for the pass header.
- `whole` — the command's own whole target, the branch against its base;
  the reason is `no ledger`, `the ledger has no pass`, `full`, or
  `the last head <sha> is not in the repository`.

Exit 2, with the reason on stderr, when the head or the range does not
resolve, a range is not `<a>..<b>`, or the ledger is a directory.
