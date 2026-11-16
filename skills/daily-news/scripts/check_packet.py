#!/usr/bin/env python3
"""Check a daily-news packet for the rules packet.mjs doesn't enforce.

Usage:
  check_packet.py PACKET_DIR      e.g. ../../Projects/firelands-current/editorial/2026-11-16

packet.mjs already validates the manifest's structure, keys, dates, times, `[NEED:` in story
bodies and the expect counts. This covers the skill's own rules:
  - every text file is valid UTF-8, with no mojibake (curly quotes written as "â€™")
  - story and event summaries are under 160 characters
  - each story body links a source inline
  - upload alt text is under 300 characters and doesn't repeat the caption
  - a reused library photo's caption ends "File photo."
  - no event is already over on the budget date
  - publish_window.until is the end of the budget date, and expect is set
  - weekday-and-date pairs ("Tuesday, Oct. 14") agree, in packet.json text and review.md
  - links in review.md to drafts and evidence resolve

Every hit is for you to judge and fix before going live. Standard library only.
Exit code: 0 with no hits, 1 with hits, 2 if the folder or packet.json can't be read.
"""

import argparse
import datetime as dt
import json
import os
import re
import sys
from urllib.parse import unquote

WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MONTH = r"(Jan(?:uary|\.)?|Feb(?:ruary|\.)?|March|Mar\.?|April|Apr\.?|May|June|Jun\.?|July|Jul\.?|Aug(?:ust|\.)?|Sept?(?:ember|\.)?|Oct(?:ober|\.)?|Nov(?:ember|\.)?|Dec(?:ember|\.)?)"
WEEKDAY_DATE = re.compile(rf"\b({'|'.join(WEEKDAYS)}),?\s+{MONTH}\s+(\d{{1,2}})(?:\s?[-–]\s?(\d{{1,2}}))?(?:,?\s+(\d{{4}}))?\b")
MOJIBAKE = re.compile("â€|Ã[\u0080-¿]|Â[ -¿ ]")


def weekday_errors(text, ref):
    out = []
    for m in WEEKDAY_DATE.finditer(text):
        month = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"].index(m.group(2)[:3].lower()) + 1
        days = [int(m.group(3))] + ([int(m.group(4))] if m.group(4) else [])
        years = [int(m.group(5))] if m.group(5) else [ref.year - 1, ref.year, ref.year + 1]
        try:
            year = min((y for y in years if _valid(y, month, days[0])), key=lambda y: abs((dt.date(y, month, days[0]) - ref).days))
            actual = [WEEKDAYS[dt.date(year, month, d).weekday()] for d in days]
        except ValueError:
            out.append((m.group(0), "not a real date"))
            continue
        if m.group(1) not in actual:
            out.append((m.group(0), f"{m.group(2)} {days[0]}, {year} is a {actual[0]}"))
    return out


def _valid(y, m, d):
    try:
        dt.date(y, m, d)
        return True
    except ValueError:
        return False


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("packet_dir")
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    root = os.path.abspath(args.packet_dir)
    hits = []
    add = lambda where, problem: hits.append((where, problem))

    texts = {}
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in ("evidence", "images")]
        for f in files:
            if f.endswith((".md", ".json")):
                path = os.path.join(dirpath, f)
                rel = os.path.relpath(path, root).replace(os.sep, "/")
                raw = open(path, "rb").read()
                try:
                    texts[rel] = raw.decode("utf-8-sig")
                except UnicodeDecodeError as e:
                    add(rel, f"not valid UTF-8 (byte {e.start}); rewrite it as UTF-8")
                    continue
                for m in list(MOJIBAKE.finditer(texts[rel]))[:3]:
                    line = texts[rel].count("\n", 0, m.start()) + 1
                    add(f"{rel}:{line}", f"mojibake {texts[rel][m.start():m.start() + 6]!r}: written with the wrong encoding")

    if "packet.json" not in texts:
        print(f"No readable packet.json in {root}.")
        return 2
    try:
        p = json.loads(texts["packet.json"])
        date = dt.date.fromisoformat(p["date"])
    except (ValueError, KeyError) as e:
        print(f"packet.json can't be read: {e}")
        return 2

    for s in p.get("stories", []):
        where = f"story {s.get('key')}"
        if len(s.get("summary") or "") >= 160:
            add(where, f"summary is {len(s['summary'])} characters; keep it under 160")
        if not re.search(r"\]\(https?://", s.get("body") or ""):
            add(where, "body has no inline source link")
        for field in ("headline", "summary", "body"):
            for found, note in weekday_errors(s.get(field) or "", date):
                add(f"{where} {field}", f"{found!r}: {note}")
    for e in p.get("events", []):
        where = f"event {e.get('key')}"
        if len(e.get("summary") or "") >= 160:
            add(where, f"summary is {len(e['summary'])} characters; keep it under 160")
        if (e.get("ends_on") or e.get("starts_on") or "9999") < date.isoformat():
            add(where, f"already over on {date} (starts {e.get('starts_on')})")
        for field in ("title", "summary", "description"):
            for found, note in weekday_errors(e.get(field) or "", date):
                add(f"{where} {field}", f"{found!r}: {note}")
    for u in p.get("updates", []):
        for field, value in (u.get("fields") or {}).items():
            for found, note in weekday_errors(value if isinstance(value, str) else "", date):
                add(f"update {u.get('slug')} {field}", f"{found!r}: {note}")
    for m in p.get("media", []):
        where = f"media {m.get('key')}"
        alt, caption = (m.get("alt") or "").strip(), (m.get("caption") or "").strip()
        if len(alt) >= 300:
            add(where, f"alt text is {len(alt)} characters; keep it under 300")
        if alt and caption and (alt.lower() in caption.lower() or caption.lower() in alt.lower()):
            add(where, "alt text repeats the caption")
        if m.get("action") == "reuse" and not caption.endswith("File photo."):
            add(where, "reused library photo: end the caption with \"File photo.\" unless it shows today's news")

    until = (p.get("publish_window") or {}).get("until")
    if not until:
        add("packet.json", "no publish_window.until; set it to the end of the budget date")
    else:
        try:
            t = dt.datetime.fromisoformat(until.replace("Z", "+00:00"))
            end = dt.datetime.combine(date + dt.timedelta(days=1), dt.time(0), t.tzinfo)
            if not (end - dt.timedelta(minutes=1) <= t <= end):
                add("packet.json", f"publish_window.until is {until}, not the end of {date}")
        except ValueError:
            add("packet.json", f"publish_window.until isn't a date-time: {until}")
    if not p.get("expect"):
        add("packet.json", "no expect counts; set them so a dropped item fails loudly")

    review = texts.get("review.md")
    if review is None:
        add("review.md", "missing")
    else:
        for found, note in weekday_errors(review, date):
            line = review.count("\n", 0, review.find(found)) + 1
            add(f"review.md:{line}", f"{found!r}: {note}")
        for m in re.finditer(r"\]\((?!https?:|mailto:|#)([^)\s]+)\)", review):
            target = unquote(m.group(1).split("#")[0])
            if target and not os.path.exists(os.path.join(root, target)):
                add(f"review.md:{review.count(chr(10), 0, m.start()) + 1}", f"link to {target} doesn't resolve")

    if not hits:
        print(f"No hits in {root}.")
        return 0
    for where, problem in hits:
        print(f"{where}: {problem}")
    print(f"\n{len(hits)} hit(s).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
