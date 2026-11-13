---
type: regex
pattern: 'co-authored-by|generated with|claude'
flags: i
match: not_contains
target:
  source: file
  path: .git/COMMIT_EDITMSG
---
