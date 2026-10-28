# Chomp Chomp Panic! sprite house rules

A top-down 2D pixel-art kaiju game in Unity, set in a night-time Tokyo and a snowy New York. The repo's `AGENTS.md` ("Art pipeline") is the authority; read it first in case anything below has gone stale.

## Contents
- [Look](#look)
- [Sizes and clips](#sizes-and-clips)
- [Palettes](#palettes)
- [Files and naming](#files-and-naming)
- [After building](#after-building)

## Look

- Chompy (the player's kaiju, `ArtSource/Kaiju/preview/kaiju_preview_8x.png`) is the quality bar and the style reference: chubby, cute-menacing, big readable features, flat shading, a crisp navy outline. Attach his preview when generating any new kaiju so the line weight and shading match.
- Navy outline `#10152D` on everything.
- The city is dark and desaturated; sprites need to read against it. Kaiju are bold and saturated; people are warm-colored and small; New York's snow is moonlit blue-grey, never white.
- Characters face right in side view. Vehicles have side, up (seen from behind) and down (seen from the front) views.

## Sizes and clips

Frame sizes are game pixels (64 px per Unity unit). Counts are what the game uses today; match them so the importer and animator work unchanged.

| Asset | Frame | Clips (frames) | Anchor | Notes |
| --- | --- | --- | --- | --- |
| Kaiju (playable, rivals, boss) | 64 x 64 | `idle` 4, `walk` 6, `chomp` 4, `death` 6 (5 drawn + 1 blank) | bottom, baseline 57 (Chompy) or 62 (the hand-drawn kaiju), height ~52 | Plus the evolved look: the same four clips as `<prefix>_evo_<clip>.png`, a bigger, spikier version of the same design. |
| People | 32 x 32 | `run` 6, `idle` 4 | bottom, baseline 26 | Stage reskins use `nyc_person_<kind>_<clip>.png`. |
| Police officer, soldiers | 32 x 32 | `run` 6, `idle` 2, `shoot` 3 | bottom, baseline 26 | |
| Bikes | 48 x 32 | `side`, `up`, `down`, 4 each | bottom | |
| Cars, police car, jeep | 64 x 32 | `side`, `up`, `down`, 4 each | bottom | |
| Tank | 128 x 64 | `side`, `up`, `down`, 4 each | bottom | |
| Jet | 176 x 176 | `fly` 4 | center | |
| Powerup tokens | 32 x 32 | 4 | center | Also the hotbar icons. |
| Ability icons | 32 x 32 | 1 | center | |
| Poop | 64 x 64 | 1 | bottom | One per kaiju, `<prefix>_poop.png`. |
| Relic | 64 x 64 | 4 | center | Hidden-kaiju unlock pickup. |
| Effects | varies (explosion 48 x 48 x 8) | | center | |

Check the group's existing `Assets/Art/<Group>/sprite_frames.json` before trusting this table.

## Palettes

Snap to an existing palette whenever the new sprite belongs to an existing family:

- **Chompy:** `Assets/Art/Kaiju/kaiju_palette.png` (use it with `palette_from`). 19 colors: navy outline, a teal-blue ramp, a purple mouth ramp, pale blues.
- **People:** the `HEX` list in `ArtSource/People/build_people.py` (23 warm skin, clothing and hair colors plus the outline).
- **Hand-drawn kaiju and props:** the colors in their existing strips; pass the strip to `palette_from`.

For a new kaiju, choose 12 to 20 colors: the navy outline, a 4-5 step ramp for the main body color, a 3-step ramp for the belly or second color, a mouth or accent ramp, and white plus a pale highlight. Show the list to the user with the model sheet, then use the same list in every prompt and in the spec.

## Files and naming

Nothing under `Assets/Art/` is edited by hand: a script in `ArtSource/` writes it. The sprite skill keeps that rule by committing everything needed to rebuild:

| What | Where |
| --- | --- |
| Generated source sheets | `ArtSource/<Group>/source_<prefix>_<clip>.png` |
| Approved model sheet | `ArtSource/<Group>/source_<prefix>_model.png` |
| Build spec | `ArtSource/<Group>/<prefix>.sprite.json` |
| Cleanup script | `ArtSource/sprite_clean.py` (a copy of the skill's script) |
| Preview | `ArtSource/<Group>/<prefix>_preview_8x.png` |
| Game strips | `Assets/Art/<Group>/<prefix>[_<variant>]_<clip>.png` |
| Frame sizes | `Assets/Art/<Group>/sprite_frames.json` (the spec's `frames_json`) |

- The importer assigns sprites by file name: `<prefix>[_<variant>]_<clip>.png`, with clips idle, run/walk/side/fly, up, down, shoot, chomp, death. Get the name right or the sprite won't show up.
- Don't commit prompt files (the repo's rule). Keep prompts in scratch space and quote them in the report instead.
- Images are stored with Git LFS; `.png` already matches. Commit each asset's Unity `.meta` file with it once Unity has made one.
- When the sprites replace a hand-drawn group, leave the old `build_<x>.py` in place until the user decides; say so in the report.

## After building

1. For a kaiju, re-run `python ArtSource/Variants/build_variants.py` (it hue-shifts every kaiju into its three alternate colors). If Chompy changed, also re-run `python ArtSource/Rivals/build_rivals.py`.
2. In Unity, run **Chomp Chomp Panic > Import Art** (through the Unity MCP if it's available, otherwise ask the user to). It slices the strips and assigns them to the GameManager, the Kaiju Roster and the Stage Roster.
3. Play it: walk, eat, get hit, die. Animation problems (a sliding walk, a jumping idle) only show in motion.
4. A brand-new kaiju or prey type also needs roster or `PreyType` data and maybe code. That's game work outside this skill; list what's missing in the report.
