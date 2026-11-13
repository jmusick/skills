# AGENTS.md

Firelands Current is a local news site for Erie, Huron, Ottawa, and Sandusky counties, Ohio.

- Stories and events live in the D1 database. Local dev uses the copy under `.wrangler/`.
- Getting a story live (only after the editor says so): `npm run import:local -- <packet>`, then `npm run sync:remote`.
- Never run a `--remote` command without the editor's go-ahead.
