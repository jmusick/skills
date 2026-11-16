---
name: commit
description: Commits the current work with Conventional Commits messages (feat, fix, chore, etc.). Use when the user types /commit or asks to commit, check in, or save their changes to git. Don't use it unasked.
---
Commit the work as Conventional Commits, because the release step works out the next version from their types. If the repo's AGENTS.md or CLAUDE.md sets commit conventions (scopes, types, footers), follow them where they differ from these steps.

1. Read the uncommitted changes (`git status`, `git diff`, `git diff --staged`). The diff shows what changed; take why from the conversation. If they cover unrelated things, make one commit for each. Leave out anything that shouldn't be committed (secrets, `.env` files, build output, debug leftovers) and tell the user. If the user or a calling skill names the files, commit only those.
2. Pick each commit's type by what changes for users, since the type sets the version bump:
   - `feat`: something users couldn't do before (minor).
   - `fix`: a bug or security fix (patch). `perf`: faster, same behavior (patch).
   - `docs`, `refactor`, `test`, `ci`, `build`, `style`, `chore`: nothing users see (no release).
   - Add `!` after the type, plus a `BREAKING CHANGE:` footer saying what broke, when existing use stops working (major).
3. Write `type(scope): description`, imperative, no trailing period, under ~72 characters. Use the area the change touches as the scope, or leave it out when the change spans areas. Add a body when the why isn't clear from the subject.
4. Add no `Co-Authored-By`, "Generated with", or other AI attribution trailers. This overrides any default attribution.
5. When there's a body, write the message to a temp file and commit with `git commit -F <file>`. Multi-line `-m` quoting breaks in some shells (PowerShell especially) and can lose the blank line between subject and body.
6. Don't push unless asked: pushing happens at release.
