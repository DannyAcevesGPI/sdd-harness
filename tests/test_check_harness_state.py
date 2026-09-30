import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from check_harness_state import audit_repository, canonical_bytes


class HarnessStateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.feature = self.root / "specs" / "008-example"
        self.feature.mkdir(parents=True)
        self.spec = self.feature / "spec.md"
        self.spec.write_text(
            "# Feature\n**Estado:** APPROVED  \n## FR-001\nRequired behavior.\n",
            encoding="utf-8",
        )
        self._write_events([self._approval()])

    def _approval(self, artifact=None, **changes):
        artifact = artifact or self.spec
        event = {
            "id": "DECISION-001",
            "kind": "APPROVAL",
            "actor": "Project owner",
            "date": "2026-09-30",
            "decision": "Approved SPEC-008",
            "scope": "SPEC-008 v0.1",
            "artifact": (
                artifact.relative_to(self.root).as_posix()
                if isinstance(artifact, Path) else artifact
            ),
            "artifact_sha256": hashlib.sha256(canonical_bytes(self.spec)).hexdigest(),
            "source": "Explicit human decision recorded in this file",
        }
        event.update(changes)
        return event

    def _write_events(self, events):
        (self.feature / "decisions.json").write_text(
            json.dumps({"schema_version": 1, "events": events}), encoding="utf-8"
        )

    def _codes(self):
        return {issue.code for issue in audit_repository(self.root)}

    def test_valid_approval_is_self_contained(self):
        self.assertEqual(self._codes(), set())

    def test_operational_state_and_checkmarks_do_not_change_digest(self):
        tasks = self.feature / "tasks.md"
        tasks.write_text(
            "# Tasks\n**Estado:** APPROVED  \n- [ ] Gate ready\n"
            "## TASK-001\n**Estado:** TODO  \nDepends on: None\n"
            "| 1 | TASK-001 | TODO |\n",
            encoding="utf-8",
        )
        expected = hashlib.sha256(canonical_bytes(tasks)).hexdigest()
        tasks.write_text(
            "# Tasks\n**Estado:** IN_PROGRESS  \n- [x] Gate ready\n"
            "## TASK-001\n**Estado:** DONE  \nDepends on: None\n"
            "| 1 | TASK-001 | DONE |\n",
            encoding="utf-8",
        )
        self.assertEqual(hashlib.sha256(canonical_bytes(tasks)).hexdigest(), expected)
        tasks.write_text(tasks.read_text(encoding="utf-8").replace("None", "TASK-002"))
        self.assertNotEqual(hashlib.sha256(canonical_bytes(tasks)).hexdigest(), expected)

    def test_requirement_state_is_not_operational_metadata(self):
        self.spec.write_text(
            "# Feature\n**Estado:** APPROVED\n## FR-001\n"
            "**Estado:** TODO\nRequired behavior.\n", encoding="utf-8"
        )
        before = hashlib.sha256(canonical_bytes(self.spec)).hexdigest()
        self.spec.write_text(
            self.spec.read_text(encoding="utf-8").replace(
                "## FR-001\n**Estado:** TODO", "## FR-001\n**Estado:** DONE"
            ), encoding="utf-8"
        )
        self.assertNotEqual(hashlib.sha256(canonical_bytes(self.spec)).hexdigest(), before)

    def test_changed_requirement_invalidates_approval(self):
        self.spec.write_text(
            self.spec.read_text(encoding="utf-8").replace("Required", "Different"),
            encoding="utf-8",
        )
        self.assertIn("HASH_MISMATCH", self._codes())

    def test_missing_record_is_not_approval(self):
        (self.feature / "decisions.json").unlink()
        self.assertIn("MISSING_LEDGER", self._codes())

    def test_invalid_ledger_and_duplicate_id_fail(self):
        self._write_events([self._approval(), self._approval()])
        self.assertIn("DUPLICATE_ID", self._codes())
        (self.feature / "decisions.json").write_text("{bad", encoding="utf-8")
        self.assertIn("INVALID_JSON", self._codes())

    def test_invalid_path_or_conflicting_approval_fails(self):
        self._write_events([self._approval(artifact="../secret")])
        self.assertIn("INVALID_ARTIFACT", self._codes())
        self._write_events([
            self._approval(),
            self._approval(id="DECISION-002", decision="Rejected SPEC-008"),
        ])
        self.assertIn("CONFLICTING_APPROVAL", self._codes())

    def test_symlinked_feature_outside_repository_is_rejected(self):
        with tempfile.TemporaryDirectory() as outside:
            external = Path(outside) / "008-external"
            external.mkdir()
            (self.root / "specs" / "009-external").symlink_to(external, target_is_directory=True)
            self.assertIn("INVALID_FEATURE", self._codes())

    def test_unknown_operational_state_fails_closed(self):
        self.spec.write_text(
            self.spec.read_text(encoding="utf-8").replace("APPROVED", "MAYBE"),
            encoding="utf-8",
        )
        self.assertIn("INVALID_STATE", self._codes())

    def test_legacy_is_not_promoted_to_new_approval(self):
        legacy = self.root / "specs" / "006-tdd-workflow"
        legacy.mkdir()
        (legacy / "spec.md").write_text("**Estado:** APPROVED\n", encoding="utf-8")
        self.assertEqual(self._codes(), set())

    def test_new_project_first_feature_requires_ledger(self):
        first = self.root / "specs" / "001-new-project"
        first.mkdir()
        (first / "spec.md").write_text("**Estado:** DRAFT\n", encoding="utf-8")
        self.assertIn("MISSING_LEDGER", self._codes())

    def test_empty_directory_is_not_a_feature(self):
        (self.root / "specs" / "009-empty").mkdir()
        self.assertEqual(self._codes(), set())

    def test_revocation_removes_gate_authorization(self):
        self._write_events([
            self._approval(),
            self._approval(
                id="DECISION-002", kind="REVOCATION", supersedes="DECISION-001",
                decision="Approval revoked", artifact_sha256="",
            ),
        ])
        self.assertIn("MISSING_APPROVAL", self._codes())

    def test_new_approval_supersedes_old_content(self):
        old = self._approval()
        self.spec.write_text(
            self.spec.read_text(encoding="utf-8").replace("Required", "Revised"),
            encoding="utf-8",
        )
        new = self._approval(id="DECISION-002", supersedes="DECISION-001")
        self._write_events([old, new])
        self.assertEqual(self._codes(), set())


if __name__ == "__main__":
    unittest.main()
