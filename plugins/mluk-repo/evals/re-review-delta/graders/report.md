---
type: llm
---

PASS if the final report is pass 2 of the review, covers the one commit after
`aaade77` (the average price in `src/stats.py`), names the division by zero
when the cart is empty or holds no items, and does not raise R1 (`count()` in
`src/cart.py`, deferred as accepted) as a new finding.
FAIL if it reviews the whole branch as a first pass, misses the empty-cart
division, or reports R1 again as new or escalated without a new cause.
