#!/usr/bin/env python3
"""Check pages for crawl, index, and on-page SEO problems from their raw HTML.

Usage:
    python seo_check.py <url-or-path> [...] [--crawl N] [--links] [--json]

A target is an http(s) URL, a local .html file, or a folder of built HTML
(dist/, build/, out/). For URLs the script also checks robots.txt, the
sitemap, and the HTTP-to-HTTPS redirect once per site. For a folder it reads
robots.txt and sitemap files from the folder root and checks internal links
against the files on disk.

  --crawl N   also follow same-site links from the start pages, up to N more
  --links     check that internal links on fetched pages resolve (URL targets)
  --json      print the results as JSON

The script sees the raw HTML a server returns, the way a crawler that doesn't
run JavaScript sees it. Tags a page adds in the browser won't show up here, so
"missing" means missing from the server's HTML, not necessarily from the
rendered page. FAIL is a definite defect, WARN needs a look, INFO is a note.
Exit code is 1 when any FAIL is found, else 0.

Standard library only; works with Python 3.8+.
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import OrderedDict, defaultdict
from html.parser import HTMLParser

USER_AGENT = "Mozilla/5.0 (compatible; seo-check/1.0)"
TIMEOUT = 15
MAX_BYTES = 5 * 1024 * 1024
SKIP_DIRS = {"node_modules", ".git", ".astro", ".next", ".nuxt", ".svelte-kit",
             ".turbo", ".cache", "coverage", "vendor"}
NON_HTML_EXT = re.compile(
    r"\.(png|jpe?g|gif|webp|avif|svg|ico|css|js|mjs|json|xml|txt|pdf|zip|mp4|"
    r"webm|mp3|woff2?|ttf|otf|map)$", re.I)
GENERIC_TITLES = {"vite app", "react app", "home", "untitled", "document",
                  "astro", "index", "my app", "new page", "page", "welcome"}
GENERIC_ANCHORS = {"click here", "here", "read more", "learn more", "more",
                   "this", "link", "this link"}
AI_BOTS = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot",
           "Claude-SearchBot", "Claude-User", "anthropic-ai", "PerplexityBot",
           "Perplexity-User", "Google-Extended", "Applebot-Extended",
           "Bytespider", "CCBot", "Meta-ExternalAgent", "Amazonbot"]
HREFLANG_RE = re.compile(r"^(x-default|[a-z]{2,3}(-[a-z]{4})?(-([a-z]{2}|\d{3}))?)$", re.I)
BAD_REGIONS = {"uk": "gb"}


# ---------------------------------------------------------------- fetching

class _RecordRedirects(urllib.request.HTTPRedirectHandler):
    def __init__(self):
        self.chain = []

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        self.chain.append((code, req.full_url, newurl))
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(url, method="GET"):
    """Return dict(status, url, headers, body, chain, error)."""
    handler = _RecordRedirects()
    opener = urllib.request.build_opener(handler)
    req = urllib.request.Request(url, method=method, headers={
        "User-Agent": USER_AGENT, "Accept": "text/html,application/xml;q=0.9,*/*;q=0.8"})
    out = {"status": None, "url": url, "headers": {}, "body": "", "chain": [], "error": None}
    try:
        resp = opener.open(req, timeout=TIMEOUT)
        out["status"] = resp.status
        out["url"] = resp.geturl()
        out["headers"] = {k.lower(): v for k, v in resp.headers.items()}
        raw = resp.read(MAX_BYTES) if method == "GET" else b""
        out["body"] = _decode(raw, out["headers"].get("content-type", ""))
    except urllib.error.HTTPError as e:
        out["status"] = e.code
        out["url"] = e.geturl() or url
        out["headers"] = {k.lower(): v for k, v in (e.headers or {}).items()}
        try:
            out["body"] = _decode(e.read(MAX_BYTES), out["headers"].get("content-type", ""))
        except Exception:
            pass
    except Exception as e:  # DNS, TLS, timeout, refused
        out["error"] = "%s: %s" % (type(e).__name__, e)
    out["chain"] = handler.chain
    return out


def _decode(raw, content_type):
    m = re.search(r"charset=([\w-]+)", content_type or "", re.I)
    enc = m.group(1) if m else "utf-8"
    try:
        return raw.decode(enc, errors="replace")
    except LookupError:
        return raw.decode("utf-8", errors="replace")


# ---------------------------------------------------------------- parsing

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = None
        self.titles = []
        self.metas = defaultdict(list)       # name/property (lowercased) -> [content]
        self.canonicals = []
        self.hreflangs = []                  # (code, href)
        self.prevnext = []
        self.headings = []                   # (level, text)
        self.images = []                     # attrs dict
        self.jsonld = []                     # raw text blocks
        self.script_count = 0
        self.links = []                      # (href, text)
        self.http_resources = []
        self.words = 0
        self._stack_svg = 0
        self._in_title = False
        self._title_buf = []
        self._heading = None
        self._heading_buf = []
        self._anchor = None
        self._anchor_buf = []
        self._skip = 0                       # inside script/style/template
        self._jsonld_buf = None

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "svg":
            self._stack_svg += 1
        if tag == "html" and "lang" in a:
            self.lang = a["lang"].strip()
        elif tag == "title" and not self._stack_svg:
            self._in_title = True
            self._title_buf = []
        elif tag == "meta":
            key = (a.get("name") or a.get("property") or "").lower().strip()
            if not key and a.get("http-equiv"):
                key = "http-equiv:" + a["http-equiv"].lower().strip()
            if key:
                self.metas[key].append(a.get("content", "").strip())
        elif tag == "link":
            rel = a.get("rel", "").lower().split()
            href = a.get("href", "").strip()
            if "canonical" in rel:
                self.canonicals.append(href)
            if "alternate" in rel and a.get("hreflang"):
                self.hreflangs.append((a["hreflang"].strip(), href))
            if "prev" in rel or "next" in rel:
                self.prevnext.append(href)
            if "stylesheet" in rel and href.startswith("http://"):
                self.http_resources.append(href)
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._heading = int(tag[1])
            self._heading_buf = []
        elif tag == "img":
            self.images.append(a)
            if a.get("src", "").startswith("http://"):
                self.http_resources.append(a["src"])
            if self._anchor is not None and a.get("alt"):
                self._anchor_buf.append(a["alt"])
        elif tag == "a":
            self._anchor = a.get("href", "").strip()
            self._anchor_buf = []
        elif tag == "script":
            self.script_count += 1
            if a.get("src", "").startswith("http://"):
                self.http_resources.append(a["src"])
            if a.get("type", "").lower() == "application/ld+json":
                self._jsonld_buf = []
            self._skip += 1
        elif tag in ("style", "template"):
            self._skip += 1
        elif tag in ("iframe", "source", "video", "audio") and a.get("src", "").startswith("http://"):
            self.http_resources.append(a["src"])

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag in ("script", "style", "template"):
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag == "svg" and self._stack_svg:
            self._stack_svg -= 1
        elif tag == "title" and self._in_title:
            self._in_title = False
            self.titles.append(" ".join("".join(self._title_buf).split()))
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6") and self._heading:
            self.headings.append((self._heading, " ".join("".join(self._heading_buf).split())))
            self._heading = None
        elif tag == "a" and self._anchor is not None:
            self.links.append((self._anchor, " ".join(" ".join(self._anchor_buf).split())))
            self._anchor = None
        elif tag == "script":
            if self._jsonld_buf is not None:
                self.jsonld.append("".join(self._jsonld_buf))
                self._jsonld_buf = None
            self._skip = max(0, self._skip - 1)
        elif tag in ("style", "template"):
            self._skip = max(0, self._skip - 1)

    def handle_data(self, data):
        if self._jsonld_buf is not None:
            self._jsonld_buf.append(data)
            return
        if self._skip:
            return
        if self._in_title:
            self._title_buf.append(data)
            return
        if self._heading:
            self._heading_buf.append(data)
        if self._anchor is not None:
            self._anchor_buf.append(data)
        self.words += len(data.split())


def jsonld_types(blocks):
    """Return (types, errors) for the JSON-LD blocks on a page."""
    types, errors = [], []

    def walk(node):  # top-level items and @graph members, not nested properties
        if isinstance(node, list):
            for n in node:
                walk(n)
        elif isinstance(node, dict):
            t = node.get("@type")
            if isinstance(t, list):
                types.extend(str(x) for x in t)
            elif t:
                types.append(str(t))
            if "@graph" in node:
                walk(node["@graph"])

    for i, raw in enumerate(blocks, 1):
        try:
            data = json.loads(raw)
        except ValueError as e:
            errors.append("block %d: %s" % (i, e))
            continue
        items = data if isinstance(data, list) else [data]
        for item in items:
            if isinstance(item, dict) and "@context" not in item and "@graph" not in item:
                errors.append("block %d: no @context" % i)
        walk(data)
    return types, errors


# ---------------------------------------------------------------- checks

class Page:
    def __init__(self, ident, kind):
        self.ident = ident          # URL or file path
        self.kind = kind            # "url" or "file"
        self.status = None
        self.final_url = ident
        self.chain = []
        self.headers = {}
        self.error = None
        self.facts = OrderedDict()
        self.findings = []          # (level, message)
        self.parser = None
        self.noindex = False
        self.redirect_stub = False

    def add(self, level, msg):
        self.findings.append((level, msg))


def check_page(page, html):
    p = PageParser()
    try:
        p.feed(html)
        p.close()
    except Exception as e:
        page.add("WARN", "HTML parser stopped early: %s" % e)
    page.parser = p
    f = page.facts

    # status and redirects
    if page.kind == "url":
        if page.status and page.status != 200:
            page.add("FAIL", "returned HTTP %s" % page.status)
        if len(page.chain) > 1:
            hops = " -> ".join([page.chain[0][1]] + [c[2] for c in page.chain])
            page.add("WARN", "redirect chain of %d hops: %s" % (len(page.chain), hops))
        xrt = page.headers.get("x-robots-tag", "")
        if "noindex" in xrt.lower():
            page.add("WARN", "X-Robots-Tag header says noindex (%s); confirm it's intentional" % xrt)
        ctype = page.headers.get("content-type", "")
        if ctype and "html" not in ctype.lower():
            page.add("WARN", "content-type is %s, not HTML" % ctype)

    # a meta-refresh stub is a redirect, not a content page; skip the content checks
    refresh = (p.metas.get("http-equiv:refresh") or [""])[0]
    m = re.search(r"url\s*=\s*['\"]?([^'\";]+)", refresh, re.I)
    if m:
        page.redirect_stub = True
        f["redirect"] = "meta refresh to %s" % m.group(1).strip()
        page.add("INFO", "redirects with a meta refresh to %s; a server-side 301 is a clearer signal "
                         "(on static hosts this is often the only option, and Google follows it)" % m.group(1).strip())
        return p

    # title
    titles = [t for t in p.titles]
    title = titles[0] if titles else None
    f["title"] = "(%d) %s" % (len(title), title) if title else "(none)"
    if not titles:
        page.add("FAIL", "no <title>")
    elif not title:
        page.add("FAIL", "<title> is empty")
    else:
        if len(titles) > 1:
            page.add("WARN", "%d <title> tags; keep one" % len(titles))
        if title.lower().strip(" |-") in GENERIC_TITLES:
            page.add("WARN", 'generic title "%s"; describe this page' % title)
        if len(title) < 15 or len(title) > 65:
            page.add("INFO", "title is %d characters; 50-60 is a rough guide, not a limit" % len(title))

    # description
    descs = p.metas.get("description", [])
    desc = descs[0] if descs else None
    f["description"] = "(%d) %s" % (len(desc), desc) if desc else "(none)"
    if not descs or not desc:
        page.add("WARN", "no meta description; search engines will pick text from the page")
    else:
        if len(descs) > 1:
            page.add("WARN", "%d meta descriptions; keep one" % len(descs))
        if len(desc) < 50 or len(desc) > 170:
            page.add("INFO", "description is %d characters; 150-160 is a rough guide" % len(desc))
        if title and desc.strip().lower() == title.strip().lower():
            page.add("INFO", "description repeats the title")

    # robots meta
    robots = ", ".join(p.metas.get("robots", []) + p.metas.get("googlebot", []))
    f["robots"] = robots or "(none)"
    directives = [r.strip().lower() for r in robots.split(",")]
    noindex = ("noindex" in directives or "none" in directives
               or "noindex" in page.headers.get("x-robots-tag", "").lower())
    page.noindex = noindex
    if "noindex" in directives:
        page.add("WARN", "meta robots noindex (%s); confirm this page should stay out of search" % robots)
    if "none" in directives:
        page.add("WARN", 'meta robots "none" means noindex, nofollow')

    # canonical
    canon = p.canonicals[0] if p.canonicals else None
    f["canonical"] = canon or "(none)"
    if not p.canonicals:
        page.add("WARN", "no canonical link")
    else:
        if len(set(p.canonicals)) > 1:
            page.add("FAIL", "%d different canonical links: %s" % (len(set(p.canonicals)), ", ".join(p.canonicals)))
        if canon and not re.match(r"^https?://", canon):
            page.add("WARN", "canonical is relative (%s); use an absolute URL" % canon)
        if canon and page.kind == "url" and re.match(r"^https?://", canon):
            cu, fu = urllib.parse.urlsplit(canon), urllib.parse.urlsplit(page.final_url)
            if cu.netloc.lower() != fu.netloc.lower():
                page.add("WARN", "canonical points to another host: %s" % canon)
            elif cu.scheme != fu.scheme:
                page.add("WARN", "canonical uses %s but the page is served over %s" % (cu.scheme, fu.scheme))
            elif _norm(canon) != _norm(page.final_url):
                page.add("INFO", "canonical points to a different URL (%s); right for a duplicate, wrong for a unique page" % canon)
        if noindex:
            page.add("WARN", "page has both a canonical and noindex; pick one signal")

    # viewport and language
    vp = ", ".join(p.metas.get("viewport", []))
    f["viewport"] = vp or "(none)"
    if not vp:
        page.add("FAIL", "no viewport meta tag; the page won't render for mobile")
    f["lang"] = p.lang or "(none)"
    if not p.lang:
        page.add("WARN", "no lang attribute on <html>")

    # headings
    h1s = [t for lvl, t in p.headings if lvl == 1]
    f["h1"] = "%d %s" % (len(h1s), ("| " + " | ".join(h1s[:3])) if h1s else "")
    if not h1s:
        page.add("WARN", "no <h1> in the raw HTML")
    elif len(h1s) > 1:
        page.add("INFO", "%d <h1> tags; fine if the main heading is still clear" % len(h1s))
    prev = 0
    for lvl, text in p.headings:
        if prev and lvl > prev + 1:
            page.add("INFO", "heading level jumps from h%d to h%d at \"%s\"" % (prev, lvl, text[:60]))
            break
        prev = lvl

    # body text and client rendering
    f["words"] = str(p.words)
    if p.words < 50 and p.script_count:
        page.add("WARN", "only %d words of text in the raw HTML; content is probably rendered by "
                         "JavaScript, so crawlers that don't run it see a near-empty page" % p.words)

    # images
    no_alt = [i.get("src", "?") for i in p.images if "alt" not in i]
    if no_alt:
        page.add("WARN", "%d <img> without an alt attribute (use alt=\"\" for decorative ones): %s"
                 % (len(no_alt), ", ".join(no_alt[:5])))
    no_dims = [i for i in p.images if not (i.get("width") and i.get("height"))]
    if no_dims:
        page.add("INFO", "%d <img> without width and height (layout shift)" % len(no_dims))

    # mixed content
    if page.final_url.startswith("https://") and p.http_resources:
        page.add("WARN", "%d resources loaded over http:// on an https page: %s"
                 % (len(p.http_resources), ", ".join(p.http_resources[:3])))

    # structured data
    types, errors = jsonld_types(p.jsonld)
    f["json-ld"] = ", ".join(types) if types else ("(none)" if not p.jsonld else "(no @type)")
    for e in errors:
        page.add("FAIL", "JSON-LD doesn't parse or is incomplete: %s" % e)
    if not p.jsonld:
        page.add("INFO", "no JSON-LD in the raw HTML (check the rendered page before calling it missing)")
    if "HowTo" in types:
        page.add("WARN", "HowTo markup no longer produces rich results")
    if "FAQPage" in types:
        page.add("INFO", "FAQPage rich results are retired for most sites; keep only if the page is a real FAQ")

    # social
    og = [k for k in ("og:title", "og:description", "og:image", "og:url") if p.metas.get(k)]
    tw = (p.metas.get("twitter:card") or [""])[0]
    f["open graph"] = (" ".join(og) or "(none)") + ("  twitter:card=" + tw if tw else "")
    missing_og = [k for k in ("og:title", "og:description", "og:image") if not p.metas.get(k)]
    if missing_og:
        page.add("INFO", "missing %s (link previews)" % ", ".join(missing_og))
    for img in p.metas.get("og:image", []):
        if img and not re.match(r"^https?://", img):
            page.add("WARN", "og:image is relative (%s); previews need an absolute URL" % img)

    # retired signals
    if p.metas.get("keywords"):
        page.add("INFO", "meta keywords is ignored by Google; harmless, don't add more")
    if p.prevnext:
        page.add("INFO", "rel=prev/next is ignored by Google; make sure pages link to each other with <a href>")

    # hreflang
    if p.hreflangs:
        codes = [c for c, _ in p.hreflangs]
        f["hreflang"] = ", ".join(codes)
        for code in codes:
            parts = code.lower().split("-")
            if not HREFLANG_RE.match(code):
                page.add("WARN", "invalid hreflang code %s" % code)
            elif len(parts) > 1 and parts[-1] in BAD_REGIONS:
                page.add("WARN", "hreflang %s should be %s-%s" % (code, parts[0], BAD_REGIONS[parts[-1]].upper()))
        page_lang = (p.lang or "").lower().split("-")[0]
        langs_listed = {c.lower().split("-")[0] for c in codes}
        by_url = {}
        for code, href in p.hreflangs:
            if re.match(r"^https?://", href):
                by_url.setdefault(_norm(href), code)
        canon_code = by_url.get(_norm(canon)) if canon and re.match(r"^https?://", canon) else None
        if page_lang and canon_code and canon_code.lower() != "x-default" \
                and canon_code.lower().split("-")[0] != page_lang:
            page.add("FAIL", "this %s page's canonical points to the %s version (%s), which asks Google to "
                             "drop this page in favor of it; each language page should be its own canonical"
                             % (page_lang, canon_code, canon))
        if page_lang and page_lang not in langs_listed:
            page.add("WARN", "hreflang set has no entry for this page's own language (%s); every variant "
                             "lists itself and all the others" % page_lang)
        elif not canon_code or canon_code.lower().split("-")[0] == page_lang:
            self_url = canon or (page.final_url if page.kind == "url" else None)
            if self_url and re.match(r"^https?://", self_url) and _norm(self_url) not in by_url:
                page.add("WARN", "hreflang set doesn't include this page itself")
        if "x-default" not in [c.lower() for c in codes]:
            page.add("INFO", "no x-default hreflang (recommended, not required)")

    # anchors
    generic = [t for h, t in p.links if t.lower().strip(" .>»→") in GENERIC_ANCHORS]
    if generic:
        page.add("INFO", "%d links with generic text (%s); say where the link goes"
                 % (len(generic), ", ".join(sorted(set(generic))[:4])))
    return p


def _norm(url):
    s = urllib.parse.urlsplit(url)
    path = s.path or "/"
    if path != "/" and path.endswith("/"):
        path = path[:-1]
    return "%s://%s%s%s" % (s.scheme.lower(), s.netloc.lower(), path, ("?" + s.query) if s.query else "")


# ---------------------------------------------------------------- site-level

def parse_robots(text):
    """Return (groups, sitemaps): groups maps user-agent (lower) -> list of disallow paths."""
    groups, sitemaps, current, last_was_agent = defaultdict(list), [], [], False
    for line in text.splitlines():
        line = line.split("#", 1)[0].strip()
        if ":" not in line:
            continue
        key, val = [x.strip() for x in line.split(":", 1)]
        key = key.lower()
        if key == "user-agent":
            if not last_was_agent:
                current = []
            current.append(val.lower())
            groups.setdefault(val.lower(), [])
            last_was_agent = True
            continue
        last_was_agent = False
        if key == "disallow":
            for ua in current:
                groups[ua].append(val)
        elif key == "sitemap":
            sitemaps.append(val)
    return groups, sitemaps


def robots_findings(text, add, served_html=False):
    if served_html or re.search(r"<html|<!doctype", text[:500], re.I):
        add("WARN", "robots.txt returns an HTML page (a catch-all route?); serve a real text file")
        return []
    groups, sitemaps = parse_robots(text)
    if "/" in groups.get("*", []):
        add("FAIL", "robots.txt blocks every crawler from the whole site (User-agent: * / Disallow: /)")
    if "googlebot" in groups and "/" in groups["googlebot"]:
        add("FAIL", "robots.txt blocks Googlebot from the whole site")
    for path in groups.get("*", []):
        if re.search(r"\.(css|js)\b|/_astro|/assets|/static|/_next", path, re.I):
            add("WARN", "robots.txt disallows %s; crawlers need CSS and JS to render pages" % path)
    named = []
    for bot in AI_BOTS:
        if bot.lower() in groups:
            named.append("%s (%s)" % (bot, "blocked" if "/" in groups[bot.lower()] else "allowed"))
    if named:
        add("INFO", "AI crawlers named in robots.txt: %s" % ", ".join(named))
    if not sitemaps:
        add("INFO", "robots.txt has no Sitemap: line")
    return sitemaps


def sitemap_findings(text, add, origin=None):
    try:
        root = ET.fromstring(text.encode("utf-8"))
    except ET.ParseError as e:
        add("FAIL", "sitemap isn't valid XML: %s" % e)
        return None, []
    tag = root.tag.split("}")[-1]
    locs = [el.text.strip() for el in root.iter() if el.tag.split("}")[-1] == "loc" and el.text]
    if tag == "sitemapindex":
        return "index", locs
    urls = locs
    lastmods = [el for el in root.iter() if el.tag.split("}")[-1] == "lastmod"]
    if not urls:
        add("WARN", "sitemap has no URLs")
    if urls and not lastmods:
        add("INFO", "sitemap has no lastmod dates")
    if origin:
        o = urllib.parse.urlsplit(origin)
        off = [u for u in urls if urllib.parse.urlsplit(u).netloc.lower() != o.netloc.lower()
               or urllib.parse.urlsplit(u).scheme != o.scheme]
        if off:
            add("WARN", "%d sitemap URLs use another host or scheme, e.g. %s" % (len(off), off[0]))
    return "urlset", urls


def check_site_url(origin):
    site = Page(origin, "url")
    add = site.add
    if not re.match(r"^https?://(localhost|127\.0\.0\.1|\[::1\]|[^/]+\.(localhost|test))(:\d+)?$", origin):
        if origin.startswith("https://"):
            r = fetch("http://" + origin[len("https://"):] + "/")
            if r["error"]:
                add("INFO", "couldn't reach the http:// version (%s)" % r["error"])
            elif not r["url"].startswith("https://"):
                add("FAIL", "http:// doesn't redirect to https://")
            r2 = fetch(origin + "/", method="HEAD")
            if r2["status"] and "strict-transport-security" not in r2["headers"]:
                add("INFO", "no Strict-Transport-Security header")
        else:
            add("WARN", "site is served over http://, not https://")

    r = fetch(origin + "/robots.txt")
    sitemaps = []
    if r["error"]:
        add("WARN", "couldn't fetch robots.txt: %s" % r["error"])
    elif r["status"] == 404:
        site.facts["robots.txt"] = "404 (everything is crawlable)"
        add("INFO", "no robots.txt")
    elif r["status"] and r["status"] >= 500:
        add("FAIL", "robots.txt returns %s; crawlers treat that as 'disallow everything'" % r["status"])
    elif r["status"] == 200:
        site.facts["robots.txt"] = "200"
        sitemaps = robots_findings(r["body"], add, "html" in r["headers"].get("content-type", ""))

    candidates = sitemaps or [origin + "/sitemap.xml", origin + "/sitemap-index.xml"]
    urls, found = [], None
    for sm in candidates:
        s = fetch(sm)
        if s["status"] != 200 or s["error"]:
            continue
        if "html" in s["headers"].get("content-type", "") or re.search(r"<html", s["body"][:500], re.I):
            add("WARN", "%s returns an HTML page, not a sitemap" % sm)
            continue
        kind, locs = sitemap_findings(s["body"], add, origin)
        found = sm
        if kind == "index":
            site.facts["sitemap"] = "%s (index of %d)" % (sm, len(locs))
            for child in locs[:3]:
                c = fetch(child)
                if c["status"] == 200:
                    _, child_urls = sitemap_findings(c["body"], add, origin)
                    urls.extend(child_urls)
                else:
                    add("WARN", "sitemap %s returns %s" % (child, c["status"] or c["error"]))
        else:
            urls = locs
            site.facts["sitemap"] = sm
        break
    if found:
        site.facts["sitemap URLs"] = str(len(urls))
    else:
        add("WARN", "no sitemap found (tried %s)" % ", ".join(candidates))
    return site, set(_norm(u) for u in urls)


def check_site_folder(folder):
    try:
        shown = os.path.relpath(folder)
    except ValueError:  # another drive on Windows
        shown = folder
    site = Page(shown, "file")
    add = site.add
    robots = os.path.join(folder, "robots.txt")
    if os.path.isfile(robots):
        site.facts["robots.txt"] = "present"
        with open(robots, encoding="utf-8", errors="replace") as fh:
            robots_findings(fh.read(), add)
    else:
        add("INFO", "no robots.txt in the folder root")
    maps = [n for n in os.listdir(folder) if re.match(r"sitemap.*\.xml$", n, re.I)]
    urls = []
    for name in maps:
        with open(os.path.join(folder, name), encoding="utf-8", errors="replace") as fh:
            kind, locs = sitemap_findings(fh.read(), add)
        if kind == "urlset":
            urls.extend(locs)
    if maps:
        site.facts["sitemap"] = ", ".join(maps)
        site.facts["sitemap URLs"] = str(len(urls))
    else:
        add("INFO", "no sitemap file in the folder root; it may be generated elsewhere")
    return site


# ---------------------------------------------------------------- driver

def html_files(folder):
    for root, dirs, files in os.walk(folder):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            if name.lower().endswith((".html", ".htm")):
                yield os.path.join(root, name)


def resolve_local(folder, href, from_file):
    path = urllib.parse.urlsplit(href).path
    if not path:
        return True
    base = folder if path.startswith("/") else os.path.dirname(from_file)
    target = os.path.normpath(os.path.join(base, urllib.parse.unquote(path.lstrip("/"))))
    options = [target, target + ".html", os.path.join(target, "index.html")]
    return any(os.path.exists(o) for o in options)


def internal_links(page, base_url):
    out = []
    for href, _ in page.parser.links:
        if not href or href.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
            continue
        full = urllib.parse.urljoin(base_url, href).split("#")[0]
        if urllib.parse.urlsplit(full).netloc.lower() == urllib.parse.urlsplit(base_url).netloc.lower():
            out.append(full)
    return out


def run(targets, crawl=0, check_links=False):
    pages, sites = [], []
    queue, seen, origins = [], set(), OrderedDict()
    for t in targets:
        if re.match(r"^https?://", t):
            queue.append(t)
            o = urllib.parse.urlsplit(t)
            origins.setdefault("%s://%s" % (o.scheme, o.netloc), None)
        elif os.path.isdir(t):
            folder = os.path.abspath(t)
            sites.append(check_site_folder(folder))
            for path in html_files(folder):
                pages.append(_local_page(path, folder))
        elif os.path.isfile(t):
            pages.append(_local_page(os.path.abspath(t), os.path.dirname(os.path.abspath(t))))
        else:
            print("not a URL, file, or folder: %s" % t, file=sys.stderr)

    sitemap_urls = {}
    for origin in origins:
        site, urls = check_site_url(origin)
        sites.append(site)
        sitemap_urls[origin] = urls

    budget = crawl
    while queue:
        url = queue.pop(0)
        key = _norm(url)
        if key in seen:
            continue
        seen.add(key)
        page = Page(url, "url")
        r = fetch(url)
        page.status, page.final_url, page.chain = r["status"], r["url"], r["chain"]
        page.headers, page.error = r["headers"], r["error"]
        pages.append(page)
        if r["error"]:
            page.add("FAIL", "couldn't fetch: %s" % r["error"])
            continue
        check_page(page, r["body"])
        o = urllib.parse.urlsplit(page.final_url)
        smap = sitemap_urls.get("%s://%s" % (o.scheme, o.netloc))
        if smap and page.status == 200 and not page.noindex:
            canon = page.parser.canonicals[0] if page.parser.canonicals else page.final_url
            if _norm(urllib.parse.urljoin(page.final_url, canon)) not in smap:
                page.add("INFO", "this page's canonical URL isn't in the sitemap")
        links = internal_links(page, page.final_url)
        if check_links:
            _check_links(page, links)
        for link in links:
            if budget <= 0:
                break
            if NON_HTML_EXT.search(urllib.parse.urlsplit(link).path):
                continue
            if _norm(link) not in seen and link not in queue:
                queue.append(link)
                budget -= 1

    cross = Page("across pages", "summary")
    _cross_page(pages, cross)
    return sites, pages, cross


def _local_page(path, folder):
    try:
        shown = os.path.relpath(path)
    except ValueError:  # another drive on Windows
        shown = path
    page = Page(shown, "file")
    with open(path, encoding="utf-8", errors="replace") as fh:
        check_page(page, fh.read())
    broken = []
    for href, _ in page.parser.links:
        if not href or re.match(r"^([a-z]+:|//|#)", href, re.I):
            continue
        if not resolve_local(folder, href, path):
            broken.append(href)
    if broken:
        page.add("WARN", "%d internal links point to files not in the folder: %s"
                 % (len(broken), ", ".join(sorted(set(broken))[:5])))
    return page


def _check_links(page, links):
    bad, checked = [], 0
    for link in sorted(set(links)):
        if checked >= 100:
            page.add("INFO", "stopped checking links after 100")
            break
        checked += 1
        r = fetch(link, method="HEAD")
        if r["status"] in (405, 501) or (r["status"] is None and not r["error"]):
            r = fetch(link)
        if r["error"] or (r["status"] and r["status"] >= 400):
            bad.append("%s (%s)" % (link, r["status"] or r["error"]))
    if bad:
        page.add("FAIL", "%d broken internal links: %s" % (len(bad), ", ".join(bad[:5])))


def _cross_page(pages, cross):
    ok = [p for p in pages if p.parser and not p.noindex and not p.redirect_stub
          and p.status in (None, 200)]
    if len(ok) < 2:
        return
    for label, getter in (("title", lambda p: p.parser.titles[0] if p.parser.titles else ""),
                          ("description", lambda p: (p.parser.metas.get("description") or [""])[0])):
        groups = defaultdict(list)
        for p in ok:
            v = getter(p).strip().lower()
            if v:
                groups[v].append(p.ident)
        for v, idents in groups.items():
            if len(idents) > 1:
                cross.add("WARN", 'same %s on %d pages ("%s"): %s'
                          % (label, len(idents), v[:70], ", ".join(idents[:5])))
    canon = defaultdict(list)
    for p in ok:
        if p.parser.canonicals:
            canon[p.parser.canonicals[0]].append(p.ident)
    for c, idents in canon.items():
        if len(idents) > 1:
            cross.add("WARN", "%d pages share the canonical %s (a hard-coded canonical in a layout?): %s"
                      % (len(idents), c, ", ".join(idents[:5])))


def report_text(sites, pages, cross):
    counts = defaultdict(int)
    order = {"FAIL": 0, "WARN": 1, "INFO": 2}

    def block(title, page):
        print("== %s" % title)
        for k, v in page.facts.items():
            print("   %-12s %s" % (k + ":", v))
        for level, msg in sorted(page.findings, key=lambda x: order[x[0]]):
            counts[level] += 1
            print("   %-4s  %s" % (level, msg))
        print()

    for s in sites:
        block("site: %s" % s.ident, s)
    for p in pages:
        head = p.ident
        if p.kind == "url":
            head += "  (%s%s)" % (p.status or "no response",
                                  ", redirected to %s" % p.final_url if p.final_url != p.ident else "")
        block(head, p)
    if cross.findings:
        block("across pages", cross)
    print("%d page%s: %d FAIL, %d WARN, %d INFO" % (len(pages), "" if len(pages) == 1 else "s",
                                                    counts["FAIL"], counts["WARN"], counts["INFO"]))
    print("Raw HTML only: check the rendered page before calling a tag missing.")
    return counts["FAIL"]


def report_json(sites, pages, cross):
    def dump(p):
        return {"target": p.ident, "status": p.status, "final_url": p.final_url,
                "facts": p.facts, "findings": [{"level": l, "message": m} for l, m in p.findings]}
    data = {"sites": [dump(s) for s in sites], "pages": [dump(p) for p in pages],
            "across_pages": [{"level": l, "message": m} for l, m in cross.findings]}
    print(json.dumps(data, indent=2))
    return sum(1 for p in sites + pages + [cross] for l, _ in p.findings if l == "FAIL")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="Check pages for SEO problems from their raw HTML.")
    ap.add_argument("targets", nargs="+", help="URLs, .html files, or folders of built HTML")
    ap.add_argument("--crawl", type=int, default=0, help="follow same-site links, up to N more pages")
    ap.add_argument("--links", action="store_true", help="check internal links on fetched pages")
    ap.add_argument("--json", action="store_true", help="print JSON")
    args = ap.parse_args()
    sites, pages, cross = run(args.targets, crawl=args.crawl, check_links=args.links)
    fails = (report_json if args.json else report_text)(sites, pages, cross)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
