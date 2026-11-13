---
type: regex
pattern: '^v?1\.\d+\.\d+ - '
flags: m
match: not_contains
target:
  source: file
  path: .git/COMMIT_EDITMSG
---
