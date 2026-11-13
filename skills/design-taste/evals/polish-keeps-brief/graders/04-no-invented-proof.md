---
type: regex
pattern: '10,000\+|99\.9%|5-star|\b\d{2,}[\d,]*\+? (marinas|harbors|boaters|customers)'
flags: i
match: not_contains
target:
  source: file
  path: index.html
---
