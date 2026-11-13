---
type: regex
pattern: '\bLAKE_API_KEY\b'
match: not_contains
target:
  source: file
  path: README.md
---
