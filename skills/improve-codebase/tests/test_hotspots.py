"""Tests for scripts/hotspots.py. Run: python -m unittest discover -s <this folder>

Most tests feed `tally` hand-written `git log` output. The last class builds a throwaway
repo with local git (no network) to check the real output format, and skips without git.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts")
sys.path.insert(0, SCRIPTS)
import hotspots as h  # noqa: E402


def log(*commits):
    """Build `git log --name-status --format=%x00%aI%x09%s` output, newest commit first."""
    out = ""
    for date, subject, changes in commits:
        out += f"\0{date}\t{subject}\n\n" + "".join("\t".join(c) + "\n" for c in changes)
    return out


class Tally(unittest.TestCase):
    def test_rename_chain_credits_current_name(self):
        stats, commits, oldest, newest = h.tally(log(
            ("2026-01-05", "new a", [("A", "src/a.py")]),
            ("2026-01-04", "rename b to c", [("R100", "src/b.py", "src/c.py")]),
            ("2026-01-03", "tweak b", [("M", "src/b.py")]),
            ("2026-01-02", "rename a to b", [("R095", "src/a.py", "src/b.py")]),
            ("2026-01-01", "fix bug in a", [("A", "src/a.py")]),
        ))
        self.assertEqual(commits, 5)
        self.assertEqual((oldest, newest), ("2026-01-01", "2026-01-05"))
        self.assertEqual(set(stats), {"src/a.py", "src/c.py"})
        # The new a.py came after the rename, so it doesn't inherit the old file's history.
        self.assertEqual(stats["src/a.py"]["commits"], 1)
        self.assertEqual(stats["src/c.py"]["commits"], 4)
        self.assertEqual(stats["src/c.py"]["fix_commits"], 1)
        self.assertEqual(stats["src/c.py"]["last_changed"], "2026-01-04")

    def test_copy_keeps_the_original_separate(self):
        stats, *_ = h.tally(log(
            ("2026-01-02", "copy", [("C100", "src/a.py", "src/b.py")]),
            ("2026-01-01", "add", [("A", "src/a.py")]),
        ))
        self.assertEqual({p: s["commits"] for p, s in stats.items()}, {"src/a.py": 1, "src/b.py": 1})

    def test_scope_and_skips(self):
        entries = [("M", p) for p in ("src/x.py", "lib/y.py", "src/node_modules/z.js", "src/package-lock.json",
                                      "src/README.md", "src/config.yaml")]
        stats, *_ = h.tally(log(("2026-01-01", "work", entries)), scope="src/")
        self.assertEqual(set(stats), {"src/x.py"})
        stats, *_ = h.tally(log(("2026-01-01", "work", entries)), scope="src/", include_docs=True)
        self.assertEqual(set(stats), {"src/x.py", "src/README.md", "src/config.yaml"})

    def test_empty_log(self):
        self.assertEqual(h.tally(""), ({}, 0, None, None))


class Skipped(unittest.TestCase):
    def test_skips(self):
        for path in ("dist/app.js", "a/vendor/b.go", "Cargo.lock", "docs/CHANGELOG.md", "app.min.js", "logo.png"):
            self.assertTrue(h.skipped(path, include_docs=True), path)

    def test_keeps_code(self):
        for path in ("src/app.ts", "build.gradle", "distance.py", "scripts/hotspots.py"):
            self.assertFalse(h.skipped(path), path)


class ResolveScope(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.root, "src", "api"))
        self.cwd = os.getcwd()

    def tearDown(self):
        os.chdir(self.cwd)
        shutil.rmtree(self.root, ignore_errors=True)

    def test_relative_to_cwd_then_root(self):
        os.chdir(os.path.join(self.root, "src"))
        self.assertEqual(h.resolve_scope("api", self.root), "src/api/")      # from the current directory
        self.assertEqual(h.resolve_scope("src/api", self.root), "src/api/")  # from the repo root
        self.assertEqual(h.resolve_scope(self.root, self.root), "")

    def test_outside_repo(self):
        self.assertIsNone(h.resolve_scope(os.path.dirname(self.root), self.root))


@unittest.skipUnless(shutil.which("git"), "needs git")
class AgainstGit(unittest.TestCase):
    def setUp(self):
        self.repo = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.repo, ignore_errors=True)

    def git(self, *args):
        subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "core.autocrlf=false", *args],
                       cwd=self.repo, check=True, capture_output=True)

    def commit(self, msg, files):
        for path, text in files.items():
            full = os.path.join(self.repo, path)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            with open(full, "w", encoding="utf-8") as f:
                f.write(text)
        self.git("add", "-A")
        self.git("commit", "-qm", msg)

    def run_script(self, *args):
        r = subprocess.run([sys.executable, os.path.join(SCRIPTS, "hotspots.py"), *args], cwd=self.repo,
                           capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        return json.loads(r.stdout)

    def test_non_ascii_current_name_is_kept(self):
        # Without core.quotePath=false, git prints "src/caf\303\251.py", which matches no file.
        self.git("init", "-q")
        self.commit("add", {"src/café.py": "x\n"})
        out = self.run_script()
        self.assertEqual([s["path"] for s in out["hotspots"]], ["src/café.py"])

    def test_scope_and_renames(self):
        self.git("init", "-q")
        body = "".join(f"line {i}\n" for i in range(30))
        self.commit("add", {"src/café.py": body})
        self.commit("fix crash", {"src/café.py": body + "x\n"})
        self.git("mv", "src/café.py", "src/menu.py")
        self.commit("rename", {})
        for i in range(5):
            self.commit(f"other {i}", {"other/o.py": f"{i}\n"})

        out = self.run_script("--path", "src", "--commits", "2")
        self.assertEqual(out["commits_read"], 2)  # only commits that touched src/
        self.assertFalse(out["shallow"])
        self.assertEqual([(s["path"], s["commits"]) for s in out["hotspots"]], [("src/menu.py", 2)])

        out = self.run_script()
        counts = {s["path"]: (s["commits"], s["fix_commits"]) for s in out["hotspots"]}
        self.assertEqual(counts, {"other/o.py": (5, 0), "src/menu.py": (3, 1)})


if __name__ == "__main__":
    unittest.main()
