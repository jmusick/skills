---
name: commit
description: Commits the current work with Conventional Commits messages (feat, fix, chore, etc.). Use when the user types /commit or asks to commit, check in, or save their changes to git. Don't use it unasked.
---
Commit the work as Conventional Commits, because the release step works out the next version from their types.

1. Read the uncommitted changes (`git status`, `git diff`, `git diff --staged`). If they cover unrelated things, make one commit for each. Leave out anything that shouldn't be committed (secrets, `.env` files, build output, debug leftovers) and tell the user.
2. Pick each commit's type by what changes for users, since the type sets the version bump:
   - `feat`: something users couldn't do before (minor).
   - `fix`: a bug or security fix (patch). `perf`: faster, same behavior (patch).
   - `docs`, `refactor`, `test`, `ci`, `build`, `style`, `chore`: nothing users see (no release).
   - Add `!` after the type, plus a `BREAKING CHANGE:` footer saying what broke, when existing use stops working (major).
3. Write `type(scope): description`, imperative, no trailing period, under ~72 characters. Use the area the change touches as the scope (in a skills repo, the skill name), or leave it out when the change spans areas. Add a body when the why isn't clear from the subject.
4. Commit, and don't push unless asked: pushing happens at release.
