# Checking a privacy policy

A privacy policy is a promise to users, so check it against what the code does, not against what the project means to do. Read the policy first and list its claims: what's collected, which services get it, what's stored on the device, how long it's kept, and who to contact.

## Where to look

Start with the manifests (`package.json`, `requirements.txt`, `pyproject.toml`, `Gemfile`, `go.mod`, `Cargo.toml`, `Podfile`, `build.gradle`), because a dependency is the fastest sign that a service is in use. Then search the source, templates, and config for the signatures below. Env var names give services away too: `*_DSN`, `*_WRITE_KEY`, `NEXT_PUBLIC_*_ID`, `VITE_*_KEY`. Check `.env.example`, deploy config, and CI secrets lists.

A dependency that's installed but never imported isn't sending anything. Confirm the call site before saying data goes somewhere.

| What | Signatures to search for |
| --- | --- |
| Analytics | `gtag(`, `googletagmanager.com`, `google-analytics.com`, `@vercel/analytics`, `plausible`, `posthog`, `mixpanel`, `@segment/`, `analytics.track`, `amplitude`, `heap`, `umami`, `fathom`, `matomo`, `_paq`, `cloudflareinsights`, `clarity.ms` |
| Session replay and heatmaps | `hotjar`, `fullstory`, `logrocket`, `smartlook`, `mouseflow`, `posthog` with `session_recording` |
| Ad and social pixels | `fbq(`, `connect.facebook.net`, `snap.licdn.com`, `ttq.`, `twq(`, `adsbygoogle`, `googlesyndication`, `doubleclick` |
| Error reporting and logs | `@sentry/`, `Sentry.init`, `bugsnag`, `rollbar`, `@datadog/`, `dd-trace`, `newrelic`, `honeybadger`, `logtail`, `axiom`, request loggers (`morgan`, `pino-http`), IP capture (`x-forwarded-for`, `req.ip`) |
| Accounts and auth | `next-auth`, `@auth/`, `@clerk/`, `auth0`, `firebase/auth`, `supabase`, `passport`, `lucia`, OAuth scopes requested |
| Payments | `stripe`, `paypal`, `paddle`, `lemonsqueezy`, `braintree` |
| Email, SMS, newsletters | `resend`, `@sendgrid/`, `mailgun`, `postmark`, `nodemailer`, `@aws-sdk/client-ses`, `mailchimp`, `convertkit`, `buttondown`, `twilio` |
| AI and other APIs sent user content | `openai`, `@anthropic-ai/sdk`, `anthropic`, `google-generativeai`, `@google/genai`, `cohere`, `replicate`, any `fetch(` to a third-party host with form or user data in the body |
| Embeds and widgets | `youtube.com/embed` (not `youtube-nocookie.com`), `maps.googleapis.com`, `fonts.googleapis.com`, `recaptcha`, `hcaptcha`, `turnstile`, `intercom`, `crisp`, `zendesk`, `drift`, `hs-scripts`, `disqus`, `typeform`, `calendly` |
| Mobile SDKs | Firebase Analytics, Crashlytics, `appsflyer`, `adjust`, `branch`, `onesignal`, push token registration |
| Storage on the device | `document.cookie`, `Set-Cookie`, `res.cookie(`, `cookies()`, `localStorage`, `sessionStorage`, `indexedDB`, service worker caches |
| What's collected | form fields (`<input name=`, `type="email"`, `type="tel"`), database schemas and migrations (`schema.prisma`, `models.py`, `migrations/`), `navigator.geolocation`, `getUserMedia`, file uploads |
| Retention | TTLs, cleanup and purge jobs, cron schedules, log retention settings, backup config |
| Hosting | `vercel.json`, `netlify.toml`, `wrangler.toml`, `fly.toml`, `render.yaml`: the host sees request logs and IPs |

## What to compare

- **Services:** every service the code sends user data to is named, and every named service is still in the code.
- **Cookies and storage:** what the policy says is stored on the device matches the cookies and storage keys the code sets, including ones set by third-party scripts.
- **Data collected:** the policy's list matches the form fields, account fields, and schema columns.
- **Retention:** each stated period has something in the code or config that enforces it. If nothing does, the code can't confirm the claim, so flag it.
- **Contact:** the contact address matches the one the project uses elsewhere (README, site footer, `SECURITY.md`).

## Fix or flag

- **Fix directly** the factual lists the code settles, like naming a service the code now sends data to or dropping one it no longer uses. Change the "last updated" date only when the content changes.
- **Flag, don't edit,** anything that changes a commitment (what's collected, shared, sold, or kept, and for how long) or that the code can't confirm. Put it under "Needs your call" with the evidence (file:line), the policy line it contradicts, and suggested wording. The user decides, and may want a lawyer to.
