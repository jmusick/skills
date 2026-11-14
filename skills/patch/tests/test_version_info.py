import importlib.util
import pathlib
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "version_info.py"
spec = importlib.util.spec_from_file_location("version_info", SCRIPT)
version_info = importlib.util.module_from_spec(spec)
spec.loader.exec_module(version_info)

PYPROJECT = '[project]\nname = "demo"\nversion = "1.2.3"\n'


class FindVersionFilesTest(unittest.TestCase):
    def found(self, paths):
        files = version_info.find_version_files(paths, lambda _path: PYPROJECT)
        return [f["path"] for f in files]

    def test_reads_a_root_version_file(self):
        self.assertEqual(self.found(["pyproject.toml"]), ["pyproject.toml"])

    def test_skips_eval_and_fixture_projects(self):
        paths = [
            "skills/patch/evals/release/files/pyproject.toml",
            "tests/fixtures/app/pyproject.toml",
            "node_modules/dep/pyproject.toml",
        ]
        self.assertEqual(self.found(paths), [])


if __name__ == "__main__":
    unittest.main()
