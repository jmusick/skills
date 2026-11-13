---
type: regex
pattern: '<img(?=[^>]*\balt="[^"]+")(?=[^>]*\bwidth=)(?=[^>]*\bheight=)[^>]*>'
target:
  source: file
  path: index.html
---
