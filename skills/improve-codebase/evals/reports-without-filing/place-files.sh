#!/usr/bin/env bash
set -eu
cp -R "$(dirname "$0")/files/." .
# Give hotspots.py some history: totals.py keeps getting rounding fixes.
git init -q
git config user.email eval@example.com
git config user.name eval
git add -A
git commit -qm "Add invoice tool"
for n in 1 2 3; do
  echo "# Rounding note $n: tax is rounded half up per line." >> invoices/totals.py
  git commit -qam "Fix tax rounding on discounted lines ($n)"
done
echo "# Layout follows the 2025 template." >> invoices/format.py
git commit -qam "Tweak invoice layout"
