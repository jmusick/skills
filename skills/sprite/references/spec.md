# sprite_clean.py spec format

`sprite_clean.py build <spec.json>` reads one JSON file per character or prop. Paths in it are relative to the spec file. Keep the spec next to the source images so the build can be re-run later.

## Example: a 64x64 kaiju with one source image per clip

```json
{
  "frame": [64, 64],
  "anchor": "bottom",
  "baseline": 62,
  "height": 52,
  "margin": 2,
  "palette": ["#10152D", "#203353", "#075275", "#066C96", "#0788B2", "#39B4D7", "#99E0EF", "#F1FCFF", "#643473", "#C37CD0"],
  "outline": "#10152D",
  "out_dir": "../../Assets/Art/Croc",
  "clips": [
    {"name": "idle",  "source": "source_croc_idle.png",  "frames": 4, "out": "croc_idle.png"},
    {"name": "walk",  "source": "source_croc_walk.png",  "frames": 6, "out": "croc_walk.png"},
    {"name": "chomp", "source": "source_croc_chomp.png", "frames": 4, "out": "croc_chomp.png"},
    {"name": "death", "source": "source_croc_death.png", "frames": 5, "pad_blank": 1, "out": "croc_death.png"}
  ],
  "frames_json": "../../Assets/Art/Croc/sprite_frames.json",
  "preview": "croc_preview_8x.png",
  "report": "croc_report.json"
}
```

## Fields

| Field | Default | Meaning |
| --- | --- | --- |
| `frame` | required | `[width, height]` of one frame in game pixels. |
| `clips` | required | One entry per output strip (see below). |
| `source` | none | Source image shared by every clip that doesn't name its own. Use it with `row` when one image holds several clips. |
| `anchor` | `"bottom"` | `"bottom"` puts each frame's lowest pixel on `baseline` (walkers, people, vehicles). `"center"` centers each frame (fliers, effects, icons, tokens). Frames are always centered horizontally. |
| `baseline` | `frame_h - 1 - margin` | Zero-based row the feet stand on, for `anchor: bottom`. |
| `height` | fills the frame | Height in game pixels of each source's reference frame (its first clip's frame `ref_frame`, default 0). Every frame in that source is scaled by the same factor, so poses keep their relative size. A clip can set its own `height`. |
| `margin` | `2` | Transparent border to keep clear. A frame too big to fit shrinks its whole source, with a warning. |
| `palette` | none | Hex colors to snap every pixel to. Strongly preferred: it keeps a new sprite in the game's palette. |
| `palette_from` | none | PNG path (or list) to take the palette from: every opaque color in it. Use an existing `*_palette.png` or a sibling sprite strip. |
| `colors` | `16` | With neither of the above, pick this many colors from the art by median cut. Fine for a first look; pin a `palette` before shipping. |
| `outline` | none | Hex color forced onto every pixel on the silhouette's edge, giving an exact one-pixel outline. Added to the palette if missing. |
| `background` | `"auto"` | `"auto"` reads it from the image border (transparent, or the most common border color as a chroma key). Or `"alpha"`, or a hex key like `"#FF00FF"`. |
| `tolerance` | `40` | How far (roughly, in RGB steps) a pixel can be from the key color and still count as background. Raise it if a halo of key color survives; lower it if parts of the art vanish. |
| `min_area` | `48` | Source-pixel area below which a blob is dropped as a speck. Thin ruled lines (cell borders) are always dropped. |
| `min_gap` | `6` | Source-pixel gap that separates two figures. Raise it if one figure splits in two (a detached spike or sweat drop); lower it if two frames merge. |
| `min_island` | `3` | Game-pixel blobs smaller than this are removed after downscaling. |
| `rows`, `cols` | from clips | Expected rows in a single shared source, and columns for the equal-cell fallback. |
| `out_dir` | spec folder | Where the strips go. |
| `frames_json` | none | `sprite_frames.json` to add each strip to as `"file": [w, h]`. Existing entries are kept. |
| `preview` | none | Enlarged preview of every clip on a dark background, one clip per row. |
| `preview_zoom` | 8 (4 above 64 px) | Preview scale. |
| `report` | none | Where to write the JSON report (it's always printed too). |

### Clip fields

| Field | Meaning |
| --- | --- |
| `name` | Clip name, used in the report. |
| `out` | Output file name, e.g. `croc_walk.png`. |
| `frames` | How many figures to find in the source row. |
| `source` | This clip's own source image. |
| `row` | Which row of the source holds this clip (0-based). Default 0. |
| `pad_blank` | Empty frames to append, e.g. the vanished last frame of a death. |
| `replace` | Frames to copy from another clip after building, as `{"<frame index>": ["<clip>", <frame index>]}`. `"replace": {"3": ["idle", 0]}` on `chomp` ends the bite exactly on the rest pose, as Chompy's does. |
| `height`, `ref_frame` | Override the size reference for this clip's source. |

## How frames are found

The script removes the background, drops specks and ruled lines, then splits the image into rows and each row into figures by looking for empty gaps. If it finds more figures than `frames` it merges the closest pairs; if it finds fewer it falls back to equal-width cells and warns. Run `sprite_clean.py inspect <source.png>` first to see what it detects: the background, each row's span, and each figure's box.

## Reading the report

- `warnings`: anything that fell back or got shrunk. Each one is worth a look at the preview.
- `clips.<name>.scale`: source-to-game factor. Clips of one character should land on similar scales; a big difference means a source drew the character at a different size, so check the preview for a clip that looks too big or small.
- `clips.<name>.bounds`: each frame's `[x0, y0, x1, y1]`. With `anchor: bottom`, `y1` should be `baseline + 1` in every frame.
- `colors_used`: how many palette entries the art actually used.
