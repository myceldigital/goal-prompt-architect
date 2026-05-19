from pathlib import Path
import importlib.util
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
VERIFY_PATH = ROOT / ".agent" / "verify_step.py"
SPEC = importlib.util.spec_from_file_location("verify_step", VERIFY_PATH)
verify_step = importlib.util.module_from_spec(SPEC)
sys.modules["verify_step"] = verify_step
SPEC.loader.exec_module(verify_step)


class VerifyStepTests(unittest.TestCase):
    def test_detect_project_unknown_in_empty_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path.cwd()
            try:
                import os
                os.chdir(tmp)
                self.assertEqual(verify_step.detect_project(), "unknown")
            finally:
                os.chdir(cwd)

    def test_detect_project_python(self):
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path.cwd()
            try:
                import os
                os.chdir(tmp)
                Path("pyproject.toml").write_text("[project]\nname='x'\n", encoding="utf-8")
                self.assertEqual(verify_step.detect_project(), "python")
            finally:
                os.chdir(cwd)

    def test_git_delta_fails_on_deleted_assertion(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            subprocess.run(["git", "init"], cwd=repo, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo, check=True)
            test_file = repo / "test_example.py"
            test_file.write_text("def test_x():\n    assert True\n", encoding="utf-8")
            subprocess.run(["git", "add", "test_example.py"], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-m", "initial"], cwd=repo, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            test_file.write_text("def test_x():\n    pass\n", encoding="utf-8")
            result = subprocess.run([sys.executable, str(VERIFY_PATH), "--target", "git_delta"], cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Forbidden test/assertion delta", result.stdout)


if __name__ == "__main__":
    unittest.main()
