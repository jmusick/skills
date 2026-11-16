# SEO checks in detail

Read the section for the checklist item you're judging. Each one says why it matters, what to check, and the mistakes that come up most.

## Contents

- robots.txt
- Sitemaps
- noindex
- Canonicals
- Redirects and status codes
- HTTPS
- JavaScript rendering
- Mobile and Core Web Vitals
- Titles and descriptions
- Headings, images, and links
- Content quality
- Structured data
- Link previews
- hreflang
- AI crawlers

## robots.txt

robots.txt controls crawling, not indexing. A page blocked in robots.txt can still get indexed from links to it, without its content, and Google can't see a `noindex` on a page it isn't allowed to fetch. To keep a page out of search, allow crawling and use `noindex`.

Check:
- It lives at the root (`/robots.txt`) and returns either 200 with plain text or 404. A 5xx makes Google treat the whole site as disallowed. A common bug is an SPA catch-all route that answers `/robots.txt` with the app's HTML.
- `User-agent: *` with `Disallow: /` blocks everything. It's usually a staging setting that shipped.
- No rules block CSS, JS, or image folders (`/_astro/`, `/assets/`, `/static/`, `/_next/`). Google renders pages and needs those files.
- A `Sitemap:` line with an absolute URL.
- Rules are path prefixes. `Disallow: /admin` also blocks `/administrators`, so use `/admin/` when that matters.

## Sitemaps

A sitemap helps search engines find pages. It doesn't guarantee they get indexed.

Check:
- It can be found from robots.txt, `/sitemap.xml`, or `/sitemap-index.xml` (Astro's `@astrojs/sitemap` writes `sitemap-index.xml` plus `sitemap-0.xml`).
- It lists only canonical, indexable URLs that return 200: no redirects, noindex pages, 404s, or parameter duplicates.
- URLs are absolute and use the same host and scheme as the live site. A common mistake is a sitemap built with `site: http://localhost:4321` or the wrong domain.
- At most 50,000 URLs or 50MB per file, with a sitemap index above that.
- `lastmod` changes only when the content does. A build date stamped on every URL teaches Google to ignore it.
- It's submitted in Search Console (the user has to confirm this).

## noindex

Check meta robots, the `googlebot` meta tag, and the `X-Robots-Tag` header. Noindex is right for search results pages, thank-you pages, drafts, account pages, and thin tag archives. On a page the site wants found, it's a Critical finding. The classic case is a layout-level `noindex` left over from staging, so check whether it comes from an environment variable or a build flag.

Don't pair `noindex` with a canonical that points elsewhere. The two signals contradict each other.

## Canonicals

A canonical tells search engines which URL is the main copy. Google treats it as a strong hint, not a rule, and may pick its own.

Check:
- One `<link rel="canonical">` per page, with an absolute URL, in the server's HTML. If JavaScript adds a second one that disagrees, Google may use either.
- Unique pages point to themselves. Variants (tracking parameters, sort orders, print views) point to the main page.
- The canonical matches how the site really serves the page: the same scheme, host (www or not), and trailing slash as the URL that returns 200 and appears in the sitemap.
- Paginated pages canonical to themselves, not to page 1.
- Many pages sharing one canonical usually means a layout hard-codes it, often to the home page. That quietly asks Google to drop every other page, so it's Critical.

## Redirects and status codes

- 301 or 308 for permanent moves. 302 or 307 only for temporary ones.
- No chains: each old URL redirects straight to its final destination in one hop. No loops.
- Missing pages return a real 404 or 410. A "page not found" message with a 200 status is a soft 404 and wastes crawling.
- Redirect http to https, and the non-preferred host to the preferred one, at the server or CDN in a single hop.

## HTTPS

- Every page is on HTTPS with a valid certificate, and http:// redirects to it.
- No mixed content: images, scripts, stylesheets, and iframes all load over https.
- HSTS is good practice. HTTPS itself is a light ranking signal. The bigger costs of skipping it are browser warnings and lost referrer data.

## JavaScript rendering

Google renders JavaScript in a second pass that can lag behind crawling. Link-preview bots (Facebook, LinkedIn, Slack, iMessage, X) and most AI crawlers don't render it at all. So:
- Put titles, descriptions, canonicals, robots directives, and JSON-LD in the server's HTML. If the raw HTML says `noindex` and JavaScript removes it, Google may still honor the noindex.
- Pages that return a non-200 status aren't rendered at all.
- An SPA whose `index.html` has one generic title and an empty `<div id="root">` looks identical on every route to anything that doesn't render JavaScript. The checker flags this as "only N words of text in the raw HTML."
- Links have to be `<a href="...">`. Crawlers don't follow click handlers on buttons or divs.
- Fixes, from smallest to largest: prerender the public routes at build time, move the public pages to a static or server-rendered framework, or server-render the whole app.

## Mobile and Core Web Vitals

Google indexes the mobile version of every site.
- The viewport meta tag is present, content fits a 390px width without horizontal scrolling, tap targets are at least 24px (48px is comfortable), text is readable without zooming, and zoom is never disabled.
- Mobile shows the same main content, headings, links, and structured data as desktop.

Core Web Vitals are judged at the 75th percentile of real visits: LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1. Lighthouse gives lab numbers. PageSpeed Insights shows field data (CrUX) when a site gets enough traffic. Common causes you can spot in code:
- LCP: a large or lazy-loaded hero image (the main image should load eagerly, with `fetchpriority="high"`), render-blocking scripts and stylesheets, slow server responses, and web fonts that block text.
- CLS: images and embeds without width and height, ads or banners injected above content, and fonts that swap without size-matched fallbacks.
- INP: heavy JavaScript on the main thread, large hydration work, and slow event handlers.

## Titles and descriptions

The title is the strongest on-page text signal and the headline in search results.
- Unique per page and describing that page. Put the main topic first and the brand last, if at all (`Blue Widget Repair Guide | Acme`).
- Not generic (`Home`, `Untitled`, `Vite App`) and not a stack of keywords.
- Google rewrites titles that are missing, generic, or stuffed, or that don't match the page's main heading. Find out why it rewrote one before shortening anything.

Descriptions don't affect ranking, but they do affect clicks. Make each one unique, specific, and an honest summary of what the page offers. Depending on the query, Google often shows page text instead.

Duplicates across pages usually come from a layout default. Fix the template so each page passes in its own values.

## Headings, images, and links

- One main heading that says what the page is about. Other headings follow the content's outline, not the font size someone wanted.
- Alt text describes what the image shows, in context. Use `alt=""` on decorative images so screen readers skip them. Don't stuff keywords into it.
- Descriptive file names help image search a little.
- Internal links: every page that should rank is linked from somewhere crawlable (orphan pages are hard to find), anchor text says where the link goes, and navigation and breadcrumbs use real `<a href>` links.
- Broken internal links: fix the link, or redirect the old URL if the page moved.

## Content quality

These checks need judgment, not a script.
- **Intent:** each page has one main purpose. If two pages target the same query (two near-identical posts, or a category page and a guide with the same title), merge them or make them clearly different.
- **Thin pages:** tag archives, empty category pages, auto-generated location pages, and placeholders with a few lines of text. Improve them, merge them, or noindex them on purpose.
- **Trust signals** (Google's E-E-A-T: experience, expertise, authoritativeness, trust): author names and bios on articles, an about page, contact details, sources for factual claims, and publish and updated dates on time-sensitive content. These matter most for health, money, and safety topics.
- **Freshness:** update old content that's wrong, or retire it. Don't bump dates without changing anything.

## Structured data

Structured data helps search engines understand a page and makes it eligible for some rich results. It doesn't boost rankings on its own.
- JSON-LD in a `<script type="application/ld+json">`, in the server's HTML. It has to parse and include `@context` and `@type`.
- It describes content that's visible on the page. Marking up reviews, FAQs, or prices the page doesn't show violates Google's spam policies.
- Use the most specific type that fits:
  - Home page: `Organization` (or `Person` for a personal site) with name, url, logo, and `sameAs` profile links, plus `WebSite`.
  - Articles: `Article`, `BlogPosting`, or `NewsArticle` with headline, image, datePublished, dateModified, and author (a `Person` with a name and url).
  - Products: `Product` with name, image, and an `Offer` (price, priceCurrency, availability). Add reviews and ratings only if they're real and shown on the page.
  - Deep pages: a `BreadcrumbList` that matches the visible breadcrumb.
  - Others where they fit: `LocalBusiness`, `Event`, `Recipe`, `VideoObject`, `SoftwareApplication`, `JobPosting`, `ProfilePage`.
- Validate with Google's Rich Results Test (it renders JavaScript) and the schema.org validator.
- Check the rendered page before recommending markup. CMS plugins and frameworks often inject JSON-LD with JavaScript.

## Link previews

Open Graph and Twitter Card tags control how a link looks when someone shares it. They don't affect ranking, so they're Low severity, but shared links bring in real traffic.
- `og:title`, `og:description`, `og:image` (an absolute URL, 1200×630, under about 5MB), `og:url` (the canonical), and `og:type`.
- `twitter:card` set to `summary_large_image` for a large image. X falls back to the og tags for everything else.
- Preview bots don't run JavaScript, so these tags have to be in the server's HTML.

## hreflang

Only for sites with the same content in more than one language or region.
- Every variant lists all the variants, itself included, and every link goes both ways. A link from A to B is ignored unless B links back to A.
- Codes are an ISO 639-1 language plus an optional ISO 3166-1 region (`en`, `en-GB`, `pt-BR`). `en-UK` is invalid; use `en-GB`.
- `x-default` points to the fallback page, often a language picker or the main language. It's recommended, not required.
- Every target returns 200, is indexable, and is its own canonical. Each locale's canonical points to itself. Pointing every locale's canonical at the English page tells Google to drop the others.
- Pick one method (head links, HTTP headers, or the sitemap). If you use more than one, they have to agree.
- Don't redirect visitors by IP or `Accept-Language`. Googlebot crawls mostly from the US without that header, so it would never see the other versions.

## AI crawlers

Each company runs separate bots for training and for search, and robots.txt controls them separately. Report the current policy and let the user decide. Don't change it on your own.

| Bot | Company | What it's for | Blocking it |
| --- | --- | --- | --- |
| GPTBot | OpenAI | Model training | Opts out of training only |
| OAI-SearchBot | OpenAI | ChatGPT search results | Removes pages from ChatGPT search answers |
| ChatGPT-User | OpenAI | Fetches a page a user asked about | Blocks those user-triggered fetches |
| ClaudeBot | Anthropic | Model training | Opts out of training only |
| Claude-SearchBot | Anthropic | Claude's search results | Reduces visibility in Claude's search |
| Claude-User | Anthropic | Fetches a page a user asked about | Blocks those user-triggered fetches |
| PerplexityBot | Perplexity | Perplexity's search index | Removes pages from Perplexity's index |
| Google-Extended | Google | Gemini training and grounding | Doesn't affect Google Search or AI Overviews (those use Googlebot) |
| Applebot-Extended | Apple | Apple Intelligence training | Doesn't affect Siri, Spotlight, or Safari (those use Applebot) |
| CCBot | Common Crawl | Open dataset used for training | Opts out of that dataset |
| Bytespider | ByteDance | Model training | Opts out of training only |

Vendors rename and add bots often, so check the vendor's own documentation before writing new rules. Some CDNs, Cloudflare among them, can block AI bots at the edge whatever robots.txt says. A site that allows a bot in robots.txt may still block it there, so ask the user if the results don't add up.

Common stances:
- **Open:** allow everything (no rules needed).
- **Search yes, training no:** disallow the training bots and allow the search and user-fetch bots.
- **Closed:** disallow all of them, accepting that the site won't appear in those assistants' answers.

What helps a site show up in AI answers is the same as what helps it in search: content in the server's HTML, clear headings, direct answers near the top of each section, accurate metadata, and a reputation elsewhere on the web. There's no proven AI-only markup.
