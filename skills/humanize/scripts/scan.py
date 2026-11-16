#!/usr/bin/env python3
"""Count the AI-writing tells that are hard to count by reading.

Usage:
  scan.py FILE            scan a file (Markdown code, frontmatter, and URLs are skipped)
  scan.py - < text.txt    scan text from stdin
  scan.py FILE --all      list every hit, not just the first five per pattern

Prints, with line numbers: AI vocabulary from humanize's literal lists and its rate per 1,000
words, stock phrases (significance, -ing tails, staged contrasts, openers, closers, chat
leftovers), em dashes, sentence-length spread, formatting tells, chatbot residue, tracking
parameters, and unfilled placeholders. Hits inside double quotes are marked "(quoted)", since
quotations stay verbatim.

These are counts, not a verdict. The script can't tell a literal sense from a tell (an underscore
character), can't see structure or meaning, and misses tells that aren't on its lists.
Standard library only.
"""

import argparse
import math
import re
import sys

SENTENCE_START = r"(?:^|(?<=[.!?]\s)|(?<=[.!?][\"”'’)]\s))"
VOCAB_OLD = {
    "delve": r"delv(?:e|es|ed|ing)", "tapestry": r"tapestr(?:y|ies)", "testament": r"testaments?",
    "pivotal": r"pivotal", "crucial": r"crucial(?:ly)?", "intricate": r"intricate(?:ly)?|intricac(?:y|ies)",
    "interplay": r"interplay", "meticulous": r"meticulous(?:ly)?", "garner": r"garner(?:s|ed|ing)?",
    "bolster": r"bolster(?:s|ed|ing)?", "underscore": r"underscor(?:e|es|ed|ing)", "showcase": r"showcas(?:e|es|ed|ing)",
    "enduring": r"enduring", "vibrant": r"vibrant", "landscape": r"landscapes?",
}
VOCAB_NEW = {
    "enhance": r"enhanc(?:e|es|ed|ing|ement)", "highlight": r"highlight(?:s|ed|ing)?",
    "emphasize": r"emphasi[sz](?:e|es|ed|ing)", "foster": r"foster(?:s|ed|ing)?", "leverage": r"leverag(?:e|es|ed|ing)",
    "multifaceted": r"multifaceted", "align with": r"align(?:s|ed|ing)? with", "matters": r"matters",
    "clearer": r"clearer", "practical": r"practical", "dependable": r"dependable", "steady": r"steady",
    "quietly": r"quietly", "prioritize": r"prioriti[sz](?:e|es|ed|ing)", "echoed": r"echoed", "universally": r"universally",
}
PHRASES = {
    "Significance and legacy": [
        r"stands? as an? (?:\w+ )?(?:testament|reminder|symbol)", r"plays? an? (?:pivotal|crucial|key|vital|significant|central) role",
        r"marks? an? (?:key |pivotal |significant )?turning point", r"reflects? (?:a )?broader", r"setting the stage for",
        r"indelible mark", r"deeply rooted", r"evolving landscape", r"(?:has )?sparked (?:a )?debate", r"shap(?:ed|ing) (?:the )?conversations?",
    ],
    "-ing tails": [r", (?:highlighting|underscoring|emphasizing|reflecting|ensuring|fostering|showcasing|contributing to|cementing|solidifying|offering valuable)\b"],
    "Avoiding is/has": [r"\b(?:serves|served|stands|stood|functions) as\b", r"\bboasts?\b", r"\brefers to the\b"],
    "Staged contrasts": [r"\bnot (?:just|only|merely) [^.;:!?]{1,60}?,? but\b", r"\bit'?s not [^.;:!?]{1,40}?[,;] it'?s\b", r"\bno \w+, no \w+, just\b"],
    "Openers and meta-commentary": [
        r"here'?s the thing", r"let'?s dive", r"the truth is", r"in today'?s (?:fast-paced|digital|ever)", r"this comprehensive guide",
        r"it'?s (?:important|worth|crucial) to (?:note|remember|mention)", r"it'?s worth noting", r"as you can see", r"in this (?:section|article|post|guide),? we",
    ],
    "Closers and aphorisms": [SENTENCE_START + r"(?:in summary|in conclusion|overall|ultimately),", r"let that sink in", r"at its core", r"only time will tell", r"that'?s the real"],
    "Vague attribution and gap-filling": [
        r"\bexperts (?:argue|say|note|believe|agree)", r"\bobservers (?:note|say)", r"\bindustry reports\b", r"\bstudies show\b",
        r"while specific details are limited", r"not widely documented", r"based on (?:the )?available information", r"keeps? a low profile",
    ],
    "Promotional": [r"\bnestled\b", r"in the heart of", r"\brenowned\b", r"\bgroundbreaking\b", r"\bcommitment to\b", r"\bdiverse array\b", r"\brich (?:history|heritage|tradition|culture)\b"],
    "Stiff synonyms": [r"\butiliz(?:e|es|ed|ing)\b", r"\bauthored\b", r"\brelocated\b", r"\bpassed away\b"],
    "Chat leftovers": [
        r"\bcertainly!", r"great question", r"i hope this helps", r"let me know if", r"would you like me to", r"as an ai\b",
        r"you'?re absolutely right", r"i apologize for any inconvenience", r"\bhere is an? (?:revised|rewritten|updated|draft)",
    ],
}
RESIDUE = [r"contentReference\[oaicite:\d+\]", r"oaicite", r"【\d+†[^】]*】", r"↩", r"utm_source=(?:chatgpt\.com|openai|copilot\.com)", r"referrer=grok\.com"]
PLACEHOLDERS = [r"\[Your [A-Z][^\]]*\]", r"\bINSERT_[A-Z_]+\b", r"\b\d{4}-xx-xx\b", r"example\.com/source\d*"]
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿⭐✅]")
SMALL = {"a", "an", "and", "as", "at", "but", "by", "for", "in", "of", "on", "or", "the", "to", "vs", "with"}


def blank(match):
    return re.sub(r"[^\n]", " ", match.group(0))


def clean(text):
    """Blank out what isn't prose, keeping every offset so line numbers stay right."""
    text = re.sub(r"\A---\n.*?\n---\n", blank, text, flags=re.S)
    text = re.sub(r"^(\s{0,3})(`{3,}|~{3,}).*?^\s{0,3}\2[^\n]*$", blank, text, flags=re.S | re.M)
    text = re.sub(r"`[^`\n]+`", blank, text)
    text = re.sub(r"\]\([^)\s]+\)", lambda m: "]" + " " * (len(m.group(0)) - 1), text)
    return re.sub(r"https?://\S+", blank, text)


def quote_mask(text):
    inside, mask = False, []
    prev = ""
    for ch in text:
        if ch == "\n" and prev == "\n":
            inside = False
        if ch in "“":
            inside = True
        elif ch in "”":
            inside = False
        elif ch == '"':
            inside = not inside
        mask.append(inside)
        prev = ch
    return mask


class Report:
    def __init__(self, text, show_all):
        self.text, self.show_all = text, show_all
        self.starts = [0] + [m.end() for m in re.finditer(r"\n", text)]
        self.mask = quote_mask(text)

    def line(self, pos):
        lo, hi = 0, len(self.starts) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if self.starts[mid] <= pos:
                lo = mid
            else:
                hi = mid - 1
        return lo + 1

    def snippet(self, m):
        a, b = max(0, m.start() - 30), min(len(self.text), m.end() + 30)
        s = re.sub(r"\s+", " ", self.text[a:b]).strip()
        return ("..." if a else "") + s + ("..." if b < len(self.text) else "")

    def hits(self, pattern, flags=re.I):
        return list(re.finditer(pattern, self.text, flags | re.M))

    def show(self, label, matches, indent="  "):
        if not matches:
            return 0
        quoted = sum(1 for m in matches if self.mask[m.start()])
        print(f"{indent}{label}: {len(matches)}" + (f" ({quoted} quoted)" if quoted else ""))
        for m in matches if self.show_all else matches[:5]:
            print(f"{indent}  L{self.line(m.start())}: {self.snippet(m)}" + ("  (quoted)" if self.mask[m.start()] else ""))
        if not self.show_all and len(matches) > 5:
            print(f"{indent}  ... {len(matches) - 5} more (--all)")
        return len(matches)


def outermost(matches):
    """Sort matches and drop any that sit inside an earlier one."""
    kept = []
    for m in sorted(matches, key=lambda m: (m.start(), -m.end())):
        if not kept or m.start() >= kept[-1].end():
            kept.append(m)
    return kept


def sentences(text):
    prose = []
    for para in re.split(r"\n\s*\n", text):
        lines = [l for l in para.splitlines() if l.strip() and not re.match(r"\s*(?:#|[-*+]\s|\d+[.)]\s|\||>)", l)]
        if lines:
            prose.append(" ".join(l.strip() for l in lines))
    out = []
    for para in prose:
        out += [s for s in re.split(r"(?<=[.!?])[\"”')\]]*\s+(?=[\"“(]?[A-Z0-9])", para) if len(s.split()) > 1]
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("file", help="file to scan, or - for stdin")
    ap.add_argument("--all", action="store_true", help="list every hit")
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    raw = sys.stdin.buffer.read() if args.file == "-" else open(args.file, "rb").read()
    raw = raw.decode("utf-8-sig", errors="replace").replace("\r\n", "\n")
    text = clean(raw)
    words = len(re.findall(r"[A-Za-z0-9’']+", text))
    per_k = lambda n: f"{n * 1000 / words:.1f} per 1,000 words" if words else "n/a"
    r = Report(text, args.all)
    print(f"Words: {words}")

    print("\nAI vocabulary (one word proves nothing; clusters do)")
    total = 0
    for title, vocab in (("2023-2025 models", VOCAB_OLD), ("newer models", VOCAB_NEW)):
        found = [(w, r.hits(rf"\b(?:{p})\b")) for w, p in vocab.items()]
        found = [(w, h) for w, h in found if h]
        if found:
            print(f"  {title}:")
            for w, h in found:
                total += r.show(w, h, "    ")
    additionally = r.hits(SENTENCE_START + r"Additionally,", 0)
    total += r.show('"Additionally," opening a sentence', additionally)
    print(f"  Total: {total} ({per_k(total)})")

    print("\nStock phrases")
    any_phrase = False
    for title, patterns in PHRASES.items():
        matches = outermost(m for p in patterns for m in r.hits(p))
        any_phrase |= bool(r.show(title, matches))
    if not any_phrase:
        print("  none")

    print("\nPunctuation and rhythm")
    dashes = r.hits("—", 0)
    spaced = r.hits(" — |\\s-{2,3}\\s| – ", 0)
    print(f"  Em dashes: {len(dashes)} ({per_k(len(dashes))}); spaced or substitute dashes: {len(spaced)}")
    lengths = [len(s.split()) for s in sentences(text)]
    if len(lengths) >= 5:
        mean = sum(lengths) / len(lengths)
        sd = math.sqrt(sum((n - mean) ** 2 for n in lengths) / len(lengths))
        mid = sum(1 for n in lengths if 8 <= n <= 20) / len(lengths)
        print(f"  Sentences: {len(lengths)}, mean {mean:.1f} words, spread (sd) {sd:.1f}, shortest {min(lengths)}, longest {max(lengths)}, {mid:.0%} in 8-20 words")
        if len(lengths) >= 10 and sd / mean < 0.35 and mid > 0.7:
            print("  Uniform rhythm: most sentences are the same middling length.")
    triads = r.hits(r"\b[\w-]+(?: [\w-]+)?, [\w-]+(?: [\w-]+)?,? and [\w-]+\b", 0)
    print(f"  Lists of three (rough): {len(triads)} ({per_k(len(triads))})")
    curly = len(re.findall("[“”‘’]", text))
    straight = len(re.findall("[\"']", text))
    if curly and straight:
        print(f"  Mixed quotes: {curly} curly and {straight} straight")

    print("\nFormatting")
    bold = r.hits(r"\*\*[^*\n]+\*\*", 0)
    labels = r.hits(r"^\s*[-*+]\s+\*\*[^*\n]+\*\*:?", 0)
    title_case = [m for m in r.hits(r"^#{1,6}\s+(.+)$", 0)
                  if len(ws := [w for w in m.group(1).split() if w.isalpha()]) >= 3
                  and all(w[0].isupper() for w in ws if w.lower() not in SMALL)]
    emoji = r.hits(EMOJI.pattern, 0)
    print(f"  Bold spans: {len(bold)}; bold-label list items: {len(labels)}; emoji: {len(emoji)}")
    r.show("Title Case headings", title_case)

    print("\nResidue and placeholders (remove residue; flag placeholders for the user)")
    rr = Report(raw, args.all)
    found = rr.show("Chatbot residue", outermost(m for p in RESIDUE for m in re.finditer(p, raw)))
    found += rr.show("Unfilled placeholders", outermost(m for p in PLACEHOLDERS for m in re.finditer(p, raw)))
    if not found:
        print("  none")
    return 0


if __name__ == "__main__":
    sys.exit(main())
