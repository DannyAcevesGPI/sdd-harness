"""Run a task through a configured model CLI with a selected effort level."""

import argparse
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time

if __package__:
    from .effort_policy import EffortSelection, select_effort
else:
    from effort_policy import EffortSelection, select_effort


def _policy(task: str) -> EffortSelection:
    return select_effort(task)


def _read_task(task: str | None, task_file: Path | None, cwd: Path) -> tuple[str, Path | None]:
    if (task is None) == (task_file is None):
        raise ValueError("provide exactly one of task or task_file")
    if task is not None:
        if not task.strip():
            raise ValueError("task must not be empty")
        return task, None

    requested = Path(task_file)
    candidate = cwd / requested if not requested.is_absolute() else requested
    current = Path(candidate.anchor)
    for part in candidate.parts[1:] if candidate.is_absolute() else candidate.parts:
        current /= part
        if current.is_symlink():
            raise ValueError("task file path cannot contain symlinks")
    try:
        resolved = candidate.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise ValueError("task file could not be resolved") from exc
    try:
        resolved.relative_to(cwd.resolve())
    except ValueError as exc:
        raise ValueError("task file must be inside the working directory") from exc
    if not resolved.is_file():
        raise ValueError("task file must be a regular file")
    contents = resolved.read_text(encoding="utf-8")
    if not contents.strip():
        raise ValueError("task file must not be empty")
    return contents, resolved


def _command(agent: str, executable: str, model: str, level: str) -> list[str]:
    if agent == "claude":
        return [executable, "--model", model, "--effort", level, "-p"]
    if agent == "codex":
        return [executable, "exec", "--model", model, "--config", f'model_reasoning_effort="{level}"', "-"]
    base_model = model.split("#", 1)[0]
    return [executable, "run", "--model", f"{base_model}#{level}"]


def _unsupported_effort(agent: str, output: str, level: str) -> bool:
    text = output.lower()
    escaped_level = re.escape(level.lower())
    if agent == "opencode":
        return bool(re.search(r"(?:unknown|unsupported|not supported)\s+variant", text) and re.search(escaped_level, text))
    if agent == "codex":
        return bool(re.search(r"model_reasoning_effort.{0,40}(?:unsupported|not supported|invalid)", text))
    return bool(re.search(r"effort.{0,40}(?:unsupported|not supported|invalid)", text))


def _without_effort_override(agent: str, command: list[str], model: str, level: str) -> list[str]:
    retry = list(command)
    if agent == "claude":
        index = retry.index("--effort")
        del retry[index:index + 2]
    elif agent == "codex":
        index = retry.index("--config")
        del retry[index:index + 2]
    else:
        index = retry.index("--model") + 1
        retry[index] = model.split("#", 1)[0]
    return retry


def execute(
    agent: str,
    model: str,
    *,
    task: str | None = None,
    task_file: Path | None = None,
    cwd: Path | None = None,
    dry_run: bool = False,
) -> int:
    if agent not in {"claude", "codex", "opencode"}:
        raise ValueError("agent must be claude, codex, or opencode")
    if not model.strip() or any(char.isspace() for char in model):
        raise ValueError("model must be a non-empty identifier without whitespace")
    working_dir = (cwd or Path.cwd()).resolve()
    contents, task_path = _read_task(task, task_file, working_dir)
    selection = _policy(contents)
    executable = shutil.which(agent)
    if executable is None:
        print(f"Runner error: CLI not found: {agent}", file=sys.stderr)
        return 2
    command = _command(agent, executable, model, selection.level)
    if dry_run:
        if agent == "opencode":
            command.extend(["--file", "<task-content>", "Execute the task in the attached file."])
        print(" ".join(command))
        print(f"agent={agent} effort={selection.level} status=would-apply", file=sys.stderr)
        return 0

    temporary_path: Path | None = None
    try:
        if agent == "opencode":
            if task_path is None:
                descriptor, name = tempfile.mkstemp(prefix=".harness-task-", suffix=".txt", dir=working_dir)
                temporary_path = Path(name)
                try:
                    os.write(descriptor, contents.encode("utf-8"))
                finally:
                    os.close(descriptor)
                temporary_path.chmod(0o600)
                task_path = temporary_path
            command.extend(["--file", str(task_path), "Execute the task in the attached file."])
            input_text = None
        else:
            input_text = contents

        started = time.monotonic()
        completed = subprocess.run(command, input=input_text, text=True, cwd=working_dir, capture_output=True, check=False)
        fallback = False
        if completed.returncode and _unsupported_effort(agent, completed.stderr, selection.level):
            fallback = True
            print(f"agent={agent} effort={selection.level} status=default-fallback", file=sys.stderr)
            retry_command = _without_effort_override(agent, command, model, selection.level)
            completed = subprocess.run(
                retry_command,
                input=input_text,
                text=True,
                cwd=working_dir,
                capture_output=True,
                check=False,
            )
        duration = time.monotonic() - started
        if completed.stdout:
            sys.stdout.write(completed.stdout)
        if completed.stderr:
            sys.stderr.write(completed.stderr)
        status = "default-fallback" if fallback else "applied" if completed.returncode == 0 else "not-confirmed"
        print(
            f"agent={agent} effort={selection.level} status={status} duration={duration:.2f}s reason={selection.reason}",
            file=sys.stderr,
        )
        return completed.returncode
    except OSError as exc:
        print(f"Runner error: could not execute {agent} ({exc.__class__.__name__})", file=sys.stderr)
        return 2
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent", required=True)
    parser.add_argument("--model", required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--task")
    group.add_argument("--task-file", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    try:
        return execute(args.agent, args.model, task=args.task, task_file=args.task_file, dry_run=args.dry_run)
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"Runner error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
