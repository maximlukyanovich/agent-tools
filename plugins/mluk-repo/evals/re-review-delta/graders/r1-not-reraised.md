---
type: regex
target: { source: file, path: docs/local/reviews/feat-stats.md }
pattern: '## Pass 2[\s\S]*\bR1\b[^\n]*\b(new|escalated)\b'
match: not_contains
---
