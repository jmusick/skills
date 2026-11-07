"""Offline tests for scripts/issue_survey.py. Run: python -m unittest discover -s <this folder>

They cover the logic that decides which issues a run picks or skips. Nothing here calls
gh, git, or the network; `run` and `gh_json` are replaced where a function needs them.
"""
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import issue_survey as s  # noqa: E402


def issue(n=1, labels=(), assignees=(), comments=(), body="Steps to reproduce"):
    return {"number": n, "title": "t", "url": "u", "body": body, "createdAt": "2026-01-01",
            "labels": [{"name": l} for l in labels],
            "assignees": [{"login": a} for a in assignees],
            "comments": [{"body": c} for c in comments]}


MINE = {"number": 9, "branch": "issue-1-fix", "author": "me", "draft": True}
THEIRS = {"number": 8, "branch": "fix", "author": "bob", "draft": False}


class Classify(unittest.TestCase):
    def test_own_pr_excluded_from_ranking_but_resumable(self):
        c = s.classify(issue(), "me", {1: MINE})
        self.assertEqual(c["resume"], MINE)
        self.assertIn("/issue 1 resumes it", c["excluded"][0])

    def test_own_pr_not_excluded_when_named(self):
        c = s.classify(issue(), "me", {1: MINE}, single=True)
        self.assertIsNone(c["excluded"])
        self.assertEqual(c["resume"], MINE)

    def test_someone_elses_pr_always_excluded(self):
        for single in (False, True):
            c = s.classify(issue(), "me", {1: THEIRS}, single=single)
            self.assertEqual(c["excluded"], ["open PR #8"])
            self.assertIsNone(c["resume"])

    def test_unknown_viewer_never_resumes(self):
        c = s.classify(issue(), None, {1: MINE})
        self.assertIsNone(c["resume"])
        self.assertEqual(c["excluded"], ["open PR #9"])

    def test_waiting_marker_on_latest_comment_excludes(self):
        c = s.classify(issue(comments=["Need a decision\n" + s.WAITING_MARKER]), "me", {})
        self.assertTrue(c["awaiting_reply"])
        self.assertTrue(c["excluded"])

    def test_reply_after_marker_clears_it(self):
        c = s.classify(issue(comments=["Need a decision\n" + s.WAITING_MARKER, "Use option B"]), "me", {})
        self.assertFalse(c["awaiting_reply"])
        self.assertIsNone(c["excluded"])

    def test_marker_does_not_exclude_named_issue(self):
        c = s.classify(issue(comments=[s.WAITING_MARKER]), "me", {}, single=True)
        self.assertTrue(c["awaiting_reply"])
        self.assertIsNone(c["excluded"])

    def test_assigned_to_others_excluded_but_not_to_me(self):
        self.assertEqual(s.classify(issue(assignees=["bob"]), "me", {})["excluded"], ["assigned to bob"])
        c = s.classify(issue(assignees=["me"]), "me", {})
        self.assertIsNone(c["excluded"])
        self.assertTrue(c["assigned_to_me"])

    def test_skip_label_excluded(self):
        self.assertEqual(s.classify(issue(labels=["wontfix"]), "me", {})["excluded"], ["skip label"])

    def test_priority_comes_only_from_priority_labels(self):
        self.assertEqual(s.classify(issue(labels=["priority: high"]), "me", {})["priority"], 3)
        self.assertEqual(s.classify(issue(labels=["P0"]), "me", {})["priority"], 4)
        # "low-hanging fruit" isn't a priority label, so it keeps the default.
        self.assertEqual(s.classify(issue(labels=["low-hanging fruit"]), "me", {})["priority"], s.DEFAULT_PRIORITY)

    def test_empty_body_needs_input(self):
        self.assertTrue(s.classify(issue(body=""), "me", {})["needs_input"])
        self.assertTrue(s.classify(issue(labels=["needs-design"]), "me", {})["needs_input"])
        self.assertFalse(s.classify(issue(), "me", {})["needs_input"])


class LinkedPrs(unittest.TestCase):
    def test_links_by_closing_reference_body_and_branch(self):
        prs = [
            {"number": 10, "headRefName": "feature", "body": "", "author": {"login": "me"}, "isDraft": False,
             "closingIssuesReferences": [{"number": 1}]},
            {"number": 11, "headRefName": "x", "body": "Fixes #2", "author": {"login": "bob"}, "isDraft": True,
             "closingIssuesReferences": []},
            {"number": 12, "headRefName": "issue-3-thing", "body": "", "author": {"login": "me"}, "isDraft": True,
             "closingIssuesReferences": []},
        ]
        with mock.patch.object(s, "gh_json", return_value=(prs, None)):
            linked, err = s.linked_prs()
        self.assertIsNone(err)
        self.assertEqual({n: pr["number"] for n, pr in linked.items()}, {1: 10, 2: 11, 3: 12})
        self.assertEqual(linked[3], {"number": 12, "branch": "issue-3-thing", "author": "me", "draft": True})


class ReleaseTags(unittest.TestCase):
    def fake_run(self, local, remote, remote_code=0):
        def run(*args):
            if args[:2] == ("git", "tag"):
                return 0, local, ""
            return remote_code, remote, ""
        return run

    def test_tags_with_and_without_v(self):
        for tags in ("v1.2.3", "1.2.3", "notes\n2.0.0"):
            with mock.patch.object(s, "run", self.fake_run(tags, "")):
                self.assertTrue(s.has_release_tags(), tags)

    def test_non_semver_tags_dont_count(self):
        with mock.patch.object(s, "run", self.fake_run("v1.2\nrelease-1", "")):
            self.assertFalse(s.has_release_tags())

    def test_falls_back_to_origin(self):
        remote = "abc\trefs/tags/v0.1.0\nabc\trefs/tags/v0.1.0^{}"
        with mock.patch.object(s, "run", self.fake_run("", remote)):
            self.assertTrue(s.has_release_tags())

    def test_unreadable_origin_with_no_local_tags_is_false(self):
        with mock.patch.object(s, "run", self.fake_run("", "", remote_code=128)):
            self.assertFalse(s.has_release_tags())


class RequiredApprovals(unittest.TestCase):
    PR_RULE = [{"type": "pull_request", "parameters": {"required_approving_review_count": 2}}]

    def test_ruleset_count(self):
        self.assertEqual(s.required_approvals(self.PR_RULE, False, None), 2)

    def test_no_rules_unprotected(self):
        self.assertEqual(s.required_approvals([], False, None), 0)
        self.assertEqual(s.required_approvals(None, False, None), 0)

    def test_pull_request_rule_without_approvals(self):
        rules = [{"type": "pull_request", "parameters": {"required_approving_review_count": 0}}]
        self.assertEqual(s.required_approvals(rules, False, None), 0)

    def test_classic_protection_read(self):
        self.assertEqual(s.required_approvals([], True, {"required_approving_review_count": 1}), 1)
        self.assertEqual(s.required_approvals([], True, {}), 0)

    def test_classic_protection_unreadable(self):
        self.assertIsNone(s.required_approvals([], True, None))
        # A ruleset that already requires review answers the question anyway.
        self.assertEqual(s.required_approvals(self.PR_RULE, True, None), 2)


if __name__ == "__main__":
    unittest.main()
