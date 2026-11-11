# Sources

patch had no upstream skill: it follows the owner's own release convention. These release and changelog skills were reviewed against it, and the rows with a note shaped its checks.

Pins are the commits reviewed on 2026-11-11. **Track** marks the sources worth checking for updates; the rest are credited only. No text was copied, so there is no NOTICE.md.

| Source | Path | Pin | License | Track | Contributed |
| --- | --- | --- | --- | --- | --- |
| [jssblck/agents](https://github.com/jssblck/agents) | [skills/tag-release/SKILL.md](https://github.com/jssblck/agents/blob/e1294cd90416/skills/tag-release/SKILL.md) | `e1294cd90416` | GPL-3.0 | yes | Fetching first and treating origin's tags as authoritative. |
| [tobi/qmd](https://github.com/tobi/qmd) | [skills/release/SKILL.md](https://github.com/tobi/qmd/blob/86d2365d17fc/skills/release/SKILL.md) | `86d2365d17fc` | MIT | yes | Turning the `Unreleased` changelog section into the release; leaving internal changes out. |
| [samber/developer-relations-skills](https://github.com/samber/developer-relations-skills) | [skills/changelog-writing/SKILL.md](https://github.com/samber/developer-relations-skills/blob/c3a1b6912791/skills/changelog-writing/SKILL.md) | `c3a1b6912791` | MIT | yes | Keeping the version number honest: a breaking change is a major. |
| [schpet/linear-cli](https://github.com/schpet/linear-cli) | [.claude/skills/release/SKILL.md](https://github.com/schpet/linear-cli/blob/02571d34be66/.claude/skills/release/SKILL.md) | `02571d34be66` | ISC |  | Running the checks before tagging; matching the bump to the changes. |
| [jayden-dang/skills](https://github.com/jayden-dang/skills) | [skills/ship/cut-release/SKILL.md](https://github.com/jayden-dang/skills/blob/71aa50d2cc60/skills/ship/cut-release/SKILL.md) | `71aa50d2cc60` | MIT |  | No tag on a failing build. |
| [jimliu/baoyu-skills](https://github.com/jimliu/baoyu-skills) | [.claude/skills/release-skills/SKILL.md](https://github.com/jimliu/baoyu-skills/blob/ca703c2d7c2c/.claude/skills/release-skills/SKILL.md) | `ca703c2d7c2c` | MIT |  | Flagging breaking changes before choosing the bump. |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | [skills/git-workflow-and-versioning/SKILL.md](https://github.com/addyosmani/agent-skills/blob/301b02b12bff/skills/git-workflow-and-versioning/SKILL.md) | `301b02b12bff` | MIT |  |  |
| [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) | [plugin/skills/version-bump/SKILL.md](https://github.com/thedotmack/claude-mem/blob/19b786b91359/plugin/skills/version-bump/SKILL.md) | `19b786b91359` | Apache-2.0 |  |  |
| [jezweb/claude-skills](https://github.com/jezweb/claude-skills) | [plugins/dev-tools/skills/github-release/SKILL.md](https://github.com/jezweb/claude-skills/blob/1260fa7439b3/plugins/dev-tools/skills/github-release/SKILL.md) | `1260fa7439b3` | MIT |  |  |
| [riekelt/technical-writer](https://github.com/riekelt/technical-writer) | [plugins/technical-writer/skills/writing-changelogs/SKILL.md](https://github.com/riekelt/technical-writer/blob/85e53729dd95/plugins/technical-writer/skills/writing-changelogs/SKILL.md) | `85e53729dd95` | MIT |  |  |
| [wshobson/agents](https://github.com/wshobson/agents) | [plugins/documentation-generation/skills/changelog-automation/SKILL.md](https://github.com/wshobson/agents/blob/9c61ab243def/plugins/documentation-generation/skills/changelog-automation/SKILL.md) | `9c61ab243def` | MIT |  |  |
| [samber/cc-skills](https://github.com/samber/cc-skills) | [skills/conventional-git/SKILL.md](https://github.com/samber/cc-skills/blob/50a33836b20f/skills/conventional-git/SKILL.md) | `50a33836b20f` | MIT |  |  |
| [vercel-labs/autoship](https://github.com/vercel-labs/autoship) | [skills/autoship/SKILL.md](https://github.com/vercel-labs/autoship/blob/0ebe9fdfb743/skills/autoship/SKILL.md) | `0ebe9fdfb743` | Apache-2.0 |  |  |

Considered, not adopted: creating a GitHub Release (the owner's releases are tags only), watching the tag's CI run, and matching tag signing.
