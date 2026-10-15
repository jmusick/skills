#!/usr/bin/env python3
"""Scan front-end source for generated-design tells and quality-floor misses.

Usage:
    python lint_tells.py <file-or-folder> [...] [--allow rule,rule]

FAIL lines are quality-floor violations (accessibility, motion safety).
WARN lines are tells: defaults to avoid unless the brief asked for them.
The scan is a heuristic over source text. It can't see the rendered page,
so it misses tells that only show in a screenshot and can flag code that
is fine in context. Exit code is 1 when any FAIL remains, else 0.

Standard library only; works with Python 3.8+.
"""

import argparse
import colorsys
import os
import re
import sys

STYLE_EXT = {".css", ".scss", ".sass", ".less"}
MARKUP_EXT = {".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte", ".astro", ".mdx"}
SCRIPT_EXT = {".js", ".ts", ".mjs", ".cjs"}
ALL_EXT = STYLE_EXT | MARKUP_EXT | SCRIPT_EXT
SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".next", ".nuxt", ".svelte-kit",
             ".astro", "out", "coverage", "vendor", ".turbo", ".cache"}

# (rule, severity, pattern, message, applies to: "all" | "style" | "markup")
LINE_RULES = [
    ("transition-all", "FAIL",
     r"transition(-property)?\s*:\s*all\b|\btransition-all\b",
     "transition: all; name the properties (transform, opacity)", "all"),
    ("zoom-disabled", "FAIL",
     r"user-scalable\s*=\s*(no|0)|maximum-scale\s*=\s*1(\.0)?\b",
     "zoom disabled in the viewport meta", "all"),
    ("click-div", "FAIL",
     r"<(div|span)\b[^>]*\bon[Cc]lick\s*=",
     "click handler on a div or span; use <button> or <a>", "markup"),
    ("scale-zero", "WARN",
     r"scale\(\s*0\s*\)|\bscale-0\b",
     "animating from scale(0); start near 0.95 with opacity", "all"),
    ("ease-in", "WARN",
     r"\bease-in\b(?!-out)",
     "ease-in delays the first movement; use a strong ease-out", "all"),
    ("gradient-text", "WARN",
     r"background-clip\s*:\s*text|\bbg-clip-text\b",
     "gradient-filled text; use solid ink", "all"),
    ("glass", "WARN",
     r"backdrop-filter\s*:\s*blur|\bbackdrop-blur(-\w+)?\b",
     "backdrop blur; is this a specific effect or decoration?", "all"),
    ("accent-border", "WARN",
     r"border-(left|inline-start)(-width)?\s*:\s*([2-9]|\d{2,})px|\bborder-l-([2-9]|\[\d)",
     "thick colored side border on a card or callout", "all"),
    ("violet-gradient", "WARN",
     r"\b(from|via|to)-(violet|indigo|purple|fuchsia)-\d{2,3}\b",
     "violet or indigo gradient", "all"),
    ("copy-cliche", "WARN",
     r"\b(elevate|elevates|seamless|seamlessly|unleash|supercharge|next-gen|"
     r"revolutioni[sz]e|empower|empowers|game-changer|cutting-edge)\b",
     "selling copy; say what the thing does", "markup"),
    ("scroll-prompt", "WARN",
     r"scroll (down )?to (explore|discover|learn more)|swipe down",
     "scroll prompt; let the content pull the reader on", "markup"),
    ("invented-proof", "WARN",
     r"trusted by|loved by \d|\b\d{1,3}(,\d{3})+\+? (teams|users|customers|companies)\b|99\.9+%",
     "a claim or number; confirm the user supplied it", "markup"),
    ("placeholder-name", "WARN",
     r"\b(acme|john doe|jane doe|lorem ipsum)\b",
     "placeholder name or filler text", "markup"),
]
LINE_RULES = [(r, s, re.compile(p, re.I if r in {"copy-cliche", "scroll-prompt",
               "invented-proof", "placeholder-name"} else 0), m, a)
              for r, s, p, m, a in LINE_RULES]

OUTLINE_NONE = re.compile(r"outline\s*:\s*(none|0)\b|\boutline-none\b")
FOCUS_VISIBLE = re.compile(r"focus-visible")
IMG_NO_ALT = re.compile(r"<img\b(?![^>]*\balt\s*=)[^>]*>", re.S | re.I)
CSS_BLOCK = re.compile(r"\{[^{}]*\}")
UPPER = re.compile(r"text-transform\s*:\s*uppercase")
TRACKING = re.compile(r"letter-spacing\s*:\s*0?\.\d+(em|rem)|letter-spacing\s*:\s*[1-9]")
TW_EYEBROW = re.compile(r"[\"'`][^\"'`]*\buppercase\b[^\"'`]*\btracking-(wide|wider|widest|\[)[^\"'`]*[\"'`]"
                        r"|[\"'`][^\"'`]*\btracking-(wide|wider|widest|\[)[^\"'`]*\buppercase\b[^\"'`]*[\"'`]")
INDEX_NUM = re.compile(r">\s*\(?0[1-9]\)?\s*[./]?\s*<|[\"'`]\(?0[1-9]\)?[./]?[\"'`]")
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿]")
GRADIENT = re.compile(r"(linear|radial|conic)-gradient\(([^;{}]*)\)")
HEX = re.compile(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")
SHADOW = re.compile(r"box-shadow\s*:\s*(?!none)|\bshadow-(sm|md|lg|xl|2xl)\b")
ANIMATION = re.compile(r"@keyframes|\btransition\s*:|\banimation\s*:|\banimate-\w+|\btransition-(transform|opacity|colors)\b|framer-motion|from ['\"]motion")
REDUCED = re.compile(r"prefers-reduced-motion|motion-safe:|motion-reduce:|useReducedMotion|MotionConfig")


def hex_to_hls(value):
    value = value.lstrip("#")
    if len(value) == 3:
        value = "".join(c * 2 for c in value)
    r, g, b = (int(value[i:i + 2], 16) / 255 for i in (0, 2, 4))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return h * 360, l, s


def is_cream(hls):
    h, l, s = hls
    return 30 <= h <= 60 and l >= 0.88 and 0.15 <= s <= 0.75


def is_terracotta(hls):
    h, l, s = hls
    return 5 <= h <= 25 and 0.40 <= l <= 0.65 and 0.35 <= s <= 0.80


def is_violet(hls):
    h, l, s = hls
    return 235 <= h <= 300 and s >= 0.35 and 0.25 <= l <= 0.80


def collect(paths):
    files = []
    for path in paths:
        if os.path.isfile(path):
            files.append(path)
            continue
        for root, dirs, names in os.walk(path):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for name in names:
                ext = os.path.splitext(name)[1].lower()
                if ext in ALL_EXT and ".min." not in name:
                    files.append(os.path.join(root, name))
    return sorted(files)


def display(path):
    try:
        path = os.path.relpath(path)
    except ValueError:  # another drive on Windows
        pass
    return os.path.normpath(path).replace(os.sep, "/")


def line_of(text, index):
    return text.count("\n", 0, index) + 1


def kind_of(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in STYLE_EXT:
        return "style"
    if ext in MARKUP_EXT:
        return "markup"
    return "script"


def scan(files, allow):
    findings = []
    creams, terracottas = [], []
    shadow_count = 0
    first_animation = None
    has_reduced = False

    def add(sev, path, line, rule, message):
        if rule not in allow:
            findings.append((sev, path, line, rule, message))

    for path in files:
        try:
            with open(path, encoding="utf-8", errors="replace") as handle:
                text = handle.read()
        except OSError as err:
            print("skip {}: {}".format(path, err), file=sys.stderr)
            continue
        kind = kind_of(path)
        lines = text.splitlines()

        for number, line in enumerate(lines, 1):
            for rule, sev, pattern, message, applies in LINE_RULES:
                if applies == "markup" and kind != "markup":
                    continue
                if pattern.search(line):
                    add(sev, path, number, rule, message)
            if kind == "markup" and EMOJI.search(line):
                add("WARN", path, number, "emoji", "emoji in markup; use an icon library or words")

        if not FOCUS_VISIBLE.search(text):
            for match in OUTLINE_NONE.finditer(text):
                add("FAIL", path, line_of(text, match.start()), "outline-none",
                    "outline removed and no :focus-visible style in this file")

        if kind == "markup":
            for match in IMG_NO_ALT.finditer(text):
                add("FAIL", path, line_of(text, match.start()), "img-alt", "<img> without alt")

        for block in CSS_BLOCK.finditer(text):
            if UPPER.search(block.group()) and TRACKING.search(block.group()):
                add("WARN", path, line_of(text, block.start()), "eyebrow",
                    "uppercase plus letter-spacing; tiny tracked labels are a tell")
        for match in TW_EYEBROW.finditer(text):
            add("WARN", path, line_of(text, match.start()), "eyebrow",
                "uppercase tracking-* label; tiny tracked labels are a tell")

        index_hits = list(INDEX_NUM.finditer(text))
        if len({m.group() for m in index_hits}) >= 2:
            add("WARN", path, line_of(text, index_hits[0].start()), "index-numbers",
                "01 / 02 / 03 numbering; only for a real sequence")

        if kind != "markup" or "<style" in text or "style=" in text or "className" in text:
            for match in GRADIENT.finditer(text):
                colors = [hex_to_hls(h) for h in HEX.findall(match.group(2))]
                if any(is_violet(c) for c in colors):
                    add("WARN", path, line_of(text, match.start()), "violet-gradient",
                        "violet or indigo gradient")
            for match in HEX.finditer(text):
                hls = hex_to_hls(match.group(1))
                where = (path, line_of(text, match.start()), "#" + match.group(1))
                if is_cream(hls):
                    creams.append(where)
                elif is_terracotta(hls):
                    terracottas.append(where)

        shadow_count += len(SHADOW.findall(text))
        if first_animation is None:
            match = ANIMATION.search(text)
            if match:
                first_animation = (path, line_of(text, match.start()))
        if REDUCED.search(text):
            has_reduced = True

    if creams and terracottas:
        path, line, value = terracottas[0]
        add("WARN", path, line, "cream-terracotta",
            "cream ground ({}) with terracotta accent ({}); the current generated look".format(
                creams[0][2], value))
    if shadow_count >= 6:
        add("WARN", files[0] if files else "-", 1, "shadows",
            "{} shadow declarations; shadows on things at rest read as the SaaS-card kit".format(
                shadow_count))
    if first_animation and not has_reduced:
        add("FAIL", first_animation[0], first_animation[1], "reduced-motion",
            "motion with no prefers-reduced-motion handling anywhere in the scanned files")
    return findings


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("paths", nargs="+", help="files or folders to scan")
    parser.add_argument("--allow", default="",
                        help="comma-separated rules to skip because the brief asks for them")
    args = parser.parse_args()
    allow = {r.strip() for r in args.allow.split(",") if r.strip()}

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    files = collect(args.paths)
    if not files:
        print("No front-end source files found.")
        return 0
    findings = scan(files, allow)
    findings.sort(key=lambda f: (f[0] != "FAIL", f[1], f[2]))
    for sev, path, line, rule, message in findings:
        print("{} {}:{} [{}] {}".format(sev, display(path), line, rule, message))
    fails = sum(1 for f in findings if f[0] == "FAIL")
    warns = len(findings) - fails
    print("\n{} file(s) scanned: {} FAIL, {} WARN".format(len(files), fails, warns))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
