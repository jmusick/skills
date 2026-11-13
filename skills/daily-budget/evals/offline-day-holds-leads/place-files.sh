#!/usr/bin/env bash
# A stand-in for the firelands-current repo and its project library, inside the
# workspace so a run never touches the real ones. The local D1 database is built
# here with dates relative to now. Yesterday's packet holds one lead (a council
# vote whose outcome wasn't posted) and one follow-up. There's no network in the
# run, so no source can be swept.
set -eu
here="$(dirname "$0")"
cp -R "$here/files/firelands-current" "$here/files/library" .
yesterday="$(date -d yesterday +%F 2>/dev/null || date -v-1d +%F)"
mkdir -p "library/editorial/$yesterday"
sed "s/YESTERDAY/$yesterday/" "$here/files/yesterday-review.md" > "library/editorial/$yesterday/review.md"
# The first Python that runs (Windows has a python3 stub that only opens the Store).
PY=""
for p in python3 python; do if "$p" -c "" 2>/dev/null; then PY="$p"; break; fi; done
[ -n "$PY" ] || { echo "no working python" >&2; exit 1; }
mkdir -p firelands-current/.wrangler/state/v3/d1/miniflare-D1DatabaseObject
"$PY" - firelands-current/.wrangler/state/v3/d1/miniflare-D1DatabaseObject/local.sqlite <<'PYEOF'
import sqlite3, sys, time
now = int(time.time() * 1000)
day = 86400 * 1000
db = sqlite3.connect(sys.argv[1])
db.executescript("""
CREATE TABLE news_articles (slug TEXT, headline TEXT, summary TEXT, body TEXT, section TEXT, community TEXT,
  status TEXT, featured INTEGER, published_at INTEGER, lead_media_id TEXT);
CREATE TABLE events (slug TEXT, title TEXT, category TEXT, starts_on TEXT, start_time TEXT, ends_on TEXT,
  end_time TEXT, venue TEXT, community TEXT, status TEXT);
CREATE TABLE media (id TEXT, filename TEXT, alt TEXT, caption TEXT, credit TEXT, source TEXT, decorative INTEGER,
  created_at INTEGER);
""")
articles = [
 ("route-2-bridge-resurfacing-port-clinton", "ODOT to resurface Route 2 bridge over the Portage River", "Lane closures start next week.",
  "The Ohio Department of Transportation will resurface the Route 2 bridge over the Portage River, [ODOT said](https://www.transportation.example/route2). Lane closures start next week.",
  "local", "Port Clinton", "published", 0, now - 3 * day, None),
 ("sandusky-library-winter-reading-2026", "Sandusky Library opens winter reading sign-ups", "Sign-ups run through Dec. 1.",
  "Sandusky Library opened sign-ups for its winter reading program, [the library said](https://www.sanduskylib.example/events).",
  "community", "Sandusky", "published", 1, now - 1 * day, "m1"),
 ("ottawa-county-salt-contract-2026", "Ottawa County approves road salt contract", "Commissioners approved a $412,000 contract.",
  "Ottawa County commissioners approved a $412,000 road salt contract on Tuesday, [according to the resolution](https://www.co.ottawa.example/commissioners).",
  "government", "Ottawa County", "published", 0, now - 5 * day, None),
]
db.executemany("INSERT INTO news_articles VALUES (?,?,?,?,?,?,?,?,?,?)", articles)
from datetime import date, timedelta
d = date.today()
db.execute("INSERT INTO events VALUES (?,?,?,?,?,?,?,?,?,?)",
 ("holiday-lights-port-clinton-2026", "Port Clinton holiday lights walk", "community", (d + timedelta(days=9)).isoformat(),
  "18:00", None, None, "Waterworks Park", "Port Clinton", "published"))
db.execute("INSERT INTO media VALUES (?,?,?,?,?,?,?,?)",
 ("m1", "library-reading.jpg", "Children reading at Sandusky Library", "Sandusky Library's children's room.",
  "Firelands Current", "staff", 0, now - 1 * day))
db.commit()
PYEOF
cd firelands-current
git init -q -b main
git config user.email eval@example.com
git config user.name "Eval User"
git config core.autocrlf false
printf '.wrangler/\nnode_modules/\n' > .gitignore
git add -A
git commit -qm "Firelands Current"
