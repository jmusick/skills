# Sources

issue had no upstream skill. These issue-to-PR skills were reviewed against it. Its release steps (8 and 9) mirror /patch and /minor, so their changelog and remote-tag checks come from the first two rows.

Pins are the commits reviewed on 2026-11-11. **Track** marks the sources worth checking for updates; the rest are credited only. No text was copied, so there is no NOTICE.md.

| Source | Path | Pin | License | Track | Contributed |
| --- | --- | --- | --- | --- | --- |
| [jssblck/agents](https://github.com/jssblck/agents) | [skills/tag-release/SKILL.md](https://github.com/jssblck/agents/blob/e1294cd90416/skills/tag-release/SKILL.md) | `e1294cd90416` | GPL-3.0 |  | Checking origin's tags before tagging. |
| [tobi/qmd](https://github.com/tobi/qmd) | [skills/release/SKILL.md](https://github.com/tobi/qmd/blob/86d2365d17fc/skills/release/SKILL.md) | `86d2365d17fc` | MIT |  | Turning the `Unreleased` changelog section into the release. |
| [open-mercato/skills](https://github.com/open-mercato/skills) | [skills/om-auto-fix-issue/SKILL.md](https://github.com/open-mercato/skills/blob/951342107718/skills/om-auto-fix-issue/SKILL.md) | `951342107718` | MIT | yes | Reproducing a bug before fixing it, and stopping when it's already fixed. |
| [fandhe-ai/agent-cli-skills](https://github.com/fandhe-ai/agent-cli-skills) | [skills/implement-issue/SKILL.md](https://github.com/fandhe-ai/agent-cli-skills/blob/de592144c879/skills/implement-issue/SKILL.md) | `de592144c879` | none stated | yes | Tracking out-of-scope findings; quoting fresh check results. |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | [skills/git-workflow-and-versioning/SKILL.md](https://github.com/addyosmani/agent-skills/blob/301b02b12bff/skills/git-workflow-and-versioning/SKILL.md) | `301b02b12bff` | MIT |  | Listing what was deliberately left alone. |
| [mattpocock/skills](https://github.com/mattpocock/skills) | [skills/engineering/wayfinder/SKILL.md](https://github.com/mattpocock/skills/blob/4ae2317ddb22/skills/engineering/wayfinder/SKILL.md) | `4ae2317ddb22` | MIT |  | Keeping out-of-scope work visible instead of doing it. |
| [giuseppe-trisciuoglio/developer-kit](https://github.com/giuseppe-trisciuoglio/developer-kit) | [plugins/developer-kit-core/skills/github-issue-workflow/SKILL.md](https://github.com/giuseppe-trisciuoglio/developer-kit/blob/fe73fb33a09e/plugins/developer-kit-core/skills/github-issue-workflow/SKILL.md) | `fe73fb33a09e` | MIT |  |  |
| [github/awesome-copilot](https://github.com/github/awesome-copilot) | [skills/make-repo-contribution/SKILL.md](https://github.com/github/awesome-copilot/blob/eaaffd5d020b/skills/make-repo-contribution/SKILL.md) | `eaaffd5d020b` | MIT |  |  |
| [code-yeongyu/oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent) | [.agents/skills/work-with-pr/SKILL.md](https://github.com/code-yeongyu/oh-my-openagent/blob/cabdb895e65b/.agents/skills/work-with-pr/SKILL.md) | `cabdb895e65b` | see repo |  |  |
| [sentimony/agentic-workflow](https://github.com/sentimony/agentic-workflow) | [skills/resolve-issue/SKILL.md](https://github.com/sentimony/agentic-workflow/blob/8ec5ecb13ddc/skills/resolve-issue/SKILL.md) | `8ec5ecb13ddc` | MIT |  |  |
| [affaan-m/ecc](https://github.com/affaan-m/ecc) | [skills/github-ops/SKILL.md](https://github.com/affaan-m/ecc/blob/d2ef2680594f/skills/github-ops/SKILL.md) | `d2ef2680594f` | MIT |  |  |
| [openai/skills](https://github.com/openai/skills) | [skills/.curated/gh-address-comments/SKILL.md](https://github.com/openai/skills/blob/49f948faa925/skills/.curated/gh-address-comments/SKILL.md) | `49f948faa925` | none stated |  |  |

Considered, not adopted: an approval gate on requirements before coding. The step 7 test pause already gives the user that check, closer to the release.
