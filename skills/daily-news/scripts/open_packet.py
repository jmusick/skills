#!/usr/bin/env python3
"""Open a day's packet folder, snapshot the local site, and summarize what the budget needs from it.

Usage (from the firelands-current repository):
  open_packet.py [--date YYYY-MM-DD] [--library DIR]

Does step 1 of daily-news, items 1 to 3:
  1. Creates editorial/<date>/ in the project library with drafts/, evidence/ and images/.
     Stops if the folder already has packet.json or local-import.json (a run in progress).
  2. Runs read-only SELECTs on the local D1 database through wrangler and writes
     evidence/existing-content.json as {"taken", "date", "articles", "events", "media"}, the shape
     scripts/editorial/manifest-from-research.mjs reads. It never overwrites an existing snapshot.
  3. Prints the digest: stories published in the past 21 days (don't repeat them) and their count
     by section, sections with fewer than three, events in the next 30 days, the newest library
     images, and the newest earlier review.md, whose held leads are today's first leads.

The library is FIRELANDS_PROJECT_DIR, or ../../Projects/firelands-current from the repository.
Standard library only; needs npx (Node) with wrangler in the repository.
Exit code: 0 on success, 1 if it stopped, 2 if a query failed (try `npm run db:migrate:local`).
"""

import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys

QUERIES = {
    "articles": "SELECT * FROM news_articles ORDER BY published_at DESC",
    "events": "SELECT * FROM events ORDER BY starts_on, start_time",
    "media": "SELECT * FROM media ORDER BY created_at DESC",
}


def query(npx, sql):
    out = subprocess.run([npx, "wrangler", "d1", "execute", "DB", "--local", "--json", "--command", sql],
                         capture_output=True, text=True, encoding="utf-8", errors="replace")
    if out.returncode != 0:
        raise RuntimeError((out.stderr or out.stdout).strip()[-800:])
    data = json.loads(out.stdout[out.stdout.find("["):])
    return data[0]["results"]


def sections(repo):
    try:
        with open(os.path.join(repo, "src", "lib", "news.ts"), encoding="utf-8") as fh:
            body = re.search(r"export const SECTIONS = \{(.*?)\}", fh.read(), re.S).group(1)
        return re.findall(r"^\s*([a-z_]+)\s*:", body, re.M)
    except (OSError, AttributeError):
        return []


def day(ms):
    return dt.datetime.fromtimestamp(ms / 1000).date() if isinstance(ms, (int, float)) else None


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--date", default=dt.date.today().isoformat(), help="budget date (default today)")
    ap.add_argument("--library", help="project library (default FIRELANDS_PROJECT_DIR or ../../Projects/firelands-current)")
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    date = dt.date.fromisoformat(args.date)
    repo = os.getcwd()
    if not os.path.exists(os.path.join(repo, "scripts", "editorial", "packet.mjs")):
        print("Run this from the firelands-current repository (scripts/editorial/packet.mjs not found).")
        return 1
    library = args.library or os.environ.get("FIRELANDS_PROJECT_DIR") or os.path.join(repo, "..", "..", "Projects", "firelands-current")
    library = os.path.abspath(library)
    if not os.path.isdir(library):
        print(f"Project library not found: {library}. Set FIRELANDS_PROJECT_DIR or pass --library.")
        return 1

    packet = os.path.join(library, "editorial", date.isoformat())
    for name in ("packet.json", "local-import.json"):
        if os.path.exists(os.path.join(packet, name)):
            print(f"STOP: {packet} already has {name}; that day has a run in progress.")
            return 1
    for sub in ("drafts", "evidence", "images"):
        os.makedirs(os.path.join(packet, sub), exist_ok=True)
    print(f"Packet folder: {packet}")

    snap_path = os.path.join(packet, "evidence", "existing-content.json")
    if os.path.exists(snap_path):
        with open(snap_path, encoding="utf-8") as fh:
            snap = json.load(fh)
        if not isinstance(snap, dict) or not {"articles", "events", "media"} <= set(snap):
            print(f"STOP: {snap_path} exists in another shape; move it aside and rerun.")
            return 1
        print(f"Snapshot: kept the existing one, taken {snap.get('taken')}")
    else:
        npx = shutil.which("npx")
        if not npx:
            print("npx not found: install Node, or take the snapshot by hand as SKILL.md describes.")
            return 2
        snap = {"taken": dt.datetime.now().isoformat(timespec="seconds"), "date": date.isoformat()}
        try:
            for key, sql in QUERIES.items():
                snap[key] = query(npx, sql)
        except (RuntimeError, ValueError, KeyError, IndexError) as e:
            print(f"Query failed. If there's no local database, run `npm run db:migrate:local` and retry.\n{e}")
            return 2
        with open(snap_path, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(snap, fh, ensure_ascii=False, indent=2)
        print(f"Snapshot: wrote {snap_path}")

    published = [a for a in snap["articles"] if a.get("status") == "published"]
    events = [e for e in snap["events"] if e.get("status") == "published"]
    print(f"Compared against: {len(published)} published stories, {len(events)} published events, {len(snap['media'])} library images")

    since = date - dt.timedelta(days=21)
    recent = [a for a in published if (d := day(a.get("published_at"))) and since <= d <= date]
    by_section = {s: 0 for s in sections(repo)}
    for a in recent:
        by_section[a.get("section")] = by_section.get(a.get("section"), 0) + 1
    print(f"\nPast 21 days ({since} to {date}): {len(recent)} stories")
    print("  By section: " + ", ".join(f"{s} {n}" for s, n in sorted(by_section.items(), key=lambda x: (-x[1], str(x[0])))))
    thin = [s for s, n in by_section.items() if n < 3]
    print("  Fewer than three (need stories most): " + (", ".join(thin) if thin else "none"))
    for a in recent:
        print(f"  {day(a['published_at'])}  {a.get('section')}  {a.get('slug')}  |  {a.get('headline')}")

    until = date + dt.timedelta(days=30)
    upcoming = [e for e in events if e.get("starts_on") and date.isoformat() <= e["starts_on"] <= until.isoformat()]
    print(f"\nEvents in the next 30 days (through {until}): {len(upcoming)}")
    for e in upcoming:
        print(f"  {e['starts_on']} {e.get('start_time') or '--:--'}  {e.get('community')}  {e.get('slug')}  |  {e.get('title')}")

    print("\nNewest library images:")
    for m in snap["media"][:8]:
        print(f"  {day(m.get('created_at'))}  {m.get('id')}  {m.get('filename')}  |  {(m.get('alt') or '')[:80]}")

    reviews = sorted(d for d in os.listdir(os.path.join(library, "editorial"))
                     if d < date.isoformat() and os.path.exists(os.path.join(library, "editorial", d, "review.md")))
    print("\nNewest earlier review.md: " + (os.path.join(library, "editorial", reviews[-1], "review.md") if reviews else "none"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
