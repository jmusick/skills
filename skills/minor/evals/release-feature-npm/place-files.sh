#!/usr/bin/env bash
# A released Node CLI (v0.4.2, annotated tags, no changelog). The --sort option
# is written but uncommitted. package.json keeps "files" on one line, which
# `npm version` would reformat. origin is a bare repo inside the workspace,
# excluded from the work tree, so pushes stay local.
set -eu
hold="$(mktemp -d)"
cp -R "$(dirname "$0")/files/." .
git init -q -b main
git config user.email eval@example.com
git config user.name "Eval User"
git config core.autocrlf false
echo ".origin.git/" >> .git/info/exclude
echo "node_modules/" >> .git/info/exclude
# The v0.4.2 tree: no --sort, no sort test, README without it.
mv lib/board.js bin/harbor-board.js test/board.test.js README.md "$hold/"
cat > lib/board.js <<'JS'
function formatBoard(arrivals) {
  return arrivals.map((r) => `${r.time}  ${r.vessel}`).join("\n");
}

module.exports = { formatBoard };
JS
cat > bin/harbor-board.js <<'JS'
#!/usr/bin/env node
const { formatBoard } = require("../lib/board");

const arrivals = [
  { time: "14:10", vessel: "Lady Kelleys" },
  { time: "09:45", vessel: "Erie Wind" },
];
console.log(formatBoard(arrivals));
JS
sed '/^test("sorts by time"/,$d' "$hold/board.test.js" > test/board.test.js
printf '# harbor-board\n\nPrints the day'"'"'s harbor arrivals.\nRun the tests with `npm test`.\n' > README.md
git add -A
git commit -qm "v0.4.0 - Print the arrivals board"
git tag -a v0.4.0 -m "v0.4.0 - Print the arrivals board"
git commit -q --allow-empty -m "v0.4.2 - Fix vessel name padding"
git tag -a v0.4.2 -m "v0.4.2 - Fix vessel name padding"
git init -q --bare -b main .origin.git
git remote add origin "$PWD/.origin.git"
git push -q -u origin main
git push -q origin v0.4.0 v0.4.2
cp "$hold/board.js" lib/board.js
cp "$hold/harbor-board.js" bin/harbor-board.js
cp "$hold/board.test.js" test/board.test.js
cp "$hold/README.md" README.md
