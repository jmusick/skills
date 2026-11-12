"""Offline tests for scripts/jobs.py. Run: python -m unittest discover -s <this folder>

They cover the logic that decides whether a posting was already seen and which
applications have gone quiet. Records are written to a temporary folder.
"""
import datetime as dt
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import jobs  # noqa: E402


def record(**fields):
    base = {"company": "Acme Health, LLC", "role": "Senior Java Engineer", "status": "found"}
    base.update(fields)
    lines = ["---"] + [f"{k}: {v}" for k, v in base.items()] + ["---", "", "## Why", "x"]
    return "\n".join(lines) + "\n"


class Folder(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = self.tmp.name

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, name, text):
        with open(os.path.join(self.dir, name), "w", encoding="utf-8") as f:
            f.write(text)

    def records(self):
        return jobs.load(self.dir)


class Load(Folder):
    def test_reads_records_and_reports_unreadable(self):
        self.write("acme-health-senior-java-engineer.md", record(pay="$130k  # posted"))
        self.write("notes.md", "no front matter here")
        self.write("README.md", "# readme")
        records, skipped = self.records()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["pay"], "$130k")
        self.assertEqual(skipped, ["notes.md"])

    def test_blank_values_are_none(self):
        self.write("a.md", record(applied=""))
        records, _ = self.records()
        self.assertIsNone(records[0]["applied"])


class Match(Folder):
    def setUp(self):
        super().setUp()
        self.write("acme.md", record(
            board_url="https://www.linkedin.com/jobs/view/4012345678/",
            url="https://acme.wd5.myworkdayjobs.com/careers/job/Remote/Senior-Java-Engineer_R123",
            status="applied"))
        self.write("clear.md", record(company="ClearCaptions, LLC", role="Software Developer",
                                      job_id="indeed:56589689ac7e155e", status="rejected"))
        self.recs, _ = self.records()

    def hit(self, **posting):
        return jobs.match(self.recs, posting)

    def test_linkedin_id_from_slugged_url(self):
        r = self.hit(url="https://www.linkedin.com/jobs/view/senior-java-engineer-at-acme-4012345678?trk=abc")
        self.assertEqual(r["matches"][0]["file"], "acme.md")
        self.assertIn("job id", r["matches"][0]["matched_on"])

    def test_linkedin_current_job_id_param(self):
        r = self.hit(url="https://www.linkedin.com/jobs/search/?currentJobId=4012345678&keywords=java")
        self.assertEqual([m["file"] for m in r["matches"]], ["acme.md"])

    def test_indeed_url_matches_stored_job_id(self):
        r = self.hit(url="https://www.indeed.com/viewjob?jk=56589689AC7E155E&from=serp")
        self.assertEqual([m["file"] for m in r["matches"]], ["clear.md"])

    def test_employer_url_ignores_tracking_and_trailing_slash(self):
        r = self.hit(url="HTTPS://acme.wd5.myworkdayjobs.com/careers/job/Remote/Senior-Java-Engineer_R123/?source=LinkedIn")
        self.assertEqual(r["matches"][0]["matched_on"], ["url"])

    def test_same_company_similar_role(self):
        r = self.hit(company="Acme Health", role="Sr. Java Engineer (Remote)")
        self.assertEqual(r["matches"][0]["matched_on"], ["same company, similar role"])
        r = self.hit(company="Acme Health Inc", role="Senior Java Engineer II")
        self.assertEqual(r["matches"][0]["matched_on"], ["same company, similar role"])

    def test_loosely_similar_role_is_history_not_match(self):
        r = self.hit(company="Acme Health", role="Senior Java Platform Architect")
        self.assertEqual(r["matches"], [])
        self.assertEqual(r["same_company"][0]["status"], "applied")

    def test_other_company_no_hit(self):
        r = self.hit(company="Acme Robotics", role="Senior Java Engineer")
        self.assertEqual(r["matches"], [])
        self.assertEqual(r["same_company"], [])

    def test_different_role_same_company_is_history_not_match(self):
        r = self.hit(company="ClearCaptions", role="Engineering Manager")
        self.assertEqual(r["matches"], [])
        self.assertEqual(r["same_company"][0]["status"], "rejected")


class Due(Folder):
    def test_quiet_active_applications_only(self):
        self.write("old.md", record(status="applied", applied="2026-10-01", updated="2026-10-01"))
        self.write("touched.md", record(status="interviewing", applied="2026-10-01", updated="2026-11-10"))
        self.write("passed.md", record(status="passed", updated="2026-09-01"))
        self.write("bad.md", record(status="applied", updated="soon"))
        result = jobs.due(self.records()[0], 14, dt.date(2026, 11, 12))
        self.assertEqual([r["file"] for r in result["quiet"]], ["old.md"])
        self.assertEqual(result["quiet"][0]["days_quiet"], 42)
        self.assertEqual(result["unreadable_dates"], ["bad.md"])

    def test_falls_back_to_applied_date(self):
        self.write("a.md", record(status="applied", applied="2026-10-20"))
        result = jobs.due(self.records()[0], 14, dt.date(2026, 11, 12))
        self.assertEqual(result["quiet"][0]["days_quiet"], 23)


class Listing(Folder):
    def test_filter_and_counts(self):
        self.write("a.md", record(status="applied"))
        self.write("b.md", record(status="passed"))
        result = jobs.listing(self.records()[0], ["Applied"])
        self.assertEqual([r["file"] for r in result["records"]], ["a.md"])
        self.assertEqual(result["status_counts"], {"applied": 1, "passed": 1})


class Slug(unittest.TestCase):
    def test_drops_legal_suffix_and_punctuation(self):
        self.assertEqual(jobs.slug("ClearCaptions, LLC", "Software Developer (Remote)")["file"],
                         "clearcaptions-software-developer-remote.md")

    def test_ampersand_and_possessive(self):
        self.assertEqual(jobs.slug("Johnson & Johnson", "Lead Dev")["folder"], "johnson-and-johnson-lead-dev")
        self.assertEqual(jobs.slug("Kohl's", "Engineer")["folder"], "kohls-engineer")


class NormUrl(unittest.TestCase):
    def test_keeps_id_params_only(self):
        self.assertEqual(jobs.norm_url("https://www.indeed.com/viewjob?from=serp&jk=ABC123&vjs=3"),
                         "indeed.com/viewjob?jk=abc123")

    def test_none(self):
        self.assertIsNone(jobs.norm_url(None))


if __name__ == "__main__":
    unittest.main()
