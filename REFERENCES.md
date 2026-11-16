# References

The sources each skill was built from, kept in one file so credits stay out of the skill folders. Add a section here when a skill draws on outside material.

In each table, **Pin** marks where the source stood when it was read, so a later check can diff from there. **Track** marks the sources worth checking for updates; the rest are credited only. **Contributed** names the rules that came from that one source; rules most sources share have no owner. Only newsroom, music-creation, and interview adapt text from sources, so their notices sit in their sections here instead of in NOTICE files.

## commit

commit and release replaced the patch and minor skills on 2026-11-14. Those two shared one `SOURCES.md`, reviewed on 2026-11-11, and its rows moved here and to release's section when the old skills were removed. These two rows are about commit messages, so they sit with commit. Neither shaped the old skills' checks, so both are credited only. The rules the 2026-11-15 rewrite brought back from the old skills (no AI trailers, the why taken from the conversation) were the owner's own convention.

| Source | Path | Pin | License | Track | Contributed |
| --- | --- | --- | --- | --- | --- |
| [samber/cc-skills](https://github.com/samber/cc-skills) | [skills/conventional-git/SKILL.md](https://github.com/samber/cc-skills/blob/50a33836b20f/skills/conventional-git/SKILL.md) | `50a33836b20f` | MIT |  |  |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | [skills/git-workflow-and-versioning/SKILL.md](https://github.com/addyosmani/agent-skills/blob/301b02b12bff/skills/git-workflow-and-versioning/SKILL.md) | `301b02b12bff` | MIT |  |  |

## daily-news

daily-news replaced daily-budget, which the 2026-11-14 cut removed along with its scripts, reference files and the newsroom skill it drafted with. daily-news drafts with the rewritten newsroom, which has its own section below. daily-budget had no upstream skill: it followed Firelands Current's own sourcing notes, and these journalism and news-monitoring skills were reviewed against it on 2026-11-11, when its verification rules were already stricter than theirs. Their pins are the commits reviewed then. The rows moved here from daily-budget's `SOURCES.md` when daily-news was written on 2026-11-16. The sources weren't re-read for it: the new skill folds the old reference files into one `SKILL.md` and hands publishing to the paper's own `packet.mjs`, both the owner's own conventions. Later that day an audit against Anthropic's [The Complete Guide to Building Skills for Claude](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf) added `scripts/open_packet.py` (the folder, snapshot and digest, after two runs had saved the snapshot in different shapes), `scripts/check_packet.py` (the skill's rules that `packet.mjs` doesn't check), and `assets/review-template.md` (the layout of the editor's recent reviews). None was taken from the sources below.

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

## design-taste

design-taste is what these frontend design skills agree on. The 2026-11-14 cut removed it, and it returned on 2026-11-16 with its `SKILL.md`, references, and `scripts/lint_tells.py` as they stood before the cut. The return made it model-invocable with trigger phrases in its description and dropped its evals and Codex settings, per AGENTS.md. The sources weren't re-read for it. The rows moved here from the skill's old `SOURCES.md`. Their pins were backfilled on 2026-11-11 from each repo's latest commit, after the skill was written, so they mark where to start watching rather than the exact version read. The lint script, the dated three-wave framing of the tells, and the two-round ceiling on the critique loop are the skill's own, not taken from a source.

| Source | Path | Pin | License | Track | Contributed |
| --- | --- | --- | --- | --- | --- |
| [anthropics/skills](https://github.com/anthropics/skills) | [skills/frontend-design/SKILL.md](https://github.com/anthropics/skills/blob/2c5958ecac7c/skills/frontend-design/SKILL.md) | `2c5958ecac7c` | folder LICENSE.txt | yes | Anthropic's frontend-design, which build mode hands direction to when it's installed. One family or two, clearly distinct, chosen on purpose. |
| [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | [skills/taste-skill/SKILL.md](https://github.com/Leonxlnx/taste-skill/blob/f6b76575f949/skills/taste-skill/SKILL.md) | `f6b76575f949` | MIT |  | The blind comparisons behind "removal is half the job". |
| [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | [.claude/skills/impeccable/SKILL.md](https://github.com/pbakaus/impeccable/blob/b4bff1626c34/.claude/skills/impeccable/SKILL.md) | `b4bff1626c34` | Apache-2.0 |  | Judging whether faces fit the product or are unexamined defaults, stress-testing for localization and missing weights, and a second family only with a role it alone can do (from its [reference/typeset.md](https://github.com/pbakaus/impeccable/blob/b4bff1626c34/.claude/skills/impeccable/reference/typeset.md)). |
| [vercel-labs/web-interface-guidelines](https://github.com/vercel-labs/web-interface-guidelines) | [AGENTS.md](https://github.com/vercel-labs/web-interface-guidelines/blob/434b7f913646/AGENTS.md) | `434b7f913646` | MIT |  | Vercel's web interface guidelines. |
| [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | [.claude/skills/ui-ux-pro-max/SKILL.md](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/6ae86f61f520/.claude/skills/ui-ux-pro-max/SKILL.md) | `6ae86f61f520` | MIT |  |  |
| [emilkowalski/skills](https://github.com/emilkowalski/skills) | [skills](https://github.com/emilkowalski/skills/tree/715c1807e08c/skills) | `715c1807e08c` | MIT | yes | Most of the motion guidance. |
| [jakubkrehel/skills](https://github.com/jakubkrehel/skills) | [skills](https://github.com/jakubkrehel/skills/tree/8b254eb75dad/skills) | `8b254eb75dad` | MIT | yes | Most of the motion guidance. |
| [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills) | [plugins/stitch-utilities/skills/taste-design/SKILL.md](https://github.com/google-labs-code/stitch-skills/blob/0337446dadde/plugins/stitch-utilities/skills/taste-design/SKILL.md) | `0337446dadde` | Apache-2.0 |  | Google's stitch taste-design. |
| [ConardLi/garden-skills](https://github.com/ConardLi/garden-skills) | [skills/web-design-engineer/SKILL.md](https://github.com/ConardLi/garden-skills/blob/08150e750bdc/skills/web-design-engineer/SKILL.md) | `08150e750bdc` | MIT |  |  |

On 2026-11-16 the type section in `references/direction.md` ("Choosing and pairing type") and its checks in `references/floor.md` were added, after the owner asked what font pairing rested on, and then how to choose the faces in the first place. The choosing steps follow the Google Fonts "Choosing type" lessons below. Most of those are by one author, Elliot Jay Stocks, so agreement among them isn't independent; each step also has support in a skill source or in Charles Berret's guide, except confirming the license (the checklist alone). Tying the feeling to the skill's subject inventory, the `Il1` and `O0` test string, and the default test's wording are the skill's own. The skill sources above were re-read at their pins for pairing and said little beyond the two contributions noted, so the method comes mostly from the typography references below. Most of its rules appear in two or more sources. Three rest on one: lower contrast often working better and no face change inside a paragraph (Butterick), and minding the era (Google Fonts). The step that screenshots the pair in the critique loop is the skill's own. The Google Fonts lessons live in [google/fonts](https://github.com/google/fonts) under `cc-by-sa/knowledge/modules/choosing_type/lessons/`, so their pins are commits in that repo.

| Source | Pin | License | Track | Contributed |
| --- | --- | --- | --- | --- |
| [Pairing typefaces](https://fonts.google.com/knowledge/choosing_type/pairing_typefaces), Elliot Jay Stocks for Google Fonts Knowledge | [`a257d29b6e37`](https://github.com/google/fonts/tree/a257d29b6e37/cc-by-sa/knowledge/modules/choosing_type/lessons/pairing_typefaces) | CC BY-SA 4.0 | yes | Exhausting one family first, the four jobs that justify a second face, matching traits (x-height, contrast, width, mood) after Jessica Hische, distinction and harmony after Jason Santa Maria, serif with sans as the fallback, and minding the era. |
| [Pairing typefaces within a family & superfamily](https://fonts.google.com/knowledge/choosing_type/pairing_typefaces_within_a_family_superfamily), Google Fonts Knowledge | [`00217e2bab7b`](https://github.com/google/fonts/tree/00217e2bab7b/cc-by-sa/knowledge/modules/choosing_type/lessons/pairing_typefaces_within_a_family_superfamily) | CC BY-SA 4.0 |  | The superfamily shortcut and what it shares. |
| [Pairing typefaces by the same type designer or type foundry](https://fonts.google.com/knowledge/choosing_type/pairing_typefaces_by_the_same_type_designer_or_type_foundry), Google Fonts Knowledge | [`00217e2bab7b`](https://github.com/google/fonts/tree/00217e2bab7b/cc-by-sa/knowledge/modules/choosing_type/lessons/pairing_typefaces_by_the_same_type_designer_or_type_foundry) | CC BY-SA 4.0 |  | The same-designer shortcut, and its caution to check the traits anyway. |
| [A checklist for choosing type](https://fonts.google.com/knowledge/choosing_type/a_checklist_for_choosing_type), Elliot Jay Stocks for Google Fonts Knowledge | [`67fe0d098cdd`](https://github.com/google/fonts/tree/67fe0d098cdd/cc-by-sa/knowledge/modules/choosing_type/lessons/a_checklist_for_choosing_type) | CC BY-SA 4.0 | yes | The order of the choosing steps: fit to purpose and use, a complete design, reliable served files, and a license that covers the use. |
| [Emotive considerations for choosing typefaces](https://fonts.google.com/knowledge/choosing_type/emotive_considerations_for_choosing_typefaces), Elliot Jay Stocks for Google Fonts Knowledge | [`a257d29b6e37`](https://github.com/google/fonts/tree/a257d29b6e37/cc-by-sa/knowledge/modules/choosing_type/lessons/emotive_considerations_for_choosing_typefaces) | CC BY-SA 4.0 |  | Feeling and era as the first filter, never the only one; associations shift by audience and over time; arrangement carries meaning as much as the letterforms. |
| [Choosing reliable typefaces](https://fonts.google.com/knowledge/choosing_type/choosing_reliable_typefaces), Elliot Jay Stocks for Google Fonts Knowledge | [`5e189853e31f`](https://github.com/google/fonts/tree/5e189853e31f/cc-by-sa/knowledge/modules/choosing_type/lessons/choosing_reliable_typefaces) | CC BY-SA 4.0 |  | The `Il1` legibility check, the base set of weights and styles, and language coverage past basic Latin. |
| [Exploring x-height & the em square](https://fonts.google.com/knowledge/choosing_type/exploring_x_height_the_em_square), Elliot Jay Stocks for Google Fonts Knowledge | [`00217e2bab7b`](https://github.com/google/fonts/tree/00217e2bab7b/cc-by-sa/knowledge/modules/choosing_type/lessons/exploring_x_height_the_em_square) | CC BY-SA 4.0 |  | A large x-height reading better at small sizes. |
| [Choosing web fonts: A beginner's all-in-one guide](https://fonts.google.com/knowledge/choosing_type/choosing_web_fonts_beginners_guide), Charles Berret for Google Fonts Knowledge | [`d69f15255135`](https://github.com/google/fonts/tree/d69f15255135/cc-by-sa/knowledge/modules/choosing_type/lessons/choosing_web_fonts_beginners_guide) | CC BY-SA 4.0 |  | Matching the face to the length and size of the text, judging quality by `a`, `g`, and the numerals, auto-translate as a reason to cover more languages, and the choice of figure styles. |
| [Mixing fonts](https://practicaltypography.com/mixing-fonts.html), Matthew Butterick, *Practical Typography* | read 2026-11-16 (no date on the page) | none stated |  | A third face is rarely right and four almost never, serif with sans isn't required, lower contrast often beats high, a fixed job for each face, no font change inside a paragraph, and the same-designer shortcut. |

Considered, not adopted: the Berret guide's named example faces for each size and length, and the named pairings that taste-skill deals from its data, stitch-skills prescribes for dashboards, and ui-ux-pro-max searches. Every named list becomes the next tell, so the skill keeps the method and leaves the names out.

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

## improve-codebase

improve-codebase is what about twenty codebase-improvement skills agree on. These are the ones that were recorded. The 2026-11-14 cut removed it, and it returned on 2026-11-16 as it stood before, made model-invocable with trigger phrases in its description and without its evals, tests, and Codex settings, per AGENTS.md. The sources weren't re-read for the return; the rows moved here from the skill's old `SOURCES.md`. Later on 2026-11-16 every source was re-read at HEAD (none had changed since its pin), the rows below gained what that pass took, and six newer skills found on GitHub that day were added at the end.

Pins were backfilled on 2026-11-11 from each repo's latest commit, after the skill was written. They mark where to start watching for changes, not the exact version that was read. The six added on 2026-11-16 are pinned to the commit read that day. **Track** marks the sources worth checking for updates; the rest are credited only.

| Source | Path | Pin | License | Track | Contributed |
| --- | --- | --- | --- | --- | --- |
| [mattpocock/skills](https://github.com/mattpocock/skills) | [skills/engineering/improve-codebase-architecture/SKILL.md](https://github.com/mattpocock/skills/blob/4ae2317ddb22/skills/engineering/improve-codebase-architecture/SKILL.md) | `4ae2317ddb22` | MIT | yes | With codebase-design: the deletion test, deep modules, git-history hotspots, and recording a rejected candidate so later runs don't re-suggest it. |
| [mattpocock/skills](https://github.com/mattpocock/skills) | [skills/engineering/codebase-design/SKILL.md](https://github.com/mattpocock/skills/blob/4ae2317ddb22/skills/engineering/codebase-design/SKILL.md) | `4ae2317ddb22` | MIT | yes | See improve-codebase-architecture. Its `DEEPENING.md`: testing a deepened module by what it depends on, and replacing old tests instead of layering. |
| [shadcn/improve](https://github.com/shadcn/improve) | [skills/improve/SKILL.md](https://github.com/shadcn/improve/blob/cac56e1ebd3c/skills/improve/SKILL.md) | `cac56e1ebd3c` | MIT | yes | Vetting subagent findings, self-contained plans, the finding format with confidence, the correctness checks, the issue's drift check and stop conditions, stale decision records as findings, and reachable advisories only (from its `references/`). |
| [ksimback/tech-debt-skill](https://github.com/ksimback/tech-debt-skill) | [SKILL.md](https://github.com/ksimback/tech-debt-skill/blob/5a15c1ca4a92/SKILL.md) | `5a15c1ca4a92` | none stated | yes | The required "looks bad but is actually fine" section, and the large-repo threshold for subagents. |
| [max4c/skills](https://github.com/max4c/skills) | [skills/improve-codebase/SKILL.md](https://github.com/max4c/skills/blob/825b94d5c28b/skills/improve-codebase/SKILL.md) | `825b94d5c28b` | MIT |  |  |
| [tomzx/agents](https://github.com/tomzx/agents) | [skills/improve-codebase/SKILL.md](https://github.com/tomzx/agents/blob/e9c4674dd397/skills/improve-codebase/SKILL.md) | `e9c4674dd397` | MIT |  | Checking work already in flight before filing. |
| [cursor/plugins](https://github.com/cursor/plugins) | [cursor-team-kit/skills/thermo-nuclear-code-quality-review/SKILL.md](https://github.com/cursor/plugins/blob/5866df557357/cursor-team-kit/skills/thermo-nuclear-code-quality-review/SKILL.md) | `5866df557357` | none stated |  |  |
| [cursor/plugins](https://github.com/cursor/plugins) | [cursor-team-kit/skills/deslop/SKILL.md](https://github.com/cursor/plugins/blob/5866df557357/cursor-team-kit/skills/deslop/SKILL.md) | `5866df557357` | none stated |  |  |
| [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | [engineering/skills/tech-debt/SKILL.md](https://github.com/anthropics/knowledge-work-plugins/blob/877a617b435e/engineering/skills/tech-debt/SKILL.md) | `877a617b435e` | Apache-2.0 |  |  |
| [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) | [skills/safe-refactor/SKILL.md](https://github.com/JuliusBrussee/caveman/blob/3dc497a7f858/skills/safe-refactor/SKILL.md) | `3dc497a7f858` | Apache-2.0 |  | Errors and ordering count as behavior to keep. |
| [chrisallenlane/claude-swe-workflows](https://github.com/chrisallenlane/claude-swe-workflows) | [skills/refactor/SKILL.md](https://github.com/chrisallenlane/claude-swe-workflows/blob/20f50d4a7d04/skills/refactor/SKILL.md) | `20f50d4a7d04` | MIT |  |  |
| [jnsahaj/skills](https://github.com/jnsahaj/skills) | [skills/zero-tech-debt/SKILL.md](https://github.com/jnsahaj/skills/blob/170b0b919284/skills/zero-tech-debt/SKILL.md) | `170b0b919284` | none stated |  |  |
| [wondelai/skills](https://github.com/wondelai/skills) | [remove-technical-debt/SKILL.md](https://github.com/wondelai/skills/blob/d8d5d75f83da/remove-technical-debt/SKILL.md) | `d8d5d75f83da` | MIT |  | Pinning bugs that characterization tests turn up, instead of fixing them in the refactor. |
| [AlmanacCode/codealmanac](https://github.com/AlmanacCode/codealmanac) | [.claude/skills/deep-refactor-audit/SKILL.md](https://github.com/AlmanacCode/codealmanac/blob/0be9dc43c411/.claude/skills/deep-refactor-audit/SKILL.md) | `0be9dc43c411` | Apache-2.0 | yes | Hand-rolled machinery, and what agent-written code piles up. |
| [majiayu000/spellbook](https://github.com/majiayu000/spellbook) | [skills/codebase-audit/SKILL.md](https://github.com/majiayu000/spellbook/blob/31bf1965641b/skills/codebase-audit/SKILL.md) | `31bf1965641b` | MIT | yes | Trying to disprove Critical and High findings, things declared but never wired up, and capping inferred findings at Medium. |
| [yonatangross/orchestkit](https://github.com/yonatangross/orchestkit) | [src/skills/audit-full/SKILL.md](https://github.com/yonatangross/orchestkit/blob/3d88ecacdb6d/src/skills/audit-full/SKILL.md) | `3d88ecacdb6d` | MIT |  | The refuter sees only the claim, deterministic proof skips it, and a Critical is never dropped silently. |
| [blakecyze/kanso](https://github.com/blakecyze/kanso) | [skills/kanso-audit/SKILL.md](https://github.com/blakecyze/kanso/blob/0b9805af3873/skills/kanso-audit/SKILL.md) | `0b9805af3873` | MIT |  | Names for defensive programming theatre, phantom bugs, and vanilla reimplementation. |
| [JetBrains/skills](https://github.com/JetBrains/skills) | [codebase-audit/SKILL.md](https://github.com/JetBrains/skills/blob/985a353f81a7/codebase-audit/SKILL.md) | `985a353f81a7` | none stated |  | Checking code against the repo's own stated rules. |
| [fallow-rs/fallow](https://github.com/fallow-rs/fallow) | [.claude/skills/fallow/SKILL.md](https://github.com/fallow-rs/fallow/blob/093cdeb80420/.claude/skills/fallow/SKILL.md) | `093cdeb80420` | MIT |  | The fallow commands in `checks.md`. |

## improve-skills

improve-skills is what fifteen skill-writing and skill-improvement skills agree on, beyond Anthropic's and OpenAI's skill-creators. The 2026-11-14 cut removed it, and it returned on 2026-11-16 as it stood before, made model-invocable with trigger phrases in its description and without its evals and Codex settings, per AGENTS.md. The sources weren't re-read for the return; the rows moved here from the skill's old `SOURCES.md`.

Pins were backfilled on 2026-11-11 from each repo's latest commit, after the skill was written. They mark where to start watching for changes, not the exact version that was read. **Track** marks the sources worth checking for updates; the rest are credited only.

| Source | Path | Pin | License | Track | Contributed |
| --- | --- | --- | --- | --- | --- |
| [anthropics/skills](https://github.com/anthropics/skills) | [skills/skill-creator/SKILL.md](https://github.com/anthropics/skills/blob/2c5958ecac7c/skills/skill-creator/SKILL.md) | `2c5958ecac7c` | folder LICENSE.txt | yes | The baseline. |
| [openai/skills](https://github.com/openai/skills) | [skills/.system/skill-creator/SKILL.md](https://github.com/openai/skills/blob/49f948faa925/skills/.system/skill-creator/SKILL.md) | `49f948faa925` | folder LICENSE.txt | yes | The baseline. |
| [mattpocock/skills](https://github.com/mattpocock/skills) | [skills/productivity/writing-for-agents/SKILL.md](https://github.com/mattpocock/skills/blob/4ae2317ddb22/skills/productivity/writing-for-agents/SKILL.md) | `4ae2317ddb22` | MIT | yes | Context pointers, no-ops, positive phrasing over bans. |
| [obra/superpowers](https://github.com/obra/superpowers) | [skills/writing-skills/SKILL.md](https://github.com/obra/superpowers/blob/22f0b463e7a5/skills/writing-skills/SKILL.md) | `22f0b463e7a5` | MIT | yes | Baseline first, and matching the form of a fix to the failure. |
| [dotnet/skills](https://github.com/dotnet/skills) | [.agents/skills/improve-skill-quality/SKILL.md](https://github.com/dotnet/skills/blob/96c3d68dad28/.agents/skills/improve-skill-quality/SKILL.md) | `96c3d68dad28` | MIT | yes | Classify the failure before editing; retirement as a valid outcome. |
| [warpdotdev/common-skills](https://github.com/warpdotdev/common-skills) | [.agents/skills/skill-doctor/SKILL.md](https://github.com/warpdotdev/common-skills/blob/8792394ff1b6/.agents/skills/skill-doctor/SKILL.md) | `8792394ff1b6` | MIT | yes | Change only what would have prevented a real failure. |
| [alchaincyf/darwin-skill](https://github.com/alchaincyf/darwin-skill) | [SKILL.md](https://github.com/alchaincyf/darwin-skill/blob/8a8b66258e3c/SKILL.md) | `8a8b66258e3c` | MIT | yes | Paired before/after judging. |
| [trailofbits/skills](https://github.com/trailofbits/skills) | [plugins/code-improver/skills/skill-improver/SKILL.md](https://github.com/trailofbits/skills/blob/e4dd0bb5b155/plugins/code-improver/skills/skill-improver/SKILL.md) | `e4dd0bb5b155` | CC-BY-SA-4.0 | yes | Don't weaken a guarantee to close a finding. |
| [affaan-m/ECC](https://github.com/affaan-m/ECC) | [skills/skill-stocktake/SKILL.md](https://github.com/affaan-m/ECC/blob/d2ef2680594f/skills/skill-stocktake/SKILL.md) | `d2ef2680594f` | MIT | yes | Keep, improve, merge, retire verdicts. |
| [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) | [skills/skill-judge/SKILL.md](https://github.com/softaworks/agent-toolkit/blob/3027f20f3181/skills/skill-judge/SKILL.md) | `3027f20f3181` | MIT | yes | Knowledge delta. |
| [grafana/skills](https://github.com/grafana/skills) | [skills/grafana-core/skill-authoring/SKILL.md](https://github.com/grafana/skills/blob/8fb72a527961/skills/grafana-core/skill-authoring/SKILL.md) | `8fb72a527961` | Apache-2.0 |  |  |
| [mcollina/skills](https://github.com/mcollina/skills) | [skills/skill-optimizer/SKILL.md](https://github.com/mcollina/skills/blob/c75d70dbfbe9/skills/skill-optimizer/SKILL.md) | `c75d70dbfbe9` | MIT |  |  |
| [sanyuan0704/sanyuan-skills](https://github.com/sanyuan0704/sanyuan-skills) | [skills/skill-review/SKILL.md](https://github.com/sanyuan0704/sanyuan-skills/blob/08b6572ef108/skills/skill-review/SKILL.md) | `08b6572ef108` | MIT |  |  |
| [daymade/claude-code-skills](https://github.com/daymade/claude-code-skills) | [daymade-skill/skill-reviewer/SKILL.md](https://github.com/daymade/claude-code-skills/blob/0619a9543d9a/daymade-skill/skill-reviewer/SKILL.md) | `0619a9543d9a` | MIT |  |  |
| [tradermonty/claude-trading-skills](https://github.com/tradermonty/claude-trading-skills) | [skills/dual-axis-skill-reviewer/SKILL.md](https://github.com/tradermonty/claude-trading-skills/blob/163ceb48968c/skills/dual-axis-skill-reviewer/SKILL.md) | `163ceb48968c` | MIT |  |  |
| [expo/skills](https://github.com/expo/skills) | [.claude/skills/expo-skill-eval/SKILL.md](https://github.com/expo/skills/blob/a9e5bd3fa00b/.claude/skills/expo-skill-eval/SKILL.md) | `a9e5bd3fa00b` | MIT |  |  |
| [dboeckli/ai-agent-skills](https://github.com/dboeckli/ai-agent-skills) | [.claude/skills/skill-best-practices/SKILL.md](https://github.com/dboeckli/ai-agent-skills/blob/ab99d0c7b12e/.claude/skills/skill-best-practices/SKILL.md) | `ab99d0c7b12e` | MIT |  |  |

## interview

interview was written on 2026-11-16 from what these interview and spec skills agree on, starting from Matt Pocock's `grill-me`. Each source was read at its pin that day. All of them agree on these points: look things up instead of asking, ask only what changes the build, ask in dependency order, never build during the interview, end on coverage rather than a question count, and never present a guess as the user's decision. Six choices where they split were put to the owner, who picked: rounds over one question at a time (Pocock); the question tool with a numbered-text fallback; an open "why" question before any options (obra); a spec that records how-decisions as well as what and why; a file in the repo with an offer to file issues; and a fresh-reader builder check (obra) over a red-team pass (Sorbh) or none (Pocock). The issue split hands off to `issue` in this repo, and that hand-off is the owner's own design.

| Source | Path | Pin | License | Track | Contributed |
| --- | --- | --- | --- | --- | --- |
| [mattpocock/skills](https://github.com/mattpocock/skills) | [skills/productivity/grilling/SKILL.md](https://github.com/mattpocock/skills/blob/5863806dd4e1/skills/productivity/grilling/SKILL.md) | `5863806dd4e1` | MIT | yes | The design tree, rounds that ask the whole frontier, a recommendation on every question worded so "yes" accepts it, facts looked up by a background subagent while decisions wait for the user, and ending on confirmation. Its [docs/productivity/grill-me.md](https://github.com/mattpocock/skills/blob/5863806dd4e1/docs/productivity/grill-me.md): questions talk can't settle go to a prototype, "I don't know" is a real answer, and an oversized tree means splitting the scope. |
| [mattpocock/skills](https://github.com/mattpocock/skills) | [skills/engineering/to-spec/SKILL.md](https://github.com/mattpocock/skills/blob/5863806dd4e1/skills/engineering/to-spec/SKILL.md) | `5863806dd4e1` | MIT | yes | No file paths or code in the spec unless a snippet records a decision, the project's own nouns, and a spec that says something the user never said is a defect (from its docs page). |
| [obra/superpowers](https://github.com/obra/superpowers) | [skills/brainstorming/SKILL.md](https://github.com/obra/superpowers/blob/22f0b463e7a5/skills/brainstorming/SKILL.md) | `22f0b463e7a5` | MIT | yes | Asking why first with an open question because options steer, the opening restatement, anti-goals, reading whether the user wants the how, laying out two or three approaches, labeling the agent's calls, the hard gate on building, and the builder check with its three piles. Its [builder-check-prompt.md](https://github.com/obra/superpowers/blob/22f0b463e7a5/skills/brainstorming/builder-check-prompt.md) is adapted in `references/builder-check.md`; notice below. |
| [github/spec-kit](https://github.com/github/spec-kit) | [templates/commands/clarify.md](https://github.com/github/spec-kit/blob/edec7946375e/templates/commands/clarify.md) | `edec7946375e` | MIT | yes | The coverage list the agent checks itself against without reading it out, and asking only what materially changes the build. Its [spec template](https://github.com/github/spec-kit/blob/edec7946375e/templates/spec-template.md): prioritized scenarios that can each be built alone, Given/When/Then acceptance, and checkable goals. |
| [Sorbh/interview-me](https://github.com/Sorbh/interview-me) | [skills/interview-me/SKILL.md](https://github.com/Sorbh/interview-me/blob/ad9e1a886396/skills/interview-me/SKILL.md) | `ad9e1a886396` | MIT |  | Reading a GitHub issue with its comments as the input, splitting the scope past about eight areas, and the decisions table. |
| [enzed/skills](https://github.com/enzed/skills) | [interview/SKILL.md](https://github.com/enzed/skills/blob/dda28ad3fb5f/interview/SKILL.md) | `dda28ad3fb5f` | none stated |  | Thariq Shihipar's widely shared "interview me with AskUserQuestion, then write the spec" prompt, as a skill: exploring the code first, and non-obvious questions only. |
| [blencorp/lisa](https://github.com/blencorp/lisa) | [commands/plan.md](https://github.com/blencorp/lisa/blob/ea4bb125620d/commands/plan.md) | `ea4bb125620d` | none stated |  | Stopping once the spec is written. |
| [grp06/useful-codex-skills](https://github.com/grp06/useful-codex-skills) | [grill-me/SKILL.md](https://github.com/grp06/useful-codex-skills/blob/70eddd8ad596/grill-me/SKILL.md) | `70eddd8ad596` | MIT |  | Playing back each settled decision before the next question. |
| [kipperacademy/skillpper](https://github.com/kipperacademy/skillpper) | [grill-me/SKILL.md](https://github.com/kipperacademy/skillpper/blob/718ee6dbb463/grill-me/SKILL.md) | `718ee6dbb463` | none stated |  | Rounds sized to the question tool's limit, with the recommended option first. |
| [nklmilojevic/claude-spec-interviewer](https://github.com/nklmilojevic/claude-spec-interviewer) | [commands/spec-interview.md](https://github.com/nklmilojevic/claude-spec-interviewer/blob/dc77ada87c3a/commands/spec-interview.md) | `dc77ada87c3a` | none stated |  |  |
| [Yeachan-Heo/oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode) | [skills/deep-interview/SKILL.md](https://github.com/Yeachan-Heo/oh-my-claudecode/blob/dec7e4188c0e/skills/deep-interview/SKILL.md) | `dec7e4188c0e` | MIT |  |  |

Considered, not adopted: numeric ambiguity scores and thresholds (oh-my-claudecode), a cap of five questions (spec-kit), security hard blocks and an opt-in red-team pass, saved interview state, drift checks, and an HTML preview (Sorbh), writing the spec after every answer (spec-kit, Lisa), and a fixed persona of relentless grilling. The user's own words decide when to stop instead.

### Notice

`references/builder-check.md` adapts obra's builder-check prompt.

```text
MIT License

Copyright (c) 2025 Jesse Vincent

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

## issue

issue had no upstream skill. These issue-to-PR skills were reviewed against it on 2026-11-11, and their pins are the commits reviewed then. The section moved here from the skill's old `SOURCES.md`, which the 2026-11-14 cut to a single file removed. The 2026-11-15 rewrite restored the picking rules, sizing, review, local-dev test, branch, batch, unattended, and failure-path steps, along with the report. The sources weren't re-read for it. The old file also credited jssblck/agents and tobi/qmd, for the version bump and tagging the old skill did itself. That work belongs to release now, so those rows sit in its section. addyosmani/agent-skills appears under commit too. On 2026-11-16 an audit against Anthropic's [The Complete Guide to Building Skills for Claude](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf) moved branch and batch mode into `references/` (its progressive disclosure: most runs use neither) and added `scripts/candidates.py` for step 2's skip rules. Neither was taken from the sources below.

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

## job-search

job-search had no upstream skill: it follows the preferences Justin set in an interview on 2026-11-12. These job-search, application, and resume-tailoring skills were reviewed against it, led by career-ops (by far the most used) and srikar0805's career-agent. The rules most of them share (never invent experience, never submit for the user, fewer and better applications, keep a record of every posting seen) were already in the plan; the rows below credit what each added. v0.18.0 removed it on 2026-11-12, and it returned on 2026-11-16 as it stood before, made model-invocable with trigger phrases in its description and without its evals, tests, and Codex settings, per AGENTS.md. The sources weren't re-read for the return; the rows moved here from the skill's old `SOURCES.md`.

Pins are the commits reviewed on 2026-11-12. **Track** marks the sources worth checking for updates; the rest are credited only. No text was copied.

| Source | Path | Pin | License | Track | Contributed |
| --- | --- | --- | --- | --- | --- |
| [career-ops-hq/career-ops](https://github.com/career-ops-hq/career-ops) | [modes/oferta.md](https://github.com/career-ops-hq/career-ops/blob/eaa74c4b0d55/modes/oferta.md) | `eaa74c4b0d55` | MIT | yes | Checking the posting is live on the employer's own page before any work; warning signs (age, reposts, generic text, layoffs) shown as observations, never accusations. |
| [career-ops-hq/career-ops](https://github.com/career-ops-hq/career-ops) | [modes/apply.md](https://github.com/career-ops-hq/career-ops/blob/eaa74c4b0d55/modes/apply.md) | `eaa74c4b0d55` | MIT | yes | The knock-out question check before drafting answers. |
| [career-ops-hq/career-ops](https://github.com/career-ops-hq/career-ops) | [modes/followup.md](https://github.com/career-ops-hq/career-ops/blob/eaa74c4b0d55/modes/followup.md) | `eaa74c4b0d55` | MIT | yes | Follow-ups that lead with something concrete, never "just checking in", and stop after two. |
| [career-ops-hq/career-ops](https://github.com/career-ops-hq/career-ops) | [AGENTS.md](https://github.com/career-ops-hq/career-ops/blob/eaa74c4b0d55/AGENTS.md) | `eaa74c4b0d55` | MIT | yes | Treating posting and recruiter text as untrusted; never running code a recruiter sends. |
| [srikar0805/career-agent](https://github.com/srikar0805/career-agent) | [skills/job-hunt/SKILL.md](https://github.com/srikar0805/career-agent/blob/2a1a2b9a9529/skills/job-hunt/SKILL.md) | `2a1a2b9a9529` | MIT | yes | The strong / stretch / weak / blocked buckets; reporting the pattern across the shortlist; saving the full posting text; flagging an earlier rejection at the same employer. |
| [advaithsarva/linkedin-jobs-skill](https://github.com/advaithsarva/linkedin-jobs-skill) | [skills/linkedin-jobs/SKILL.md](https://github.com/advaithsarva/linkedin-jobs-skill/blob/51a6fa1f053b/skills/linkedin-jobs/SKILL.md) | `51a6fa1f053b` | MIT |  | Quoting pay exactly with its source; "unconfirmed" is not "fake". |
| [vmarafetti/right-fit](https://github.com/vmarafetti/right-fit) | [SKILL.md](https://github.com/vmarafetti/right-fit/blob/8ca471541301/SKILL.md) | `8ca471541301` | MIT |  | Showing what was skipped and why. |
| [proficientlyjobs/proficiently-claude-skills](https://github.com/proficientlyjobs/proficiently-claude-skills) | [skills/job-search/SKILL.md](https://github.com/proficientlyjobs/proficiently-claude-skills/blob/9bc1f6fd7af5/skills/job-search/SKILL.md) | `9bc1f6fd7af5` | none stated |  | Reading listing pages without whole-page text; resolving each job to the employer's own link; saving lasting preferences from feedback; noting connections at the company. |
| [proficientlyjobs/proficiently-claude-skills](https://github.com/proficientlyjobs/proficiently-claude-skills) | [skills/tailor-resume/SKILL.md](https://github.com/proficientlyjobs/proficiently-claude-skills/blob/9bc1f6fd7af5/skills/tailor-resume/SKILL.md) | `9bc1f6fd7af5` | none stated |  | Tailoring limits: titles and dates unchanged, no roles dropped, two pages at most. |
| [rwtibbs/open-to-work](https://github.com/rwtibbs/open-to-work) | [SKILL.md](https://github.com/rwtibbs/open-to-work/blob/e6f7f5aaa220/SKILL.md) | `e6f7f5aaa220` | MIT |  | Growing the answer bank only with answers the user confirmed; checking pages after export. |
| [alabenkhlifa/JobHunter](https://github.com/alabenkhlifa/JobHunter) | [job-hunter.skill.md](https://github.com/alabenkhlifa/JobHunter/blob/ef49f6fac64d/job-hunter.skill.md) | `ef49f6fac64d` | Apache-2.0 |  | Never carrying a board's pay estimate as the employer's figure. |
| [areeves9/daily-job-search](https://github.com/areeves9/daily-job-search) | [SKILL.md](https://github.com/areeves9/daily-job-search/blob/e92625317674/SKILL.md) | `e92625317674` | MIT |  | Saying so when nothing good turned up, instead of padding. |
| [wexxwuther/job-hunter](https://github.com/wexxwuther/job-hunter) | [job-hunter/SKILL.md](https://github.com/wexxwuther/job-hunter/blob/8c03dd4c6b7a/job-hunter/SKILL.md) | `8c03dd4c6b7a` | MIT |  |  |
| [amanattar/resume-tailoring-skill](https://github.com/amanattar/resume-tailoring-skill) | [SKILL.md](https://github.com/amanattar/resume-tailoring-skill/blob/998ee7e4b70b/SKILL.md) | `998ee7e4b70b` | MIT |  |  |
| [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | [tailored-resume-generator/SKILL.md](https://github.com/ComposioHQ/awesome-claude-skills/blob/be2a406907db/tailored-resume-generator/SKILL.md) | `be2a406907db` | none stated |  |  |
| [mayankjoshii/claude-job-skill](https://github.com/mayankjoshii/claude-job-skill) | [SKILL.md](https://github.com/mayankjoshii/claude-job-skill/blob/f0d29e4f608a/SKILL.md) | `f0d29e4f608a` | none stated |  |  |
| [yanliudesign/offer-toolkit-skill](https://github.com/yanliudesign/offer-toolkit-skill) | [job-search-skill/SKILL.md](https://github.com/yanliudesign/offer-toolkit-skill/blob/3b85d2e1b836/job-search-skill/SKILL.md) | `3b85d2e1b836` | MIT |  |  |

Considered, not adopted: filling and submitting forms in the browser (Justin submits himself), a weighted 1–5 score (three buckets read faster on a three-job list), repeated ATS keyword-scoring passes (terms are mirrored only where they're true), scheduled daily runs and Gmail scanning for rejections (he runs it on demand), and interview prep and outcome-learning modes (out of scope for now).

## music-creation

music-creation is what four songwriting skill collections agree on. This is an original condensed synthesis, not independent validation of the upstream methods. The 2026-11-14 cut removed it, and it returned on 2026-11-16 as it stood before, made model-invocable with trigger phrases in its description and without its evals and Codex settings, per AGENTS.md. The sources weren't re-read for the return; the rows moved here from the skill's old `SOURCES.md`.

All four were reviewed on 2026-10-25 at the pinned commits, so the pins are the versions actually read.

| Source | Path | Pin | License | Track | Contributed |
| --- | --- | --- | --- | --- | --- |
| [bitwize-music-studio/claude-ai-music-skills](https://github.com/bitwize-music-studio/claude-ai-music-skills) (B) | [whole repo](https://github.com/bitwize-music-studio/claude-ai-music-skills/tree/597d928fb2c8) | `597d928fb2c8` | CC0-1.0 | yes | Lyric writing/revision, voice review, Suno packaging, album cohesion. |
| [jtydhr88/music-composition-skills](https://github.com/jtydhr88/music-composition-skills) (C) | [whole repo](https://github.com/jtydhr88/music-composition-skills/tree/5d5d22803517) | `5d5d22803517` | MIT | yes | Motifs, melody, harmony, groove, arrangement, generation handoff. |
| [jtydhr88/lyric-writing-skills](https://github.com/jtydhr88/lyric-writing-skills) (L) | [whole repo](https://github.com/jtydhr88/lyric-writing-skills/tree/d2c3c780afea) | `d2c3c780afea` | MIT | yes | Intent, imagery, lyric structure, rhyme, language-specific prosody. |
| [melodic-software/claude-code-plugins](https://github.com/melodic-software/claude-code-plugins) (M) | [plugins/songwriting](https://github.com/melodic-software/claude-code-plugins/tree/aa42c27ed277/plugins/songwriting) | `aa42c27ed277` | MIT | yes | Coaching, object writing, rhyme, prosody, form, diagnosis, Suno. |

The review downloaded 346 text files spanning instructions, references, and notices. It inventoried entrypoints and examined representative core instructions and relevant reference sections; it was not a line-by-line audit of every document. No upstream scripts were executed. Operational and release modules were screened for scope rather than incorporated wholesale.

### Convergence prioritized

| Principle | Supporting source locations |
| --- | --- |
| Intent and existing constraints | B album-conceptualizer; C mc-workflow; L lw-song-intent; M workflow. |
| Natural stress, phrasing, singability | B lyric-writer; C mc-melody and mc-vocal-direction; L lw-english; M meter-prosody. |
| Memorable focus and hook placement | B lyric-writer; C mc-arrangement-arch and mc-development; L lw-structure; M song-form. |
| Section purpose, contrast, development | B lyric-writer and lyric-refiner; C mc-arrangement-arch; L lw-structure; M song-form and diagnose. |
| Specific voice and coherent imagery | B lyric-writer and voice-checker; L lw-imagery and lw-narrative; M object-writing and metaphor. C supplies the musical counterpart. |
| Rhyme serving meaning and phrasing | B lyric-writer/craft-reference.md; L lw-rhyme; M rhyme and rhyme-strategy. |
| Targeted revision | B lyric-refiner and voice-checker; C mc-ai-tell-audit; L lw-ai-tell-audit; M diagnose. |
| Separate words from musical instructions | B suno-engineer; C mc-render-compile; L lw-workflow handoff; M suno. |

Agreement is not independent empirical evidence: C and L share an author, while L and M draw substantially on Pat Pattison. Count shared teachers as shared lineage rather than independent confirmation.

Composition detail comes mainly from C; coaching particularly from M/L; optional album planning mainly from B. These complement the common core without pretending all projects cover them equally. Suno is a main workflow and scope is songs, arrangements, and optional album planning by explicit user choice.

### Differences resolved

- Replace fixed word, syllable, section, and genre quotas with actual phrasing and relevant platform constraints.
- Make chorus variation, asymmetry, subtraction, and rhyme breaks purposeful options, not compulsory anti-AI devices.
- Allow direct, atmospheric, and instrumental work without compulsory narratives or photographable anchors.
- Examine voice and specificity without forbidden-word lists, AI-authorship verdicts, or numerical acceptance thresholds.
- Match lexical stress to actual musical emphasis rather than always beats one and three.
- Put the defining Suno priority early without a universal prompt-order recipe.
- Resolve obvious pronunciation from context; ask about meaningful ambiguity.
- Verify changeable Suno controls rather than preserving conflicting version-specific instructions.
- Use compact plans rather than mandatory schemas, approval gates, model tiers, or upstream plugin dependencies.
- Exclude mixing/mastering, artwork, marketing, distribution, and release operations according to the user's scope.

No book passages, commercial lyrics, or exhaustive upstream reference corpora are bundled. The notices follow. Upstream corpus claims and numerical thresholds were not independently reproduced and are not inherited as rules.

### Notices

music-creation synthesizes guidance from the four projects above. Original wording and focused procedures replace the upstream corpora. Book and song quotations are not included.

Bitwize publishes its repository under CC0 1.0: https://creativecommons.org/publicdomain/zero/1.0/

The following upstream MIT notices are retained for adaptations. Their licenses do not relicense third-party books, lyrics, or quotations mentioned upstream.

#### composition

```text
MIT License

Copyright (c) 2026 Terry Jia

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

#### lyrics

```text
MIT License

Copyright (c) 2026 Terry Jia

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

#### melodic

```text
MIT License

Copyright (c) 2026 Melodic Software

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

## prospect

prospect had no upstream skill: it follows Stone Dragon Media's own outreach rules. These cold-outreach and prospecting skills were reviewed against it, led by coreyhaines31's cold-email and prospecting (the latter's `references/local-prospecting.md` is the closest match). The 2026-11-14 cut removed it, and it returned on 2026-11-16 as it stood before, made model-invocable with trigger phrases in its description and without its evals and Codex settings, per AGENTS.md. The sources weren't re-read for the return; the rows moved here from the skill's old `SOURCES.md`.

Pins are the commits reviewed on 2026-11-11. **Track** marks the sources worth checking for updates; the rest are credited only. No text was copied.

| Source | Path | Pin | License | Track | Contributed |
| --- | --- | --- | --- | --- | --- |
| [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | [skills/cold-email/SKILL.md](https://github.com/coreyhaines31/marketingskills/blob/1f837447b20b/skills/cold-email/SKILL.md) | `1f837447b20b` | MIT | yes | One low-friction ask, by default the offer to send notes; short plain subject lines. |
| [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | [skills/prospecting/SKILL.md](https://github.com/coreyhaines31/marketingskills/blob/1f837447b20b/skills/prospecting/SKILL.md) | `1f837447b20b` | MIT | yes | Preferring an engaged owner; recording where each contact was published. |
| [humanizerai/agent-skills](https://github.com/humanizerai/agent-skills) | [skills/cold-email/SKILL.md](https://github.com/humanizerai/agent-skills/blob/307912e3acdc/skills/cold-email/SKILL.md) | `307912e3acdc` | MIT |  | The word-count ceiling. |
| [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | [sales/skills/draft-outreach/SKILL.md](https://github.com/anthropics/knowledge-work-plugins/blob/877a617b435e/sales/skills/draft-outreach/SKILL.md) | `877a617b435e` | Apache-2.0 |  | The word-count ceiling. |
| [mbfinotti/sales-skills](https://github.com/mbfinotti/sales-skills) | [skills/sales-outreach-personalization/SKILL.md](https://github.com/mbfinotti/sales-skills/blob/b2ed3628695e/skills/sales-outreach-personalization/SKILL.md) | `b2ed3628695e` | MIT |  |  |
| [mbfinotti/sales-skills](https://github.com/mbfinotti/sales-skills) | [skills/cold-email-deliverability/SKILL.md](https://github.com/mbfinotti/sales-skills/blob/b2ed3628695e/skills/cold-email-deliverability/SKILL.md) | `b2ed3628695e` | MIT |  |  |
| [louisblythe/sales-skills](https://github.com/louisblythe/sales-skills) | [skills/outbound-prospecting/SKILL.md](https://github.com/louisblythe/sales-skills/blob/e0f13a6eb41b/skills/outbound-prospecting/SKILL.md) | `e0f13a6eb41b` | none stated |  |  |
| [louisblythe/sales-skills](https://github.com/louisblythe/sales-skills) | [skills/follow-up-discipline/SKILL.md](https://github.com/louisblythe/sales-skills/blob/e0f13a6eb41b/skills/follow-up-discipline/SKILL.md) | `e0f13a6eb41b` | none stated |  |  |
| [techking007/agency-client-audit-skill](https://github.com/techking007/agency-client-audit-skill) | [skills/agency-client-audit/SKILL.md](https://github.com/techking007/agency-client-audit-skill/blob/77807aa5006a/skills/agency-client-audit/SKILL.md) | `77807aa5006a` | MIT |  |  |

Considered, not adopted: opening with the observation before Justin's introduction (most sources do; left for the owner to decide), 3 to 5 follow-ups (one is deliberate for a local agency), and secondary sending domains with warmup (advice for bulk senders).

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

## seo-audit

seo-audit is what the most-installed SEO skills agree on. Where they disagree, the skill follows Google's current documentation. The 2026-11-14 cut removed it, and it returned on 2026-11-16 as it stood before, made model-invocable with trigger phrases in its description and without its evals and Codex settings, per AGENTS.md. The sources weren't re-read for the return; the rows moved here from the skill's old `SOURCES.md`.

Pins were backfilled on 2026-11-11 from each repo's latest commit, after the skill was written. They mark where to start watching for changes, not the exact version that was read. **Track** marks the sources worth checking for updates; the rest are credited only.

| Source | Path | Pin | License | Track | Contributed |
| --- | --- | --- | --- | --- | --- |
| [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | [skills/seo-audit/SKILL.md](https://github.com/coreyhaines31/marketingskills/blob/1f837447b20b/skills/seo-audit/SKILL.md) | `1f837447b20b` | MIT |  |  |
| [addyosmani/web-quality-skills](https://github.com/addyosmani/web-quality-skills) | [skills/seo/SKILL.md](https://github.com/addyosmani/web-quality-skills/blob/afa8da942115/skills/seo/SKILL.md) | `afa8da942115` | MIT |  |  |
| [AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo) | [skills/seo/SKILL.md](https://github.com/AgriciDaniel/claude-seo/blob/cca7e4a26799/skills/seo/SKILL.md) | `cca7e4a26799` | MIT |  |  |
| [firecrawl/skills](https://github.com/firecrawl/skills) | [skills/workflows/firecrawl-seo-audit/SKILL.md](https://github.com/firecrawl/skills/blob/667d3f7fe804/skills/workflows/firecrawl-seo-audit/SKILL.md) | `667d3f7fe804` | ISC |  |  |
| [ReScienceLab/opc-skills](https://github.com/ReScienceLab/opc-skills) | [skills/seo-geo/SKILL.md](https://github.com/ReScienceLab/opc-skills/blob/d7865b345b8d/skills/seo-geo/SKILL.md) | `d7865b345b8d` | Apache-2.0 |  |  |
| [zubair-trabzada/geo-seo-claude](https://github.com/zubair-trabzada/geo-seo-claude) | [geo/SKILL.md](https://github.com/zubair-trabzada/geo-seo-claude/blob/989cae01e8eb/geo/SKILL.md) | `989cae01e8eb` | MIT |  |  |
| [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | [marketing/skills/seo-audit/SKILL.md](https://github.com/anthropics/knowledge-work-plugins/blob/877a617b435e/marketing/skills/seo-audit/SKILL.md) | `877a617b435e` | Apache-2.0 |  |  |
| [affaan-m/ECC](https://github.com/affaan-m/ECC) | [skills/seo/SKILL.md](https://github.com/affaan-m/ECC/blob/d2ef2680594f/skills/seo/SKILL.md) | `d2ef2680594f` | MIT |  |  |
| [sanity-io/agent-toolkit](https://github.com/sanity-io/agent-toolkit) | [skills/seo-aeo-best-practices/SKILL.md](https://github.com/sanity-io/agent-toolkit/blob/3ed3a143f8d3/skills/seo-aeo-best-practices/SKILL.md) | `3ed3a143f8d3` | MIT |  |  |
| [aaron-he-zhu/seo-geo-claude-skills](https://github.com/aaron-he-zhu/seo-geo-claude-skills) | [optimize/technical-seo-checker/SKILL.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/3a1578a63cdd/optimize/technical-seo-checker/SKILL.md) | `3a1578a63cdd` | Apache-2.0 |  |  |
| [Bhanunamikaze/Agentic-SEO-Skill](https://github.com/Bhanunamikaze/Agentic-SEO-Skill) | [SKILL.md](https://github.com/Bhanunamikaze/Agentic-SEO-Skill/blob/445c46c268d9/SKILL.md) | `445c46c268d9` | MIT |  |  |
| [squirrelscan/skills](https://github.com/squirrelscan/skills) | [skills/audit-website/SKILL.md](https://github.com/squirrelscan/skills/blob/29f17762cc1c/skills/audit-website/SKILL.md) | `29f17762cc1c` | MIT | yes | The fix loop. |
| [aleclindz/seo-skill-bench](https://github.com/aleclindz/seo-skill-bench) | [whole repo](https://github.com/aleclindz/seo-skill-bench/tree/95e7256ffb8c) | `95e7256ffb8c` | MIT | yes | The "look before you recommend" rule: skills lost the most points for "fixing" things that were already fine. |

Other sources:

- [Google Search Central documentation](https://developers.google.com/search/docs): the tiebreaker when the skills disagree. It has no commit to pin, so recheck the pages the skill relies on when you review it.

## sprite

sprite adapts its prompt structure from a post, not a repo, so there is nothing to pin. The 2026-11-14 cut removed it, and it returned on 2026-11-16 as it stood before, made model-invocable with trigger phrases in its description and without its evals and Codex settings, per AGENTS.md. The sources weren't re-read for the return; its credits moved here from the skill's old `SOURCES.md`.

Other sources:

- **The Sprite Wizard's "prompt bible"** on r/aigamedev (post URL not recorded). The prompt structure comes from it: a logical pixel grid with an exact nearest-neighbor enlargement, a ranked detail budget, and the AI-cliché blocklist with its "don't make it plain" guard.
- **[Sprite Grid](https://thespritewizard.itch.io/sprite-grid)**, The Sprite Wizard's processor for generated art. `sprite_clean.py` plays the same role here.

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
