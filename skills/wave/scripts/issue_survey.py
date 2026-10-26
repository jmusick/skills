#!/usr/bin/env python3
"""Read-only survey for working a GitHub issue in the current repo.

Usage: python issue_survey.py [--issue N] [--limit 100]

Prints JSON: whether gh is ready, the repo and its default branch, merge
settings, rules that guard the default branch, the local checkout's state,
and open issues ranked for picking (or just issue N with --issue). Changes
nothing.
"""
import argparse
import json
import os
import re
import subprocess
import sys

PRIORITY = [
    (4, re.compile(r"(^|[^a-z])(p0|critical|urgent|blocker|sev[- ]?[01])([^a-z0-9]|$)")),
    (3, re.compile(r"(^|[^a-z])(p1|high)([^a-z0-9]|$)")),
    (2, re.compile(r"(^|[^a-z])(p2|medium|normal)([^a-z0-9]|$)")),
    (1, re.compile(r"(^|[^a-z])(p3|p4|low|minor|trivial)([^a-z0-9]|$)")),
]
DEFAULT_PRIORITY = 2
SKIP = re.compile(r"blocked|wontfix|won't fix|duplicate|invalid|on[- ]hold|stale|not planned|icebox")
NEEDS_INPUT = re.compile(r"question|discussion|needs[- ]?(design|decision|input|info|discussion|triage|spec)|proposal|rfc")
BUG = re.compile(r"bug|regression|defect|crash|(^|[^a-z])fix")
FEATURE = re.compile(r"enhancement|feature|improvement")
BREAKING = re.compile(r"breaking")


def run(*args):
    r = subprocess.run(list(args), capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.returncode, r.stdout.strip(), r.stderr.strip()


def gh_json(*args):
    code, out, err = run("gh", *args)
    if code != 0:
        return None, err or out
    try:
        return json.loads(out) if out else None, None
    except ValueError:
        return None, f"unparseable output from gh {' '.join(args)}"


def git(*args):
    code, out, _ = run("git", *args)
    return out if code == 0 else None


def checkout_state():
    top = git("rev-parse", "--show-toplevel")
    if not top:
        return {"in_git_repo": False}
    git_dir = git("rev-parse", "--git-dir") or ".git"
    ops = {name for name, marker in (("merge", "MERGE_HEAD"), ("rebase", "rebase-merge"), ("rebase", "rebase-apply"))
           if os.path.exists(os.path.join(git_dir, marker))}
    status = git("status", "--porcelain") or ""
    return {
        "in_git_repo": True,
        "toplevel": top,
        "current_branch": git("symbolic-ref", "--short", "-q", "HEAD"),
        "uncommitted_changes": [line for line in status.splitlines() if line],
        "in_progress_operation": sorted(set(ops)) or None,
        "worktrees": [line[len("worktree "):] for line in (git("worktree", "list", "--porcelain") or "").splitlines()
                      if line.startswith("worktree ")],
    }


def classify(issue, me, linked):
    labels = [l["name"] for l in issue.get("labels", [])]
    low = [l.lower() for l in labels]
    joined = " ".join(low)
    # Only labels that look like priority labels count, so "low-hanging fruit" isn't read as low priority.
    priority_labels = [l for l in low if "priority" in l or re.fullmatch(r"p\d|critical|urgent|blocker|sev[- ]?\d", l)]
    priority = next((score for score, pat in PRIORITY if any(pat.search(l) for l in priority_labels)), DEFAULT_PRIORITY)
    assignees = [a["login"] for a in issue.get("assignees", [])]
    reasons = []
    if any(SKIP.search(l) for l in low):
        reasons.append("skip label")
    if assignees and me not in assignees:
        reasons.append(f"assigned to {', '.join(assignees)}")
    if issue["number"] in linked:
        reasons.append(f"open PR #{linked[issue['number']]}")
    if BREAKING.search(joined):
        kind = "breaking"
    elif BUG.search(joined):
        kind = "bug"
    elif FEATURE.search(joined):
        kind = "feature"
    else:
        kind = "other"
    body = issue.get("body") or ""
    return {
        "number": issue["number"],
        "title": issue["title"],
        "url": issue["url"],
        "labels": labels,
        "kind": kind,
        "priority": priority,
        "needs_input": bool(NEEDS_INPUT.search(joined)) or not body.strip(),
        "assigned_to_me": me in assignees,
        "created_at": issue.get("createdAt"),
        "comments": len(issue.get("comments") or []),
        "body_chars": len(body),
        "body_preview": body[:400],
        "excluded": reasons or None,
    }


def linked_prs():
    """Map issue number -> open PR number, from closing references and branch names."""
    prs, err = gh_json("pr", "list", "--state", "open", "--limit", "200",
                       "--json", "number,headRefName,body,closingIssuesReferences")
    if prs is None:
        prs, err = gh_json("pr", "list", "--state", "open", "--limit", "200", "--json", "number,headRefName,body")
    linked = {}
    for pr in prs or []:
        nums = {ref["number"] for ref in pr.get("closingIssuesReferences") or []}
        nums |= {int(n) for n in re.findall(r"(?i)\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+#(\d+)", pr.get("body") or "")}
        m = re.search(r"(?i)issue[-_/]?(\d+)", pr.get("headRefName") or "")
        if m:
            nums.add(int(m.group(1)))
        for n in nums:
            linked.setdefault(n, pr["number"])
    return linked, err


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--issue", type=int)
    ap.add_argument("--limit", type=int, default=100)
    args = ap.parse_args()

    result = {"checkout": checkout_state()}

    code, out, err = run("gh", "auth", "status")
    if code != 0:
        result["gh_ready"] = False
        result["error"] = "gh is not installed or not logged in: " + (err or out)[:300]
        print(json.dumps(result, indent=2))
        return

    repo, err = gh_json("repo", "view", "--json",
                        "nameWithOwner,defaultBranchRef,viewerPermission,squashMergeAllowed,"
                        "mergeCommitAllowed,rebaseMergeAllowed,deleteBranchOnMerge")
    if repo is None:
        result["gh_ready"] = False
        result["error"] = "no GitHub repo for this checkout: " + (err or "")[:300]
        print(json.dumps(result, indent=2))
        return
    result["gh_ready"] = True
    nwo = repo["nameWithOwner"]
    default = (repo.get("defaultBranchRef") or {}).get("name")
    me_code, me, _ = run("gh", "api", "user", "--jq", ".login")
    me = me if me_code == 0 else None

    merge_methods = [m for m, key in (("squash", "squashMergeAllowed"), ("merge", "mergeCommitAllowed"),
                                      ("rebase", "rebaseMergeAllowed")) if repo.get(key)]
    rules, _ = gh_json("api", f"repos/{nwo}/rules/branches/{default}")
    branch, _ = gh_json("api", f"repos/{nwo}/branches/{default}")
    rule_types = sorted({r.get("type") for r in rules or [] if r.get("type")})
    protected = bool((branch or {}).get("protected"))
    result["repo"] = {
        "name": nwo,
        "default_branch": default,
        "viewer": me,
        "viewer_permission": repo.get("viewerPermission"),
        "can_push": repo.get("viewerPermission") in ("ADMIN", "MAINTAIN", "WRITE"),
        "merge_methods": merge_methods,
        "delete_branch_on_merge": repo.get("deleteBranchOnMerge"),
        "default_branch_protected": protected,
        "default_branch_rules": rule_types,
        # A pull_request rule or classic protection usually rejects the release push straight to the default branch.
        "direct_push_may_be_blocked": protected or "pull_request" in rule_types,
    }
    code, tags, _ = run("git", "tag", "--list", "v*")
    result["repo"]["has_release_tags"] = bool(tags.strip()) if code == 0 else None

    linked, pr_err = linked_prs()
    fields = "number,title,url,labels,assignees,body,createdAt,comments"
    if args.issue:
        issue, err = gh_json("issue", "view", str(args.issue), "--json", fields + ",state")
        if issue is None:
            result["error"] = f"could not read issue #{args.issue}: {err}"
        else:
            c = classify(issue, me, linked)
            c["state"] = issue.get("state")
            c["body_preview"] = (issue.get("body") or "")[:2000]
            result["issue"] = c
    else:
        issues, err = gh_json("issue", "list", "--state", "open", "--limit", str(args.limit), "--json", fields)
        if issues is None:
            result["error"] = f"could not list issues: {err}"
            issues = []
        ranked = [classify(i, me, linked) for i in issues]
        ok = [c for c in ranked if not c["excluded"]]
        # Highest priority first; within a priority, issues that can be done end to end; then oldest.
        ok.sort(key=lambda c: (-c["priority"], c["needs_input"], c["created_at"] or ""))
        result["open_issues"] = len(ranked)
        result["candidates"] = ok
        result["excluded"] = [{"number": c["number"], "title": c["title"], "why": c["excluded"]}
                              for c in ranked if c["excluded"]]
    if pr_err:
        result["warning"] = f"could not check open PRs for links: {pr_err[:200]}"
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    sys.exit(main())
