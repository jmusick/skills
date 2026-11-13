---
type: regex
pattern: '<div[^>]*onclick'
match: not_contains
target:
  source: file
  path: index.html
---
