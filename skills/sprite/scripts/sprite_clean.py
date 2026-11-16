#!/usr/bin/env python3
"""Turn a generated sprite sheet into game-ready pixel-art strips.

Image models draw "pixel art" at high resolution with a fake, uneven pixel
grid, soft edges and dozens of near-duplicate colors. This script snaps that
art onto a real grid: it removes the background, finds each frame, downscales
every frame by the same factor (majority vote per target pixel), maps colors
onto a fixed palette, forces a one-pixel outline, aligns frames on a shared
anchor, and writes one PNG strip per clip plus an enlarged preview and a JSON
report.

Standard library only (PNG reading and writing included), so it runs anywhere
Python 3.8+ does.

Usage:
  python sprite_clean.py inspect <source.png> [--rows N]
  python sprite_clean.py build <spec.json>

The spec format is documented in the sprite skill's references/spec.md.
"""

from __future__ import annotations

import argparse
import json
import struct
import sys
import zlib
from collections import Counter, deque
from pathlib import Path

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


# ---------------------------------------------------------------- PNG I/O ---

def _paeth(a, b, c):
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    return b if pb <= pc else c


def read_png(path):
    """Return (width, height, rgba bytearray) for an 8- or 16-bit PNG."""
    data = Path(path).read_bytes()
    if data[:8] != PNG_SIGNATURE:
        raise SystemExit(f"{path}: not a PNG file")
    pos, idat, palette, trns = 8, [], None, None
    width = height = depth = ctype = interlace = None
    while pos < len(data):
        length, kind = struct.unpack(">I4s", data[pos:pos + 8])
        body = data[pos + 8:pos + 8 + length]
        pos += 12 + length
        if kind == b"IHDR":
            width, height, depth, ctype, _, _, interlace = struct.unpack(">IIBBBBB", body)
        elif kind == b"PLTE":
            palette = body
        elif kind == b"tRNS":
            trns = body
        elif kind == b"IDAT":
            idat.append(body)
        elif kind == b"IEND":
            break
    if interlace:
        raise SystemExit(f"{path}: interlaced PNGs aren't supported; re-save it without interlacing")
    channels = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}.get(ctype)
    if channels is None or depth not in (8, 16) and not (ctype == 3 and depth == 8):
        raise SystemExit(f"{path}: unsupported PNG (color type {ctype}, bit depth {depth})")
    raw = zlib.decompress(b"".join(idat))
    sample = depth // 8
    bpp = channels * sample
    stride = width * bpp
    out = bytearray(height * stride)
    prev = bytearray(stride)
    src = 0
    for y in range(height):
        kind = raw[src]
        line = bytearray(raw[src + 1:src + 1 + stride])
        src += 1 + stride
        if kind == 1:
            for i in range(bpp, stride):
                line[i] = (line[i] + line[i - bpp]) & 255
        elif kind == 2:
            for i in range(stride):
                line[i] = (line[i] + prev[i]) & 255
        elif kind == 3:
            for i in range(stride):
                left = line[i - bpp] if i >= bpp else 0
                line[i] = (line[i] + ((left + prev[i]) >> 1)) & 255
        elif kind == 4:
            for i in range(stride):
                left = line[i - bpp] if i >= bpp else 0
                upleft = prev[i - bpp] if i >= bpp else 0
                line[i] = (line[i] + _paeth(left, prev[i], upleft)) & 255
        out[y * stride:(y + 1) * stride] = line
        prev = line
    if sample == 2:
        out = out[0::2]  # keep the high byte of each 16-bit sample
    rgba = bytearray(width * height * 4)
    n = width * height
    if ctype == 6:
        rgba[:] = out
    elif ctype == 2:
        rgba[0::4], rgba[1::4], rgba[2::4] = out[0::3], out[1::3], out[2::3]
        rgba[3::4] = b"\xff" * n
        if trns and len(trns) == 6:
            key = (trns[1], trns[3], trns[5])
            for i in range(n):
                if (rgba[4 * i], rgba[4 * i + 1], rgba[4 * i + 2]) == key:
                    rgba[4 * i + 3] = 0
    elif ctype in (0, 4):
        gray = out[0::channels]
        rgba[0::4] = rgba[1::4] = rgba[2::4] = gray
        rgba[3::4] = out[1::2] if ctype == 4 else b"\xff" * n
    else:
        alpha = trns or b""
        for i, idx in enumerate(out):
            rgba[4 * i:4 * i + 3] = palette[3 * idx:3 * idx + 3]
            rgba[4 * i + 3] = alpha[idx] if idx < len(alpha) else 255
    return width, height, rgba


def write_png(path, width, height, rgba):
    def chunk(kind, body):
        return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", zlib.crc32(kind + body) & 0xFFFFFFFF)

    stride = width * 4
    raw = b"".join(b"\x00" + bytes(rgba[y * stride:(y + 1) * stride]) for y in range(height))
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_bytes(
        PNG_SIGNATURE
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw, 9))
        + chunk(b"IEND", b"")
    )


# ------------------------------------------------------------- color utils ---

def parse_hex(value):
    value = value.strip().lstrip("#")
    if len(value) != 6:
        raise SystemExit(f"bad color {value!r}; use #RRGGBB")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def to_hex(rgb):
    return "#%02X%02X%02X" % tuple(rgb)


def color_distance(a, b):
    """Squared 'redmean' distance: cheap and closer to perception than plain RGB."""
    rmean = (a[0] + b[0]) >> 1
    dr, dg, db = a[0] - b[0], a[1] - b[1], a[2] - b[2]
    return (((512 + rmean) * dr * dr) >> 8) + 4 * dg * dg + (((767 - rmean) * db * db) >> 8)


class Palette:
    def __init__(self, colors):
        self.colors = [tuple(c) for c in colors]
        self.cache = {}

    def nearest(self, rgb):
        key = (rgb[0] >> 2, rgb[1] >> 2, rgb[2] >> 2)
        hit = self.cache.get(key)
        if hit is None:
            hit = min(range(len(self.colors)), key=lambda i: color_distance(rgb, self.colors[i]))
            self.cache[key] = hit
        return hit


def median_cut(pixels, count):
    """Reduce a list of RGB tuples to at most `count` representative colors."""
    boxes = [list(pixels)]
    while len(boxes) < count:
        boxes.sort(key=lambda b: max(max(p[c] for p in b) - min(p[c] for p in b) for c in range(3)) if len(b) > 1 else -1)
        box = boxes.pop()
        if len(box) < 2:
            boxes.append(box)
            break
        ranges = [max(p[c] for p in box) - min(p[c] for p in box) for c in range(3)]
        channel = ranges.index(max(ranges))
        box.sort(key=lambda p: p[channel])
        mid = len(box) // 2
        boxes.extend([box[:mid], box[mid:]])
    return [tuple(sum(p[c] for p in b) // len(b) for c in range(3)) for b in boxes if b]


def palette_from_pngs(paths):
    colors = Counter()
    for path in paths:
        w, h, px = read_png(path)
        for i in range(w * h):
            if px[4 * i + 3] >= 128:
                colors[(px[4 * i], px[4 * i + 1], px[4 * i + 2])] += 1
    if not colors:
        raise SystemExit("palette_from: those images have no opaque pixels")
    return [c for c, _ in colors.most_common()]


# --------------------------------------------------------- source analysis ---

def detect_background(w, h, px):
    """Return ('alpha', None) when the image is transparent, else ('key', rgb)."""
    border = []
    for x in range(w):
        border += [x, (h - 1) * w + x]
    for y in range(h):
        border += [y * w, y * w + w - 1]
    if sum(1 for i in border if px[4 * i + 3] < 128) > len(border) // 2:
        return "alpha", None
    counts = Counter((px[4 * i] >> 3, px[4 * i + 1] >> 3, px[4 * i + 2] >> 3) for i in border)
    bucket = counts.most_common(1)[0][0]
    members = [(px[4 * i], px[4 * i + 1], px[4 * i + 2]) for i in border
               if (px[4 * i] >> 3, px[4 * i + 1] >> 3, px[4 * i + 2] >> 3) == bucket]
    return "key", tuple(sorted(m[c] for m in members)[len(members) // 2] for c in range(3))


def opaque_mask(w, h, px, background, tolerance):
    mode, key = background
    mask = bytearray(w * h)
    if mode == "alpha":
        for i in range(w * h):
            mask[i] = px[4 * i + 3] >= 128
    else:
        limit = tolerance * tolerance * 9  # redmean distance runs roughly 9x plain RGB
        for i in range(w * h):
            if px[4 * i + 3] >= 128 and color_distance((px[4 * i], px[4 * i + 1], px[4 * i + 2]), key) > limit:
                mask[i] = 1
    return mask


def clean_mask(w, h, mask, min_area):
    """Drop specks, stray marks and thin ruled lines (cell borders) from the mask."""
    seen = bytearray(w * h)
    for start in range(w * h):
        if not mask[start] or seen[start]:
            continue
        seen[start] = 1
        queue, members = deque([start]), [start]
        x0 = x1 = start % w
        y0 = y1 = start // w
        while queue:
            i = queue.popleft()
            x, y = i % w, i // w
            x0, x1, y0, y1 = min(x0, x), max(x1, x), min(y0, y), max(y1, y)
            for j, ok in ((i - 1, x > 0), (i + 1, x < w - 1), (i - w, y > 0), (i + w, y < h - 1)):
                if ok and mask[j] and not seen[j]:
                    seen[j] = 1
                    queue.append(j)
                    members.append(j)
        bw, bh = x1 - x0 + 1, y1 - y0 + 1
        is_line = min(bw, bh) <= 4 and max(bw, bh) >= 40
        if len(members) < min_area or is_line:
            for i in members:
                mask[i] = 0
    return mask


def runs(profile, min_gap):
    """Spans of non-zero entries, merging spans separated by fewer than min_gap zeros."""
    spans, start, end, gap = [], None, 0, 0
    for i, v in enumerate(profile):
        if v:
            if start is None:
                start = i
            elif gap >= min_gap:
                spans.append((start, end))
                start = i
            end, gap = i + 1, 0
        elif start is not None:
            gap += 1
    if start is not None:
        spans.append((start, end))
    return spans


def fit_count(spans, count):
    """Merge the closest neighbours until there are exactly `count` spans."""
    spans = list(spans)
    while len(spans) > count:
        gaps = [spans[i + 1][0] - spans[i][1] for i in range(len(spans) - 1)]
        k = gaps.index(min(gaps))
        spans[k:k + 2] = [(spans[k][0], spans[k + 1][1])]
    return spans


def find_rows(w, h, mask, rows, min_gap):
    profile = [any(mask[y * w:(y + 1) * w]) for y in range(h)]
    spans = runs(profile, min_gap)
    if len(spans) >= rows:
        return fit_count(spans, rows), None
    step = h / rows
    return [(round(r * step), round((r + 1) * step)) for r in range(rows)], \
        f"found {len(spans)} row(s) of art, expected {rows}; split the sheet into equal rows instead"


def find_frames(w, mask, band, frames, min_gap, cols):
    y0, y1 = band
    profile = [0] * w
    for y in range(y0, y1):
        row = mask[y * w:(y + 1) * w]
        for x in range(w):
            if row[x]:
                profile[x] = 1
    spans = runs(profile, min_gap)
    if len(spans) >= frames:
        return fit_count(spans, frames), None
    step = w / (cols or frames)
    return [(round(c * step), round((c + 1) * step)) for c in range(frames)], \
        f"found {len(spans)} figure(s) in rows {y0}-{y1}, expected {frames}; used equal-width cells instead"


def content_box(w, mask, x0, x1, y0, y1):
    bx0, by0, bx1, by1 = x1, y1, x0, y0
    for y in range(y0, y1):
        base = y * w
        for x in range(x0, x1):
            if mask[base + x]:
                bx0, bx1 = min(bx0, x), max(bx1, x + 1)
                by0, by1 = min(by0, y), max(by1, y + 1)
    return (bx0, by0, bx1, by1) if bx1 > bx0 else None


# ------------------------------------------------------------ frame build ---

def sample_frame(w, px, mask, box, scale, palette, samples=4):
    """Downscale one frame by majority vote; returns (tw, th, list of palette index or None)."""
    x0, y0, x1, y1 = box
    tw = max(1, round((x1 - x0) * scale))
    th = max(1, round((y1 - y0) * scale))
    sx, sy = (x1 - x0) / tw, (y1 - y0) / th
    cells = []
    for ty in range(th):
        for tx in range(tw):
            votes, total = Counter(), 0
            for j in range(samples):
                y = min(y1 - 1, int(y0 + (ty + (j + 0.5) / samples) * sy))
                for k in range(samples):
                    x = min(x1 - 1, int(x0 + (tx + (k + 0.5) / samples) * sx))
                    total += 1
                    i = y * w + x
                    if mask[i]:
                        votes[palette.nearest((px[4 * i], px[4 * i + 1], px[4 * i + 2]))] += 1
            opaque = sum(votes.values())
            cells.append(votes.most_common(1)[0][0] if opaque * 2 > total else None)
    return tw, th, cells


def drop_islands(tw, th, cells, min_island):
    if min_island <= 1:
        return cells
    seen = [False] * len(cells)
    for start, value in enumerate(cells):
        if value is None or seen[start]:
            continue
        seen[start] = True
        queue, members = deque([start]), [start]
        while queue:
            i = queue.popleft()
            x, y = i % tw, i // tw
            for j, ok in ((i - 1, x > 0), (i + 1, x < tw - 1), (i - tw, y > 0), (i + tw, y < th - 1)):
                if ok and cells[j] is not None and not seen[j]:
                    seen[j] = True
                    queue.append(j)
                    members.append(j)
        if len(members) < min_island:
            for i in members:
                cells[i] = None
    return cells


def apply_outline(tw, th, cells, outline_index):
    out = list(cells)
    for i, value in enumerate(cells):
        if value is None:
            continue
        x, y = i % tw, i // tw
        edge = (x == 0 or cells[i - 1] is None or x == tw - 1 or cells[i + 1] is None
                or y == 0 or cells[i - tw] is None or y == th - 1 or cells[i + tw] is None)
        if edge:
            out[i] = outline_index
    return out


def place(frame_w, frame_h, tw, th, cells, colors, anchor, baseline):
    """Return an RGBA bytearray for one frame with the sprite placed on the anchor."""
    left = (frame_w - tw) // 2
    if anchor == "bottom":
        top = baseline - th + 1
    else:
        top = (frame_h - th) // 2
    left = max(0, min(left, frame_w - tw))
    top = max(0, min(top, frame_h - th))
    rgba = bytearray(frame_w * frame_h * 4)
    for i, value in enumerate(cells):
        if value is None:
            continue
        x, y = left + i % tw, top + i // tw
        o = 4 * (y * frame_w + x)
        rgba[o:o + 4] = bytes(colors[value]) + b"\xff"
    return rgba


def frame_bounds(frame_w, frame_h, rgba):
    xs, ys = [], []
    for y in range(frame_h):
        for x in range(frame_w):
            if rgba[4 * (y * frame_w + x) + 3]:
                xs.append(x)
                ys.append(y)
    return [min(xs), min(ys), max(xs) + 1, max(ys) + 1] if xs else None


def strip(frames, frame_w, frame_h):
    out = bytearray(len(frames) * frame_w * frame_h * 4)
    sw = len(frames) * frame_w
    for n, fr in enumerate(frames):
        for y in range(frame_h):
            dst = 4 * (y * sw + n * frame_w)
            out[dst:dst + 4 * frame_w] = fr[4 * y * frame_w:4 * (y + 1) * frame_w]
    return sw, frame_h, out


def preview(rows, frame_w, frame_h, zoom, background=(18, 20, 28)):
    cols = max(len(r) for r in rows)
    pw, ph = cols * frame_w * zoom, len(rows) * frame_h * zoom
    bg = bytes(background) + b"\xff"
    out = bytearray(bg * (pw * ph))
    for r, frames in enumerate(rows):
        for c, fr in enumerate(frames):
            for y in range(frame_h):
                line = bytearray()
                for x in range(frame_w):
                    o = 4 * (y * frame_w + x)
                    line += (bytes(fr[o:o + 4]) if fr[o + 3] else bg) * zoom
                for zy in range(zoom):
                    dst = 4 * (((r * frame_h + y) * zoom + zy) * pw + c * frame_w * zoom)
                    out[dst:dst + len(line)] = line
    return pw, ph, out


# ---------------------------------------------------------------- commands ---

def load_source(path, spec, cache):
    if path in cache:
        return cache[path]
    w, h, px = read_png(path)
    bg = spec.get("background", "auto")
    background = detect_background(w, h, px) if bg == "auto" else (("alpha", None) if bg == "alpha" else ("key", parse_hex(bg)))
    mask = opaque_mask(w, h, px, background, spec.get("tolerance", 40))
    mask = clean_mask(w, h, mask, spec.get("min_area", 48))
    cache[path] = (w, h, px, mask, background)
    return cache[path]


def cmd_inspect(args):
    w, h, px = read_png(args.source)
    background = detect_background(w, h, px)
    mask = clean_mask(w, h, opaque_mask(w, h, px, background, args.tolerance), args.min_area)
    profile = [any(mask[y * w:(y + 1) * w]) for y in range(h)]
    bands = runs(profile, args.min_gap)
    if args.rows:
        bands, _ = find_rows(w, h, mask, args.rows, args.min_gap)
    report = {
        "size": [w, h],
        "background": "transparent" if background[0] == "alpha" else to_hex(background[1]),
        "rows": [],
    }
    for band in bands:
        col = [0] * w
        for y in range(*band):
            for x in range(w):
                if mask[y * w + x]:
                    col[x] = 1
        figures = runs(col, args.min_gap)
        boxes = [content_box(w, mask, a, b, band[0], band[1]) for a, b in figures]
        report["rows"].append({
            "y": list(band),
            "figures": len(figures),
            "boxes": [list(b) for b in boxes if b],
        })
    print(json.dumps(report, indent=2))


def cmd_build(args):
    spec_path = Path(args.spec).resolve()
    base = spec_path.parent
    spec = json.loads(spec_path.read_text(encoding="utf-8"))

    def resolve(p):
        return (base / p).resolve()

    frame_w, frame_h = spec["frame"]
    margin = spec.get("margin", 2)
    anchor = spec.get("anchor", "bottom")
    baseline = spec.get("baseline", frame_h - 1 - margin)
    target_h = spec.get("height", (baseline + 1 - margin) if anchor == "bottom" else frame_h - 2 * margin)
    out_dir = resolve(spec.get("out_dir", "."))
    warnings = []
    cache = {}

    clips = spec["clips"]
    sources = []
    for clip in clips:
        src = resolve(clip.get("source", spec.get("source", "")))
        if src not in sources:
            sources.append(src)

    # Locate every frame in every source first, so the scale can be shared.
    located = []  # (clip, src, [boxes])
    for src in sources:
        w, h, px, mask, background = load_source(src, spec, cache)
        mine = [c for c in clips if resolve(c.get("source", spec.get("source", ""))) == src]
        rows = max(c.get("row", 0) for c in mine) + 1
        bands, warn = find_rows(w, h, mask, spec.get("rows", rows) if len(sources) == 1 else rows, spec.get("min_gap", 6))
        if warn:
            warnings.append(f"{src.name}: {warn}")
        for clip in mine:
            band = bands[clip.get("row", 0)]
            cells, warn = find_frames(w, mask, band, clip["frames"], spec.get("min_gap", 6), spec.get("cols"))
            if warn:
                warnings.append(f"{src.name} / {clip['name']}: {warn}")
            boxes = [content_box(w, mask, a, b, band[0], band[1]) for a, b in cells]
            located.append((clip, src, boxes))

    # One scale per source: its reference frame (first frame of its first clip,
    # or the clip's ref_frame) maps to target_h, shrunk if any frame overflows.
    scales = {}
    for src in sources:
        mine = [(c, b) for c, s, b in located if s == src]
        clip, boxes = mine[0]
        ref = boxes[clip.get("ref_frame", 0)]
        if ref is None:
            raise SystemExit(f"{src.name}: the reference frame of clip {clip['name']!r} is empty")
        scale = clip.get("height", target_h) / (ref[3] - ref[1])
        for c, bxs in mine:
            for b in bxs:
                if b is None:
                    continue
                fit = min((frame_w - 2 * margin) / (b[2] - b[0]), (frame_h - 2 * margin) / (b[3] - b[1]))
                if fit < scale:
                    warnings.append(f"{src.name} / {c['name']}: a frame was too big for the cell, so the whole source was scaled down to fit")
                    scale = fit
        scales[src] = scale

    # Palette.
    if "palette" in spec:
        colors = [parse_hex(c) for c in spec["palette"]]
    elif "palette_from" in spec:
        paths = spec["palette_from"] if isinstance(spec["palette_from"], list) else [spec["palette_from"]]
        colors = palette_from_pngs([resolve(p) for p in paths])
    else:
        pool = []
        for clip, src, boxes in located:
            w, h, px, mask, _ = cache[src]
            for b in boxes:
                if b is None:
                    continue
                for y in range(b[1], b[3], 3):
                    for x in range(b[0], b[2], 3):
                        i = y * w + x
                        if mask[i]:
                            pool.append((px[4 * i], px[4 * i + 1], px[4 * i + 2]))
        colors = median_cut(pool, spec.get("colors", 16))
    outline = parse_hex(spec["outline"]) if spec.get("outline") else None
    if outline and outline not in colors:
        colors.append(outline)
    palette = Palette(colors)
    outline_index = colors.index(outline) if outline else None

    # Build frames.
    report = {"frame": [frame_w, frame_h], "anchor": anchor, "palette": [to_hex(c) for c in colors],
              "clips": {}, "warnings": warnings}
    preview_rows = []
    used = set()
    built = {}
    for clip, src, boxes in located:
        w, h, px, mask, _ = cache[src]
        frames = []
        for b in boxes:
            if b is None:
                frames.append(bytearray(frame_w * frame_h * 4))
                continue
            tw, th, cells = sample_frame(w, px, mask, b, scales[src], palette)
            cells = drop_islands(tw, th, cells, spec.get("min_island", 3))
            if outline_index is not None:
                cells = apply_outline(tw, th, cells, outline_index)
            used.update(v for v in cells if v is not None)
            frames.append(place(frame_w, frame_h, tw, th, cells, colors, anchor, baseline))
        for _ in range(clip.get("pad_blank", 0)):
            frames.append(bytearray(frame_w * frame_h * 4))
        built[clip["name"]] = frames
    for clip, _, _ in located:
        frames = built[clip["name"]]
        for index, (other, other_index) in clip.get("replace", {}).items():
            if other not in built:
                raise SystemExit(f"clip {clip['name']!r}: replace names unknown clip {other!r}")
            frames[int(index)] = bytearray(built[other][other_index])
    for clip, src, _ in located:
        frames = built[clip["name"]]
        sw, sh, data = strip(frames, frame_w, frame_h)
        out = out_dir / clip["out"]
        write_png(out, sw, sh, data)
        preview_rows.append(frames)
        bounds = [frame_bounds(frame_w, frame_h, f) for f in frames]
        report["clips"][clip["name"]] = {
            "file": str(out),
            "source": src.name,
            "frames": len(frames),
            "strip": [sw, sh],
            "scale": round(scales[src], 4),
            "bounds": bounds,
        }
        for n, bnd in enumerate(bounds):
            if bnd and (bnd[0] < margin or bnd[1] < margin or bnd[2] > frame_w - margin or bnd[3] > frame_h - margin):
                warnings.append(f"{clip['name']} frame {n}: art reaches inside the {margin}px margin")

    report["colors_used"] = len(used)
    zoom = spec.get("preview_zoom", 8 if max(frame_w, frame_h) <= 64 else 4)
    if spec.get("preview"):
        pw, ph, data = preview(preview_rows, frame_w, frame_h, zoom)
        write_png(resolve(spec["preview"]), pw, ph, data)
        report["preview"] = str(resolve(spec["preview"]))
    if spec.get("frames_json"):
        fj = resolve(spec["frames_json"])
        existing = json.loads(fj.read_text(encoding="utf-8")) if fj.exists() else {}
        for clip in clips:
            existing[clip["out"]] = [frame_w, frame_h]
        fj.write_text(json.dumps(existing, indent=2) + "\n", encoding="utf-8")
        report["frames_json"] = str(fj)
    if spec.get("report"):
        resolve(spec["report"]).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    if warnings:
        print(f"\n{len(warnings)} warning(s); check the preview before importing.", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("inspect", help="report the background and the rows and figures the script can see")
    p.add_argument("source")
    p.add_argument("--rows", type=int, help="expected number of rows (merges or splits to fit)")
    p.add_argument("--tolerance", type=int, default=40)
    p.add_argument("--min-area", type=int, default=48)
    p.add_argument("--min-gap", type=int, default=6)
    p.set_defaults(func=cmd_inspect)
    b = sub.add_parser("build", help="build strips, preview and report from a spec file")
    b.add_argument("spec")
    b.set_defaults(func=cmd_build)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
