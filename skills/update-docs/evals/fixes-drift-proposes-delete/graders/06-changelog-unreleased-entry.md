---
type: regex
pattern: '## \[Unreleased\]\s*\n(?:(?!## \[)[\s\S])*/health(?:(?!## \[)[\s\S])*\n## \[0\.3\.0\] - 2026-09-14'
target:
  source: file
  path: CHANGELOG.md
---
