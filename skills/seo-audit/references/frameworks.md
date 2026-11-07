# Where SEO lives in common stacks

Find the stack from `package.json` and the config files, then read its section. A finding should point at the file that produces the problem, which is nearly always a shared layout, a head component, or a config file, not the page where you saw it.

## Astro

- **Head tags:** a layout in `src/layouts/` (often `BaseLayout.astro` or `Layout.astro`) renders `<head>`. Pages pass in `title`, `description`, and an image as props. Duplicate or generic titles usually mean a page doesn't pass its own, so the layout's default wins.
- **Site URL:** `site` in `astro.config.mjs`. Canonicals, sitemap URLs, and absolute `og:image` URLs need it. Build canonicals with `new URL(Astro.url.pathname, Astro.site)`. A missing or wrong `site` (localhost, or a preview domain) shows up as relative or wrong-host canonicals and sitemap entries.
- **Trailing slashes:** `trailingSlash` and `build.format` in the config decide whether `/about` or `/about/` is the real URL. Canonicals, internal links, and the sitemap should all use the one the host serves with a 200.
- **Sitemap:** the `@astrojs/sitemap` integration writes `sitemap-index.xml` and `sitemap-0.xml` at build time and needs `site` set. Its `filter` option keeps noindex pages, drafts, and admin routes out. Without the integration, look for `src/pages/sitemap.xml.ts`.
- **robots.txt:** `public/robots.txt`, or `src/pages/robots.txt.ts` when it's generated (for example, to block everything on staging). Check that the production build gets the production rules.
- **Rendering:** static output and `prerender = true` pages ship full HTML, which is good. With an adapter (`@astrojs/cloudflare`, `@astrojs/node`), on-demand pages render on the server and are fine too. Client-only islands (`client:only`) don't render on the server, so keep text that should rank out of them.
- **Images:** `<Image>` and `<Picture>` from `astro:assets` set width and height and output WebP or AVIF. A plain `<img>` in Markdown or a component doesn't.
- **404s:** `src/pages/404.astro`. Check the host returns a 404 status for unknown URLs, not a 200.
- **Structured data:** usually a `<script type="application/ld+json" set:html={JSON.stringify(data)} />` in the layout or page. Without `set:html`, Astro escapes the JSON and it won't parse.

## Vite with React, Vue, or Svelte (single-page apps)

- **Head tags:** `index.html` holds the only server-sent `<head>`, so every route gets the same title and description. Per-route tags set by hooks (`useEffect` writing `document.title`), `react-helmet`, `@unhead/vue`, or similar exist only after JavaScript runs. Google may pick them up when it renders; link previews and most AI crawlers never see them.
- **Content:** the server sends an empty `<div id="root">` or `<div id="app">`. The checker reports this as very little text in the raw HTML.
- **Fixes**, from least to most work:
  1. Give `index.html` an accurate site-wide title, description, and og tags, so the fallback is at least right.
  2. Prerender the public routes at build time (React Router's `prerender` option in framework mode, `vite-ssg` for Vue, `vite-plugin-ssr`/Vike, or a prerender plugin). Each route then ships its own HTML and head.
  3. Move the public pages (home, pricing, docs, blog) to a static or server-rendered framework and keep the SPA for the logged-in app.
- **robots.txt and sitemap:** `public/robots.txt` is copied as is. A sitemap needs a build script or plugin, since nothing generates one by default.
- **Host rewrites:** an SPA fallback (`/* /index.html 200` in `_redirects`, `rewrites` in `vercel.json`, `not_found_handling = "single-page-application"` on Cloudflare) makes every unknown URL return 200 with the app shell. That turns real 404s into soft 404s, and if robots.txt or the sitemap is missing, those URLs return HTML too. Return a 404 status for unknown routes where the host allows it, and make sure the real files exist.

## Next.js

- **App Router:** `export const metadata` or `generateMetadata()` in `layout.tsx` and `page.tsx`. Set `metadataBase` in the root layout so relative URLs become absolute. Canonicals go in `alternates.canonical`, hreflang in `alternates.languages`, and robots in `robots: { index: false }`. Child pages that don't set a title inherit the parent's, which shows up as duplicate titles. Use `title.template` in the root layout.
- **Sitemap and robots:** `app/sitemap.ts` and `app/robots.ts`, or static files in `public/`.
- **Missing pages:** `notFound()` returns a real 404. Check dynamic routes call it when the record doesn't exist, rather than rendering an empty page with a 200.
- **Pages Router:** `next/head` in each page or a shared `_app`/layout component. Data from `getStaticProps` or `getServerSideProps` is in the server HTML; data fetched in `useEffect` isn't.
- **Images:** `next/image` sets dimensions. Use `priority` on the main above-the-fold image.

## Static sites and other generators

- **Plain HTML:** every page has its own `<head>`, so problems repeat wherever a page was copied from another. Fix each file, or move the head into a shared include if the project has one.
- **Hugo:** `baseURL` in the config and `layouts/partials/head.html` (or the theme's equivalent). `enableRobotsTXT = true` generates robots.txt. The sitemap is built in.
- **Eleventy:** a base layout in `_includes/` builds the head. The sitemap and robots.txt are usually templates (`sitemap.njk`, `robots.njk`) or a plugin.
- **Jekyll:** `_includes/head.html`, `url` in `_config.yml`, and the `jekyll-seo-tag` and `jekyll-sitemap` plugins.
- **WordPress and other CMSs:** an SEO plugin (Yoast, Rank Math, AIOSEO) usually sets titles, canonicals, the sitemap, and JSON-LD. Fix things in its settings or the theme, not by editing generated HTML, and check the rendered page because some of it is injected with JavaScript.
