---
type: regex
pattern: 'npm run dev\b[\s\S]*npm test|npm test[\s\S]*npm run dev\b'
target:
  source: file
  path: CONTRIBUTING.md
---
