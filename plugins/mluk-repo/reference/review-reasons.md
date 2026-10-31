# Why `review` works as it does

For whoever edits `commands/review.md`: the reasons behind its rules, kept
out of the command so a review run does not pay for them. No run reads this
file. A rule changed there changes its reason here.

- **A fresh session.** The session that wrote the code remembers its own
  reasons and tends to confirm them; everything a review needs from the past
  is in the ledger, not in the conversation.
- **Groups on the session's model, not a cheaper default.** On a large diff
  the groups are what reads the code, and the refutation of step 6 drops
  false findings but never recovers missed ones.
- **Blind first.** Reading a previous verdict before the rubric anchors the
  new one to it.
- **Missed findings outside the delta are counted, not listed.** They
  survived the passes that read them, and listing them is what kept a large
  range from converging: each full repeat found a fresh batch of old nits.
- **No `minor` or `nit` stays `open` past the merge.** The ledger lives
  outside git, by branch, so an `open` is lost after the merge, and `next`
  sees only techdebt with a priority.
- **The fix round before the promote.** A fix in the same unmerged branch is
  one commit, one delta and one PR; after the merge it is a new branch, a
  PR, CI and a review.
- **A ready range with old `missed` growth closes, not with another full
  pass.** On a large range a full pass finds a fresh batch of old nits every
  time.
