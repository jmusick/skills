---
type: regex
pattern: '^#+ .*\b20\d\d-\d\d-\d\d\b'
flags: m
match: not_contains
target:
  source: file
  path: firelands-current/docs/news-sources.md
---
