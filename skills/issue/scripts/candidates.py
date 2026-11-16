#!/usr/bin/env python3
"""Apply the issue skill's skip rules to the open issues and rank what's left.

Usage (from the repo):
  candidates.py                 rank the open issues
  candidates.py 12 15           report on the named issues (closed, claimed, waiting, ...)
  candidates.py --limit 200     read more issues (default 100)

Skips, with the reason: issues assigned to someone else, linked to someone else's open PR,
labelled blocked / wontfix / duplicate / invalid / on hold / stale / not planned, waiting on a
reply (the last comment has <!-- agent-waiting-for-reply -->), or naming an open issue in a
"Depends on #N" or "Blocked by #N" line. Lists your own open PRs' issues as resumable.
Ranks the rest by priority label (critical, urgent and p0 first, then priority: high and p1,
then p2; unlabeled issues come before p3 and low), then age.

It can't judge whether an issue is clear enough to finish, needs a decision, or is easy:
read the top candidates in full for that. Standard library only; needs gh, authenticated.
Exit code: 0 on success, 2 if gh fails.
"""

import argparse
import datetime as dt
import json
import re
import subprocess
import sys

MARKER = "<!-- agent-waiting-for-reply -->"
SKIP_LABELS = {"blocked", "wontfix", "duplicate", "invalid", "onhold", "stale", "notplanned"}
PRIORITY = {"critical": 0, "prioritycritical": 0, "urgent": 0, "priorityurgent": 0, "priorityhigh": 1, "highpriority": 1,
            "prioritymedium": 2, "prioritylow": 4, "lowpriority": 4}
UNLABELED = 2.5  # after p0-p2 and high, before p3 and low
DEPENDS = re.compile(r"(?im)^[\s>*-]*(?:depends on|blocked by)\s*:?\s*((?:#\d+[\s,and]*)+)")
CLOSES = re.compile(r"(?i)\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+#(\d+)")
FIELDS = "number,title,state,labels,assignees,createdAt,body,comments,url"


def gh(*args):
    out = subprocess.run(["gh", *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if out.returncode != 0:
        raise RuntimeError(out.stderr.strip() or "gh " + " ".join(args) + " failed")
    return out.stdout


def norm(label):
    return re.sub(r"[^a-z0-9]", "", label.lower())


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("numbers", nargs="*", type=int, help="issues the user named")
    ap.add_argument("--limit", type=int, default=100)
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    try:
        me = gh("api", "user", "--jq", ".login").strip()
        issues = {i["number"]: i for i in json.loads(gh("issue", "list", "--state", "open", "--limit", str(args.limit), "--json", FIELDS))}
        prs = json.loads(gh("pr", "list", "--state", "open", "--limit", "200", "--json", "number,title,author,headRefName,isDraft,body,closingIssuesReferences"))
    except (RuntimeError, OSError, ValueError) as e:
        print(f"gh failed: {e}")
        return 2

    linked = {}  # issue number -> [(pr number, author, draft)]
    for pr in prs:
        nums = {ref["number"] for ref in pr.get("closingIssuesReferences") or []}
        nums |= {int(n) for n in CLOSES.findall(pr.get("body") or "")}
        if m := re.match(r"issue-(\d+)\b", pr.get("headRefName") or ""):
            nums.add(int(m.group(1)))
        for n in nums:
            linked.setdefault(n, []).append((pr["number"], (pr.get("author") or {}).get("login"), pr.get("isDraft")))

    state_cache = {}

    def is_open(n):
        if n in issues:
            return True
        if n not in state_cache:
            try:
                state_cache[n] = json.loads(gh("issue", "view", str(n), "--json", "state"))["state"] == "OPEN"
            except (RuntimeError, ValueError):
                state_cache[n] = False
        return state_cache[n]

    def status(i):
        """Return (kind, reason): kind is work, resume, or skip."""
        if i.get("state", "OPEN") != "OPEN":
            return "skip", "closed"
        others = [a["login"] for a in i.get("assignees") or [] if a["login"] != me]
        if others:
            return "skip", "assigned to " + ", ".join(others)
        mine = [p for p in linked.get(i["number"], []) if p[1] == me]
        theirs = [p for p in linked.get(i["number"], []) if p[1] != me]
        if theirs:
            return "skip", "open PR " + ", ".join(f"#{p[0]} by {p[1]}" for p in theirs)
        if mine:
            return "resume", "your open PR " + ", ".join(f"#{p[0]}" + (" (draft)" if p[2] else "") for p in mine)
        bad = [l["name"] for l in i.get("labels") or [] if norm(l["name"]) in SKIP_LABELS]
        if bad:
            return "skip", "labelled " + ", ".join(bad)
        comments = i.get("comments") or []
        if comments and MARKER in (comments[-1].get("body") or ""):
            return "skip", "waiting on a reply to the last comment"
        texts = [i.get("body") or ""] + [c.get("body") or "" for c in comments]
        deps = sorted({int(n) for t in texts for group in DEPENDS.findall(t) for n in re.findall(r"#(\d+)", group)} - {i["number"]})
        open_deps = [n for n in deps if is_open(n)]
        if open_deps:
            return "skip", "depends on open " + ", ".join(f"#{n}" for n in open_deps)
        return "work", "assigned to you" if i.get("assignees") else ""

    def rank(label):
        n = norm(label)
        m = re.fullmatch(r"(?:priority)?p(\d)", n)
        return int(m.group(1)) if m else PRIORITY.get(n)

    def tier(i):
        ranks = [r for l in i.get("labels") or [] if (r := rank(l["name"])) is not None]
        return min(ranks, default=UNLABELED)

    def line(i, reason=""):
        age = (dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(i["createdAt"].replace("Z", "+00:00"))).days
        labels = ", ".join(l["name"] for l in i.get("labels") or [])
        return f"  #{i['number']}  {age}d  {i['title']}" + (f"  [{labels}]" if labels else "") + (f"  ({reason})" if reason else "")

    if args.numbers:
        print("Named issues:")
        for n in args.numbers:
            i = issues.get(n)
            if i is None:
                try:
                    i = json.loads(gh("issue", "view", str(n), "--json", FIELDS))
                except (RuntimeError, ValueError):
                    print(f"  #{n}  not found")
                    continue
            kind, reason = status(i)
            print(line(i, {"work": "workable", "resume": "resume", "skip": "skip"}[kind] + (f": {reason}" if reason else "")))
        return 0

    groups = {"work": [], "resume": [], "skip": []}
    for i in issues.values():
        kind, reason = status(i)
        groups[kind].append((i, reason))
    groups["work"].sort(key=lambda x: (tier(x[0]), x[0]["createdAt"]))
    print(f"Open issues read: {len(issues)}" + (f" (the limit; pass --limit to read more)" if len(issues) >= args.limit else ""))
    print(f"\nCandidates, best first ({len(groups['work'])}). Read the top ones in full before choosing:")
    for i, reason in groups["work"]:
        print(line(i, reason))
    if groups["resume"]:
        print(f"\nResumable ({len(groups['resume'])}):")
        for i, reason in groups["resume"]:
            print(line(i, reason))
    if groups["skip"]:
        print(f"\nSkipped ({len(groups['skip'])}):")
        for i, reason in sorted(groups["skip"], key=lambda x: x[0]["number"]):
            print(line(i, reason))
    return 0


if __name__ == "__main__":
    sys.exit(main())
