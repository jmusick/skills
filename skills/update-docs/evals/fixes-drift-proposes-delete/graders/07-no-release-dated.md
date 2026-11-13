---
type: regex
pattern: '## \[0\.(3\.[1-9]|4\.0)\]'
match: not_contains
target:
  source: file
  path: CHANGELOG.md
---
