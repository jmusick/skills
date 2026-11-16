"""Read the job-search records: find postings already seen, list applications gone quiet, name new records.

Usage:
  python jobs.py match <jobs folder> [--company C] [--role R] [--url URL] [--job-id ID]
  python jobs.py match <jobs folder> --batch <file.json | ->
  python jobs.py due <jobs folder> [--days 14] [--today YYYY-MM-DD]
  python jobs.py list <jobs folder> [--status S ...]
  python jobs.py slug --company C --role R

--batch takes a JSON list of postings, each an object with any of company, role,
url, job_id, and checks them all in one pass.

Prints JSON. Reads only; never writes to the folder. Files it can't parse are listed
under `unreadable_records`: check those by hand, since one may be the posting.
Records are the `<company>-<role>.md` files with YAML-style front matter; anything
without front matter or a `company` field is skipped.
"""

import argparse
import datetime as dt
import json
import os
import re
import sys

FIELDS = ("company", "role", "status", "fit", "url", "board_url", "job_id", "location", "pay",
          "source", "found", "applied", "updated", "follow_ups")
ACTIVE = ("applied", "interviewing")
COMPANY_NOISE = {"the", "and", "llc", "inc", "co", "company", "corp", "corporation", "ltd", "group",
                 "holdings", "of", "us", "usa", "na"}
ROLE_NOISE = {"the", "and", "of", "a", "an", "for", "to", "in", "i", "ii", "iii", "iv", "remote",
              "hybrid", "onsite", "on", "site", "us", "usa", "fulltime", "full", "time"}
# Query parameters that identify a posting; every other parameter is tracking noise.
ID_PARAMS = ("jk", "currentjobid", "gh_jid", "jobid", "job_id", "id", "lever-source", "req", "reqid")


def read_front_matter(path):
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except (OSError, UnicodeDecodeError):
        return None
    m = re.match(r"---\s*\n(.*?)\n---", text, re.S)
    if not m:
        return None
    data = {}
    for line in m.group(1).splitlines():
        if ":" not in line or line.lstrip().startswith("#"):
            continue
        key, value = line.split(":", 1)
        value = re.sub(r"\s+#.*$", "", value).strip().strip("\"'")
        data[key.strip()] = None if value.lower() in ("", "null", "none", "~") else value
    return data


def load(folder):
    if not os.path.isdir(folder):
        sys.exit(f"No jobs folder at {folder}")
    records, skipped = [], []
    for name in sorted(os.listdir(folder)):
        if not name.endswith(".md") or name.lower() == "readme.md":
            continue
        data = read_front_matter(os.path.join(folder, name))
        if data and data.get("company"):
            rec = {k: data.get(k) for k in FIELDS}
            rec["file"] = name
            records.append(rec)
        else:
            skipped.append(name)
    return records, skipped


def norm_url(url):
    """Lowercase host and path without scheme, www, trailing slash, or tracking parameters."""
    if not url:
        return None
    url = url.strip().lower()
    url = re.sub(r"^[a-z]+://", "", url)
    url = re.sub(r"^(www\.|m\.)", "", url)
    path, _, query = url.partition("?")
    path = path.split("#")[0].rstrip("/")
    keep = sorted(p for p in query.split("&") if p.split("=")[0] in ID_PARAMS)
    return path + ("?" + "&".join(keep) if keep else "") or None


def job_ids(url):
    """Board job IDs a URL carries, as `board:id` strings."""
    if not url:
        return set()
    u = url.lower()
    ids = set()
    for pattern, board in ((r"linkedin\.com/jobs/view/(?:[^/?#]*-)?(\d{6,})", "linkedin"),
                           (r"[?&]currentjobid=(\d{6,})", "linkedin"),
                           (r"indeed\.com/.*[?&]jk=([0-9a-f]{10,})", "indeed"),
                           (r"[?&]gh_jid=(\d+)", "greenhouse"),
                           (r"greenhouse\.io/[^/]+/jobs/(\d+)", "greenhouse"),
                           (r"lever\.co/[^/]+/([0-9a-f-]{36})", "lever")):
        ids.update(f"{board}:{m}" for m in re.findall(pattern, u))
    return ids


def norm_id(job_id):
    return (job_id or "").strip().lower() or None


ROLE_ALIASES = {"sr": "senior", "jr": "junior", "mgr": "manager", "eng": "engineer", "dev": "developer"}


def tokens(text, noise):
    words = re.findall(r"[a-z0-9]+", (text or "").lower().replace("'s", "").replace("full-stack", "fullstack"))
    return {ROLE_ALIASES.get(w, w) for w in words if w not in noise}


def same_company(a, b):
    ta, tb = tokens(a, COMPANY_NOISE), tokens(b, COMPANY_NOISE)
    return bool(ta and tb) and (ta <= tb or tb <= ta)


def similar_role(a, b):
    ta, tb = tokens(a, ROLE_NOISE), tokens(b, ROLE_NOISE)
    if not ta or not tb:
        return False
    return len(ta & tb) / len(ta | tb) >= 0.6


POSTING_KEYS = ("company", "role", "url", "job_id")
# What a match reports: enough to find the record and decide whether to drop the posting.
# The agent opens the file when it needs more, so the rest of the front matter is noise.
SUMMARY = ("file", "company", "role", "status", "applied", "updated")


def match(records, posting):
    url = norm_url(posting.get("url"))
    ids = job_ids(posting.get("url"))
    if posting.get("job_id"):
        ids.add(norm_id(posting["job_id"]))
    hits, company_history = [], []
    for rec in records:
        why = []
        rec_urls = {norm_url(rec["url"]), norm_url(rec["board_url"])} - {None}
        rec_ids = job_ids(rec["url"]) | job_ids(rec["board_url"])
        if rec["job_id"]:
            rec_ids.add(norm_id(rec["job_id"]))
        if url and url in rec_urls:
            why.append("url")
        if ids & rec_ids:
            why.append("job id")
        company = posting.get("company") and same_company(posting["company"], rec["company"])
        if company and posting.get("role") and similar_role(posting["role"], rec["role"]):
            why.append("same company, similar role")
        if why:
            hits.append({**{k: rec[k] for k in SUMMARY}, "matched_on": why})
        elif company:
            company_history.append({k: rec[k] for k in SUMMARY if k != "company"})
    # Other records at the same employer: a recent rejection or a live application there
    # changes whether this posting is worth showing.
    return {"matches": hits, "same_company": company_history}


def label(posting):
    """Name a batch posting in the output by company and role, falling back to its URL or ID."""
    named = {k: posting[k] for k in ("company", "role") if posting[k]}
    return named or {k: posting[k] for k in ("url", "job_id") if posting[k]}


def read_batch(source):
    try:
        if source == "-":
            raw = sys.stdin.buffer.read().decode("utf-8-sig")
        else:
            with open(source, encoding="utf-8-sig") as f:
                raw = f.read()
        data = json.loads(raw)
    except (OSError, UnicodeDecodeError, ValueError) as e:
        sys.exit(f"Can't read the --batch postings: {e}")
    if isinstance(data, dict):
        data = [data]
    if not isinstance(data, list) or not all(isinstance(c, dict) for c in data):
        sys.exit("--batch needs a JSON list of posting objects")
    postings = [{k: (str(c[k]) if c.get(k) is not None else None) for k in POSTING_KEYS} for c in data]
    empty = [i for i, c in enumerate(postings) if not (c["url"] or c["job_id"] or c["company"])]
    if empty:
        sys.exit(f"--batch postings at positions {empty} have no url, job_id, or company")
    return postings


def due(records, days, today):
    cutoff = today - dt.timedelta(days=days)
    out, unreadable = [], []
    for rec in records:
        if (rec["status"] or "").lower() not in ACTIVE:
            continue
        try:
            last = dt.date.fromisoformat(rec["updated"] or rec["applied"] or "")
        except ValueError:
            unreadable.append(rec["file"])
            continue
        if last <= cutoff:
            out.append({**rec, "days_quiet": (today - last).days})
    out.sort(key=lambda r: -r["days_quiet"])
    return {"today": today.isoformat(), "quiet": out, "unreadable_dates": unreadable}


def listing(records, statuses):
    want = {s.lower() for s in statuses or ()}
    rows = [{k: r[k] for k in ("file", "company", "role", "status", "fit", "pay", "applied", "updated")}
            for r in records if not want or (r["status"] or "").lower() in want]
    counts = {}
    for r in records:
        counts[r["status"] or "(none)"] = counts.get(r["status"] or "(none)", 0) + 1
    return {"records": rows, "status_counts": dict(sorted(counts.items()))}


def slug(company, role):
    def part(text, noise):
        words = re.findall(r"[a-z0-9]+", (text or "").lower().replace("'s", "s").replace("&", " and "))
        return [w for w in words if w not in noise]
    words = part(company, {"llc", "inc", "corp", "corporation", "ltd", "co"}) + part(role, set())
    name = "-".join(words)[:80].rstrip("-")
    if not name:
        sys.exit("slug needs a company or role with letters or digits in it")
    return {"file": f"{name}.md", "folder": name}


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("match")
    m.add_argument("folder")
    for key in POSTING_KEYS:
        m.add_argument(f"--{key.replace('_', '-')}", dest=key)
    m.add_argument("--batch", metavar="FILE", help="JSON list of postings; - reads stdin")
    d = sub.add_parser("due")
    d.add_argument("folder")
    d.add_argument("--days", type=int, default=14)
    d.add_argument("--today", type=dt.date.fromisoformat, default=dt.date.today())
    li = sub.add_parser("list")
    li.add_argument("folder")
    li.add_argument("--status", nargs="*")
    s = sub.add_parser("slug")
    s.add_argument("--company", required=True)
    s.add_argument("--role", required=True)
    args = p.parse_args()

    if args.cmd == "slug":
        print(json.dumps(slug(args.company, args.role), indent=2))
        return
    records, skipped = load(args.folder)
    if args.cmd == "match":
        posting = {k: getattr(args, k) for k in POSTING_KEYS}
        if args.batch:
            if any(posting.values()):
                p.error("use --batch or the single-posting flags, not both")
            result = {"results": [{"posting": label(c), **match(records, c)} for c in read_batch(args.batch)]}
        elif posting["url"] or posting["job_id"] or posting["company"]:
            result = match(records, posting)
        else:
            p.error("match needs --batch or at least one of --url, --job-id, --company")
    elif args.cmd == "due":
        result = due(records, args.days, args.today)
    else:
        result = listing(records, args.status)
    if skipped:
        # A record the script can't read could hide a posting already seen.
        result["unreadable_records"] = skipped
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
