# References

The sources each skill was built from, kept in one file so the skills themselves stay a single `SKILL.md`. Add a section here when a skill draws on outside material.

In each table, **Pin** marks where the source stood when it was read, so a later check can diff from there. **Track** marks the sources worth checking for updates; the rest are credited only. **Contributed** names the rules that came from that one source; rules most sources share have no owner. No text was copied from any source, so there is no NOTICE file.

## humanize

The baseline is Wikipedia's [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), maintained by WikiProject AI Cleanup. humanize follows its catalog and caveats, so re-read it first when updating the skill: the page dates each sign, and signs move to its "Historical indicators" section as models change.

| Source | Pin | License | Track | Contributed |
| --- | --- | --- | --- | --- |
| [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) | [revision 1385960173](https://en.wikipedia.org/w/index.php?oldid=1385960173) (2026-11-16) | CC BY-SA 4.0 | yes | The pattern catalog and its 2026 dating (corrective-framing disclaimers, "identify" phrasing, newer AI vocabulary, the comma-and-period rhythm left behind when dashes are suppressed), the regression-to-the-mean framing, the warning not to fix only the surface, the signs of human writing, the ineffective indicators, and the caution against guessing authorship. |

These anti-AI-writing skills supplement the article; most of them descend from it. Their pins were backfilled on 2026-11-11 from each repo's latest commit, after the original skill was written, so they mark where to start watching rather than the exact version read. The exceptions are blader/humanizer and the last three rows, which were reviewed at their pins on 2026-11-11. On 2026-11-15 the tracked repos had no changes past their pins beyond formatting.

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
