---
type: regex
pattern: '"version": "0\.5\.0"'
match: count:2
target:
  source: file
  path: package-lock.json
---
