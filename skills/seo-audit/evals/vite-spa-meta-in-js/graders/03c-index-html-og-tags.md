---
type: regex
pattern: 'og:title[\s\S]*og:description|og:description[\s\S]*og:title'
target:
  source: file
  path: index.html
---
