"""Check a drafted first message before Justin sees it.

Usage:
  python check_message.py <message file> --channel email|form|facebook [--follow-up]

The file holds the message as it will be sent. For email, put the subject on the
first line as `Subject: ...`. The sign-off starts at the line naming Justin Musick
(plus a short closing line such as "Thanks," just above it); everything above it
is the body that gets counted.

Prints JSON with the body word count and any issues, and exits 1 if there are
issues. Heuristic checks (opt-out line, postal address) are warnings to confirm
by eye, not proof.
"""

import argparse
import json
import re
import sys

RANGES = {"email": (75, 125), "form": (75, 125), "facebook": (60, 100)}
FOLLOW_UP_RANGE = (40, 80)
URL = re.compile(r"(https?://|www\.)\S+", re.I)
EMAIL = re.compile(r"\b[\w.+-]+@[\w-]+(\.[\w-]+)+\b")
DOMAIN = re.compile(r"\b[a-z0-9][a-z0-9-]*(\.[a-z0-9-]+)*\.(com|net|org|biz|info|co|us|io|site|online|shop|store|business|app|dev|me|ai)\b", re.I)
PHONE = re.compile(r"\(?\b\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b")
OPT_OUT = re.compile(r"won'?t (reach out|contact|follow up|message|bother|write)|not (useful|interested|a fit)|let me know and I|no worries|stop (reaching|contacting)", re.I)
POSTAL = re.compile(r"P\.?\s?O\.?\s+Box|\b\d{5}(-\d{4})?\b", re.I)


def split(text):
    lines = text.strip().splitlines()
    subject = None
    if lines and lines[0].lower().startswith("subject:"):
        subject = lines[0].split(":", 1)[1].strip()
        lines = lines[1:]
    start = None
    for i in range(len(lines) - 1, -1, -1):
        if "justin musick" in lines[i].lower():
            start = i
            break
    if start is None:
        return subject, "\n".join(lines), ""
    j = start - 1
    while j >= 0 and not lines[j].strip():
        j -= 1
    if j >= 0 and len(lines[j].split()) <= 3 and lines[j].rstrip().endswith((",", "-", "—")):
        start = j
    return subject, "\n".join(lines[:start]).strip(), "\n".join(lines[start:]).strip()


def check(text, channel, follow_up):
    subject, body, signoff = split(text)
    issues, warnings = [], []
    # Count like `wc -w`, skipping lone dashes, so "$85,000" is one word.
    words = sum(1 for token in body.split() if re.search(r"\w", token))
    low, high = FOLLOW_UP_RANGE if follow_up else RANGES[channel]
    if not low <= words <= high:
        issues.append(f"body is {words} words; keep it to {low}-{high}")

    links = []
    for label, rx in (("URL", URL), ("email address", EMAIL), ("bare domain", DOMAIN)):
        found = sorted({m.group(0) for m in rx.finditer(text)})
        if label == "bare domain":
            # Skip domains that are part of a URL or email address already found.
            found = [d for d in found if not any(d in other for other in links)]
        links += found
        if found and not follow_up:
            issues.append(f"{label} in a first message: {', '.join(found)}")
    if follow_up and len(links) > 1:
        issues.append(f"a follow-up may carry one link at most; found {', '.join(links)}")
    if PHONE.search(body):
        issues.append("phone number in the body; give it once, in the sign-off")

    if not signoff:
        issues.append("no sign-off found (expected a line with 'Justin Musick')")
    else:
        for needed in ("Stone Dragon Media",):
            if needed.lower() not in signoff.lower():
                issues.append(f"sign-off is missing '{needed}'")
        if not PHONE.search(signoff):
            issues.append("sign-off has no phone number")
        if channel == "email" and not POSTAL.search(signoff):
            warnings.append("couldn't find a postal address in the sign-off (CAN-SPAM needs one in email)")
    if not OPT_OUT.search(body):
        warnings.append("couldn't find an opt-out line; confirm one is there")

    if channel == "email":
        if not subject:
            issues.append("no subject line (put 'Subject: ...' on the first line)")
        else:
            if re.match(r"(re|fwd?):", subject, re.I):
                issues.append("subject starts with Re:/Fwd:, which is misleading")
            n = len(subject.split())
            if not 2 <= n <= 6:
                issues.append(f"subject is {n} words; keep it to 2-6")

    return {
        "channel": channel,
        "follow_up": follow_up,
        "subject": subject,
        "body_words": words,
        "range": [low, high],
        "issues": issues,
        "warnings": warnings,
        "ok": not issues,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("file")
    p.add_argument("--channel", required=True, choices=sorted(RANGES))
    p.add_argument("--follow-up", action="store_true", help="40-80 words, and one link is allowed")
    args = p.parse_args()
    try:
        with open(args.file, encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        sys.exit(f"Can't read {args.file}: {e}")
    result = check(text, args.channel, args.follow_up)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
