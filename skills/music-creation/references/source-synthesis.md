# Source comparison and decisions

Reviewed 2026-10-25. This is an original condensed synthesis, not independent validation of the upstream methods.

## Snapshots inspected

| Source | Revision | Contribution |
| --- | --- | --- |
| [Bitwize Music Skills](https://github.com/bitwize-music-studio/claude-ai-music-skills) (B) | `597d928fb2c8316ee13159771405813174aa01de` | Lyric writing/revision, voice review, Suno packaging, album cohesion. |
| [Music Composition Skills](https://github.com/jtydhr88/music-composition-skills) (C) | `5d5d22803517ac5828a01218e775555920451dd9` | Motifs, melody, harmony, groove, arrangement, generation handoff. |
| [Lyric Writing Skills](https://github.com/jtydhr88/lyric-writing-skills) (L) | `d2c3c780afeaaba0801c324fa2d3a9100277e8e1` | Intent, imagery, lyric structure, rhyme, language-specific prosody. |
| [Melodic songwriting plugin](https://github.com/melodic-software/claude-code-plugins/tree/main/plugins/songwriting) (M) | `aa42c27ed2778f1c8122e193f2a796bd8f5055e1` | Coaching, object writing, rhyme, prosody, form, diagnosis, Suno. |

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

No book passages, commercial lyrics, or exhaustive upstream reference corpora are bundled. See [NOTICE.md](../NOTICE.md). Upstream corpus claims and numerical thresholds were not independently reproduced and are not inherited as rules.
