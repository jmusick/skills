# Prompting image models for sprites

Image models draw a polished single illustration and a sloppy sprite. Left to guess, they pack every surface with texture, rim light and ornament, round the pixels off, lose count of frames, and redraw the character a little differently each time. That is what makes AI sprites look like AI. The prompt's job is to take the guessing away: a clear art direction, a small pixel grid, a short palette, a ranked list of the details that matter, and a list of the clichés to leave out. The cleanup script then fixes what the model still gets wrong (the exact grid, stray colors, the outline).

## Contents
- [The three levers](#the-three-levers)
- [The order of work](#the-order-of-work)
- [Model sheet template](#model-sheet-template)
- [Clip sheet template](#clip-sheet-template)
- [The cliché list](#the-cliché-list)
- [Field notes](#field-notes)
- [Pose lists for common clips](#pose-lists-for-common-clips)
- [Judging a sheet](#judging-a-sheet)
- [Rerolling](#rerolling)

## The three levers

1. **Color direction.** A thin palette and a small frame. List the exact hex colors (8 to 20) and keep each material to about three values: shadow, base, highlight.
2. **Detail hierarchy.** Pixels are big, so a sprite carries little detail. Rank the features that identify the character and tell the model to spend its pixels on those, in that order, and drop everything else.
3. **Restrictions.** Name the clichés to leave out (the list below), and say that leaving them out doesn't mean making the character plain.

Without an art direction the model fills the gap with its defaults, and its defaults are the clichés.

## The order of work

1. **Model sheet first.** For a new character, generate one standalone sprite in a neutral pose and get the user's OK on the design. Every clip sheet attaches it as a reference. A character described only in words comes out different in every sheet; a character shown in a reference image stays put.
2. **One clip per image.** One animation per generation, one row, a stated number of frames. Models lose count and mix poses when one image holds several animations.
3. **Attach the reference every time,** and say in words that it's the same character. For an existing game character, attach its `*_preview_8x.png` from `ArtSource/` instead of a model sheet.
4. **Same wording across a character's prompts.** Only the asset line, layout, frame list and output lines change between clips. Identical CHARACTER, ART DIRECTION and DETAIL BUDGET text is what keeps the clips matching.

## Model sheet template

Fill every line. Labeled sections beat a paragraph; the model treats each line as its own requirement.

```text
Create ONE standalone 2D pixel-art character sprite for a top-down retro arcade game about a kaiju rampaging through a city at night.

CHARACTER:
<Name>, <one or two sentences: what it is, body shape, main colors, 2-4 signature features, its attitude>.
Full body, side view facing right, neutral standing pose with personality. Centered composition. Strong, recognizable silhouette.

PIXEL ART CONSTRUCTION:
- Final canvas: 1024 x 1024 pixels.
- Design using a logical 64 x 64 pixel grid; the character fills about 52 pixels of its height.
- Enlarge exactly 16x using nearest-neighbor scaling, so every logical pixel is a uniform 16 x 16 block.
- Consistent pixel size throughout. No antialiasing or fractional-looking pixels. Crisp, hard pixel boundaries.
- Maximum <N> solid colors, only these: <hex list, outline first>.
- No gradients or dithering.

ART DIRECTION:
Authentic, deliberately constructed retro arcade pixel art, not a high-resolution illustration converted into pixels.
Prioritize large, connected pixel clusters over small details. Build the character from simple, recognizable shapes.
<One line per material, e.g. "Scales are broad flat areas of teal, not individual scales." "The belly is one pale region with two or three band lines.">
One light source from the upper left. About three values per material: shadow, base, highlight.
Consistent one-pixel dark navy #10152D outline around the whole silhouette.

DETAIL BUDGET:
Only include details needed to recognize the character at 64 pixels. Prioritize:
1. Silhouette.
2. <signature feature>.
3. <second feature>.
4. Face: eyes and mouth, readable and expressive.
5. <color regions>.
Eliminate decorative micro-details, texture, seams, rivets, ornaments and reflective spots.

VISUAL STYLE:
Restrained, clean, readable, handcrafted pixel art. Flat colors, controlled contrast, simplified anatomy, deliberate pixel placement. Cute-menacing and full of attitude, not realistic or gory.

OUTPUT:
Exactly one complete character sprite. Flat solid <#FF00FF magenta | #00FF00 green> background, edge to edge. No scenery. No ground shadow. No text. No labels. No borders. No sprite sheets. No turnarounds. No presentation layouts.

Negative prompt:
<the negative prompt below, with the equipment line adapted to the character>
```

## Clip sheet template

Same CHARACTER, ART DIRECTION, DETAIL BUDGET and VISUAL STYLE text as the model sheet, word for word. Change the rest:

```text
Create ONE horizontal sprite strip: a <N>-frame <clip> animation of the character in the attached reference image, for a top-down retro arcade game.

CHARACTER:
Identical to the attached reference image: same design, proportions, colors, outline and pixel size. Do not redesign it.
<the same character sentence as the model sheet>
Side view facing right in every frame.

FRAMES:
1 <pose>, 2 <pose>, ... <N> <pose>.
Make the movement between frames big enough to see at 64 pixels.

LAYOUT:
Exactly <N> frames in one row, evenly spaced, each the same size, <feet on the same ground line | each centered on the same point>, clear empty space between frames, nothing touching the image edge.

PIXEL ART CONSTRUCTION:
- Design each frame on a logical 64 x 64 pixel grid; the character is the same size in every frame, matching the reference.
- Enlarge with nearest-neighbor scaling so every logical pixel is a uniform square block, the same size in every frame.
- (the rest of the construction lines from the model sheet)

ART DIRECTION / DETAIL BUDGET / VISUAL STYLE:
(word for word from the model sheet)

OUTPUT:
Exactly <N> frames of the one character. Flat solid <key color> background, edge to edge. No scenery. No ground shadow. No text, numbers or frame labels. No grid lines or borders. No extra characters.

Negative prompt:
<the negative prompt below, minus "sprite sheet" and "duplicated figures">
```

Other frame sizes scale the same way: people are a 32 x 32 grid (the figure about 22 pixels tall), cars a 64 x 32 grid, tokens 32 x 32. Vehicles use "side view facing right", "seen from behind, driving up the screen" or "seen from the front, driving down the screen", one view per image.

## The cliché list

Put this, adapted, in every prompt's negative section. Each line is a habit that marks a sprite as generated.

```text
multiple characters, duplicated figures, sprite sheet, character sheet, turnaround, collage, poster layout, text, captions, labels, numbers, watermark, scenery, background objects, ground shadow, cropped body,
generic movie-monster realism, gore, plastic or rubbery skin, overly symmetrical face, stiff mannequin pose, generic heroic pose, broken anatomy, floating limbs,
invented accessories, armor plating, chains, straps, buckles, ornaments, extra spikes or horns not in the design,
excessive detail, individually drawn scales, unnecessary texture, visual noise, tiny highlights, random seams, complicated patterns, over-rendering,
golden-hour tint, cinematic lighting, bloom, lens flare, glowing edges, rim lighting, glossy surfaces, random bright highlights on dark areas, oversaturated colors,
fake pixelation, inconsistent pixel sizes, fractional-looking pixels, antialiasing, airbrushed gradients, blurry edges, excessive dithering, scattered pixels, pixel noise,
flat personality, expressionless face, shapeless body, overly simplified design
```

And add this sentence after it, because a model told what not to do tends to overcorrect into blandness: "Removing these clichés does not mean making the character plain, stiff, expressionless or unremarkable."

Adapt the middle lines to the subject. For people, add the thread-tested ones: generic anime features, oversized eyes, doll-like skin, excessive hair strands, overcomplicated clothing folds. For a mecha, drop "armor plating" and say instead which plates it has and that it has no others.

## Field notes

**CHARACTER.** Name what a player recognizes at game size: the silhouette, one or two colors, one signature detail. Keep the sentence identical across clips.

**PIXEL ART CONSTRUCTION.** The logical grid plus an exact nearest-neighbor enlargement is what pushes the model away from "illustration with a pixel filter" toward chunky, even pixels. It won't hit the grid exactly; the cleanup script snaps it. Use the game's frame size as the logical grid so the model draws at roughly the detail level the game can show.

**ART DIRECTION.** One line per material saying how to simplify it (broad masses, not strands or scales) does more than any style adjective.

**DETAIL BUDGET.** The ranked list is what stops micro-detail. Five items is plenty. The face belongs on it for characters: at 64 pixels the eyes and mouth carry the personality.

**Palette.** Use the game's palette for that family (see the house rules) and give the same list to the cleanup spec. A color the list lacks (a cream belly against a palette with no cream) turns into speckle after cleanup, so add it to both.

**Background.** A flat chroma color the character doesn't contain: magenta `#FF00FF` by default, green `#00FF00` when the subject has pink, purple or magenta. Never black, white or navy: the outline and highlights would vanish with it. A transparent background also works with Codex's image tool, but a flat key color has proven more reliable.

## Pose lists for common clips

Starting points that read well at game size. Exaggerate: small motion vanishes at 64 pixels.

| Clip | Frames | Poses |
| --- | --- | --- |
| idle | 4 | 1 neutral stand, 2 breathe in (body rises 1-2 px, chest out), 3 neutral, 4 breathe out (body sinks slightly) |
| walk (kaiju) | 6 | 1 right foot far forward, weight down; 2 body low, legs crossing; 3 left leg lifting high, body high; 4 left foot far forward, weight down; 5 body low, legs crossing; 6 right leg lifting high, body high. Tail and arms swing opposite the legs. |
| run (people) | 6 | 1 contact, right foot forward, arms opposite; 2 down; 3 push off, airborne; 4 contact, left foot forward; 5 down; 6 push off. Panicked: arms flailing, mouth open. |
| chomp | 4 | 1 jaws wide open, leaning forward; 2 jaws snapping shut, head lunged forward; 3 chewing, cheeks full; 4 back to the neutral stand (the spec's `replace` copies idle frame 1 here) |
| death | 5 + 1 blank | 1 shocked, eyes wide; 2 staggering back; 3 collapsing; 4 flat on the ground; 5 a puff of smoke where it lay. Pad one blank frame in the spec. |
| shoot | 3 | 1 aim, 2 fire with a small muzzle flash, 3 recoil |
| vehicle side/up/down | 4 | the same vehicle with wheels turning, a small bounce on frames 2 and 4 |
| token / powerup | 4 | spinning or bobbing in place, centered |

## Judging a sheet

Look at every generated image before cleaning it. Reroll when any of these fail; the script can't fix them:

- **Identity.** Same character as the reference: shape, features, colors, proportions.
- **Frame count and separation.** Exactly N figures with gaps between them.
- **Motion.** Consecutive frames differ visibly. A walk whose legs barely move reads as a slide in the game. This is the most common failure.
- **Size.** Every frame draws the character at the same size.
- **Detail budget.** No invented accessories, texture or glow crept back in.
- **Completeness.** Nothing cropped; no text, labels or grid lines.
- **Readability.** Shrunk to game size, the silhouette still says what it is.

The script fixes these, so don't reroll for them: soft edges, uneven pixel size, colors near the palette, a missing or uneven outline, small specks, frames off-center.

## Rerolling

Change one thing per retry and keep everything else word for word. Name the failure in the new prompt ("the legs must clearly alternate: frame 1 right foot far forward, frame 4 left foot far forward"). After two failed rerolls on the same clip, simplify: fewer frames, a bigger pose difference, or a plainer design. When one frame of an otherwise good sheet is off, regenerate the sheet rather than mixing frames from different sheets; frames from different sheets rarely match in size and line weight.
