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
from check_harness_state import audit_repository, canonical_bytes, projected_state


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

    def test_effort_runner_is_shipped_and_documented(self):
        required = {
            Path("src/effort_policy.py"),
            Path("src/run_task.py"),
            Path("tests/test_effort_policy.py"),
            Path("tests/test_run_task.py"),
            Path("docs/agents/model-effort.md"),
        }
        self.assertTrue(required.issubset(set(reusable_files(SOURCE))))
        adopt(SOURCE, self.destination)
        for relative in required:
            self.assertTrue((self.destination / relative).is_file(), relative)
        for relative in (Path("AGENTS.md"), Path("docs/quickstart.md"), Path("docs/adoption.md"), Path("docs/index.md")):
            content = (self.destination / relative).read_text(encoding="utf-8")
            self.assertIn("run_task.py", content, relative)
        policy = (self.destination / "docs/agents/model-effort.md").read_text(encoding="utf-8")
        for agent in ("claude", "codex", "opencode"):
            self.assertIn(agent.lower(), policy.lower())

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

    def test_adopted_project_completes_full_lifecycle_and_rejects_bad_closure(self):
        adopt(SOURCE, self.destination)
        feature = self.destination / "specs/001-first-lifecycle"
        feature.mkdir()
        ledger = feature / "decisions.json"
        events = []

        def save_events():
            ledger.write_text(
                json.dumps({"schema_version": 1, "events": events}), encoding="utf-8"
            )

        def approve(path):
            events.append({
                "id": f"DECISION-{len(events) + 1:03d}", "kind": "APPROVAL",
                "actor": "Synthetic test fixture", "date": "2026-10-07",
                "decision": f"Synthetic approval for {path.name}",
                "scope": "Only this temporary lifecycle test",
                "artifact": path.relative_to(self.destination).as_posix(),
                "artifact_sha256": hashlib.sha256(canonical_bytes(path)).hexdigest(),
                "source": "Automated fixture; no human approval claimed",
            })
            save_events()

        def sync_projection():
            state, links = projected_state(self.destination)
            (self.destination / "handoff.md").write_text(
                "# Test handoff\n```json harness-state\n"
                + json.dumps(state) + "\n```\n", encoding="utf-8",
            )
            (self.destination / "docs/index.md").write_text(
                "# Test index\n" + "".join(f"- `{link}`\n" for link in sorted(links)),
                encoding="utf-8",
            )

        def check(expected_code=0, issue=None):
            result = subprocess.run(
                [sys.executable, "src/check_harness_state.py"],
                cwd=self.destination, capture_output=True, text=True, check=False,
            )
            self.assertEqual(result.returncode, expected_code, result.stdout + result.stderr)
            if issue:
                self.assertIn(issue, result.stdout)

        spec = feature / "spec.md"
        spec.write_text(
            "# Spec\n**Estado:** DRAFT\n## AC-001 — Observable\nExpected.\n",
            encoding="utf-8",
        )
        save_events()
        sync_projection()
        check()
        spec.write_text(spec.read_text().replace("DRAFT", "APPROVED"), encoding="utf-8")
        approve(spec)
        sync_projection()
        check()

        plan = feature / "plan.md"
        plan.write_text("# Plan\n**Estado:** DRAFT\n", encoding="utf-8")
        sync_projection()
        check()
        plan.write_text("# Plan\n**Estado:** APPROVED\n", encoding="utf-8")
        approve(plan)
        sync_projection()
        check()

        tasks = feature / "tasks.md"
        tasks.write_text(
            "# Tasks\n**Estado:** DRAFT\n"
            "## TASK-001 — Work\n**Estado:** TODO\n"
            "**TEST-001:** Verify AC-001.\n"
            "| Orden | Tarea | Estado |\n| 1 | TASK-001 | TODO |\n",
            encoding="utf-8",
        )
        sync_projection()
        check()
        tasks.write_text(tasks.read_text().replace("**Estado:** DRAFT", "**Estado:** APPROVED"), encoding="utf-8")
        approve(tasks)
        sync_projection()
        check()
        tasks.write_text(
            tasks.read_text().replace("**Estado:** APPROVED", "**Estado:** IN_PROGRESS")
            .replace("**Estado:** TODO", "**Estado:** IN_PROGRESS")
            .replace("| TASK-001 | TODO |", "| TASK-001 | IN_PROGRESS |"),
            encoding="utf-8",
        )
        sync_projection()
        check()

        evidence = feature / "evidence"
        evidence.mkdir()
        (evidence / "result.md").write_text("Synthetic observed result\n", encoding="utf-8")
        validation = feature / "validation.md"
        validation.write_text(
            "**Result:** PASS\n"
            "| AC | Evidence | Result |\n| AC-001 | TEST-001; `evidence/result.md` | PASS |\n"
            "| TASK | Evidence | Result |\n| TASK-001 | `evidence/result.md` | PASS |\n"
            "| TEST | Evidence | Result |\n| TEST-001 | `evidence/result.md` | PASS |\n"
            "**SPEC Compliance:** PASS\n**Feature Status:** VALIDATED\n",
            encoding="utf-8",
        )
        sync_projection()
        check(1, "PREMATURE_VALIDATION")

        tasks.write_text(
            tasks.read_text().replace("**Estado:** IN_PROGRESS", "**Estado:** COMPLETED", 1)
            .replace("**Estado:** IN_PROGRESS", "**Estado:** DONE", 1)
            .replace("| TASK-001 | IN_PROGRESS |", "| TASK-001 | DONE |"),
            encoding="utf-8",
        )
        sync_projection()
        check()
        self.assertEqual(projected_state(self.destination)[0]["validated"], ["SPEC-001"])

        tasks.write_text(
            tasks.read_text().replace("**Estado:** DONE", "**Estado:** TODO", 1),
            encoding="utf-8",
        )
        sync_projection()
        check(1, "TASK_STATE_MISMATCH")


if __name__ == "__main__":
    unittest.main()
