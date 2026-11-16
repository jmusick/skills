"""Write the Codex image prompts for one sprite from a small JSON brief.

Every prompt for a character shares its CHARACTER, ART DIRECTION, DETAIL BUDGET,
VISUAL STYLE and cliché list word for word; this script is what keeps them that
way across the model sheet, every clip, and every reroll.

Usage:
  python make_prompt.py <brief.json> all   --out-dir <scratch>   # model sheet + every clip
  python make_prompt.py <brief.json> model --out-dir <scratch>
  python make_prompt.py <brief.json> <clip> --out-dir <scratch>

Writes <prefix>_model.txt and <prefix>_<clip>.txt (UTF-8) and prints their paths.

Brief fields (see references/prompting.md for how to fill them):
  prefix          file prefix, e.g. "croc"                                required
  name            display name, e.g. "Croc"                               required
  character       one or two sentences: what it is, shape, colors,
                  2-4 signature features, attitude                        required
  palette         hex colors, outline first (8-20)                        required
  materials       one line per material saying how to simplify it         required
  detail_budget   ranked features after the silhouette (face included)    required
  key             "magenta" (default) or "green"
  grid            [w, h] logical grid, default [64, 64]
  figure_height   pixels of the grid the figure fills, default 52
  canvas          model-sheet canvas size, default 1024
  view            default "side view facing right"
  game            default "a top-down retro arcade game about a kaiju rampaging through a city at night"
  style           VISUAL STYLE line; default is the kaiju line
  negative_add    extra cliché terms for this subject (e.g. people's anime terms)
  negative_drop   cliché terms to remove (e.g. "armor plating" for a mecha)
  clips           {"walk": {"frames": ["pose 1", ...], "anchor": "bottom"|"center",
                            "fix": "optional line naming a failure to fix on a reroll"}}
"""
import argparse
import json
import sys
from pathlib import Path

KEYS = {"magenta": "#FF00FF magenta", "green": "#00FF00 green"}
OUTLINE_LINE = "Consistent one-pixel dark navy #10152D outline around the whole silhouette."
DEFAULT_STYLE = ("Restrained, clean, readable, handcrafted pixel art. Flat colors, controlled contrast, simplified "
                 "anatomy, deliberate pixel placement. Cute-menacing and full of attitude, not realistic or gory.")
DEFAULT_GAME = "a top-down retro arcade game about a kaiju rampaging through a city at night"
CLICHES = [
    "multiple characters", "duplicated figures", "sprite sheet", "character sheet", "turnaround", "collage",
    "poster layout", "text", "captions", "labels", "numbers", "watermark", "scenery", "background objects",
    "ground shadow", "cropped body",
    "generic movie-monster realism", "gore", "plastic or rubbery skin", "overly symmetrical face",
    "stiff mannequin pose", "generic heroic pose", "broken anatomy", "floating limbs",
    "invented accessories", "armor plating", "chains", "straps", "buckles", "ornaments",
    "extra spikes or horns not in the design",
    "excessive detail", "individually drawn scales", "unnecessary texture", "visual noise", "tiny highlights",
    "random seams", "complicated patterns", "over-rendering",
    "golden-hour tint", "cinematic lighting", "bloom", "lens flare", "glowing edges", "rim lighting",
    "glossy surfaces", "random bright highlights on dark areas", "oversaturated colors",
    "fake pixelation", "inconsistent pixel sizes", "fractional-looking pixels", "antialiasing",
    "airbrushed gradients", "blurry edges", "excessive dithering", "scattered pixels", "pixel noise",
    "flat personality", "expressionless face", "shapeless body", "overly simplified design",
]
NOT_PLAIN = "Removing these clichés does not mean making the character plain, stiff, expressionless or unremarkable."
REQUIRED = ("prefix", "name", "character", "palette", "materials", "detail_budget")


def negative(brief, drop=()):
    removed = set(brief.get("negative_drop", [])) | set(drop)
    terms = [t for t in CLICHES if t not in removed] + list(brief.get("negative_add", []))
    return "Negative prompt:\n" + ", ".join(terms) + "\n" + NOT_PLAIN


def shared(brief):
    """The blocks that must be identical in every prompt for this character."""
    budget = ["1. Silhouette."] + [f"{i}. {item.rstrip('.')}." for i, item in enumerate(brief["detail_budget"], 2)]
    w, h = brief.get("grid", [64, 64])
    return {
        "art": "\n".join([
            "ART DIRECTION:",
            "Authentic, deliberately constructed retro arcade pixel art, not a high-resolution illustration converted into pixels.",
            "Prioritize large, connected pixel clusters over small details. Build the character from simple, recognizable shapes.",
            *brief["materials"],
            "One light source from the upper left. About three values per material: shadow, base, highlight.",
            OUTLINE_LINE,
        ]),
        "budget": "\n".join([
            "DETAIL BUDGET:",
            f"Only include details needed to recognize the character at {max(w, h)} pixels. Prioritize:",
            *budget,
            "Eliminate decorative micro-details, texture, seams, rivets, ornaments and reflective spots.",
        ]),
        "style": "VISUAL STYLE:\n" + brief.get("style", DEFAULT_STYLE),
        "colors": "\n".join([
            "- Consistent pixel size throughout. No antialiasing or fractional-looking pixels. Crisp, hard pixel boundaries.",
            f"- Maximum {len(brief['palette'])} solid colors, only these: {', '.join(brief['palette'])}.",
            "- No gradients or dithering.",
        ]),
    }


def model_prompt(brief):
    s = shared(brief)
    w, h = brief.get("grid", [64, 64])
    canvas = brief.get("canvas", 1024)
    scale = canvas // max(w, h)
    view = brief.get("view", "side view facing right")
    return "\n\n".join([
        f"Create ONE standalone 2D pixel-art character sprite for {brief.get('game', DEFAULT_GAME)}.",
        "CHARACTER:\n" + f"{brief['name']}, {brief['character']}\n"
        f"Full body, {view}, neutral standing pose with personality. Centered composition. Strong, recognizable silhouette.",
        "PIXEL ART CONSTRUCTION:\n"
        f"- Final canvas: {scale * w} x {scale * h} pixels.\n"
        f"- Design using a logical {w} x {h} pixel grid; the character fills about {brief.get('figure_height', 52)} pixels of its height.\n"
        f"- Enlarge exactly {scale}x using nearest-neighbor scaling, so every logical pixel is a uniform {scale} x {scale} block.\n"
        + s["colors"],
        s["art"], s["budget"], s["style"],
        "OUTPUT:\nExactly one complete character sprite. Flat solid " + KEYS[brief.get("key", "magenta")]
        + " background, edge to edge. No scenery. No ground shadow. No text. No labels. No borders. No sprite sheets. "
          "No turnarounds. No presentation layouts.",
        negative(brief),
    ]) + "\n"


def clip_prompt(brief, clip):
    spec = brief.get("clips", {}).get(clip)
    if not spec or not spec.get("frames"):
        sys.exit(f'No clip "{clip}" with frames in the brief. Clips: {", ".join(brief.get("clips", {})) or "none"}')
    s = shared(brief)
    frames = spec["frames"]
    n = len(frames)
    w, h = brief.get("grid", [64, 64])
    view = brief.get("view", "side view facing right")
    place = "feet on the same ground line" if spec.get("anchor", "bottom") == "bottom" else "each centered on the same point"
    frame_lines = "; ".join(f"{i} {pose.rstrip('.')}" for i, pose in enumerate(frames, 1)) + "."
    frames_block = "FRAMES:\n" + frame_lines + f"\nMake the movement between frames big enough to see at {max(w, h)} pixels."
    if spec.get("fix"):
        frames_block += "\n" + spec["fix"]
    return "\n\n".join([
        f"Create ONE horizontal sprite strip: a {n}-frame {clip} animation of the character in the attached "
        f"reference image, for {brief.get('game', DEFAULT_GAME)}.",
        "CHARACTER:\nIdentical to the attached reference image: same design, proportions, colors, outline and pixel "
        f"size. Do not redesign it.\n{brief['name']}, {brief['character']}\n{view[0].upper() + view[1:]} in every frame.",
        frames_block,
        f"LAYOUT:\nExactly {n} frames in one row, evenly spaced, each the same size, {place}, clear empty space "
        "between frames, nothing touching the image edge.",
        "PIXEL ART CONSTRUCTION:\n"
        f"- Design each frame on a logical {w} x {h} pixel grid; the character is the same size in every frame, matching the reference.\n"
        "- Enlarge with nearest-neighbor scaling so every logical pixel is a uniform square block, the same size in every frame.\n"
        + s["colors"],
        s["art"], s["budget"], s["style"],
        f"OUTPUT:\nExactly {n} frames of the one character. Flat solid " + KEYS[brief.get("key", "magenta")]
        + " background, edge to edge. No scenery. No ground shadow. No text, numbers or frame labels. "
          "No grid lines or borders. No extra characters.",
        negative(brief, drop=("sprite sheet", "duplicated figures")),
    ]) + "\n"


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("brief")
    p.add_argument("which", help='"all", "model", or a clip name')
    p.add_argument("--out-dir", required=True)
    args = p.parse_args()
    try:
        brief = json.loads(Path(args.brief).read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        sys.exit(f"Can't read {args.brief}: {e}")
    missing = [k for k in REQUIRED if not brief.get(k)]
    if missing:
        sys.exit(f"Brief is missing: {', '.join(missing)}")
    if "model" in brief.get("clips", {}):
        sys.exit('A clip can\'t be named "model"; that name is the model sheet\'s file.')
    if brief.get("key", "magenta") not in KEYS:
        sys.exit('key must be "magenta" or "green"')

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    jobs = []
    if args.which in ("all", "model"):
        jobs.append(("model", model_prompt(brief)))
    if args.which == "all":
        jobs += [(c, clip_prompt(brief, c)) for c in brief.get("clips", {})]
    elif args.which != "model":
        jobs.append((args.which, clip_prompt(brief, args.which)))
    for name, text in jobs:
        path = out / f"{brief['prefix']}_{name}.txt"
        path.write_text(text, encoding="utf-8")
        print(path)


if __name__ == "__main__":
    main()
