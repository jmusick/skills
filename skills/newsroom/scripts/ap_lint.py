#!/usr/bin/env python3
"""Flag the mechanical AP slips and date errors in news copy.

Usage:
  ap_lint.py FILE [--date YYYY-MM-DD]     lint a story file (or newsroom's whole output)
  ap_lint.py - [--date YYYY-MM-DD]        lint text from stdin

--date is the publication date (default today). It sets the year for a weekday-and-date pair
like "Tuesday, Oct. 14" that gives none: the nearest such date to it.

If the text has newsroom's sections ("Headlines", "Story", "Notes", "Flags", and a "Summary" if
one was added, as bold labels or headings), the story rules run on the Story section and the headline rules on Headlines.
Otherwise everything is treated as story copy.

Checks: weekday/date mismatches, date and month style, times, percent, numerals, word choice
and loaded words, dash rate, state and street abbreviations, lede length, paragraph length,
unclosed quotes, and headline form. Word-choice hits inside quotation marks are skipped,
because quotes stay verbatim.

Every hit is a lead to judge, not a correction to apply: the script can't read context (a
workplace accident is an accident; "5 points" may be a score). House style overrides AP.
Standard library only.
"""

import argparse
import datetime as dt
import re
import sys

WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MONTHS = {"jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6, "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12}
MONTH = r"(?:Jan(?:uary|\.)?|Feb(?:ruary|\.)?|March|Mar\.?|April|Apr\.?|May|June|Jun\.?|July|Jul\.?|Aug(?:ust|\.)?|Sept?(?:ember|\.)?|Oct(?:ober|\.)?|Nov(?:ember|\.)?|Dec(?:ember|\.)?)"
STATES = "AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY".split()
SENTENCE_START = r"(?:^|(?<=[.!?]\s)|(?<=[.!?][\"”'’)]\s))"

WORDS = [  # (pattern, suggestion); skipped inside quotes
    (r"\bpled\b", "pleaded"),
    (r"\bin excess of\b", "more than"),
    (r"\baccidents?\b", "crash, if it's a vehicle"),
    (r"\belderly\b", "give the age"),
    (r"\bpro-(?:life|choice)\b", "anti-abortion / abortion-rights"),
    (r"\bcommitted suicide\b", "died by suicide"),
    (r"\b(?:slammed|blasted|lashed out|ripped|torched)\b", "neutral verb, or put it in a quote"),
    (r"\b(?:claimed|admitted|stated|exclaimed|noted|explained)\b", "said, unless the judgment is the point"),
    (r"\b(?:clearly|obviously|unfortunately|fortunately|sadly|shocking|controversial|tragic)\b", "editorializing: cut or attribute"),
    (r"\b(?:bustling|nestled|close-knit|hidden gem|came together|packed house|heated debate|sparked outrage|tight-knit)\b", "cliché: give the fact (count, what was said)"),
    (r"\b(?:pivotal|crucial|testament|landmark|game-chang\w*)\b", "significance inflation"),
    (r"\bhistoric\b", "only if it's a first"),
    (r"\b(?:it'?s worth noting|it should be noted|only time will tell|in other business)\b", "cut"),
    (r"\bnot (?:just|only|merely) [^.;:!?]{1,50}? but\b", "staged contrast: state the point"),
    (r",\s(?:highlighting|underscoring|showcasing|reflecting|signaling|fostering)\b", "-ing tail: cut it or state the consequence"),
    (r"\balleged (?:suspect|thief|killer|murderer|robber|shooter|attacker|rapist|abuser)\b", "attach alleged to the act, not the person"),
    (r"\bmurder(?:ed|s)?\b", "homicide/killed, until there's a murder conviction"),
    (r"\btowards\b", "toward"),
]
NUM_SKIP_BEFORE = re.compile(MONTH + r"\s$|(?:No\.|Route|Zone|Ward|District|Precinct|Room|Suite|Unit|Exit|Channel|Chapter|Page|Section|Issue|Highway|Interstate|SR|Level|Phase|Grade|Title|Article|Item|Lot|Building|Box|Station|Lane|Court|Division|Category|Class|Region|Step|Game|Week|Round|Act|Part|ages?|aged)\s$", re.I)
ABBREV_BEFORE = re.compile(r"\b(?:Jan|Feb|Aug|Sept?|Oct|Nov|Dec|No|St|Ave|Blvd|Mr|Mrs|Ms|Dr|Jr|Sr|Gov|Sen|Rep|Lt|Sgt|Capt|a\.m|p\.m|U\.S)\.\s$")
NUM_SKIP_AFTER = re.compile(r"(?:a\.m\.|p\.m\.|%|percent|percentage|million|billion|trillion|years? old|months? old|feet|foot|inch(?:es)?|miles?|mph|pounds?|degrees?|yards?|meters?|ounces?|tons?|points?|votes?|pages?\)|to \d|-\d|p\.m|a\.m)", re.I)


def blank(match):
    return re.sub(r"[^\n]", " ", match.group(0))


def clean(text):
    text = re.sub(r"\A---\n.*?\n---\n", blank, text, flags=re.S)
    text = re.sub(r"^(\s{0,3})(`{3,}|~{3,}).*?^\s{0,3}\2[^\n]*$", blank, text, flags=re.S | re.M)
    text = re.sub(r"\]\([^)\s]+\)", lambda m: "]" + " " * (len(m.group(0)) - 1), text)
    return re.sub(r"https?://\S+", blank, text)


def quote_mask(text):
    inside, mask, prev = False, [], ""
    for ch in text:
        if ch == "\n" and prev == "\n":
            inside = False
        if ch == "“":
            inside = True
        elif ch == "”":
            inside = False
        elif ch == '"':
            inside = not inside
        mask.append(inside)
        prev = ch
    return mask


def sections(text):
    """Return {name: (start, end)} for newsroom's labeled sections, or {} if none."""
    label = re.compile(r"^\s*(?:#{1,6}\s*|\*\*)?(Headlines?|Summary|Story|Notes|Flags)\s*:?\s*(?:\*\*)?\s*:?\s*$", re.I | re.M)
    marks = [(m.group(1).lower().rstrip("s") if m.group(1).lower().startswith("headline") else m.group(1).lower(), m.start(), m.end()) for m in label.finditer(text)]
    out = {}
    for i, (name, _, end) in enumerate(marks):
        out[name] = (end, marks[i + 1][1] if i + 1 < len(marks) else len(text))
    return out


def resolve_year(month, day, year, ref):
    if year:
        return int(year)
    best = None
    for y in (ref.year - 1, ref.year, ref.year + 1):
        try:
            d = dt.date(y, month, day)
        except ValueError:
            continue
        if best is None or abs((d - ref).days) < abs((dt.date(best, month, day) - ref).days):
            best = y
    return best


class Linter:
    def __init__(self, text, ref):
        self.text, self.ref = text, ref
        self.mask = quote_mask(text)
        self.starts = [0] + [m.end() for m in re.finditer(r"\n", text)]
        self.hits = []

    def line(self, pos):
        return sum(1 for s in self.starts if s <= pos)

    def add(self, pos, rule, found, note):
        self.hits.append((pos, rule, re.sub(r"\s+", " ", found).strip(), note))

    def scan(self, pattern, rule, note, lo, hi, flags=0, skip_quoted=False):
        for m in re.compile(pattern, flags | re.M).finditer(self.text, lo, hi):
            if skip_quoted and self.mask[m.start()]:
                continue
            self.add(m.start(), rule, m.group(0), note(m) if callable(note) else note)

    def story(self, lo, hi):
        t = self.text
        # Weekday against date.
        for m in re.finditer(rf"\b({'|'.join(WEEKDAYS)}),?\s+({MONTH})\s+(\d{{1,2}})(?:\s?[-–]\s?(\d{{1,2}}))?(?:,?\s+(\d{{4}}))?\b", t[:hi]):
            if m.start() < lo:
                continue
            month = MONTHS[m.group(2)[:3].lower()]
            days = [int(m.group(3))] + ([int(m.group(4))] if m.group(4) else [])
            year = resolve_year(month, days[0], m.group(5), self.ref)
            try:
                actual = [WEEKDAYS[dt.date(year, month, d).weekday()] for d in days]
            except (ValueError, TypeError):
                self.add(m.start(), "DATE", m.group(0), "not a real date")
                continue
            if m.group(1) not in actual:  # a range ("Saturday and Sunday, Nov. 21-22") may name either end
                self.add(m.start(), "WEEKDAY", m.group(0), f"{m.group(2)} {m.group(3)}, {year} is a {actual[0]}")
        # Months.
        self.scan(r"\b(?:January|February|August|September|October|November|December)\s+\d{1,2}\b", "MONTH",
                  lambda m: "abbreviate with a day: " + {"Sep": "Sept."}.get(m.group(0)[:3], m.group(0)[:3] + ".") + m.group(0)[m.group(0).find(" "):], lo, hi)
        self.scan(r"\b(?:Mar|Apr|Jun|Jul)\.?\s+\d|\bMay\.\s+\d", "MONTH", "spell out March through July", lo, hi)
        self.scan(r"\b(?:Jan|Feb|Aug|Oct|Nov|Dec)(?![.a-z])\s+\d{1,2}\b", "MONTH", "abbreviation takes a period", lo, hi)
        self.scan(r"\bSep\.?\s+\d", "MONTH", "Sept.", lo, hi)
        self.scan(rf"\b{MONTH}\s+\d{{1,2}}(?:st|nd|rd|th)\b", "MONTH", "no ordinal: Oct. 14", lo, hi)
        # Times.
        self.scan(r"\b\d{1,2}:00\s*(?:a\.?m\.?|p\.?m\.?)", "TIME", "drop :00 (7 p.m.)", lo, hi, re.I)
        self.scan(r"\b\d{1,2}(?::\d\d)?\s?(?:AM|PM|A\.M\.|P\.M\.|am|pm)(?![\w.])", "TIME", "a.m. / p.m.", lo, hi)
        self.scan(r"\b12(?::00)?\s?(?:p\.?m\.?)", "TIME", "noon", lo, hi, re.I)
        self.scan(r"\b12(?::00)?\s?(?:a\.?m\.?)", "TIME", "midnight", lo, hi, re.I)
        # Percent and numbers.
        self.scan(r"\d+(?:\.\d+)?\s?(?:percent|per cent)\b", "PERCENT", "use % (5%)", lo, hi, re.I)
        self.scan(r"\d\s%", "PERCENT", "no space before %", lo, hi)
        for m in re.finditer(SENTENCE_START + r"(?![12]\d{3}\b)\d[\d,.]*\s", t[:hi], re.M):
            if m.start() >= lo and not ABBREV_BEFORE.search(t[max(0, m.start() - 8):m.start()]):
                self.add(m.start(), "NUMBER", m.group(0), "spell out a number that starts a sentence")
        for m in re.finditer(r"(?<![\d$.,:/#\-–])\b([1-9])\b(?![\d.,:/%\-–])\s+(\S+(?:\s\S+)?)", t[:hi]):
            if m.start() < lo or NUM_SKIP_BEFORE.search(t[max(0, m.start() - 15):m.start()]) or NUM_SKIP_AFTER.match(m.group(2)):
                continue
            self.add(m.start(), "NUMBER", m.group(0), "spell out one through nine, unless it's an age, money, time, address, vote, dimension or score")
        # Word choice and voice (quotes are verbatim).
        for pattern, note in WORDS:
            self.scan(pattern, "WORD", note, lo, hi, re.I, skip_quoted=True)
        # States and streets.
        self.scan(rf",\s({'|'.join(STATES)})\b(?![-\d])", "STATE", "spell out state names in body text", lo, hi)
        self.scan(r"\bRd\.|\b[A-Z][a-z]+\sDr\.(?=[\s,]|$)", "STREET", "never abbreviate Road or Drive", lo, hi)
        self.scan(r"\b\d+\s(?:[NSEW]\.\s)?(?:[A-Z][\w']*\s){1,3}(?:Street|Avenue|Boulevard)\b", "STREET", "abbreviate St., Ave., Blvd. with a numbered address", lo, hi)
        for m in re.finditer(r"\b((?:[A-Z][\w']*\s){1,3})(St|Ave|Blvd)\.", t[:hi]):
            if m.start() >= lo and not re.search(r"\d+\s(?:[NSEW]\.\s)?$", t[max(0, m.start() - 12):m.start()]):
                self.add(m.start(), "STREET", m.group(0), "spell out without a numbered address")
        # Dashes.
        words = len(re.findall(r"[A-Za-z0-9’']+", t[lo:hi]))
        dashes = [m.start() for m in re.finditer("—| -- ", t[lo:hi])]
        if dashes and len(dashes) > max(1, words // 1000):
            self.add(lo + dashes[1 if len(dashes) > 1 else 0], "DASH", f"{len(dashes)} dashes in {words} words", "at most one per 1,000 words")
        # Lede, paragraphs, quotes.
        paras = [(m.start(), m.group(0)) for m in re.finditer(r"[^\n]+(?:\n(?!\s*\n)[^\n]+)*", t[lo:hi])]
        paras = [(lo + s, p) for s, p in paras if p.strip() and not re.match(r"\s*(?:#|[-*]\s|\*\*\w)", p)]
        for i, (start, para) in enumerate(paras):
            sents = [s for s in re.split(r"(?<=[.!?])[\"”']?\s+(?=[\"“]?[A-Z0-9])", para.strip()) if s]
            if i == 0 and sents:
                n = len(sents[0].split())
                if n > 35:
                    self.add(start, "LEDE", sents[0][:60] + "...", f"{n} words; keep the lede to 35 or fewer")
                if re.match(r"[\"“]", sents[0]) or sents[0].rstrip().endswith("?"):
                    self.add(start, "LEDE", sents[0][:60], "no quote or question ledes")
            if len(sents) > 3:
                self.add(start, "PARAGRAPH", para.strip()[:50] + "...", f"{len(sents)} sentences; keep to one to three")
            opens = para.count('"') % 2 == 1 or para.count("“") > para.count("”")
            next_opens = i + 1 < len(paras) and re.match(r"\s*[\"“]", paras[i + 1][1])
            if opens and not next_opens:
                self.add(start, "QUOTE", para.strip()[:50] + "...", "unclosed quotation mark")

    def headlines(self, lo, hi):
        for m in re.finditer(r"^\s*(?:[-*]|\d+[.)])?\s*(.+?)\s*$", self.text[lo:hi], re.M):
            h, pos = m.group(1).strip("*_ "), lo + m.start(1)
            if not h:
                continue
            if '"' in h or "“" in h:
                self.add(pos, "HEADLINE", h, "single quotation marks in headlines")
            if re.search(r"[.?]$", h):
                self.add(pos, "HEADLINE", h, "no period or question mark")
            ws = [w for w in h.split() if w[:1].isalpha()]
            if len(ws) >= 4 and sum(w[0].isupper() for w in ws[1:]) >= len(ws[1:]) - 1:
                self.add(pos, "HEADLINE", h, "sentence case")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("file", help="file to lint, or - for stdin")
    ap.add_argument("--date", help="publication date, YYYY-MM-DD (default today)")
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    ref = dt.date.fromisoformat(args.date) if args.date else dt.date.today()
    raw = sys.stdin.buffer.read() if args.file == "-" else open(args.file, "rb").read()
    text = clean(raw.decode("utf-8-sig", errors="replace").replace("\r\n", "\n"))

    lint = Linter(text, ref)
    parts = sections(text)
    if "story" in parts:
        lint.story(*parts["story"])
        if "headline" in parts:
            lint.headlines(*parts["headline"])
        scope = "the Story section" + (" and Headlines" if "headline" in parts else "")
    else:
        lint.story(0, len(text))
        scope = "the whole text"

    seen, unique = set(), []
    for hit in sorted(lint.hits):
        if (hit[0], hit[1]) not in seen:
            seen.add((hit[0], hit[1]))
            unique.append(hit)
    lint.hits = unique
    print(f"Linted {scope}, dates resolved against {ref.isoformat()}.")
    if not lint.hits:
        print("No hits.")
        return 0
    for pos, rule, found, note in lint.hits:
        print(f"L{lint.line(pos)}  {rule:<9} {found[:70]}  ->  {note}")
    counts = {}
    for _, rule, _, _ in lint.hits:
        counts[rule] = counts.get(rule, 0) + 1
    print("\n" + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
