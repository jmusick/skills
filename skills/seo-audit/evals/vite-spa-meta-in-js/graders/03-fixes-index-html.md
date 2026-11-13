---
type: regex
pattern: '<title>\s*Vite App\s*</title>'
match: not_contains
target:
  source: file
  path: index.html
---
