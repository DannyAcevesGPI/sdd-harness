import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from effort_policy import select_effort


class EffortPolicyTests(unittest.TestCase):
    def test_small_mechanical_change_selects_low(self):
        result = select_effort("Fix the typo in one heading.")

        self.assertEqual(result.level, "low")
        self.assertTrue(result.reason)

    def test_routine_multi_step_task_selects_medium(self):
        result = select_effort("Add pagination to the report endpoint and document it.")

        self.assertEqual(result.level, "medium")

    def test_security_architecture_or_migration_selects_high(self):
        result = select_effort("Review authorization and security implications of a migration.")

        self.assertEqual(result.level, "high")

    def test_high_impact_signal_wins_over_mechanical_signal(self):
        result = select_effort("Format the file and update the authentication boundary.")

        self.assertEqual(result.level, "high")

    def test_ambiguous_or_empty_input_defaults_to_medium(self):
        for task in ("Improve this.", "", "   "):
            with self.subTest(task=task):
                self.assertEqual(select_effort(task).level, "medium")

    def test_selection_is_deterministic(self):
        task = "Migrate authorization checks across several services."

        self.assertEqual(select_effort(task), select_effort(task))


if __name__ == "__main__":
    unittest.main()
