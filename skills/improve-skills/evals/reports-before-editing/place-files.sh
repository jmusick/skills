#!/usr/bin/env bash
# A two-skill catalog with house rules in AGENTS.md. tide-report is
# model-invocable on purpose (buoy-alert calls it), but its description can't
# trigger, it links a references/format.md that doesn't exist, and it opens with
# generic advice. buoy-alert follows the house rules and should be a Keep.
set -eu
cp -R "$(dirname "$0")/files/." .
# Fixture skills are stored as *.fixture so the eval runner and skill loaders
# don't mistake them for this repo's own skills and eval cases.
find . -name "*.fixture" -type f | while read -r f; do mv "$f" "${f%.fixture}"; done
git init -q -b main
git config user.email eval@example.com
git config user.name "Eval User"
git config core.autocrlf false
git add -A
git commit -qm "Add tide-report and buoy-alert"
