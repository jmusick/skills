#!/usr/bin/env bash
# lakefront-api at v0.3.0 plus two commits: GET /health was added and
# scripts/seed.sh was removed. The docs were never updated, so the README has
# the wrong dev script, port default, and endpoint list, AGENTS.md still points
# at seed.sh, docs/setup-old.md duplicates the README's setup with stale facts,
# and the changelog has nothing under Unreleased. On top, the user has an
# uncommitted rename of LAKE_API_KEY to LAKEFRONT_API_KEY in src/config.js.
set -eu
cp -R "$(dirname "$0")/files/." .
git init -q -b main
git config user.email eval@example.com
git config user.name "Eval User"
git config core.autocrlf false
echo "node_modules/" > .gitignore
# The v0.3.0 tree: no /health, seed.sh present.
mkdir -p scripts
printf '#!/usr/bin/env bash\ncp data/tides.sample.json data/tides.json\n' > scripts/seed.sh
sed -i '/\/health/d' src/server.js
git add -A
git commit -qm "v0.3.0 - Serve the tide table"
git tag v0.3.0
cp "$(dirname "$0")/files/src/server.js" src/server.js
git commit -qam "Add GET /health for the load balancer"
git rm -q scripts/seed.sh
git commit -qm "Remove seed script; data loads from data/tides.json"
# The user's uncommitted change: the env var is renamed.
sed -i 's/process.env.LAKE_API_KEY/process.env.LAKEFRONT_API_KEY/' src/config.js
