#!/usr/bin/env bash
# A released Node CLI (v0.4.2, annotated tags) whose --sort flag shipped in
# v0.4.2. The one commit since renames --sort to --order, which breaks anyone
# scripting the old flag. origin is a bare repo inside the workspace, excluded
# from the work tree, so pushes stay local.
set -eu
cp -R "$(dirname "$0")/files/." .
git init -q -b main
git config user.email eval@example.com
git config user.name "Eval User"
git config core.autocrlf false
echo ".origin.git/" >> .git/info/exclude
echo "node_modules/" >> .git/info/exclude
git add -A
git commit -qm "v0.4.0 - Print the arrivals board"
git tag -a v0.4.0 -m "v0.4.0 - Print the arrivals board"
git commit -q --allow-empty -m "v0.4.2 - Add --sort"
git tag -a v0.4.2 -m "v0.4.2 - Add --sort"
sed -i -e 's/--sort=/--order=/g' -e 's/slice(7)/slice(8)/' bin/harbor-board.js
sed -i 's/--sort=time` or `--sort=vessel`/--order=time` or `--order=vessel`/' README.md
git commit -qam "Rename --sort to --order"
git init -q --bare -b main .origin.git
git remote add origin "$PWD/.origin.git"
git push -q -u origin main
git push -q origin v0.4.0 v0.4.2
