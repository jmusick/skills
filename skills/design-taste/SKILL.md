---
name: design-taste
description: Audit, polish, or check web UI so it stops reading as AI-generated. Covers the generated-page tells (tiny uppercase eyebrow labels, rows of identical icon cards, gradient text, 01/02/03 numbering, one accented headline word, cream-and-terracotta palettes), the accessibility and typography quality floor, motion timing, and a two-round screenshot critique. Use when the user types /design-taste; says a page, component, or app looks generic, templated, sloppy, or "AI-made"; asks to de-slop, polish, or review a UI's design before shipping; asks whether a design reads as AI; or as the check pass after building new UI. Not for picking a fresh aesthetic direction when frontend-design is installed (that skill owns direction, this one checks the result), not for backend or non-visual code, and not for prose (use humanize).
---

# Design taste

Find and remove what makes an interface read as generated, and hold it to the quality floor that careful designers ship by default.

## Why generated UI looks the way it does

A model builds the average of every page it has seen: a centered headline, a small label above it, three icon cards, a soft gradient, a few thin rules. Nothing in it is wrong and nothing in it was decided. A tell is a device that shows up by default, whatever the subject. The fix is a decision made from the subject, never a different stock device. The last round of "fixes" (warm cream, serif display, terracotta accent, editorial hairlines) became the most recognizable generated look of all, because models adopted the remedy wholesale.

## Modes

- **Audit** (default when pointed at existing UI, or when the user says "review", "flag only", or "does this look AI"): report findings and change nothing. Use the report format at the end.
- **Polish:** fix in place with the smallest changes that clear the findings. Keep the project's components, tokens, density, and identity.
- **Build:** a new page or screen. If frontend-design is installed, let it set the direction, then use this skill for the floor and the critique loop. Otherwise follow `references/direction.md` first, and also when a polish request is really a redesign.

## Hard rules

1. **The brief wins.** If the user or the brand pins a look, a color, a font, or one of the tells below, follow it exactly. The tells are defaults to avoid where the brief leaves a choice open, not bans on what the user asked for.
2. **Never invent proof.** No customers, logos, testimonials, quotes, press mentions, ratings, user counts, uptime, benchmarks, or "trusted by" lines the user didn't supply. Use a visible placeholder such as `[metric]`. Sample content where the brief has gaps (dish names, room names, project titles) is fine, as long as the report lists it for the user to replace.
3. **Refinement preserves.** In audit and polish, keep the existing identity, copy, behavior, and everything outside the request. Ask before changing factual copy or adding a claim.
4. **Removal is half the job.** A page stripped of its ornaments and given nothing in their place reads as thin and unfinished. Fill the space with scale (make the main thing bigger), the full real content, a real picture of the subject, or one deliberate empty area. Never fill it with a different ornament.
5. **Report only checks you ran.** If you couldn't take screenshots or run the lint script, say "not verified" for those checks.

## The tells

Treat a single hit as a question and a cluster as a finding. `references/tells.md` has the dated registry, the reason each one reads as generated, what to do instead, and when it's fine.

**Structure**
- Same-size cards of icon, heading, and text as the page's structure; cards nested in cards.
- The hero-metric template: big number, small label, supporting stats, gradient accent.
- Centered headline, subtitle, two buttons, screenshot below, then logos, three features, testimonial, pricing, call to action, in that order.
- Section numbers (01 / 02 / 03, "Step 2") on content that isn't a real sequence.
- Every section in the same layout family; a distinctive first screen followed by stock blocks.
- Fake dashboards of grey bars and donut charts standing in for a real interface.

**Type**
- A tiny tracked uppercase eyebrow label above headings, or a pill badge ("New", "Introducing") above the hero headline.
- One word of a headline set in italic, serif, a different color, or underlined.
- Headlines that run to three or more lines at display size; a full sentence set as a headline.
- Monospace used as a "technical" costume for labels and captions rather than for code or data.
- The typeface you'd reach for on any project, chosen without a reason from this subject.

**Surface and color**
- Violet or indigo gradients, gradient-filled text, glowing buttons.
- The same soft grey shadow under every card; one radius on everything regardless of hierarchy.
- Glass panels and backdrop blur as decoration; floating pill navigation.
- Cream ground with a high-contrast serif and a terracotta or clay accent (near `#F4F1EA` and `#D97757`).
- Near-black ground with one neon or acid accent and glowing edges.
- Broadsheet cosplay: hairline rules everywhere, zero radius, dense newspaper columns, crop marks.
- A colored left border thicker than 1px on cards, callouts, or alerts.
- Emoji or Unicode glyphs standing in for an icon system.

**Copy**
- "Elevate", "seamless", "unleash", "next-gen", "supercharge", and other copy that sells instead of saying what the thing does.
- Meta strings joined with middle dots (`A · B · C`), `WORD — fragment` labels, `→` appended to every link.
- "Scroll to explore", bouncing chevrons, performative section labels ("Field notes", "Quietly trusted by").
- Generic names (Acme, John Doe, Nexus) and round invented numbers (99.9%, 10x).

**Motion**
- The same fade-and-rise entrance on every section; hover lift on every card.
- Pulsing status dots, perpetual shimmer, and other loops with no meaning.

## Quality floor

Build to this without announcing it, and check it on the result. `references/floor.md` has the full list with the reason for each rule.

- Body text contrast at least 4.5:1, large text and UI boundaries at least 3:1. Secondary text on a colored surface is tinted from that color, not grey.
- Every interactive element has a visible `:focus-visible` state. Never remove an outline without a replacement.
- Real `<button>` for actions and `<a>` for navigation. Icon-only buttons get `aria-label`. Inputs get a visible label.
- Responsive down to 390px wide with no horizontal scroll. Touch targets at least 44px. Never disable zoom.
- Body text 16px or more, line length 45 to 75 characters, line height 1.4 to 1.6 for body and about 1.1 for display. Headings use `text-wrap: balance`.
- `font-variant-numeric: tabular-nums` on prices, counters, timers, and number columns.
- Hover, active, focus, disabled, loading, empty, and error states all exist. Errors say what went wrong and how to fix it.
- `<img>` has width, height, and alt text. Long words, URLs, and user content can't break the layout.
- Theme the parts browsers draw by default: text selection, focus rings, scrollbars, `color-scheme`, and `<meta name="theme-color">`.

## Motion

Before animating anything, read `references/motion.md`. It has the frequency rule (the more often the user sees something, the less it moves, and anything seen hundreds of times a day doesn't animate at all), durations, easing, recipes, and reduced-motion and performance rules. One orchestrated moment on a page beats effects scattered across every section.

## Critique loop

1. **Lint the source.** Run `python <skill-dir>/scripts/lint_tells.py <files or folder>` (use `python3` if `python` isn't found). It flags floor violations as `FAIL` and tells as `WARN`. Fix each `FAIL`. Treat each `WARN` as wrong unless you can defend it in one sentence. When the brief asks for a flagged device, pass `--allow <rule>` and note it in the report. The script reads source, not the rendered page, so a clean run is not a pass.
2. **Capture.** Screenshot the full page at 1440px and 390px wide, plus the user's own viewport if you know it, with entrance motion settled or disabled so nothing reads as missing. Use whatever browser tool the environment has. Open every capture and confirm it shows what you think it shows.
3. **Look.** Judge the pictures, not the code. Ask:
   - If someone left after the first screen, what would they remember an hour later? If the answer is a mood, the idea hasn't landed.
   - Does each screen have one dominant thing, with the big things big and the small things small?
   - Does anything from the tells list show? Do neighboring sections share a layout?
   - Does any text overflow, wrap badly, or sit on a low-contrast ground at either width?
   - Is every section the brief asked for present, complete, and findable in seconds?
4. **Fix and look once more.** Fix the top problems in one batch, recapture the same widths, and look again. Two rounds is the ceiling. Open-ended self-review costs the user time and tends to make the page worse, so stop after the second round and report what still falls short.

## Judgment calls

These have no single right answer. Decide per project and say what you decided.

- **Named fonts.** Lists of "premium" faces and lists of banned faces both exist, and every published list has become the next wave of tells within months. Don't use a list in either direction: choose a face whose character fits the subject, and avoid the one you'd pick for any project.
- **How much motion.** There is no quota of moving elements, and per-section entrances are a tell. Use the frequency rule and the one-moment rule.
- **Monospace, hairline rules, and numbering.** These are common on award-winning sites and are also what generators copy first. They're tells when they decorate and fine when they carry information: code, data, real tables, a real sequence.
- **Restraint versus richness.** "Remove one accessory" and "a stripped page loses to a fuller one" are both true. Remove ornament, then add real content and scale until each screen is full.
- **Small conventions.** Pure black versus near-black, sentence case versus Title Case, shadows versus borders for depth, square versus pill buttons. Follow the project's existing convention. The same detail done two ways in one project is a finding; a consistent choice is not.
- **Asking versus deciding.** Ask when a missing fact blocks the work or the user wants to steer; otherwise decide, state the reading, and show a draft early.

## Report

Group findings by section (Tells, Floor, Motion, Critique), most severe first, one row per root cause listing every place it occurs:

| Severity | Location | Before | After | Why |
| --- | --- | --- | --- | --- |

`HIGH` breaks use or accessibility. `MEDIUM` is a visible tell or inconsistency. `LOW` is isolated polish. Location is `path/to/file:line`. Then list sample content to replace, any tell kept because the brief asked for it, and any check marked "not verified". If nothing needs fixing, say so and stop; over-polishing is its own fingerprint.
