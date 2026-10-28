---
name: sprite
description: >-
  Make game-ready pixel-art sprites for Chomp Chomp Panic!: generate the art with Codex CLI's image tool from a structured prompt and a reference image, then snap it onto the game's frame grid, palette and outline with a bundled cleanup script, and drop the strips into the Unity project. Use when the user types /sprite or $sprite, or asks to make, draw, generate, redo, or improve a sprite, sprite sheet, animation, kaiju, character, prey, vehicle, powerup, icon, or effect for the game, says the current sprites look bad or low quality, or wants a new kaiju's art, even if they never say "sprite." Not for the city atlas or stage-select cards (those come from the city scripts), the logo, the pixel font, sound, or game code; and not for recoloring an existing kaiju (build_variants.py does that).
---

# Sprites for Chomp Chomp Panic!

The game's hand-coded Python sprites look stiff. Chompy, the one sprite drawn by an image model and then cleaned up, looks far better. This skill makes every new sprite that way:

1. **Codex draws the art.** `scripts/codex_image.py` runs `codex exec` with Codex's built-in image tool, a structured prompt and a reference image, and saves the sheet. The prompt does the art direction: a logical pixel grid, a short palette, a ranked detail budget, and a list of AI clichés to leave out. That's what keeps the result from looking generated.
2. **A script makes it real pixel art.** `scripts/sprite_clean.py` removes the background, finds the frames, downscales them onto the game's grid, snaps colors to the palette, forces the navy outline, and writes the strips the importer expects.

Read [references/chomp-chomp-panic.md](references/chomp-chomp-panic.md) now for sizes, clips, palettes and file names. Read [references/prompting.md](references/prompting.md) before writing the first prompt. Read [references/spec.md](references/spec.md) when writing the build spec.

## Before you start

- Find the game repo: the current directory if it holds `Assets/Art` and `ArtSource`, else `C:\Users\JD\source\chomp-chomp-panic`. Read its `AGENTS.md` "Art pipeline" section; it wins over this skill if they disagree.
- Check the tools: `codex --version` and `codex login status`. Without Codex there's nothing to generate with; stop and tell the user how to install and log in.
- Call the scripts with `python`, falling back to `python3`. They need only the standard library.
- Each image is a real generation billed to the user's Codex plan and takes about a minute. Say how many you're about to make before a batch bigger than a few (a full kaiju is about 9: a model sheet, four clips, and four evolved clips).

## 1. Pin down the asset

Settle these before generating anything, from the user's request, the house rules, and the group's existing `sprite_frames.json`:

- **What it is and looks like:** one sentence a player would recognize, plus 2-4 signature features. If the user gave nothing but a name ("a crab kaiju"), propose a design in one or two lines and go on; the model sheet is where they'll react.
- **Group, prefix and clips:** e.g. group `Croc`, prefix `croc`, clips `idle`/`walk`/`chomp`/`death` plus `_evo_` versions.
- **Frame size, frame counts and anchor** from the house-rules table.
- **Palette:** an existing palette for an existing family, or a new 12-20 color list for a new character (house rules say how to build one).
- **Background key:** magenta `#FF00FF`, or green `#00FF00` if the design has pink or purple.

For a redo of existing art, look at the current preview first and say what the new version should fix. Then run `sprite_clean.py inspect` on the current strip and copy its feet row (each box's bottom edge minus 1) and figure height into the spec. The game places sprites by their frame, so a redo that stands even 3 px higher than the old one floats.

## 2. Model sheet (new characters only)

Fill in the prompting guide's model sheet template (one standalone sprite in a neutral pose) and generate it, attaching Chompy's preview as a style reference:

```bash
python <skill>/scripts/codex_image.py --prompt-file <scratch>/croc_model.txt --out <repo>/ArtSource/Croc/source_croc_model.png --ref <repo>/ArtSource/Kaiju/preview/kaiju_preview_8x.png
```

Write prompt files in your scratch directory, not the repo: the game doesn't commit prompts. Show the user the image and the palette and wait for their OK. This is the one stop in the workflow, because every later sheet copies this design; a fix now costs one image, a fix later costs all of them.

For an existing character, skip this: its `*_preview_8x.png` is the reference.

## 3. Generate one sheet per clip

Write one prompt per clip from the clip sheet template. Copy the CHARACTER, ART DIRECTION, DETAIL BUDGET and VISUAL STYLE text word for word from the model sheet prompt; only the frames, layout and output lines change. Attach the model sheet (or existing preview) to every one. The clips don't depend on each other, so run them in parallel in the background:

```bash
python <skill>/scripts/codex_image.py --prompt-file <scratch>/croc_walk.txt --out <repo>/ArtSource/Croc/source_croc_walk.png --ref <repo>/ArtSource/Croc/source_croc_model.png
```

The script prints the saved path and Codex's reply, and exits non-zero if no image came back. If Codex saved more than one image, the extras are kept as `.alt1.png` and so on; pick the best.

Look at every sheet (open the PNG) and judge it against the checklist in the prompting guide: identity, frame count, separation, visible motion, consistent size, detail budget kept, nothing cropped, no text. Reroll a failing sheet with one targeted change. Don't reroll for soft edges, off colors or a ragged outline; the cleanup fixes those.

## 4. Clean up

1. Run `python <skill>/scripts/sprite_clean.py inspect <sheet.png>` on each sheet. It reports the background it found and the figures in each row. If the count is wrong, fix it with `min_gap` in the spec, or reroll.
2. Write `ArtSource/<Group>/<prefix>.sprite.json` (format in [references/spec.md](references/spec.md)) with the frame size, anchor, palette, outline, every clip, `frames_json`, `preview` and `report`.
3. Copy `scripts/sprite_clean.py` to `ArtSource/sprite_clean.py` if it's missing or differs, so the game can rebuild its art without this skill. Then build from the repo's copy:

   ```bash
   python ArtSource/sprite_clean.py build ArtSource/Croc/croc.sprite.json
   ```

4. Look at the preview and read the report. Check that every clip draws the character at the same size, feet sit on the baseline, nothing is clipped, the palette held (no speckle from a missing color), and the features survived at game size (eyes, mouth, signature detail). Fix the spec and rebuild, or reroll the clip. Put the preview next to an existing sprite's preview when size relative to the rest of the cast matters.
5. End the chomp on the exact rest pose with `"replace": {"3": ["idle", 0]}` on the chomp clip; the prompting guide's pose list expects that.

## 5. Put it in the game

Follow "After building" in the house rules: re-run variants (and rivals for Chompy), run **Import Art**, and play it. Don't commit unless the user asks; when they do, include the source sheets, the spec, `ArtSource/sprite_clean.py`, the preview, the strips, `sprite_frames.json`, and `.meta` files, and never the prompts.

## Report

End with:
- The preview image, and each strip's path.
- How many images were generated and how many were rerolls, and why.
- The final prompt for each clip, quoted (they aren't saved anywhere else).
- Anything left: report warnings you accepted, clips that still look weak, the in-game check if you couldn't run Unity, and game data or code a new character still needs.
