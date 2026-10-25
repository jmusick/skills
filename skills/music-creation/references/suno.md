# Suno creation and iteration

## Prepare a coherent song

Start from supplied lyrics, music, or the requested sound. Reconcile genre, vocal delivery, arrangement, and lyric density. For instrumentals, preserve the absence of lyrics and develop a musical hook.

Translate choices into compatible instructions. Assign influences to roles, such as a rock rhythm section with electronic texture. Avoid unrelated genre stacks and synonymous mood adjectives.

## Deliver separate pasteable fields

Unless the request is narrower, provide:

- Title: preserve a supplied title or propose one.
- Style: concise prose for defining sound, groove or tempo where relevant, instruments, vocal or instrumental character, section contrast, and ending. Put the defining priority early; there is no universally superior ordering.
- Lyrics: words to sing with simple section labels such as `[Verse]` and `[Chorus]`. For instrumentals, state that Instrumental should be enabled and no sung lyrics supplied; put any section plan separately.
- Exclusions: genuinely unwanted elements for the dedicated exclusion field where available. Do not invent exclusions for every song.

Give each field its own block so the user can copy it in one motion, for example:

````markdown
**Title:** Porch Light

**Style**
```text
Warm acoustic folk-pop, fingerpicked guitar and brushed drums, intimate low male vocal; sparse verses, chorus opens up with harmonies, ends on solo guitar
```

**Lyrics**
```text
[Verse 1]
...

[Chorus]
...
```

**Exclude**
```text
electric guitar
```
````

Leave out the Exclude block when nothing needs excluding.

Keep explanations and extensive production notes outside the lyric content. Parentheses may be performed as words or backing vocals; use them only intentionally. Section/performance tags are probabilistic cues, not guaranteed commands. Prefer a few useful cues over invented syntax.

Keep a clean master lyric. For pronunciation problems, create a separate generation version and a small substitution list. Resolve clear context normally; ask about genuinely ambiguous names, dialect, or readings rather than every common homograph. Packaging supplied lyrics does not authorize rewriting them.

Ensure lyrics and arrangement agree on order, repeats, vocal identity, instrumental passages, and ending.

## Verify changeable platform details

Do not freeze model names, limits, credit prices, plan access, sliders, duration caps, or UI controls into permanent rules. Check the current interface or official documentation when the task depends on them. Otherwise give a version-neutral package and identify unresolved controls.

Separate verified features from community observations and proposed experiments. A prompt cannot guarantee exact key, BPM, chords, bars, exclusions, pronunciation, or duration. Preserve precise requirements in the musical plan even when the generator approximates them.

Official starting points checked 2026-10-25:

- [Custom mode and supplied lyrics](https://help.suno.com/en/articles/2415873).
- [Excluding elements](https://help.suno.com/en/articles/3161921).
- [Reusing prompts and changing endings](https://help.suno.com/en/articles/2417409).

## Iterate against evidence

Use supplied audio or the user's listening report. Without audio access, do not invent listening impressions, timestamps, or measurements.

Judge compliance with the brief separately from musical effectiveness. A pleasing deviation can be worth keeping; literal compliance does not prove quality.

Change the smallest useful variable or related group, holding other material steady for comparison. Keep prompts/settings associated with takes when a project log exists. When attempts repeatedly fail, reconsider the musical plan or a supported editing path rather than regenerating blindly.

Starting hypotheses: rushed or missing words suggest density or competing instructions; vague genre suggests unclear instrument roles or groove; identical sections suggest missing contrast; generic vocals suggest imprecise register, articulation, or texture; abrupt endings suggest an overloaded section plan or duration mismatch. Treat these as experiments, not diagnoses established without listening.

A package is not audio. Use generation tools only when available and within the user's authorized service actions and budget. Do not upload material, spend credits, or publish merely because drafting is complete. This skill supplies no renderer and requires no Suno integration.
