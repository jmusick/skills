# References

The sources each skill was built from, kept in one file so credits stay out of the skill folders. Add a section here when a skill draws on outside material.

In each table, **Pin** marks where the source stood when it was read, so a later check can diff from there. **Track** marks the sources worth checking for updates; the rest are credited only. **Contributed** names the rules that came from that one source; rules most sources share have no owner. Only newsroom adapts text from a source, so its MIT notice sits in its section here instead of in a NOTICE file.

## commit

commit and release replaced the patch and minor skills on 2026-11-14. Those two shared one `SOURCES.md`, reviewed on 2026-11-11, and its rows moved here and to release's section when the old skills were removed. These two rows are about commit messages, so they sit with commit. Neither shaped the old skills' checks, so both are credited only. The rules the 2026-11-15 rewrite brought back from the old skills (no AI trailers, the why taken from the conversation) were the owner's own convention.

| Source | Path | Pin | License | Track | Contributed |
| --- | --- | --- | --- | --- | --- |
| [samber/cc-skills](https://github.com/samber/cc-skills) | [skills/conventional-git/SKILL.md](https://github.com/samber/cc-skills/blob/50a33836b20f/skills/conventional-git/SKILL.md) | `50a33836b20f` | MIT |  |  |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | [skills/git-workflow-and-versioning/SKILL.md](https://github.com/addyosmani/agent-skills/blob/301b02b12bff/skills/git-workflow-and-versioning/SKILL.md) | `301b02b12bff` | MIT |  |  |

## daily-news

daily-news replaced daily-budget, which the 2026-11-14 cut removed along with its scripts, reference files and the newsroom skill it drafted with. daily-news drafts with the rewritten newsroom, which has its own section below. daily-budget had no upstream skill: it followed Firelands Current's own sourcing notes, and these journalism and news-monitoring skills were reviewed against it on 2026-11-11, when its verification rules were already stricter than theirs. Their pins are the commits reviewed then. The rows moved here from daily-budget's `SOURCES.md` when daily-news was written on 2026-11-16. The sources weren't re-read for it: the new skill folds the old reference files into one `SKILL.md` and hands publishing to the paper's own `packet.mjs`, both the owner's own conventions.

| Source | Path | Pin | License | Track | Contributed |
| --- | --- | --- | --- | --- | --- |
| [jamditis/claude-skills-journalism](https://github.com/jamditis/claude-skills-journalism) | [journalism-core/skills/source-verification/SKILL.md](https://github.com/jamditis/claude-skills-journalism/blob/e1f38cb11521/journalism-core/skills/source-verification/SKILL.md) | `e1f38cb11521` | MIT | yes | Recording when each source was checked. |
| [claude-office-skills/skills](https://github.com/claude-office-skills/skills) | [news-monitor/SKILL.md](https://github.com/claude-office-skills/skills/blob/9c4c7d5cd281/news-monitor/SKILL.md) | `9c4c7d5cd281` | MIT |  | Listing every source monitored in the digest. |
| [jamditis/claude-skills-journalism](https://github.com/jamditis/claude-skills-journalism) | [journalism-core/skills/fact-check-workflow/SKILL.md](https://github.com/jamditis/claude-skills-journalism/blob/e1f38cb11521/journalism-core/skills/fact-check-workflow/SKILL.md) | `e1f38cb11521` | MIT |  |  |
| [jamditis/claude-skills-journalism](https://github.com/jamditis/claude-skills-journalism) | [research-toolkit/skills/page-monitoring/SKILL.md](https://github.com/jamditis/claude-skills-journalism/blob/e1f38cb11521/research-toolkit/skills/page-monitoring/SKILL.md) | `e1f38cb11521` | MIT |  |  |
| [jamditis/claude-skills-journalism](https://github.com/jamditis/claude-skills-journalism) | [journalism-core/skills/editorial-workflow/SKILL.md](https://github.com/jamditis/claude-skills-journalism/blob/e1f38cb11521/journalism-core/skills/editorial-workflow/SKILL.md) | `e1f38cb11521` | MIT |  |  |
| [jamditis/claude-skills-journalism](https://github.com/jamditis/claude-skills-journalism) | [journalism-core/skills/social-media-intelligence/SKILL.md](https://github.com/jamditis/claude-skills-journalism/blob/e1f38cb11521/journalism-core/skills/social-media-intelligence/SKILL.md) | `e1f38cb11521` | MIT |  |  |
| [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | [sales/skills/daily-briefing/SKILL.md](https://github.com/anthropics/knowledge-work-plugins/blob/877a617b435e/sales/skills/daily-briefing/SKILL.md) | `877a617b435e` | Apache-2.0 |  |  |
| [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | [skills/public/newsletter-generation/SKILL.md](https://github.com/bytedance/deer-flow/blob/fc7c7e012c44/skills/public/newsletter-generation/SKILL.md) | `fc7c7e012c44` | MIT |  |  |

Considered, not adopted: RSS and change-detection monitoring for each source.

## humanize

The baseline is Wikipedia's [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), maintained by WikiProject AI Cleanup. humanize follows its catalog and caveats, so re-read it first when updating the skill: the page dates each sign, and signs move to its "Historical indicators" section as models change.

| Source | Pin | License | Track | Contributed |
| --- | --- | --- | --- | --- |
| [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) | [revision 1385960173](https://en.wikipedia.org/w/index.php?oldid=1385960173) (2026-11-16) | CC BY-SA 4.0 | yes | The pattern catalog and its 2026 dating (corrective-framing disclaimers, "identify" phrasing, newer AI vocabulary, the comma-and-period rhythm left behind when dashes are suppressed), the regression-to-the-mean framing, the warning not to fix only the surface, the signs of human writing, the ineffective indicators, and the caution against guessing authorship. |

These anti-AI-writing skills supplement the article; most of them descend from it. Their pins were backfilled on 2026-11-11 from each repo's latest commit, after the original skill was written, so they mark where to start watching rather than the exact version read. The exceptions are blader/humanizer and the last three rows, which were reviewed at their pins on 2026-11-11. On 2026-11-15 the tracked repos had no changes past their pins beyond formatting. On 2026-11-16 an audit against Anthropic's [The Complete Guide to Building Skills for Claude](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf) added `scripts/scan.py`, which counts the skill's own literal lists, dashes, and sentence-length spread, since counting is what reading does worst. It wasn't taken from these sources.

| Source | Path | Pin | License | Track | Contributed |
| --- | --- | --- | --- | --- | --- |
| [blader/humanizer](https://github.com/blader/humanizer) | [SKILL.md](https://github.com/blader/humanizer/blob/b48c832f0f80/SKILL.md) | `b48c832f0f80` | MIT | yes | Matching a sample's dash rate, treating fake tags and operator notes as material, and file mode reading the whole file. Its 4.0.0 lets the rewrite add true specifics; humanize keeps the no-invention rule instead. |
| [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop) | [SKILL.md](https://github.com/hardikpandya/stop-slop/blob/8da1f030185b/SKILL.md) | `8da1f030185b` | MIT | yes | False agency (things doing what needs a mind). |
| [petergyang/no-ai-slop](https://github.com/petergyang/no-ai-slop) | [skills/no-ai-slop/SKILL.md](https://github.com/petergyang/no-ai-slop/blob/000650b15698/skills/no-ai-slop/SKILL.md) | `000650b15698` | MIT | yes | Meta-commentary that explains the text to the reader. |
| [cursor/plugins](https://github.com/cursor/plugins) | [pstack/skills/unslop/SKILL.md](https://github.com/cursor/plugins/blob/5866df557357/pstack/skills/unslop/SKILL.md) | `5866df557357` | none stated |  | Cursor's unslop. |
| [conorbronsdon/avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing) | [SKILL.md](https://github.com/conorbronsdon/avoid-ai-writing/blob/30971f1c50c6/SKILL.md) | `30971f1c50c6` | MIT |  |  |
| [Nanako0129/sepia](https://github.com/Nanako0129/sepia) | [skills/sepia/SKILL.md](https://github.com/Nanako0129/sepia/blob/0eb11d6c64c9/skills/sepia/SKILL.md) | `0eb11d6c64c9` | MIT |  |  |
| [AIScientists-Dev/academic-humanizer](https://github.com/AIScientists-Dev/academic-humanizer) | [SKILL.md](https://github.com/AIScientists-Dev/academic-humanizer/blob/94b88b23703b/SKILL.md) | `94b88b23703b` | see repo |  | Match unconfirmed: the most-starred of several repos with this name. |
| [aplaceforallmystuff/the-antislop](https://github.com/aplaceforallmystuff/the-antislop) | [skills/antislop/SKILL.md](https://github.com/aplaceforallmystuff/the-antislop/blob/f123fdc53574/skills/antislop/SKILL.md) | `f123fdc53574` | MIT |  | Match unconfirmed: the Claude skill named antislop. |
| [theclaymethod/unslop](https://github.com/theclaymethod/unslop) | [SKILL.md](https://github.com/theclaymethod/unslop/blob/17ed39c9d0b5/SKILL.md) | `17ed39c9d0b5` | none stated |  |  |
| [jalaalrd/anti-ai-slop-writing](https://github.com/jalaalrd/anti-ai-slop-writing) | [skills/anti-ai-slop-writing/SKILL.md](https://github.com/jalaalrd/anti-ai-slop-writing/blob/63255f9bbb75/skills/anti-ai-slop-writing/SKILL.md) | `63255f9bbb75` | none stated |  |  |
| [miqdadbadjuber/anti-slop](https://github.com/miqdadbadjuber/anti-slop) | [skills/antislop-copywriting/SKILL.md](https://github.com/miqdadbadjuber/anti-slop/blob/4520786d3dff/skills/antislop-copywriting/SKILL.md) | `4520786d3dff` | MIT | yes | Opening runways ("In today's fast-paced world"), false ranges, and the mind-verb test for false agency. |
| [Aboudjem/humanizer-skill](https://github.com/Aboudjem/humanizer-skill) | [skills/humanizer/SKILL.md](https://github.com/Aboudjem/humanizer-skill/blob/a58df0653675/skills/humanizer/SKILL.md) | `a58df0653675` | MIT |  | Markdown that won't render, and docs that narrate a change. |
| [MohamedAbdallah-14/unslop](https://github.com/MohamedAbdallah-14/unslop) | [skills/unslop/SKILL.md](https://github.com/MohamedAbdallah-14/unslop/blob/5e955765a78c/skills/unslop/SKILL.md) | `5e955765a78c` | MIT |  | Change style, not stance: no added warmth or agreement. |

## issue

issue had no upstream skill. These issue-to-PR skills were reviewed against it on 2026-11-11, and their pins are the commits reviewed then. The section moved here from the skill's old `SOURCES.md`, which the 2026-11-14 cut to a single file removed. The 2026-11-15 rewrite restored the picking rules, sizing, review, local-dev test, branch, batch, unattended, and failure-path steps, along with the report. The sources weren't re-read for it. The old file also credited jssblck/agents and tobi/qmd, for the version bump and tagging the old skill did itself. That work belongs to release now, so those rows sit in its section. addyosmani/agent-skills appears under commit too.

| Source | Path | Pin | License | Track | Contributed |
| --- | --- | --- | --- | --- | --- |
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

Considered, not adopted: a gate where the user approves the requirements before any coding. The local-dev test pause already gives the user that check, closer to the commit.

## newsroom

newsroom builds on one upstream skill, keeping the rules most published newsroom skills agree on. The original, written for Firelands Current, was removed in the 2026-11-14 cut and returned on 2026-11-16 as a single file. The rewrite folded its AP-style, story-type, and AI-tells references into SKILL.md and swapped the Firelands house-style file for a step that reads the project's own style guide. The crime-naming policy stayed as a default. The row moved here from the old skill's `SOURCES.md`, and its pin was backfilled on 2026-11-11 from the repo's latest commit, so it marks where to start watching rather than the exact version read. The source wasn't re-read for the rewrite. Later that day an audit against Anthropic's [The Complete Guide to Building Skills for Claude](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf) added `scripts/ap_lint.py`, which checks weekdays against dates and the skill's own mechanical AP rules. It wasn't taken from the source.

| Source | Path | Pin | License | Track | Contributed |
| --- | --- | --- | --- | --- | --- |
| [jamditis/claude-skills-journalism](https://github.com/jamditis/claude-skills-journalism) | [journalism-core/skills/newsroom-style/SKILL.md](https://github.com/jamditis/claude-skills-journalism/blob/e1f38cb11521/journalism-core/skills/newsroom-style/SKILL.md) | `e1f38cb11521` | MIT | yes | The base the skill was adapted from. |

Parts of newsroom are adapted from that skill under the MIT License:

```
MIT License

Copyright (c) 2025 Joe Amditis

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## release

release had no upstream skill. It replaced patch and minor, which followed the owner's own `vX.Y.Z - Summary` release convention, and these release and changelog skills were reviewed against those on 2026-11-11. Their pins are the commits reviewed then. The section moved here from the old skills' shared `SOURCES.md` when they were removed. The 2026-11-15 rewrite brought back from the old skills the checks the replacement had dropped: fetching origin's tags, the preflight stops, the changelog rules, and the version-file details. The sources weren't re-read for it. On 2026-11-16 an audit against Anthropic's [The Complete Guide to Building Skills for Claude](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf) moved the survey (the stop checks, sorting commits by bump, the tag clash and version-file checks) into `scripts/next_version.py`, following its advice to bundle a script for checks the model does unreliably. It wasn't taken from the sources below.

| Source | Path | Pin | License | Track | Contributed |
| --- | --- | --- | --- | --- | --- |
| [jssblck/agents](https://github.com/jssblck/agents) | [skills/tag-release/SKILL.md](https://github.com/jssblck/agents/blob/e1294cd90416/skills/tag-release/SKILL.md) | `e1294cd90416` | GPL-3.0 | yes | Fetching first and treating origin's tags as authoritative. |
| [tobi/qmd](https://github.com/tobi/qmd) | [skills/release/SKILL.md](https://github.com/tobi/qmd/blob/86d2365d17fc/skills/release/SKILL.md) | `86d2365d17fc` | MIT | yes | Turning the `Unreleased` changelog section into the release; leaving internal changes out. |
| [samber/developer-relations-skills](https://github.com/samber/developer-relations-skills) | [skills/changelog-writing/SKILL.md](https://github.com/samber/developer-relations-skills/blob/c3a1b6912791/skills/changelog-writing/SKILL.md) | `c3a1b6912791` | MIT | yes | Keeping the version number honest: a breaking change is a major. |
| [schpet/linear-cli](https://github.com/schpet/linear-cli) | [.claude/skills/release/SKILL.md](https://github.com/schpet/linear-cli/blob/02571d34be66/.claude/skills/release/SKILL.md) | `02571d34be66` | ISC |  | Running the checks before tagging; matching the bump to the changes. |
| [jayden-dang/skills](https://github.com/jayden-dang/skills) | [skills/ship/cut-release/SKILL.md](https://github.com/jayden-dang/skills/blob/71aa50d2cc60/skills/ship/cut-release/SKILL.md) | `71aa50d2cc60` | MIT |  | No tag on a failing build. |
| [jimliu/baoyu-skills](https://github.com/jimliu/baoyu-skills) | [.claude/skills/release-skills/SKILL.md](https://github.com/jimliu/baoyu-skills/blob/ca703c2d7c2c/.claude/skills/release-skills/SKILL.md) | `ca703c2d7c2c` | MIT |  | Flagging breaking changes before choosing the bump. |
| [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) | [plugin/skills/version-bump/SKILL.md](https://github.com/thedotmack/claude-mem/blob/19b786b91359/plugin/skills/version-bump/SKILL.md) | `19b786b91359` | Apache-2.0 |  |  |
| [jezweb/claude-skills](https://github.com/jezweb/claude-skills) | [plugins/dev-tools/skills/github-release/SKILL.md](https://github.com/jezweb/claude-skills/blob/1260fa7439b3/plugins/dev-tools/skills/github-release/SKILL.md) | `1260fa7439b3` | MIT |  |  |
| [riekelt/technical-writer](https://github.com/riekelt/technical-writer) | [plugins/technical-writer/skills/writing-changelogs/SKILL.md](https://github.com/riekelt/technical-writer/blob/85e53729dd95/plugins/technical-writer/skills/writing-changelogs/SKILL.md) | `85e53729dd95` | MIT |  |  |
| [wshobson/agents](https://github.com/wshobson/agents) | [plugins/documentation-generation/skills/changelog-automation/SKILL.md](https://github.com/wshobson/agents/blob/9c61ab243def/plugins/documentation-generation/skills/changelog-automation/SKILL.md) | `9c61ab243def` | MIT |  |  |
| [vercel-labs/autoship](https://github.com/vercel-labs/autoship) | [skills/autoship/SKILL.md](https://github.com/vercel-labs/autoship/blob/0ebe9fdfb743/skills/autoship/SKILL.md) | `0ebe9fdfb743` | Apache-2.0 |  |  |

Considered, not adopted: creating a GitHub Release (the owner's releases are tags only), watching the tag's CI run, and matching tag signing.

## title

title had no upstream skill. These session- and tab-renaming skills were reviewed against it on 2026-11-11, and their pins are the commits reviewed then. The section moved here from the skill's old `SOURCES.md` when the skill was cut to a single file. The 2026-11-15 rewrite restored the rules credited below, which the cut had dropped.

| Source | Path | Pin | License | Track | Contributed |
| --- | --- | --- | --- | --- | --- |
| [thejiajun/jcskill](https://github.com/thejiajun/jcskill) | [plugins/jcskill/skills/rename-codex-session/SKILL.md](https://github.com/thejiajun/jcskill/blob/0a26ff582af7/plugins/jcskill/skills/rename-codex-session/SKILL.md) | `0a26ff582af7` | MIT | yes | Keeping the user's language; no sensitive details; skipping meta turns. |
| [jackcannon/skills](https://github.com/jackcannon/skills) | [skills/auto-rename-chat/SKILL.md](https://github.com/jackcannon/skills/blob/4214b95d4858/skills/auto-rename-chat/SKILL.md) | `4214b95d4858` | none stated | yes | Putting the ticket number in the title. |
| [moatai-io/towersource](https://github.com/moatai-io/towersource) | [skills/managed/session-rename/SKILL.md](https://github.com/moatai-io/towersource/blob/2f0fef99c9d6/skills/managed/session-rename/SKILL.md) | `2f0fef99c9d6` | Apache-2.0 |  | Language and sensitive-details rules. |
| [bluzername/claude-code-terminal-title](https://github.com/bluzername/claude-code-terminal-title) | [skill/terminal-title/SKILL.md](https://github.com/bluzername/claude-code-terminal-title/blob/c405953699e4/skill/terminal-title/SKILL.md) | `c405953699e4` | none stated |  | Ignoring tweaks and follow-ups when judging the topic. |
| [goern/bead-workflow-skills](https://github.com/goern/bead-workflow-skills) | [skills/work-on/SKILL.md](https://github.com/goern/bead-workflow-skills/blob/ddffd3c3b0b9/skills/work-on/SKILL.md) | `ddffd3c3b0b9` | GPL-3.0 |  | Naming the session after the ticket it works on. |
| [damilareoo/damilares-skills](https://github.com/damilareoo/damilares-skills) | [plugins/v-skills/skills/rename-chat/SKILL.md](https://github.com/damilareoo/damilares-skills/blob/bb3eb123f149/plugins/v-skills/skills/rename-chat/SKILL.md) | `bb3eb123f149` | none stated |  | A copy of Cursor's built-in rename-chat; levi0527/codex-skills and kritika810/copilot-skills carry the same text. |
| [trifle-labs/skills](https://github.com/trifle-labs/skills) | [rename-sessions/SKILL.md](https://github.com/trifle-labs/skills/blob/143bae98371c/rename-sessions/SKILL.md) | `143bae98371c` | none stated |  |  |
| [davidondrej/skills](https://github.com/davidondrej/skills) | [skills/rename/SKILL.md](https://github.com/davidondrej/skills/blob/0a83467417fe/skills/rename/SKILL.md) | `0a83467417fe` | MIT |  |  |
| [akenlabs/aken-skills](https://github.com/akenlabs/aken-skills) | [skills/rename-chat/SKILL.md](https://github.com/akenlabs/aken-skills/blob/50b9d0ca7ab6/skills/rename-chat/SKILL.md) | `50b9d0ca7ab6` | see repo |  |  |
| [enkira-ai/claude-plugins](https://github.com/enkira-ai/claude-plugins) | [plugins/session-manager/skills/rename-session/SKILL.md](https://github.com/enkira-ai/claude-plugins/blob/4b368350bddb/plugins/session-manager/skills/rename-session/SKILL.md) | `4b368350bddb` | none stated |  |  |
| [harrywang/ghostty-tab-title](https://github.com/harrywang/ghostty-tab-title) | [skills/tab-title/SKILL.md](https://github.com/harrywang/ghostty-tab-title/blob/7b10e202b24f/skills/tab-title/SKILL.md) | `7b10e202b24f` | MIT |  |  |
| [piusn/skills-plugin-marketplace](https://github.com/piusn/skills-plugin-marketplace) | [skills/session-rename/SKILL.md](https://github.com/piusn/skills-plugin-marketplace/blob/0cc4b509539b/skills/session-rename/SKILL.md) | `0cc4b509539b` | none stated |  |  |

Considered, not adopted: renaming a Claude Code CLI session by appending to its JSONL transcript (trifle-labs) or through a hook (goern). Both depend on internal formats, so the skill still suggests `/rename`.

## update-docs

update-docs draws on these docs-maintenance skills. Their pins were backfilled on 2026-11-11 from each repo's latest commit, after the skill was written, so they mark where to start watching rather than the exact version read. The section moved here from the skill's old `SOURCES.md` when the skill was cut to a single file. The 2026-11-15 rewrite restored the organization review, the agent-notes and privacy-policy checks, the contradiction check, and the report format, which the cut had dropped. The sources weren't re-read for it. On 2026-11-16 an audit against Anthropic's [The Complete Guide to Building Skills for Claude](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf) moved link checking into `scripts/doc_links.py` (its advice: bundle a script for checks where "code is deterministic; language interpretation isn't") and the privacy-policy check into `references/privacy-policy.md`, with a new list of tracking and third-party signatures. Neither was taken from the sources below.

| Source | Path | Pin | License | Track | Contributed |
| --- | --- | --- | --- | --- | --- |
| [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | [plugins/claude-md-management/skills/claude-md-improver/SKILL.md](https://github.com/anthropics/claude-plugins-official/blob/e37d307bd9f8/plugins/claude-md-management/skills/claude-md-improver/SKILL.md) | `e37d307bd9f8` | Apache-2.0 | yes | Anthropic's claude-md-improver. |
| [getsentry/skills](https://github.com/getsentry/skills) | [skills/agents-md/SKILL.md](https://github.com/getsentry/skills/blob/e94f22214528/skills/agents-md/SKILL.md) | `e94f22214528` | Apache-2.0 |  |  |
| [amElnagdy/guard-skills](https://github.com/amElnagdy/guard-skills) | [skills/docs-guard/SKILL.md](https://github.com/amElnagdy/guard-skills/blob/ffa26036b7b5/skills/docs-guard/SKILL.md) | `ffa26036b7b5` | MIT | yes | Checking each doc statement as a claim. |
| [giuseppe-trisciuoglio/developer-kit](https://github.com/giuseppe-trisciuoglio/developer-kit) | [plugins/developer-kit-core/skills/docs-updater/SKILL.md](https://github.com/giuseppe-trisciuoglio/developer-kit/blob/fe73fb33a09e/plugins/developer-kit-core/skills/docs-updater/SKILL.md) | `fe73fb33a09e` | MIT |  |  |
| ruchernchong's sync-docs | | not found | | | No public ruchernchong repo has a sync-docs skill now, so this can't be pinned. |
| [iliaal/ai-skills](https://github.com/iliaal/ai-skills) | [skills/md-docs/SKILL.md](https://github.com/iliaal/ai-skills/blob/6e16f4a0798f/skills/md-docs/SKILL.md) | `6e16f4a0798f` | MIT |  |  |
| [tartinerlabs/skills](https://github.com/tartinerlabs/skills) | [plugins/tooling/skills/update-project/SKILL.md](https://github.com/tartinerlabs/skills/blob/e9d405714501/plugins/tooling/skills/update-project/SKILL.md) | `e9d405714501` | MIT |  |  |
| [laurigates/claude-plugins](https://github.com/laurigates/claude-plugins) | [documentation-plugin/skills/docs-sync/SKILL.md](https://github.com/laurigates/claude-plugins/blob/34a98323c289/documentation-plugin/skills/docs-sync/SKILL.md) | `34a98323c289` | MIT | yes | Catalog and count drift. |
