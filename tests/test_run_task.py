"""Contract tests for the task runner. Maps to TEST-005..008, AC-001/003."""

from contextlib import redirect_stderr, redirect_stdout
import io
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from src import run_task


class RunTaskTests(unittest.TestCase):
    def test_each_agent_receives_model_effort_and_task_as_data(self):
        cases = (
            ("claude", ["/bin/claude", "--model", "provider/model", "--effort", "low", "-p"], "--effort"),
            ("codex", ["/bin/codex", "exec", "--model", "provider/model", "--config", 'model_reasoning_effort="low"', "-"], "model_reasoning_effort"),
            ("opencode", ["/bin/opencode", "run", "--model", "provider/model#low"], "--file"),
        )
        for agent, expected, marker in cases:
            with self.subTest(agent=agent), tempfile.TemporaryDirectory() as directory:
                calls = []

                def fake_run(argv, **kwargs):
                    calls.append((argv, kwargs))
                    if agent == "opencode":
                        file_arg = argv[argv.index("--file") + 1]
                        self.assertEqual(Path(file_arg).read_text(), "-- unsafe; task")
                    return run_task.subprocess.CompletedProcess(argv, 0, "ok\n", "")

                with patch.object(run_task.shutil, "which", return_value=f"/bin/{agent}"), patch.object(
                    run_task.subprocess, "run", side_effect=fake_run
                ), patch.object(run_task, "_policy", return_value=run_task.EffortSelection("low", "small task")):
                    result = run_task.execute(agent, "provider/model" if agent == "opencode" else "provider/model", task="-- unsafe; task", cwd=Path(directory))

                self.assertEqual(result, 0)
                argv, kwargs = calls[0]
                if agent != "opencode":
                    self.assertEqual(argv, expected)
                    self.assertEqual(kwargs["input"], "-- unsafe; task")
                else:
                    self.assertEqual(argv[:4], expected)
                    self.assertIn(marker, argv)
                    self.assertIn("Execute the task in the attached file.", argv)
                    self.assertFalse(Path(argv[argv.index(marker) + 1]).exists())
                self.assertFalse(kwargs.get("shell", False))

    def test_dry_run_redacts_task_content(self):
        output, errors = io.StringIO(), io.StringIO()
        with patch.object(run_task.shutil, "which", return_value="/bin/claude"), patch.object(
            run_task, "_policy", return_value=run_task.EffortSelection("high", "security change")
        ), redirect_stdout(output), redirect_stderr(errors):
            code = run_task.main(["--agent", "claude", "--model", "m", "--task", "private task text", "--dry-run"])
        self.assertEqual(code, 0)
        self.assertNotIn("private task text", output.getvalue() + errors.getvalue())
        self.assertIn("--effort high", output.getvalue())

    def test_task_text_with_shell_metacharacters_is_never_command(self):
        captured = []
        with patch.object(run_task.shutil, "which", return_value="/bin/codex"), patch.object(
            run_task.subprocess, "run", side_effect=lambda argv, **kwargs: captured.append((argv, kwargs)) or run_task.subprocess.CompletedProcess(argv, 0, "", "")
        ), patch.object(run_task, "_policy", return_value=run_task.EffortSelection("medium", "routine")):
            run_task.execute("codex", "m", task="$(touch nope); --danger", cwd=Path.cwd())
        argv, kwargs = captured[0]
        self.assertNotIn("$(touch nope); --danger", argv)
        self.assertEqual(kwargs["input"], "$(touch nope); --danger")

    def test_invalid_agent_model_and_task_file_are_rejected(self):
        for operation in (
            lambda: run_task.execute("unknown", "m", task="t"),
            lambda: run_task.execute("claude", " ", task="t"),
            lambda: run_task.execute("claude", "m", task_file=Path("missing-task-file")),
        ):
            with self.subTest(operation=operation), self.assertRaises(ValueError):
                operation()

    def test_missing_cli_returns_controlled_error(self):
        errors = io.StringIO()
        with patch.object(run_task.shutil, "which", return_value=None), redirect_stderr(errors):
            result = run_task.main(["--agent", "claude", "--model", "m", "--task", "task"])
        self.assertEqual(result, 2)
        self.assertIn("not found", errors.getvalue())

    def test_script_entrypoint_runs_dry_run_from_repository_root(self):
        root = Path(__file__).resolve().parents[1]
        # Dry-run still resolves the CLI on PATH; provide a fake one so the
        # test does not depend on what is installed (FINDING-004).
        with tempfile.TemporaryDirectory() as bin_dir:
            fake_cli = Path(bin_dir) / "claude"
            fake_cli.write_text("#!/bin/sh\nexit 0\n")
            fake_cli.chmod(0o755)
            env = {**os.environ, "PATH": bin_dir + os.pathsep + os.environ.get("PATH", "")}
            result = run_task.subprocess.run(
                [
                    run_task.sys.executable,
                    str(root / "src/run_task.py"),
                    "--agent", "claude",
                    "--model", "test-model",
                    "--task", "fix typo",
                    "--dry-run",
                ],
                cwd=root,
                env=env,
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--effort low", result.stdout)

    def test_explicit_unsupported_effort_retries_once_without_override(self):
        calls = []

        def fake_run(argv, **kwargs):
            calls.append(argv)
            if len(calls) == 1:
                return run_task.subprocess.CompletedProcess(argv, 2, "", "effort high is not supported")
            return run_task.subprocess.CompletedProcess(argv, 0, "completed", "")

        errors = io.StringIO()
        with patch.object(run_task.shutil, "which", return_value="/bin/claude"), patch.object(
            run_task.subprocess, "run", side_effect=fake_run
        ), patch.object(run_task, "_policy", return_value=run_task.EffortSelection("high", "security work")), redirect_stderr(errors):
            result = run_task.execute("claude", "m", task="security work")
        self.assertEqual(result, 0)
        self.assertEqual(len(calls), 2)
        self.assertIn("--effort", calls[0])
        self.assertNotIn("--effort", calls[1])
        self.assertIn("default-fallback", errors.getvalue())

    def test_unrelated_cli_errors_do_not_retry(self):
        for error in ("authentication failed", "permission denied", "network timeout", "model not found"):
            with self.subTest(error=error):
                calls = []

                def fake_run(argv, **kwargs):
                    calls.append(argv)
                    return run_task.subprocess.CompletedProcess(argv, 7, "", error)

                with patch.object(run_task.shutil, "which", return_value="/bin/codex"), patch.object(
                    run_task.subprocess, "run", side_effect=fake_run
                ), patch.object(run_task, "_policy", return_value=run_task.EffortSelection("high", "security work")), redirect_stderr(io.StringIO()):
                    result = run_task.execute("codex", "m", task="security work")
                self.assertEqual(result, 7)
                self.assertEqual(len(calls), 1)

    def test_effort_phrase_in_stdout_does_not_override_unrelated_stderr(self):
        calls = []

        def fake_run(argv, **kwargs):
            calls.append(argv)
            return run_task.subprocess.CompletedProcess(
                argv, 7, "Task said: effort high is not supported", "authentication failed"
            )

        with patch.object(run_task.shutil, "which", return_value="/bin/claude"), patch.object(
            run_task.subprocess, "run", side_effect=fake_run
        ), patch.object(run_task, "_policy", return_value=run_task.EffortSelection("high", "security work")), redirect_stderr(io.StringIO()):
            result = run_task.execute("claude", "m", task="security work")
        self.assertEqual(result, 7)
        self.assertEqual(len(calls), 1)

    def test_second_unsupported_effort_failure_does_not_loop(self):
        calls = []

        def fake_run(argv, **kwargs):
            calls.append(argv)
            return run_task.subprocess.CompletedProcess(argv, 4, "", "effort high is unsupported")

        with patch.object(run_task.shutil, "which", return_value="/bin/claude"), patch.object(
            run_task.subprocess, "run", side_effect=fake_run
        ), patch.object(run_task, "_policy", return_value=run_task.EffortSelection("high", "security work")), redirect_stderr(io.StringIO()):
            result = run_task.execute("claude", "m", task="security work")
        self.assertEqual(result, 4)
        self.assertEqual(len(calls), 2)


if __name__ == "__main__":
    unittest.main()
