"""Read the prospect outreach folder: find existing records, count towns, list follow-ups due.

Usage:
  python outreach.py match <folder> [--name N] [--website URL] [--phone P] [--facebook URL] [--email E]
  python outreach.py match <folder> --batch <file.json | ->
  python outreach.py towns <folder>
  python outreach.py due <folder> [--days 7] [--today YYYY-MM-DD]

--batch takes a JSON list of candidates, each an object with any of name, website,
phone, facebook, email, and checks them all in one pass.

Prints JSON. Reads only; never writes to the folder. Files it can't parse are listed
under `unreadable_records`: check those by hand, since one may be the business.
Records are the `<town>-<business-slug>.md` files with YAML-style front matter;
sender.md and anything without front matter are skipped.
"""

import argparse
import datetime as dt
import json
import os
import re
import sys

FIELDS = ("business", "town", "website", "facebook", "email", "phone", "status", "channel", "first_contact")
NAME_NOISE = {"the", "and", "llc", "inc", "co", "company", "corp", "ltd", "of", "shop", "store"}


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
        sys.exit(f"No outreach folder at {folder}")
    records, skipped = [], []
    for name in sorted(os.listdir(folder)):
        if not name.endswith(".md") or name.lower() == "sender.md":
            continue
        data = read_front_matter(os.path.join(folder, name))
        if data and data.get("business"):
            rec = {k: data.get(k) for k in FIELDS}
            rec["file"] = name
            records.append(rec)
        else:
            skipped.append(name)
    return records, skipped


def norm_domain(url):
    if not url:
        return None
    url = url.lower().strip()
    url = re.sub(r"^[a-z]+://", "", url)
    url = re.sub(r"^(www\.|m\.)", "", url)
    return url.split("/")[0].split("?")[0] or None


def norm_facebook(url):
    if not url:
        return None
    url = url.lower().strip()
    url = re.sub(r"^[a-z]+://", "", url)
    url = re.sub(r"^(www\.|m\.|web\.)", "", url)
    path, _, query = url.partition("?")
    page_id = re.search(r"(?:^|&)id=(\d+)", query)
    if "profile.php" in path and page_id:
        return f"{path.rstrip('/')}?id={page_id.group(1)}"
    return path.rstrip("/") or None


def norm_phone(phone):
    digits = re.sub(r"\D", "", phone or "")
    return digits[-10:] if len(digits) >= 10 else None


def name_tokens(name):
    words = re.findall(r"[a-z0-9]+", (name or "").lower().replace("'s", ""))
    return {w for w in words if w not in NAME_NOISE}


CANDIDATE_KEYS = ("name", "website", "phone", "facebook", "email")


def match(records, cand):
    want = {
        "website": norm_domain(cand.get("website")),
        "facebook": norm_facebook(cand.get("facebook")),
        "phone": norm_phone(cand.get("phone")),
        "email": (cand.get("email") or "").lower().strip() or None,
    }
    want_domain_from_email = want["email"].split("@")[-1] if want["email"] else None
    tokens = name_tokens(cand.get("name"))
    hits = []
    for rec in records:
        why = []
        rec_domain = norm_domain(rec["website"])
        if want["website"] and want["website"] == rec_domain:
            why.append("website")
        if want_domain_from_email and want_domain_from_email == rec_domain:
            why.append("email domain matches website")
        if want["facebook"] and want["facebook"] == norm_facebook(rec["facebook"]):
            why.append("facebook")
        if want["phone"] and want["phone"] == norm_phone(rec["phone"]):
            why.append("phone")
        if want["email"] and want["email"] == (rec["email"] or "").lower():
            why.append("email")
        rec_tokens = name_tokens(rec["business"])
        if tokens and rec_tokens:
            overlap = len(tokens & rec_tokens) / len(tokens | rec_tokens)
            if overlap >= 0.5 or tokens <= rec_tokens or rec_tokens <= tokens:
                why.append("similar name")
        if why:
            hits.append({**rec, "matched_on": why})
    return {"matches": hits}


def read_batch(source):
    try:
        if source == "-":
            raw = sys.stdin.buffer.read().decode("utf-8-sig")
        else:
            with open(source, encoding="utf-8-sig") as f:
                raw = f.read()
        data = json.loads(raw)
    except (OSError, UnicodeDecodeError, ValueError) as e:
        sys.exit(f"Can't read the --batch candidates: {e}")
    if isinstance(data, dict):
        data = [data]
    if not isinstance(data, list) or not all(isinstance(c, dict) for c in data):
        sys.exit("--batch needs a JSON list of candidate objects")
    cands = [{k: (str(c[k]) if c.get(k) is not None else None) for k in CANDIDATE_KEYS} for c in data]
    empty = [i for i, c in enumerate(cands) if not any(c.values())]
    if empty:
        sys.exit(f"--batch candidates at positions {empty} have none of {', '.join(CANDIDATE_KEYS)}")
    return cands


def towns(records):
    counts = {}
    for rec in records:
        town = rec["town"] or "(no town)"
        counts[town] = counts.get(town, 0) + 1
    return {"records_per_town": dict(sorted(counts.items(), key=lambda kv: (kv[1], kv[0])))}


def due(records, days, today):
    cutoff = today - dt.timedelta(days=days)
    out, unreadable = [], []
    for rec in records:
        if (rec["status"] or "").lower() != "sent":
            continue
        try:
            sent = dt.date.fromisoformat(rec["first_contact"] or "")
        except ValueError:
            unreadable.append(rec["file"])
            continue
        if sent <= cutoff:
            out.append({**rec, "days_since": (today - sent).days})
    out.sort(key=lambda r: r["first_contact"])
    return {"today": today.isoformat(), "due": out, "unreadable_first_contact": unreadable}


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("towns").add_argument("folder")
    m = sub.add_parser("match")
    m.add_argument("folder")
    for key in CANDIDATE_KEYS:
        m.add_argument(f"--{key}")
    m.add_argument("--batch", metavar="FILE", help="JSON list of candidates; - reads stdin")
    d = sub.add_parser("due")
    d.add_argument("folder")
    d.add_argument("--days", type=int, default=7)
    d.add_argument("--today", type=dt.date.fromisoformat, default=dt.date.today())
    args = p.parse_args()

    records, skipped = load(args.folder)
    if args.cmd == "match":
        cand = {k: getattr(args, k) for k in CANDIDATE_KEYS}
        if args.batch:
            if any(cand.values()):
                p.error("use --batch or the single-candidate flags, not both")
            result = {"results": [{"candidate": c, **match(records, c)} for c in read_batch(args.batch)]}
        elif any(cand.values()):
            result = match(records, cand)
        else:
            p.error("match needs --batch or at least one of --name, --website, --phone, --facebook, --email")
    elif args.cmd == "towns":
        result = towns(records)
    else:
        result = due(records, args.days, args.today)
    if skipped:
        # A record the script can't read could hide a business already contacted.
        result["unreadable_records"] = skipped
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
