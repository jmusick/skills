# Sources

music-creation is what four songwriting skill collections agree on. This is an original condensed synthesis, not independent validation of the upstream methods.

All four were reviewed on 2026-10-25 at the pinned commits, so the pins are the versions actually read.

| Source | Path | Pin | License | Track | Contributed |
| --- | --- | --- | --- | --- | --- |
| [bitwize-music-studio/claude-ai-music-skills](https://github.com/bitwize-music-studio/claude-ai-music-skills) (B) | [whole repo](https://github.com/bitwize-music-studio/claude-ai-music-skills/tree/597d928fb2c8) | `597d928fb2c8` | CC0-1.0 | yes | Lyric writing/revision, voice review, Suno packaging, album cohesion. |
| [jtydhr88/music-composition-skills](https://github.com/jtydhr88/music-composition-skills) (C) | [whole repo](https://github.com/jtydhr88/music-composition-skills/tree/5d5d22803517) | `5d5d22803517` | MIT | yes | Motifs, melody, harmony, groove, arrangement, generation handoff. |
| [jtydhr88/lyric-writing-skills](https://github.com/jtydhr88/lyric-writing-skills) (L) | [whole repo](https://github.com/jtydhr88/lyric-writing-skills/tree/d2c3c780afea) | `d2c3c780afea` | MIT | yes | Intent, imagery, lyric structure, rhyme, language-specific prosody. |
| [melodic-software/claude-code-plugins](https://github.com/melodic-software/claude-code-plugins) (M) | [plugins/songwriting](https://github.com/melodic-software/claude-code-plugins/tree/aa42c27ed277/plugins/songwriting) | `aa42c27ed277` | MIT | yes | Coaching, object writing, rhyme, prosody, form, diagnosis, Suno. |

The review downloaded 346 text files spanning instructions, references, and notices. It inventoried entrypoints and examined representative core instructions and relevant reference sections; it was not a line-by-line audit of every document. No upstream scripts were executed. Operational and release modules were screened for scope rather than incorporated wholesale.

## Convergence prioritized

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

## Differences resolved

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

No book passages, commercial lyrics, or exhaustive upstream reference corpora are bundled. See [NOTICE.md](NOTICE.md). Upstream corpus claims and numerical thresholds were not independently reproduced and are not inherited as rules.
