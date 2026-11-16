#!/usr/bin/env python3
"""Find a repo's hotspots from git history. Read-only.

Prints JSON: the files touched by the most recent commits in scope (with how
many of those commits look like fixes, the file's size, and when it last
changed), counted under each file's current name across renames, and the
largest tracked source files. Lockfiles, changelogs, vendored code, build
output, and binary files are left out, and so are docs and data files
(.md, .json, .yaml, ...) unless --include-docs is passed.

Usage: hotspots.py [--path DIR] [--commits N] [--top N] [--include-docs]
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
# Docs and data churn a lot without being code a refactor would touch.
DOC_EXT = re.compile(r"\.(md|mdx|markdown|rst|adoc|txt|json|jsonc|ya?ml|toml|ini|cfg|csv|tsv|xml)$", re.I)
LARGE = 500


def git(*args, cwd=None):
    # quotePath=false keeps non-ASCII paths as UTF-8 instead of "caf\303\251.py", which matches no file.
    r = subprocess.run(["git", "-c", "core.quotePath=false", *args], cwd=cwd,
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        return None
    return r.stdout


def skipped(path, include_docs=False):
    parts = path.split("/")
    return (any(p in SKIP_DIRS for p in parts[:-1]) or bool(SKIP_NAMES.search(path))
            or bool(SKIP_EXT.search(path)) or (not include_docs and bool(DOC_EXT.search(path))))


def line_count(full):
    try:
        with open(full, "rb") as f:
            data = f.read()
    except OSError:
        return None
    if b"\0" in data[:8192]:
        return None  # binary
    return data.count(b"\n") + (1 if data and not data.endswith(b"\n") else 0)


def tally(log, scope="", include_docs=False):
    """Count commits per file from `git log --name-status -M --format=%x00%aI%x09%s` output.

    Returns (stats by current path, commits read, oldest date, newest date). The log runs
    newest-first, so a rename is seen before the older commits made under the old name,
    and those are credited to the name the file has now.
    """
    stats = {}
    renamed = {}  # old path -> its current name
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
        for line in lines[1:]:
            fields = line.split("\t")
            if len(fields) < 2:
                continue
            path = renamed.get(fields[-1], fields[-1])
            if fields[0].startswith("R") and len(fields) == 3:
                renamed[fields[1]] = path
            if not path.startswith(scope) or skipped(path, include_docs):
                continue
            s = stats.setdefault(path, {"path": path, "commits": 0, "fix_commits": 0, "last_changed": date[:10]})
            s["commits"] += 1
            s["fix_commits"] += is_fix
    return stats, commits, oldest, newest


def resolve_scope(path, root):
    """The scope as a repo-relative prefix ("" for the whole repo), or None if it's outside the repo.

    `path` is tried against the current directory first, then the repo root.
    """
    full = os.path.abspath(path)
    if not os.path.exists(full):
        full = os.path.abspath(os.path.join(root, path))
    try:
        scope = os.path.relpath(full, root).replace(os.sep, "/")
    except ValueError:  # another drive on Windows
        return None
    if scope == ".." or scope.startswith("../"):
        return None
    return "" if scope == "." else scope.rstrip("/") + "/"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--path", default=".", help="limit to this folder (relative to the current directory, else the repo root)")
    ap.add_argument("--commits", type=int, default=500, help="how many recent non-merge commits in scope to read")
    ap.add_argument("--top", type=int, default=25, help="how many files to list in each section")
    ap.add_argument("--include-docs", action="store_true", help="also count docs and data files (.md, .json, .yaml, ...)")
    args = ap.parse_args()

    top = git("rev-parse", "--show-toplevel")
    if not top:
        print(json.dumps({"error": "not inside a git repository"}))
        return 1
    root = top.strip()
    scope = resolve_scope(args.path, root)
    if scope is None:
        print(json.dumps({"error": f"{args.path} is outside the repository"}))
        return 1
    if scope and not os.path.isdir(os.path.join(root, scope)):
        print(json.dumps({"error": f"{args.path} is not a folder in the repository"}))
        return 1

    # The pathspec makes -n count only commits that touched the scope. -M reports
    # renames as "R<score>\told\tnew" so history under an old name isn't lost.
    log_args = ["log", "--no-merges", "-M", f"-n{args.commits}", "--name-status", "--format=%x00%aI%x09%s"]
    if scope:
        log_args += ["--", scope]
    stats, commits, oldest, newest = tally(git(*log_args, cwd=root) or "", scope, args.include_docs)

    hot = []
    for s in stats.values():
        full = os.path.join(root, s["path"])
        if not os.path.isfile(full):
            continue  # deleted since
        s["lines"] = line_count(full)
        if s["lines"] is None:
            continue
        hot.append(s)
    hot.sort(key=lambda s: (-s["commits"], -s["fix_commits"], -s["lines"]))

    tracked = (git("ls-files", "--", scope or ".", cwd=root) or "").splitlines()
    sizes = []
    for path in tracked:
        if skipped(path, args.include_docs):
            continue
        n = line_count(os.path.join(root, path))
        if n and n >= LARGE:
            sizes.append({"path": path, "lines": n, "commits": stats.get(path, {}).get("commits", 0)})
    sizes.sort(key=lambda s: -s["lines"])

    shallow = (git("rev-parse", "--is-shallow-repository", cwd=root) or "").strip() == "true"
    notes = ["Fix commits are guessed from commit subjects (fix, bug, revert, ...), so they depend on how the repo writes messages."]
    if shallow:
        notes.append("This is a shallow clone, so history is cut off and every file looks colder than it is. "
                     "Run `git fetch --unshallow` for real counts, or weight the large files list instead.")
    if scope:
        notes.append("A file moved into the scope from outside it counts only from the move.")
    if not args.include_docs:
        notes.append("Docs and data files are left out; pass --include-docs if they're what this repo ships.")

    out = {
        "repo": root,
        "head": (git("rev-parse", "--short", "HEAD", cwd=root) or "").strip() or None,
        "scope": scope or "(whole repo)",
        "shallow": shallow,
        "commits_read": commits,
        "date_range": [oldest[:10] if oldest else None, newest[:10] if newest else None],
        "hotspots": hot[: args.top],
        "large_files": sizes[: args.top],
        "notes": notes,
    }
    json.dump(out, sys.stdout, indent=2)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
