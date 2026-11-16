#!/usr/bin/env python3
"""Check a repo's Markdown links, find unlinked docs, and find what points at a path.

Usage:
  doc_links.py [--root DIR] [FILE ...]   broken links and anchors, plus orphan docs
  doc_links.py [--root DIR] --to PATH    every link to PATH and every mention of it

Standard library only. Paths in the output are relative to the repo root.
External links (http:, mailto:, //host) are skipped, never fetched.
"""

import argparse
import os
import re
import subprocess
import sys
from urllib.parse import unquote

DOC_EXTS = (".md", ".mdx", ".markdown")
SKIP_DIRS = {".git", "node_modules", "vendor", "third_party", "dist", "build", ".venv", "venv", "__pycache__"}
# GitHub surfaces these without a link, so they're never orphans.
ENTRY_NAMES = {"readme", "index", "agents", "claude", "contributing", "security", "changelog",
               "code_of_conduct", "license", "support", "governance", "funding", "codeowners"}

FENCE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")
INLINE_CODE = re.compile(r"(`+)(.+?)\1")
INLINE_LINK = re.compile(r"!?\[(?:[^\[\]]|\[[^\]]*\])*\]\(\s*(<[^>]*>|[^)\s]+)(?:\s+(?:\"[^\"]*\"|'[^']*'|\([^)]*\)))?\s*\)")
REF_DEF = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*(<[^>]*>|\S+)")
HTML_ATTR = re.compile(r"""\b(?:href|src)\s*=\s*["']([^"']+)["']""", re.I)
HTML_ID = re.compile(r"""<[^>]+\b(?:id|name)\s*=\s*["']([^"']+)["']""", re.I)
ATX = re.compile(r"^\s{0,3}(#{1,6})\s+(.*?)(?:\s+#+)?\s*$")
SETEXT = re.compile(r"^\s{0,3}(=+|-+)\s*$")
SCHEME = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")


def run_git(root, *args):
    try:
        out = subprocess.run(["git", "-C", root, *args], capture_output=True, check=True)
    except (OSError, subprocess.CalledProcessError):
        return None
    return out.stdout


def find_root(start):
    out = run_git(start, "rev-parse", "--show-toplevel")
    return os.path.normpath(out.decode().strip()) if out else os.path.abspath(start)


def list_files(root):
    """Tracked plus untracked-but-not-ignored files, as repo-relative POSIX paths."""
    out = run_git(root, "ls-files", "-z", "--cached", "--others", "--exclude-standard")
    if out is not None:
        files = [p for p in out.decode("utf-8", "replace").split("\0") if p]
    else:
        files = []
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            rel = os.path.relpath(dirpath, root)
            for name in filenames:
                files.append(name if rel == "." else f"{rel}/{name}".replace(os.sep, "/"))
    return sorted(f for f in files if not set(f.split("/")[:-1]) & SKIP_DIRS
                  and os.path.isfile(os.path.join(root, f)))


def read_text(root, rel):
    try:
        with open(os.path.join(root, rel), encoding="utf-8", errors="replace") as fh:
            return fh.read().splitlines()
    except OSError:
        return []


def prose_lines(lines, blank_code=True):
    """Yield (line_no, text) outside front matter and fenced code, with inline code blanked."""
    fence = None
    start = 0
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() in ("---", "..."):
                start = i + 1
                break
    for i in range(start, len(lines)):
        line = lines[i]
        m = FENCE.match(line)
        if fence:
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence):
                fence = None
            continue
        if m:
            fence = m.group(1)
            continue
        yield i + 1, INLINE_CODE.sub(lambda c: " " * len(c.group(0)), line) if blank_code else line


def slugify(text):
    """GitHub's heading anchor: rendered text, lowercased, punctuation dropped, spaces to hyphens."""
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)   # links -> their text
    text = re.sub(r"<[^>]+>", "", text)                         # HTML tags
    text = text.replace("`", "")
    text = re.sub(r"(\*\*|__|\*|~~)", "", text)                 # emphasis markers
    text = text.strip().lower()
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def anchors_of(lines):
    seen = {}
    anchors = set()
    prev = None
    for no, line in prose_lines(lines, blank_code=False):
        title = None
        m = ATX.match(line)
        if m:
            title = m.group(2)
        elif prev and prev[1].strip() and SETEXT.match(line) and not prev[1].lstrip().startswith(("-", "*", ">", "|")):
            title = prev[1].strip()
        if title is not None:
            slug = slugify(title)
            n = seen.get(slug, 0)
            seen[slug] = n + 1
            anchors.add(slug if n == 0 else f"{slug}-{n}")
        anchors.update(a.lower() for a in HTML_ID.findall(line))
        prev = (no, line)
    return anchors


def links_in(lines):
    for no, line in prose_lines(lines):
        targets = [m.group(1) for m in INLINE_LINK.finditer(line)]
        m = REF_DEF.match(line)
        if m:
            targets.append(m.group(1))
        targets += HTML_ATTR.findall(line)
        for t in targets:
            t = t.strip("<>").strip()
            if t and not SCHEME.match(t) and not t.startswith("//") and not re.search(r"[{}$]", t):
                yield no, t


def resolve(src, target):
    """Repo-relative POSIX path and anchor for a link target found in src."""
    path, _, anchor = target.partition("#")
    path = unquote(path.split("?", 1)[0])
    if not path:
        return src, unquote(anchor)
    base = "" if path.startswith("/") else os.path.dirname(src)
    joined = os.path.normpath(os.path.join(base, path.lstrip("/"))).replace(os.sep, "/")
    return ("" if joined == "." else joined), unquote(anchor)


class Repo:
    def __init__(self, root):
        self.root = root
        self.files = list_files(root)
        self.file_set = set(self.files)
        self.dirs = {""}
        for f in self.files:
            parts = f.split("/")
            for i in range(1, len(parts)):
                self.dirs.add("/".join(parts[:i]))
        self.docs = [f for f in self.files if f.lower().endswith(DOC_EXTS)]
        self._anchors = {}

    def anchors(self, rel):
        if rel not in self._anchors:
            self._anchors[rel] = anchors_of(read_text(self.root, rel))
        return self._anchors[rel]

    def exists(self, rel):
        if rel in self.file_set or rel in self.dirs:
            return "ok"
        full = os.path.join(self.root, rel)
        if not os.path.exists(full):
            return "missing"
        # Present on disk but not listed: either git-ignored, or the case differs (Windows/macOS
        # find it, GitHub and Linux don't).
        lowered = rel.lower()
        if any(p.lower() == lowered for p in self.file_set | self.dirs):
            return "case"
        return "ok"

    def index_of(self, rel):
        """The doc GitHub renders for a directory link, if any."""
        for name in ("README.md", "readme.md", "index.md"):
            cand = f"{rel}/{name}" if rel else name
            if cand in self.file_set:
                return cand
        return None


def check(repo, only):
    broken = []
    inbound = {d: 0 for d in repo.docs}
    for src in repo.docs:
        for no, target in links_in(read_text(repo.root, src)):
            rel, anchor = resolve(src, target)
            dest = rel if rel in repo.file_set else repo.index_of(rel) if rel in repo.dirs else None
            if dest in inbound and dest != src:
                inbound[dest] += 1
            if only and src not in only:
                continue
            state = repo.exists(rel)
            if rel.startswith("../"):
                broken.append((src, no, target, "points outside the repo"))
            elif state == "missing":
                broken.append((src, no, target, "no such file"))
            elif state == "case":
                broken.append((src, no, target, "case differs from the file on disk (breaks on GitHub and Linux)"))
            elif anchor and dest and dest.lower().endswith(DOC_EXTS) and anchor.lower() not in repo.anchors(dest):
                broken.append((src, no, target, f"no heading or id for #{anchor} in {dest}"))

    print("Broken links" + (f" (in {len(only)} named file(s))" if only else ""))
    if broken:
        for src, no, target, why in broken:
            print(f"- {src}:{no}: {target} ({why})")
    else:
        print("- none")

    if only:
        return
    orphans = [d for d, n in inbound.items() if n == 0
               and os.path.splitext(d.rsplit("/", 1)[-1])[0].lower() not in ENTRY_NAMES
               and not d.startswith((".github/", ".claude/"))]
    print("\nDocs no other doc links to (code may still load them; check with --to before calling one unused)")
    print("\n".join(f"- {d}" for d in orphans) if orphans else "- none")
    print(f"\nChecked {len(repo.docs)} docs.")


def find_refs(repo, path):
    path = os.path.normpath(path.strip("/")).replace(os.sep, "/")
    under = path + "/"
    links, mentions = [], []
    parts = path.split("/")
    base = parts[-1]
    # Prose often names a doc by a shorter path (references/x.md) or just its file name. Match
    # every trailing part of the path, and the bare name unless other files share it (SKILL.md).
    distinctive = (os.path.splitext(base)[0].lower() not in ENTRY_NAMES
                   and not any(f.rsplit("/", 1)[-1] == base and f != path for f in repo.files))
    tails = ["/".join(parts[i:]) for i in range(len(parts) - (0 if distinctive else 1))]
    pattern = re.compile(r"(?<![\w.-])(?:" + "|".join(map(re.escape, tails)) + r")(?![\w-])")
    for src in repo.files:
        lines = read_text(repo.root, src)
        linked_lines = set()
        if src.lower().endswith(DOC_EXTS):
            for no, target in links_in(lines):
                rel, _ = resolve(src, target)
                if rel == path or rel.startswith(under):
                    links.append((src, no, target))
                    linked_lines.add(no)
        if src == path or src.startswith(under):
            continue
        for no, line in enumerate(lines, 1):
            if no not in linked_lines and pattern.search(line):
                mentions.append((src, no, line.strip()[:160]))
    print(f"Links to {path}")
    print("\n".join(f"- {s}:{n}: {t}" for s, n, t in links) if links else "- none")
    print(f"\nOther mentions of {path}, a shorter form of it" + (f", or {base}" if distinctive else "") + " (prose, code comments, config)")
    print("\n".join(f"- {s}:{n}: {t}" for s, n, t in mentions) if mentions else "- none")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="*", help="check links only in these docs (skips the orphan list)")
    ap.add_argument("--root", default=".", help="repo root (default: the git top level above the current directory)")
    ap.add_argument("--to", metavar="PATH", help="list links to and mentions of PATH, which may no longer exist")
    args = ap.parse_args()

    root = find_root(args.root)
    repo = Repo(root)
    if args.to:
        find_refs(repo, os.path.relpath(os.path.abspath(args.to), root))
        return 0
    only = set()
    for f in args.files:
        rel = os.path.relpath(os.path.abspath(f), root).replace(os.sep, "/")
        if rel not in repo.file_set:
            print(f"warning: {f} is not a file in {root}", file=sys.stderr)
        only.add(rel)
    check(repo, only)
    return 0


if __name__ == "__main__":
    sys.exit(main())
