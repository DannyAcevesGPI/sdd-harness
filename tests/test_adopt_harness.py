from pathlib import Path
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from adopt_harness import BASE_FILES, adopt, reusable_files
from check_harness_state import audit_repository, canonical_bytes


SOURCE = Path(__file__).resolve().parents[1]


class AdoptionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.destination = Path(self.temp.name) / "project"
        self.destination.mkdir()

    def test_base_is_complete_and_has_fresh_state(self):
        paths = reusable_files(SOURCE)
        self.assertIn(Path("src/check_harness_state.py"), paths)
        self.assertIn(Path("tests/test_check_harness_state.py"), paths)
        self.assertIn(Path("docs/state-reconstruction.md"), paths)
        adopt(SOURCE, self.destination)
        for path in paths:
            self.assertTrue((self.destination / path).is_file(), path)
        self.assertTrue((self.destination / "handoff.md").is_file())
        self.assertTrue((self.destination / "docs/index.md").is_file())
        self.assertTrue((self.destination / "specs").is_dir())
        self.assertEqual(list((self.destination / "specs").iterdir()), [])
        self.assertFalse((self.destination / "CHANGELOG.md").exists())
        check = subprocess.run(
            [sys.executable, "src/check_harness_state.py"],
            cwd=self.destination, capture_output=True, text=True, check=False,
        )
        self.assertEqual(check.returncode, 0, check.stdout + check.stderr)
        quickstart = (self.destination / "docs/quickstart.md").read_text(encoding="utf-8")
        for path in re.findall(r"`((?:docs|specs)/[^`<>]+)`", quickstart):
            if not path.endswith("/"):
                self.assertTrue((self.destination / path).exists(), path)

    def test_rejects_collisions_without_partial_copy(self):
        (self.destination / "AGENTS.md").write_text("existing", encoding="utf-8")
        with self.assertRaises(ValueError):
            adopt(SOURCE, self.destination)
        self.assertEqual((self.destination / "AGENTS.md").read_text(), "existing")
        self.assertFalse((self.destination / ".spec").exists())

    def test_rejects_unsafe_destination_symlink(self):
        with tempfile.TemporaryDirectory() as outside:
            (self.destination / "docs").symlink_to(outside, target_is_directory=True)
            with self.assertRaises(ValueError):
                adopt(SOURCE, self.destination)
            self.assertFalse((self.destination / ".spec").exists())

    def test_rejects_missing_source_without_partial_copy(self):
        with tempfile.TemporaryDirectory() as source:
            with self.assertRaises(ValueError):
                adopt(Path(source), self.destination)
        self.assertEqual(list(self.destination.iterdir()), [])

    def test_rejects_incomplete_spec_source(self):
        with tempfile.TemporaryDirectory() as temp_source:
            source = Path(temp_source)
            shutil.copytree(SOURCE / ".spec", source / ".spec")
            for relative in BASE_FILES:
                target = source / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(SOURCE / relative, target)
            (source / ".spec/commands/validate.md").unlink()
            with self.assertRaises(ValueError):
                reusable_files(source)

    def test_synthetic_history_and_secret_are_not_copied(self):
        with tempfile.TemporaryDirectory() as temp_source:
            source = Path(temp_source)
            for relative in reusable_files(SOURCE):
                target = source / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(SOURCE / relative, target)
            (source / ".env").write_text("FAKE_TOKEN=fixture-only\n", encoding="utf-8")
            (source / "handoff.md").write_text("historical fixture", encoding="utf-8")
            history = source / "specs/001-history"
            history.mkdir(parents=True)
            (history / "validation.md").write_text("synthetic history", encoding="utf-8")
            adopt(source, self.destination)
        self.assertFalse((self.destination / ".env").exists())
        self.assertFalse((self.destination / "specs/001-history").exists())
        self.assertNotIn("historical fixture", (self.destination / "handoff.md").read_text())

    def test_rejects_file_in_parent_path(self):
        (self.destination / "docs").write_text("existing", encoding="utf-8")
        with self.assertRaises(ValueError):
            adopt(SOURCE, self.destination)
        self.assertFalse((self.destination / ".spec").exists())

    def test_first_feature_has_no_legacy_exemption(self):
        adopt(SOURCE, self.destination)
        feature = self.destination / "specs" / "001-first-feature"
        feature.mkdir()
        spec = feature / "spec.md"
        spec.write_text("# First feature\n**Estado:** DRAFT\n", encoding="utf-8")
        index = self.destination / "docs/index.md"
        index.write_text(
            index.read_text(encoding="utf-8") + "- `specs/001-first-feature/spec.md`\n",
            encoding="utf-8",
        )
        handoff = self.destination / "handoff.md"
        handoff.write_text(
            handoff.read_text(encoding="utf-8").replace(
                '"active": []',
                '"active": [{"id": "SPEC-001", "phase": "SPEC", "next": "/specify"}]',
            ), encoding="utf-8",
        )
        self.assertIn("MISSING_LEDGER", {item.code for item in audit_repository(self.destination)})
        ledger = feature / "decisions.json"
        ledger.write_text('{"schema_version": 1, "events": []}', encoding="utf-8")
        self.assertEqual(audit_repository(self.destination), [])
        spec.write_text("# First feature\n**Estado:** APPROVED\n", encoding="utf-8")
        handoff.write_text(
            handoff.read_text(encoding="utf-8").replace(
                '"phase": "SPEC", "next": "/specify"',
                '"phase": "PLAN", "next": "/plan"',
            ), encoding="utf-8",
        )
        self.assertIn("MISSING_APPROVAL", {item.code for item in audit_repository(self.destination)})
        event = {
            "id": "DECISION-001", "kind": "APPROVAL", "actor": "Synthetic fixture",
            "date": "2026-09-30", "decision": "Fixture approval only",
            "scope": "Synthetic first feature", "source": "Automated test fixture",
            "artifact": "specs/001-first-feature/spec.md",
            "artifact_sha256": hashlib.sha256(canonical_bytes(spec)).hexdigest(),
        }
        ledger.write_text(json.dumps({"schema_version": 1, "events": [event]}), encoding="utf-8")
        self.assertEqual(audit_repository(self.destination), [])
        spec.write_text(spec.read_text(encoding="utf-8") + "Changed requirement\n", encoding="utf-8")
        self.assertIn("HASH_MISMATCH", {item.code for item in audit_repository(self.destination)})
        check = subprocess.run(
            [sys.executable, "src/check_harness_state.py"],
            cwd=self.destination, capture_output=True, text=True, check=False,
        )
        self.assertEqual(check.returncode, 1)
        self.assertIn("HASH_MISMATCH", check.stdout)

    def test_first_feature_with_historical_slug_still_requires_ledger(self):
        adopt(SOURCE, self.destination)
        feature = self.destination / "specs/001-audit-task-management"
        feature.mkdir()
        (feature / "spec.md").write_text(
            "# New project feature\n**Estado:** DRAFT\n", encoding="utf-8"
        )
        codes = {item.code for item in audit_repository(self.destination)}
        self.assertIn("MISSING_LEDGER", codes)


if __name__ == "__main__":
    unittest.main()
