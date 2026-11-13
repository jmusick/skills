---
type: regex
pattern: 'user-scalable=no|maximum-scale=1\b'
match: not_contains
target:
  source: file
  path: index.html
---
