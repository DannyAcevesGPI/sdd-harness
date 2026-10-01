"""Install the reusable SDD Harness in an existing empty project."""

import argparse
from pathlib import Path
import shutil


BASE_FILES = (
    Path("AGENTS.md"),
    Path("docs/adoption.md"),
    Path("docs/quickstart.md"),
    Path("docs/state-reconstruction.md"),
    Path("docs/tdd.md"),
    Path("docs/agents/hooks.md"),
    Path("docs/agents/subagents.md"),
    Path("src/adopt_harness.py"),
    Path("src/check_harness_state.py"),
    Path("tests/test_adopt_harness.py"),
    Path("tests/test_check_harness_state.py"),
)
SPEC_FILES = (
    Path(".spec/constitution.md"),
    *(Path(".spec/commands") / f"{name}.md" for name in (
        "clarify", "implement", "plan", "specify", "tasks", "validate"
    )),
    *(Path(".spec/standards") / f"{name}.md" for name in (
        "architecture", "coding", "security", "testing"
    )),
    *(Path(".spec/templates") / f"{name}.template.md" for name in (
        "plan", "specification", "tasks", "validation"
    )),
)


def reusable_files(source: Path) -> tuple[Path, ...]:
    paths = tuple(sorted((*BASE_FILES, *SPEC_FILES)))
    for relative in paths:
        _check_path(source, relative, must_exist=True)
    return paths


def _check_path(root: Path, relative: Path, must_exist: bool) -> None:
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"Unsafe path: {relative}")
    current = root
    for index, part in enumerate(relative.parts):
        current /= part
        if current.is_symlink():
            raise ValueError(f"Symlink not allowed: {current}")
        if index < len(relative.parts) - 1 and current.exists() and not current.is_dir():
            raise ValueError(f"Destination parent is not a directory: {current}")
    if must_exist and not current.is_file():
        raise ValueError(f"Missing source file: {current}")
    if not must_exist and current.exists():
        raise ValueError(f"Destination collision: {current}")


def adopt(source: Path, destination: Path) -> tuple[Path, ...]:
    source = source.resolve()
    if not destination.is_dir() or destination.is_symlink():
        raise ValueError(f"Destination must be an existing directory: {destination}")
    destination = destination.resolve()
    if destination == source or destination.is_relative_to(source):
        raise ValueError("Destination cannot be inside the Harness source")
    paths = reusable_files(source)
    for relative in paths:
        _check_path(source, relative, must_exist=True)
        _check_path(destination, relative, must_exist=False)
    for relative in (Path("handoff.md"), Path("docs/index.md")):
        _check_path(destination, relative, must_exist=False)
    specs = destination / "specs"
    if specs.is_symlink() or (specs.exists() and (not specs.is_dir() or list(specs.iterdir()))):
        raise ValueError(f"Destination specs must be absent or empty: {specs}")

    for relative in paths:
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source / relative, target)
    specs.mkdir(exist_ok=True)
    (destination / "handoff.md").write_text(
        "# SDD Harness - Live Handoff\n\n"
        "No features yet. Next: /specify. Evidence belongs in specs/.\n\n"
        "```json harness-state\n"
        '{"schema_version": 1, "active": [], "validated": []}\n'
        "```\n",
        encoding="utf-8",
    )
    (destination / "docs/index.md").write_text(
        "# Documentation Index\n\n"
        "- `AGENTS.md` - agent rules\n"
        "- `.spec/constitution.md` - authority\n"
        "- `handoff.md` - live state\n"
        "- `docs/quickstart.md` - bootstrap\n"
        "- `docs/adoption.md` - adoption\n"
        "- `docs/state-reconstruction.md` - gates without chat\n",
        encoding="utf-8",
    )
    return paths


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path, nargs="?")
    parser.add_argument("--list", action="store_true", help="List reusable paths")
    args = parser.parse_args()
    source = Path(__file__).resolve().parents[1]
    try:
        if args.list:
            for path in reusable_files(source):
                print(path)
            return 0
        if args.destination is None:
            parser.error("destination is required unless --list is used")
        paths = adopt(source, args.destination)
    except ValueError as exc:
        parser.exit(1, f"ADOPTION FAILED: {exc}\n")
    print(f"ADOPTION PASS: {len(paths)} reusable files installed in {args.destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
