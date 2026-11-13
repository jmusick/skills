#!/usr/bin/env bash
# A released repo (v1.2.3) whose only remote is a bare repo inside the
# workspace, not GitHub, so issue_survey.py reports gh_ready false whether or
# not gh is logged in.
set -eu
hold="$(mktemp -d)"
cp -R "$(dirname "$0")/files/." .
git init -q -b main
git config user.email eval@example.com
git config user.name "Eval User"
git config core.autocrlf false
echo ".origin.git/" >> .git/info/exclude
echo "__pycache__/" >> .git/info/exclude
# The v1.2.3 tree: the changelog without the Unreleased entry, the old conversion.
mv CHANGELOG.md "$hold/CHANGELOG.next"
mv tidewater/tides.py "$hold/tides.next"
printf 'def feet_to_meters(feet):\n    """Convert a tide height in feet to meters, rounded to the centimeter."""\n    return round(abs(feet) * 0.3048, 2)\n' > tidewater/tides.py
sed '/^## \[Unreleased\]/,/^## \[1.2.3\]/{/^## \[1.2.3\]/!d}' "$hold/CHANGELOG.next" > CHANGELOG.md
git add -A
git commit -qm "v1.2.3 - Print heights for every argument"
git tag v1.2.3
mv "$hold/tides.next" tidewater/tides.py
mv "$hold/CHANGELOG.next" CHANGELOG.md
git commit -qam "Keep the sign of negative tide heights"
git init -q --bare -b main .origin.git
git remote add origin "$PWD/.origin.git"
git push -q -u origin main
git push -q origin v1.2.3
