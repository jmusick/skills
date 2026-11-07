#!/usr/bin/env python3
"""Read-only survey for working a GitHub issue in the current repo.

Usage: python issue_survey.py [--issue N] [--limit 100]

Prints JSON: whether gh is ready, the repo and its default branch, merge
settings, rules that guard the default branch, the local checkout's state,
and open issues ranked for picking (or just issue N with --issue). Changes
nothing.

An issue whose open PR is the viewer's own carries `resume` (and with --issue
isn't excluded), so an earlier run's work can be picked back up. An issue
whose latest comment carries WAITING_MARKER is excluded from the ranking: an
earlier run left it waiting on a reply, and a loop shouldn't retry it.
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
SEMVER_TAG = re.compile(r"^v?\d+\.\d+\.\d+$")
# The issue and wave skills end the comment they leave on an issue they couldn't do with this.
WAITING_MARKER = "<!-- agent-waiting-for-reply -->"


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


def classify(issue, me, linked, single=False):
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
    pr = linked.get(issue["number"])
    resume = None
    if pr and me and pr["author"] == me:
        resume = pr
        if not single:
            reasons.append(f"your open PR #{pr['number']}; /issue {issue['number']} resumes it")
    elif pr:
        reasons.append(f"open PR #{pr['number']}")
    comments = issue.get("comments") or []
    waiting = bool(comments) and WAITING_MARKER in (comments[-1].get("body") or "")
    if waiting and not single:
        reasons.append("waiting on a reply to an earlier run's comment")
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
        "comments": len(comments),
        "awaiting_reply": waiting,
        "resume": resume,
        "body_chars": len(body),
        "body_preview": body[:400],
        "excluded": reasons or None,
    }


def linked_prs():
    """Map issue number -> its open PR, from closing references and branch names."""
    fields = "number,headRefName,body,author,isDraft"
    prs, err = gh_json("pr", "list", "--state", "open", "--limit", "200",
                       "--json", fields + ",closingIssuesReferences")
    if prs is None:
        prs, err = gh_json("pr", "list", "--state", "open", "--limit", "200", "--json", fields)
    linked = {}
    for pr in prs or []:
        nums = {ref["number"] for ref in pr.get("closingIssuesReferences") or []}
        nums |= {int(n) for n in re.findall(r"(?i)\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+#(\d+)", pr.get("body") or "")}
        m = re.search(r"(?i)issue[-_/]?(\d+)", pr.get("headRefName") or "")
        if m:
            nums.add(int(m.group(1)))
        info = {"number": pr["number"], "branch": pr.get("headRefName"),
                "author": (pr.get("author") or {}).get("login"), "draft": pr.get("isDraft")}
        for n in nums:
            linked.setdefault(n, info)
    return linked, err


def has_release_tags():
    """Whether any semver tag (v1.2.3 or 1.2.3) exists locally or on origin; None if neither could be read."""
    code, out, _ = run("git", "tag", "--list")
    if code == 0 and any(SEMVER_TAG.match(t) for t in out.splitlines()):
        return True
    remote_code, remote, _ = run("git", "ls-remote", "--tags", "origin")
    if remote_code == 0:
        names = (line.split("refs/tags/", 1)[-1] for line in remote.splitlines())
        return any(SEMVER_TAG.match(n[:-3] if n.endswith("^{}") else n) for n in names)
    return False if code == 0 else None


def required_approvals(rules, protected, classic_reviews):
    """Approving reviews a PR into the default branch needs, or None if it couldn't be read.

    `rules` is the rules/branches response (readable by any collaborator). Classic branch
    protection's review settings usually need admin to read, so `classic_reviews` is None
    when that read failed; it only matters when the branch is protected.
    """
    counts = [(r.get("parameters") or {}).get("required_approving_review_count") or 0
              for r in rules or [] if r.get("type") == "pull_request"]
    if protected:
        if classic_reviews is None:
            return max(counts) if any(counts) else None
        counts.append(classic_reviews.get("required_approving_review_count") or 0)
    return max(counts, default=0)


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
    classic_reviews = None
    if protected:
        classic_reviews, _ = gh_json("api", f"repos/{nwo}/branches/{default}/protection/required_pull_request_reviews")
        # An admin can always read it, so a failed read there means no review rule is set.
        if classic_reviews is None and repo.get("viewerPermission") == "ADMIN":
            classic_reviews = {}
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
        # Approving reviews a PR needs before merge; None means protection exists but couldn't be read.
        # GitHub doesn't let a PR's author approve it, so any nonzero count stops the run at merge.
        "required_approvals": required_approvals(rules, protected, classic_reviews),
        # A pull_request rule or classic protection usually rejects the release push straight to the default branch.
        "direct_push_may_be_blocked": protected or "pull_request" in rule_types,
    }
    result["repo"]["has_release_tags"] = has_release_tags()

    linked, pr_err = linked_prs()
    fields = "number,title,url,labels,assignees,body,createdAt,comments"
    if args.issue:
        issue, err = gh_json("issue", "view", str(args.issue), "--json", fields + ",state")
        if issue is None:
            result["error"] = f"could not read issue #{args.issue}: {err}"
        else:
            c = classify(issue, me, linked, single=True)
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
