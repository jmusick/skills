#!/usr/bin/env python3
"""Survey a repo for the release skill: stop checks, the commits since the last tag, and the bump.

Usage (from the repo root):
  next_version.py [--remote NAME] [--no-fetch]

Fetches the remote's tags first (origin's tags are the record of what's released), then prints:
  - stop conditions: detached HEAD, a merge/rebase/cherry-pick/revert in progress, behind upstream,
    uncommitted changes
  - the latest vX.Y.Z tag, whether it's annotated or lightweight, and the commits since it,
    sorted into major / minor / patch / no release / needs judgment
  - the bump and next version those commits call for, and whether that tag (or a newer one)
    is already on the remote
  - tracked version files and whether each matches, trails, or is ahead of the latest tag
  - the changelog, if any, and whether it has an Unreleased section

It decides nothing. Commits that aren't Conventional are listed for you to judge from their diffs,
and the bump it prints is then only a floor. Standard library only; needs git on PATH.
Exit code: 0 after a survey (even with stop conditions), 2 if git isn't usable here.
"""

import argparse
import json
import os
import re
import subprocess
import sys

TAG = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")
HEADER = re.compile(r"^(?P<type>[A-Za-z]+)(?:\((?P<scope>[^)]*)\))?(?P<bang>!)?: \S")
BREAKING = re.compile(r"^BREAKING[ -]CHANGE: ", re.M)
NO_RELEASE = {"docs", "chore", "ci", "build", "style", "refactor", "test", "tests"}
RANK = {"major": 3, "minor": 2, "patch": 1, "none": 0}
SKIP_DIRS = ("node_modules/", "vendor/", "dist/", "build/", "evals/", "fixtures/", "third_party/")


def git(*args, check=True):
    out = subprocess.run(["git", *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if check and out.returncode != 0:
        raise RuntimeError(out.stderr.strip() or f"git {' '.join(args)} failed")
    return out.stdout if check else out


def parse_tag(name):
    m = TAG.match(name)
    return tuple(int(x) for x in m.groups()) if m else None


def fmt(v):
    return "v%d.%d.%d" % v


def bump(v, kind):
    major, minor, patch = v
    if kind == "major":
        return (major + 1, 0, 0)
    if kind == "minor":
        return (major, minor + 1, 0)
    if kind == "patch":
        return (major, minor, patch + 1)
    return v


def stop_checks():
    stops = []
    if git("symbolic-ref", "-q", "HEAD", check=False).returncode != 0:
        stops.append("HEAD is detached.")
    for marker, what in (("MERGE_HEAD", "a merge"), ("rebase-merge", "a rebase"), ("rebase-apply", "a rebase or am"),
                         ("CHERRY_PICK_HEAD", "a cherry-pick"), ("REVERT_HEAD", "a revert")):
        path = git("rev-parse", "--git-path", marker).strip()
        if os.path.exists(path):
            stops.append(f"{what[0].upper() + what[1:]} is in progress.")
    upstream = git("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}", check=False)
    if upstream.returncode == 0:
        behind, ahead = git("rev-list", "--left-right", "--count", "@{u}...HEAD").split()
        if int(behind):
            stops.append(f"The branch is {behind} commit(s) behind {upstream.stdout.strip()}.")
        upstream_note = f"{upstream.stdout.strip()} ({ahead} ahead, {behind} behind)"
    else:
        upstream_note = "none (push with -u)"
    dirty = [line for line in git("status", "--porcelain").splitlines() if line.strip()]
    if dirty:
        stops.append(f"{len(dirty)} uncommitted change(s): " + ", ".join(l[3:] for l in dirty[:8]) + (" ..." if len(dirty) > 8 else ""))
    return stops, upstream_note


def remote_tags(remote):
    out = git("ls-remote", "--tags", "--refs", remote, check=False)
    if out.returncode != 0:
        return None
    return {line.split("refs/tags/", 1)[1] for line in out.stdout.splitlines() if "refs/tags/" in line}


def classify(subject, body):
    m = HEADER.match(subject)
    if not m:
        return "judge", "not Conventional"
    ctype = m.group("type").lower()
    if m.group("bang") or BREAKING.search(body):
        return "major", ctype + ("!" if m.group("bang") else " + BREAKING CHANGE footer")
    if ctype == "feat":
        return "minor", ctype
    if ctype in ("fix", "perf"):
        return "patch", ctype
    if ctype in NO_RELEASE:
        return "none", ctype
    return "judge", f"unknown type '{ctype}'"


def version_files(latest):
    found = []
    files = [f for f in git("ls-files").splitlines() if not any(f.startswith(d) or ("/" + d) in f for d in SKIP_DIRS)]
    for f in files:
        base = f.rsplit("/", 1)[-1]
        version = None
        try:
            if base in ("package.json", "manifest.json", "plugin.json", "marketplace.json", "composer.json"):
                with open(f, encoding="utf-8") as fh:
                    data = json.load(fh)
                version = data.get("version") if isinstance(data, dict) else None
            elif base in ("pyproject.toml", "Cargo.toml"):
                with open(f, encoding="utf-8") as fh:
                    text = fh.read()
                m = re.search(r'^\[(?:project|package|tool\.poetry)\][^\[]*?^version\s*=\s*"([^"]+)"', text, re.M | re.S)
                version = m.group(1) if m else None
            elif base.endswith(".csproj") or base == "Directory.Build.props":
                if base.startswith("Assembly-CSharp"):
                    continue
                with open(f, encoding="utf-8-sig") as fh:
                    m = re.search(r"<(?:Version|VersionPrefix)>([^<]+)</", fh.read())
                version = m.group(1) if m else None
            elif base == "VERSION":
                with open(f, encoding="utf-8") as fh:
                    version = fh.read().strip() or None
            elif f.endswith("ProjectSettings/ProjectSettings.asset"):
                with open(f, encoding="utf-8", errors="replace") as fh:
                    m = re.search(r"^\s*bundleVersion:\s*(\S+)", fh.read(), re.M)
                version = m.group(1) if m else None
        except (OSError, ValueError):
            continue
        if not version:
            continue
        parsed = parse_tag("v" + version.lstrip("v"))
        if latest and parsed:
            state = "matches" if parsed == latest else ("AHEAD of the latest tag" if parsed > latest else "behind the latest tag")
        else:
            state = "not X.Y.Z" if not parsed else "no tag to compare"
        found.append((f, version, state))
    return found


def changelog():
    for name in git("ls-files").splitlines():
        if re.fullmatch(r"(?i)(changelog|changes|history)(\.md|\.markdown|\.txt|\.rst)?", name):
            with open(name, encoding="utf-8", errors="replace") as fh:
                has_unreleased = re.search(r"^#+\s*\[?unreleased\]?", fh.read(), re.M | re.I) is not None
            return name, has_unreleased
    return None, False


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--remote", default="origin")
    ap.add_argument("--no-fetch", action="store_true", help="skip fetching tags (offline)")
    args = ap.parse_args()
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass

    try:
        git("rev-parse", "--show-toplevel")
    except (RuntimeError, OSError) as e:
        print(f"Not a usable git repo: {e}")
        return 2

    has_remote = args.remote in git("remote").split()
    if not has_remote:
        fetch_note = f"no remote named {args.remote}: nothing can be pushed"
    elif args.no_fetch:
        fetch_note = "skipped (--no-fetch); local tags may lag the remote"
    else:
        r = git("fetch", args.remote, "--tags", check=False)
        fetch_note = "ok" if r.returncode == 0 else "FAILED: " + (r.stderr.strip().splitlines() or ["?"])[-1]

    stops, upstream_note = stop_checks()
    print(f"Branch: {git('rev-parse', '--abbrev-ref', 'HEAD').strip()}   upstream: {upstream_note}")
    print(f"Fetch {args.remote} tags: {fetch_note}")
    print("\nStop conditions: " + ("none" if not stops else ""))
    for s in stops:
        print(f"  - {s}")

    tags = sorted((v, t) for t in git("tag", "--list", "v*").split() if (v := parse_tag(t)))
    latest = tags[-1][0] if tags else None
    if latest:
        tag = fmt(latest)
        style = "annotated" if git("cat-file", "-t", tag).strip() == "tag" else "lightweight"
        reachable = git("merge-base", "--is-ancestor", tag, "HEAD", check=False).returncode == 0
        print(f"\nLatest tag: {tag} ({style}{'' if reachable else ', NOT an ancestor of HEAD: check the branch'})")
        rng = [f"{tag}..HEAD"]
    else:
        print("\nLatest tag: none. This is the first release; the version is the user's call.")
        rng = ["HEAD"]

    log = git("log", "--no-merges", "--format=%h%x1f%s%x1f%b%x1e", *rng)
    commits = [c.strip("\n").split("\x1f") for c in log.split("\x1e") if c.strip()]
    merges = int(git("rev-list", "--merges", "--count", *rng).strip() or 0)
    print(f"Commits since: {len(commits)}" + (f" (plus {merges} merge commit(s), not counted)" if merges else ""))
    if not commits:
        print("\nNothing to release.")
        return 0

    groups = {k: [] for k in ("major", "minor", "patch", "none", "judge")}
    for sha, subject, body in commits:
        kind, why = classify(subject, body)
        groups[kind].append((sha, subject, why))
    labels = {"major": "Major (breaking)", "minor": "Minor (feat)", "patch": "Patch (fix, perf)",
              "none": "No release", "judge": "Needs your judgment (read the diff: git show <sha>)"}
    for kind in ("major", "minor", "patch", "none", "judge"):
        if groups[kind]:
            print(f"\n{labels[kind]}:")
            for sha, subject, why in groups[kind]:
                print(f"  {sha} {subject}" + (f"   [{why}]" if kind in ("major", "judge") else ""))

    kind = max((k for k in RANK if groups[k]), key=RANK.get, default="none")
    floor = " at least, after you judge the commits above" if groups["judge"] and kind != "major" else ""
    print()
    if kind == "none" and not groups["judge"]:
        print("Bump: none. No commit calls for a version; push the branch without a tag.")
    else:
        nxt = bump(latest or (0, 0, 0), kind) if kind != "none" else None
        print(f"Bump: {kind}{floor}" + (f" -> {fmt(nxt)}" if nxt else ""))
        if kind == "major":
            print("  A major bump (or 1.0.0 from 0.x) is the user's call: confirm first.")
        if nxt and has_remote:
            remote = remote_tags(args.remote)
            if remote is None:
                print(f"  Couldn't list {args.remote}'s tags; check for {fmt(nxt)} before tagging.")
            else:
                clash = sorted(t for t in remote if (v := parse_tag(t)) and v >= nxt)
                if clash:
                    print(f"  STOP: {args.remote} already has {', '.join(clash)}.")

    files = version_files(latest)
    print("\nVersion files: " + ("none tracked" if not files else ""))
    for f, version, state in files:
        print(f"  {f}: {version} ({state})")
    name, unreleased = changelog()
    print(f"\nChangelog: {name + (' (has an Unreleased section)' if unreleased else '') if name else 'none (do not create one)'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
