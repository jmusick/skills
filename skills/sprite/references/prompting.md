# Prompting image models for sprites

Image models draw a polished single illustration and a sloppy sprite. Left to guess, they pack every surface with texture, rim light and ornament, round the pixels off, lose count of frames, and redraw the character a little differently each time. The prompt takes the guessing away; the cleanup script then fixes what the model still gets wrong (the exact grid, stray colors, the outline).

## Contents
- [The brief](#the-brief)
- [Filling the brief](#filling-the-brief)
- [Pose lists for common clips](#pose-lists-for-common-clips)
- [Judging a sheet](#judging-a-sheet)
- [Rerolling](#rerolling)

## The brief

`scripts/make_prompt.py` writes every prompt from one JSON brief, so the art direction, detail budget, style and cliché list stay word for word the same across the model sheet, every clip, and every reroll. Its docstring lists the fields. A kaiju brief looks like this:

```json
{
  "prefix": "croc",
  "name": "Croc",
  "character": "a stocky green crocodile kaiju with a long toothy snout, a ridged tail and tiny angry eyes, swaggering and hungry.",
  "palette": ["#10152D", "#1E5E3A", "#2F8A4E", "#7FC46A", "#F2E8C9", "#FFFFFF"],
  "key": "magenta",
  "materials": ["Scales are broad flat areas of green, not individual scales.", "The belly is one pale region with two or three band lines."],
  "detail_budget": ["Long toothy snout", "Ridged tail", "Face: eyes and mouth, readable and expressive", "Green body, cream belly"],
  "clips": {
    "walk": {"frames": ["right foot far forward, weight down", "body low, legs crossing", "..."], "anchor": "bottom"}
  }
}
```

Other frame sizes set `grid` and `figure_height`: people are a 32 x 32 grid with the figure about 22 pixels tall, cars a 64 x 32 grid, tokens 32 x 32. Vehicles set `view` to "side view facing right", "seen from behind, driving up the screen" or "seen from the front, driving down the screen", one view per image. People and vehicles also need their own `game` and `style` lines in place of the kaiju defaults, or every prompt will describe a kaiju game.

## Filling the brief

**character.** Name what a player recognizes at game size: the silhouette, one or two colors, one signature detail, and its attitude.

**materials.** One line per material saying how to simplify it (broad masses, not strands or scales) does more than any style adjective.

**grid.** Use the game's frame size as the logical grid, so the model draws at roughly the detail level the game can show. The grid plus an exact nearest-neighbor enlargement is what pushes the model toward chunky, even pixels; the cleanup script snaps what it misses.

**detail_budget.** The ranked list is what stops micro-detail; the script puts the silhouette first. Four items after it is plenty. The face belongs on it for characters: at 64 pixels the eyes and mouth carry the personality.

**palette.** Use the game's palette for that family (see the house rules), outline first, and give the same list to the cleanup spec. A color the list lacks (a cream belly against a palette with no cream) turns into speckle after cleanup, so add it to both.

**key.** A flat chroma color the character doesn't contain: magenta by default, green when the subject has pink, purple or magenta. Never black, white or navy: the outline and highlights would vanish with it. A flat key color has proven more reliable with Codex's image tool than a transparent background.

**negative_add / negative_drop.** The script appends the cliché list, followed by the sentence that leaving the clichés out doesn't mean making the character plain, because a model told what not to do tends to overcorrect into blandness. For people, add the thread-tested terms: generic anime features, oversized eyes, doll-like skin, excessive hair strands, overcomplicated clothing folds. For a mecha, drop "armor plating" and name its plates in `materials` instead, saying it has no others.

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

Change one thing per retry and keep everything else word for word: edit the brief and rerun the script for that clip. Name the failure in the clip's `fix` field ("The legs must clearly alternate: frame 1 right foot far forward, frame 4 left foot far forward."). After two failed rerolls on the same clip, simplify: fewer frames, a bigger pose difference, or a plainer design. When one frame of an otherwise good sheet is off, regenerate the sheet rather than mixing frames from different sheets; frames from different sheets rarely match in size and line weight.
