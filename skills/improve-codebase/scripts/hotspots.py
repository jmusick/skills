#!/usr/bin/env python3
"""Find a repo's hotspots from git history. Read-only.

Prints JSON: the files touched by the most recent commits (with how many of
those commits look like fixes, the file's size, and when it last changed) and
the largest tracked source files. Lockfiles, changelogs, vendored code, build
output, and binary files are left out.

Usage: hotspots.py [--path DIR] [--commits N] [--top N]
"""
import argparse
import json
import os
import re
import subprocess
import sys

FIX = re.compile(r"\b(fix(es|ed)?|bug|hotfix|revert|regression|broken|crash)\b", re.I)
SKIP_DIRS = {
    "node_modules", "vendor", "third_party", "dist", "build", "out", "target", ".git",
    "__pycache__", ".venv", "venv", ".next", ".nuxt", "coverage", ".turbo", ".cache",
}
SKIP_NAMES = re.compile(
    r"(^|/)(package-lock\.json|yarn\.lock|pnpm-lock\.yaml|bun\.lockb?|Cargo\.lock|poetry\.lock|uv\.lock|"
    r"Pipfile\.lock|go\.sum|composer\.lock|Gemfile\.lock|CHANGELOG[^/]*|CHANGES[^/]*|HISTORY[^/]*)$",
    re.I,
)
SKIP_EXT = re.compile(r"\.(min\.(js|css)|map|snap|svg|png|jpe?g|gif|webp|ico|pdf|zip|gz|woff2?|ttf|lock)$", re.I)
LARGE = 500


def git(*args, cwd=None):
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        return None
    return r.stdout


def skipped(path):
    parts = path.split("/")
    return any(p in SKIP_DIRS for p in parts[:-1]) or bool(SKIP_NAMES.search(path)) or bool(SKIP_EXT.search(path))


def line_count(full):
    try:
        with open(full, "rb") as f:
            data = f.read()
    except OSError:
        return None
    if b"\0" in data[:8192]:
        return None  # binary
    return data.count(b"\n") + (1 if data and not data.endswith(b"\n") else 0)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--path", default=".", help="limit to this folder (relative to the repo root or cwd)")
    ap.add_argument("--commits", type=int, default=500, help="how many recent non-merge commits to read")
    ap.add_argument("--top", type=int, default=25, help="how many files to list in each section")
    args = ap.parse_args()

    top = git("rev-parse", "--show-toplevel")
    if not top:
        print(json.dumps({"error": "not inside a git repository"}))
        return 1
    root = top.strip()
    try:
        scope = os.path.relpath(os.path.abspath(args.path), root).replace(os.sep, "/")
    except ValueError:  # another drive on Windows
        scope = ".."
    if scope.startswith(".."):
        print(json.dumps({"error": f"{args.path} is outside the repository"}))
        return 1
    scope = "" if scope == "." else scope.rstrip("/") + "/"

    log = git("log", "--no-merges", f"-n{args.commits}", "--name-only", "--format=%x00%aI%x09%s", cwd=root) or ""
    stats = {}
    commits = 0
    oldest = newest = None
    for chunk in log.split("\0")[1:]:
        lines = chunk.splitlines()
        if not lines:
            continue
        date, _, subject = lines[0].partition("\t")
        commits += 1
        newest = newest or date
        oldest = date
        is_fix = bool(FIX.search(subject))
        for path in lines[1:]:
            path = path.strip()
            if not path or not path.startswith(scope) or skipped(path):
                continue
            s = stats.setdefault(path, {"path": path, "commits": 0, "fix_commits": 0, "last_changed": date[:10]})
            s["commits"] += 1
            s["fix_commits"] += is_fix

    hot = []
    for s in stats.values():
        full = os.path.join(root, s["path"])
        if not os.path.isfile(full):
            continue  # deleted or renamed since
        s["lines"] = line_count(full)
        if s["lines"] is None:
            continue
        hot.append(s)
    hot.sort(key=lambda s: (-s["commits"], -s["fix_commits"], -s["lines"]))

    tracked = (git("ls-files", "--", scope or ".", cwd=root) or "").splitlines()
    sizes = []
    for path in tracked:
        if skipped(path):
            continue
        n = line_count(os.path.join(root, path))
        if n and n >= LARGE:
            sizes.append({"path": path, "lines": n, "commits": stats.get(path, {}).get("commits", 0)})
    sizes.sort(key=lambda s: -s["lines"])

    out = {
        "repo": root,
        "head": (git("rev-parse", "--short", "HEAD", cwd=root) or "").strip() or None,
        "scope": scope or "(whole repo)",
        "commits_read": commits,
        "date_range": [oldest[:10] if oldest else None, newest[:10] if newest else None],
        "hotspots": hot[: args.top],
        "large_files": sizes[: args.top],
        "note": "Fix commits are guessed from commit subjects (fix, bug, revert, ...), so they depend on how the repo writes messages.",
    }
    json.dump(out, sys.stdout, indent=2)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
