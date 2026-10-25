#!/usr/bin/env python3
"""Read-only release survey for the current git repo.

Usage: python version_info.py <major|minor|patch>

Prints JSON describing the current version (from semver tags and tracked
version files), the next version for the requested bump, where the version
lives, the repo's tag style, and the state of the branch. Changes nothing.
"""
import json
import os
import re
import subprocess
import sys

SEMVER = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)$")
SKIP_DIRS = ("node_modules/", "vendor/", "Library/", "dist/", "build/", ".venv/")


def git(*args, check=False):
    r = subprocess.run(["git", *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if check and r.returncode != 0:
        sys.exit(json.dumps({"error": f"git {' '.join(args)} failed: {r.stderr.strip()}"}))
    return r.stdout.strip() if r.returncode == 0 else None


def parse(v):
    m = SEMVER.match(v.strip()) if v else None
    return tuple(int(x) for x in m.groups()) if m else None


def fmt(t):
    return f"{t[0]}.{t[1]}.{t[2]}"


def bump(t, kind):
    if kind == "major":
        return (t[0] + 1, 0, 0)
    if kind == "minor":
        return (t[0], t[1] + 1, 0)
    return (t[0], t[1], t[2] + 1)


def read(path):
    try:
        with open(path, encoding="utf-8-sig") as f:
            return f.read()
    except (OSError, UnicodeDecodeError):
        return None


def version_in(path, text):
    """Return (version, how_to_update) for a known version file, else None."""
    name = os.path.basename(path)
    if name in ("package.json", "app.json", "tauri.conf.json"):
        try:
            data = json.loads(text)
        except ValueError:
            return None
        if name == "app.json" and isinstance(data.get("expo"), dict):
            data = data["expo"]
        v = data.get("version") if isinstance(data, dict) else None
        if not isinstance(v, str):
            return None
        how = "npm version <X.Y.Z> --no-git-tag-version (also updates package-lock.json)" if name == "package.json" else 'edit "version"'
        return v, how
    if name == "package-lock.json":
        m = re.search(r'^\s{2}"version":\s*"([^"]+)"', text, re.M)
        return (m.group(1), 'top-level "version" and packages[""].version; npm version handles it') if m else None
    if name == "manifest.json":
        try:
            data = json.loads(text)
        except ValueError:
            return None
        if isinstance(data, dict) and "manifest_version" in data and isinstance(data.get("version"), str):
            return data["version"], 'edit "version" (browser extension)'
        return None
    if name == "ProjectSettings.asset":
        m = re.search(r"^\s*bundleVersion:\s*(\S+)", text, re.M)
        return (m.group(1), "edit bundleVersion (Unity)") if m else None
    if name in ("pyproject.toml", "Cargo.toml"):
        section = None
        for line in text.splitlines():
            s = line.strip()
            if s.startswith("["):
                section = s
                continue
            if section in ("[project]", "[tool.poetry]", "[package]", "[workspace.package]"):
                m = re.match(r'version\s*=\s*"([^"]+)"', s)
                if m:
                    return m.group(1), f"edit version under {section}"
        return None
    if name.endswith((".csproj", ".props")):
        m = re.search(r"<(Version|VersionPrefix)>([^<]+)</\1>", text)
        return (m.group(2), f"edit <{m.group(1)}>") if m else None
    if name in ("VERSION", "version.txt"):
        v = text.strip()
        return (v, "replace file contents") if parse(v) else None
    return None


CANDIDATES = {
    "package.json", "package-lock.json", "app.json", "tauri.conf.json", "manifest.json",
    "ProjectSettings.asset", "pyproject.toml", "Cargo.toml", "Directory.Build.props",
    "VERSION", "version.txt",
}


def main():
    kind = (sys.argv[1] if len(sys.argv) > 1 else "").lower()
    if kind not in ("major", "minor", "patch"):
        sys.exit("usage: version_info.py <major|minor|patch>")

    root = git("rev-parse", "--show-toplevel", check=True)
    os.chdir(root)

    # Tags
    tags = []
    for t in (git("tag", "--list") or "").splitlines():
        p = parse(t)
        if p:
            tags.append((p, t))
    tags.sort()
    latest_tag = tags[-1][1] if tags else None
    tag_style = None
    if latest_tag:
        tag_style = "annotated" if git("cat-file", "-t", latest_tag) == "tag" else "lightweight"
    tag_prefix = "v" if (latest_tag is None or latest_tag.startswith("v")) else ""

    # Version files (tracked only)
    files = []
    for path in (git("ls-files") or "").splitlines():
        if any(seg in path for seg in SKIP_DIRS):
            continue
        name = os.path.basename(path)
        if name in CANDIDATES or name.endswith(".csproj"):
            text = read(path)
            found = version_in(path, text) if text is not None else None
            if found:
                files.append({"path": path, "version": found[0], "update": found[1]})
    # Unity regenerates Assembly-CSharp*.csproj; they never hold the release version.
    files = [f for f in files if not os.path.basename(f["path"]).startswith("Assembly-CSharp")]

    candidates = [p for p, _ in tags[-1:]] + [parse(f["version"]) for f in files if parse(f["version"])]
    current = max(candidates) if candidates else (0, 0, 0)
    nxt = bump(current, kind)
    for f in files:
        f["in_lockstep"] = parse(f["version"]) == current
    seen = {f["version"] for f in files} | ({fmt(tags[-1][0])} if tags else set())

    next_tag = f"{tag_prefix}{fmt(nxt)}"
    since = latest_tag
    log = git("log", "--format=%h %s", f"{since}..HEAD") if since else git("log", "--format=%h %s", "-50")
    status = git("status", "--porcelain") or ""
    branch = git("branch", "--show-current") or None
    upstream = git("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")
    ahead_behind = git("rev-list", "--left-right", "--count", "@{u}...HEAD") if upstream else None

    changelog = next((c for c in ("CHANGELOG.md", "CHANGELOG", "CHANGES.md", "HISTORY.md") if os.path.exists(c)), None)

    out = {
        "repo_root": root,
        "bump": kind,
        "current_version": fmt(current),
        "next_version": fmt(nxt),
        "next_tag": next_tag,
        "next_tag_exists_locally": git("rev-parse", "-q", "--verify", f"refs/tags/{next_tag}") is not None,
        "latest_tag": latest_tag,
        "tag_style": tag_style or "lightweight (no existing tags; default)",
        "version_files": files,
        "versions_disagree": len(seen) > 1,
        "versions_seen": sorted(seen),
        "changelog": changelog,
        "branch": branch,
        "upstream": upstream,
        "behind_ahead_upstream": ahead_behind,
        "uncommitted_changes": status.splitlines(),
        "commits_since_latest_tag": (log or "").splitlines()[:50],
    }
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
