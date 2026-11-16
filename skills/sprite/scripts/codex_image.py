#!/usr/bin/env python3
"""Generate one image with Codex CLI's built-in image_gen tool and save it.

Runs `codex exec` read-only with the prompt on stdin (so long prompts survive
Windows quoting), attaches any reference images, then copies the image Codex
saved under $CODEX_HOME/generated_images to --out. The copy happens here
rather than inside Codex, so Codex never needs write access to the project.

Usage:
  python codex_image.py --prompt-file prompt.txt --out source_walk.png [--ref model_sheet.png ...]

Exits non-zero if Codex fails or no new image appears. Prints JSON with the
saved path(s) and Codex's final message.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

PREAMBLE = (
    "Use your built-in image_gen tool to generate exactly one image from the spec below. "
    "Do not write code, do not draw the image yourself, and do not edit any files. "
    "If reference images are attached, they show the character or style to match exactly. "
    "When the image is done, reply with one short line describing it.\n\n"
)


def codex_home():
    return Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex")


def snapshot(folder):
    if not folder.exists():
        return {}
    return {p: p.stat().st_mtime for p in folder.rglob("*.png")}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--prompt-file", required=True, help="text file holding the image spec")
    parser.add_argument("--out", required=True, help="where to save the image (.png)")
    parser.add_argument("--ref", action="append", default=[], help="reference image to attach (repeatable)")
    parser.add_argument("--model", help="Codex model override (default: the user's Codex config)")
    parser.add_argument("--timeout", type=int, default=600, help="seconds before giving up (default 600)")
    args = parser.parse_args()

    codex = shutil.which("codex")
    if not codex:
        sys.exit("codex CLI not found on PATH. Install it (npm i -g @openai/codex) and run `codex login`.")
    prompt = PREAMBLE + Path(args.prompt_file).read_text(encoding="utf-8")
    refs = [str(Path(r).resolve()) for r in args.ref]
    for r in refs:
        if not Path(r).exists():
            sys.exit(f"reference image not found: {r}")

    images = codex_home() / "generated_images"
    before = snapshot(images)
    started = time.time()
    cmd = [codex, "exec", "--skip-git-repo-check", "-s", "read-only", "--json"]
    if args.model:
        cmd += ["-m", args.model]
    cmd += [f"--image={r}" for r in refs]
    cmd.append("-")  # read the prompt from stdin
    try:
        run = subprocess.run(cmd, input=prompt, capture_output=True, text=True, encoding="utf-8",
                             errors="replace", timeout=args.timeout)
    except subprocess.TimeoutExpired:
        sys.exit(f"codex timed out after {args.timeout}s")

    message, thread = "", None
    for line in run.stdout.splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        thread = event.get("thread_id") or thread
        item = event.get("item") or {}
        if item.get("type") == "agent_message":
            message = item.get("text", message)
    if run.returncode != 0:
        sys.exit(f"codex exited {run.returncode}:\n{run.stderr.strip()[-2000:]}")

    # Codex saves each session's images under generated_images/<thread id>. Read
    # only this session's folder, so parallel runs don't pick up each other's images.
    if thread and (images / thread).is_dir():
        images = images / thread
    after = snapshot(images)
    new = sorted((p for p, m in after.items() if p not in before or m > before[p]),
                 key=lambda p: after[p])
    if not new:
        sys.exit("codex finished but saved no new image. Its reply was:\n" + (message or "(none)"))

    out = Path(args.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    saved = []
    for n, src in enumerate(new):
        dest = out if n == len(new) - 1 else out.with_name(f"{out.stem}.alt{n + 1}{out.suffix}")
        shutil.copy2(src, dest)
        saved.append(str(dest))
    print(json.dumps({"saved": saved[::-1], "codex_source": str(new[-1]),
                      "seconds": round(time.time() - started), "codex_reply": message}, indent=2))


if __name__ == "__main__":
    main()
