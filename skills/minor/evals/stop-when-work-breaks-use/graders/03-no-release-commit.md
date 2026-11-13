---
type: regex
pattern: '^v?(0\.5|1\.0)\.0 - '
flags: m
match: not_contains
target:
  source: file
  path: .git/COMMIT_EDITMSG
---
