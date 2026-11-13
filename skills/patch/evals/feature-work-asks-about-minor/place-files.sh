#!/usr/bin/env bash
# A released repo (v1.2.3, lightweight tag) with one feature (--json) committed
# since the tag and listed under Unreleased. origin is a bare repo inside the
# workspace, excluded from the work tree, so pushes stay local.
set -eu
hold="$(mktemp -d)"
cp -R "$(dirname "$0")/files/." .
git init -q -b main
git config user.email eval@example.com
git config user.name "Eval User"
git config core.autocrlf false
echo ".origin.git/" >> .git/info/exclude
echo "__pycache__/" >> .git/info/exclude
# The v1.2.3 tree: the changelog without the Unreleased entry, the CLI without --json.
mv CHANGELOG.md "$hold/CHANGELOG.next"
mv tidewater/cli.py "$hold/cli.next"
cat > tidewater/cli.py <<'PY'
import sys

from tidewater.tides import feet_to_meters


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    for arg in argv:
        print(f"{arg} ft = {feet_to_meters(float(arg))} m")
    return 0
PY
sed '/^## \[Unreleased\]/,/^## \[1.2.3\]/{/^## \[1.2.3\]/!d}' "$hold/CHANGELOG.next" > CHANGELOG.md
git add -A
git commit -qm "v1.2.3 - Print heights for every argument"
git tag v1.2.3
mv "$hold/cli.next" tidewater/cli.py
mv "$hold/CHANGELOG.next" CHANGELOG.md
git commit -qam "Add --json output"
git init -q --bare -b main .origin.git
git remote add origin "$PWD/.origin.git"
git push -q -u origin main
git push -q origin v1.2.3
