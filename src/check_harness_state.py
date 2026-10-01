import argparse
from dataclasses import dataclass
from datetime import date
import hashlib
import json
from pathlib import Path
import re


DOCUMENT_STATES = {
    "DRAFT", "IN_REVIEW", "APPROVED", "SUPERSEDED", "IN_PROGRESS",
    "COMPLETED", "TODO", "BLOCKED", "DONE",
}
STATE_LINE = re.compile(r"^(\*\*Estado(?: actual)?:\*\* )(\S+)(\s*)$")
CHECKBOX_LINE = re.compile(r"^(\s*- \[)[ xX](\] .*)$")
ORDER_ROW = re.compile(r"^(\|\s*\d+\s*\|\s*TASK-\d{3}\s*\|\s*)(TODO|IN_PROGRESS|BLOCKED|DONE)(\s*\|.*)$")
ORDER_ROW_FOUR = re.compile(r"^(\|\s*\d+\s*\|\s*TASK-\d{3}\s*\|[^|]*\|\s*)(TODO|IN_PROGRESS|BLOCKED|DONE)(\s*\|.*)$")
HEX_DIGEST = re.compile(r"[0-9a-f]{64}")
FEATURE_DIR = re.compile(r"^(\d{3})-[a-z0-9-]+$")
LEGACY_FEATURES = frozenset({
    "001-audit-task-management",
    "002-agent-operating-readiness",
    "003-context-window-optimization",
    "004-harness-adoption-guide",
    "005-harness-changelog",
    "006-tdd-workflow",
})
HANDOFF_BLOCK = re.compile(r"```json harness-state\s*\n(.*?)\n```", re.DOTALL)
INDEX_ARTIFACT = re.compile(r"specs/[0-9]{3}-[a-z0-9-]+/(?:spec|plan|tasks|validation)\.md")
SPEC_RESULT = re.compile(r"(?im)^\*{0,2}SPEC Compliance:\*{0,2}\s*(PASS|FAIL)\s*$")
FEATURE_RESULT = re.compile(r"(?im)^\*{0,2}Feature Status:\*{0,2}\s*(VALIDATED|BLOCKED|IN_PROGRESS)\s*$")


@dataclass(frozen=True)
class Issue:
    code: str
    path: str
    detail: str


def canonical_bytes(path: Path) -> bytes:
    normalized = []
    seen_title = False
    in_header = True
    in_task = False
    in_status_section = False
    for line in path.read_text(encoding="utf-8").splitlines(keepends=True):
        content = line.rstrip("\r\n")
        ending = line[len(content):]
        heading = re.match(r"^(#{1,6}) (.+)$", content)
        if heading:
            if seen_title:
                in_header = False
            else:
                seen_title = True
            if len(heading.group(1)) <= 2:
                in_task = bool(re.match(r"TASK-\d{3}\b", heading.group(2)))
                in_status_section = "Estado" in heading.group(2)
        match = STATE_LINE.fullmatch(content)
        is_operational = in_header or in_task or (
            in_status_section and content.startswith("**Estado actual:**")
        )
        if match and is_operational and match.group(2) in DOCUMENT_STATES:
            content = f"{match.group(1)}<STATE>{match.group(3)}"
        checkbox = CHECKBOX_LINE.fullmatch(content) if path.name == "tasks.md" else None
        if checkbox:
            content = f"{checkbox.group(1)} {checkbox.group(2)}"
        order_row = ORDER_ROW.fullmatch(content) if path.name == "tasks.md" else None
        if order_row:
            content = f"{order_row.group(1)}<STATE>{order_row.group(3)}"
        four_column = ORDER_ROW_FOUR.fullmatch(content) if path.name == "tasks.md" else None
        if four_column:
            # Preserve the v1 approved TODO baseline while normalizing later task progress.
            content = f"{four_column.group(1)}TODO{four_column.group(3)}"
        normalized.append(content + ending)
    return "".join(normalized).encode("utf-8")


def _issue(issues: list[Issue], code: str, path: Path, detail: str) -> None:
    issues.append(Issue(code, str(path), detail))


def _artifact_path(root: Path, feature: Path, value: object) -> Path | None:
    if not isinstance(value, str) or not value:
        return None
    relative = Path(value)
    if relative.is_absolute() or ".." in relative.parts:
        return None
    candidate = (root / relative).resolve()
    if not candidate.is_relative_to(feature.resolve()):
        return None
    if candidate.name not in {"spec.md", "plan.md", "tasks.md"}:
        return None
    return candidate if candidate.is_file() else None


def _document_state(path: Path, issues: list[Issue]) -> str | None:
    states = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = STATE_LINE.fullmatch(line)
        if not match:
            continue
        state = match.group(2)
        if state not in DOCUMENT_STATES and state not in {
            "[CLARIFIED]", "[NEEDS",  # Clarification sections are not gates.
        }:
            _issue(issues, "INVALID_STATE", path, f"Unknown state: {state}")
        if match.group(1) == "**Estado:** ":
            states.append(state)
    return states[0] if states else None


def projected_state(root: Path) -> tuple[dict, set[str]]:
    active = []
    validated = []
    links = set()
    for feature in sorted((root / "specs").iterdir()):
        match = FEATURE_DIR.fullmatch(feature.name)
        if not match or not feature.is_dir() or feature.is_symlink():
            continue
        prefix = f"specs/{feature.name}/"
        validation = feature / "validation.md"
        if validation.is_file():
            report = validation.read_text(encoding="utf-8")
            spec_results = SPEC_RESULT.findall(report)
            feature_results = FEATURE_RESULT.findall(report)
            if spec_results and feature_results and spec_results[-1].upper() == "PASS" and feature_results[-1].upper() == "VALIDATED":
                validated.append(f"SPEC-{match.group(1)}")
                links.add(prefix + "validation.md")
                continue
        files = [feature / name for name in ("spec.md", "plan.md", "tasks.md")]
        present = [path for path in files if path.is_file()]
        if not present:
            continue
        links.update(prefix + path.name for path in present)
        spec_state = _document_state(files[0], []) if files[0].is_file() else None
        plan_state = _document_state(files[1], []) if files[1].is_file() else None
        task_state = _document_state(files[2], []) if files[2].is_file() else None
        if task_state == "COMPLETED":
            phase, next_action = "VALIDATE", "/validate"
        elif task_state in {"APPROVED", "IN_PROGRESS"}:
            phase, next_action = "IMPLEMENT", "/implement"
        elif task_state == "IN_REVIEW":
            phase, next_action = "TASKS", "approve TASKS"
        elif task_state == "DRAFT":
            phase, next_action = "TASKS", "/tasks"
        elif plan_state == "APPROVED":
            phase, next_action = "TASKS", "/tasks"
        elif plan_state == "IN_REVIEW":
            phase, next_action = "PLAN", "approve PLAN"
        elif plan_state == "DRAFT":
            phase, next_action = "PLAN", "/plan"
        elif spec_state == "APPROVED":
            phase, next_action = "PLAN", "/plan"
        elif spec_state == "IN_REVIEW":
            phase, next_action = "SPEC", "approve SPEC"
        else:
            phase, next_action = "SPEC", "/specify"
        active.append({"id": f"SPEC-{match.group(1)}", "phase": phase, "next": next_action})
    return {"schema_version": 1, "active": active, "validated": validated}, links


def _audit_projection(root: Path, issues: list[Issue]) -> None:
    expected, links = projected_state(root)
    handoff = root / "handoff.md"
    if not handoff.is_file():
        _issue(issues, "INVALID_HANDOFF", handoff, "Missing live handoff")
    else:
        blocks = HANDOFF_BLOCK.findall(handoff.read_text(encoding="utf-8"))
        if len(blocks) != 1:
            _issue(issues, "INVALID_HANDOFF", handoff, f"Expected one json harness-state block, found {len(blocks)}")
        else:
            try:
                actual = json.loads(blocks[0])
            except json.JSONDecodeError as exc:
                _issue(issues, "INVALID_HANDOFF", handoff, str(exc))
            else:
                if actual != expected:
                    _issue(issues, "STALE_HANDOFF", handoff, f"Expected {json.dumps(expected, sort_keys=True)}")
    index = root / "docs" / "index.md"
    if not index.is_file():
        _issue(issues, "STALE_INDEX", index, "Missing documentation index")
    else:
        actual_links = set(INDEX_ARTIFACT.findall(index.read_text(encoding="utf-8")))
        for missing in sorted(links - actual_links):
            _issue(issues, "STALE_INDEX", index, f"Missing link: {missing}")
        for extra in sorted(actual_links - links):
            _issue(issues, "STALE_INDEX", index, f"Obsolete link: {extra}")


def audit_repository(root: Path) -> list[Issue]:
    root = root.resolve()
    issues: list[Issue] = []
    specs = root / "specs"
    if not specs.is_dir():
        return [Issue("MISSING_SPECS", str(specs), "specs directory not found")]
    legacy_context = (
        (root / "docs" / "audit-history.md").is_file()
        and (specs / "007-chat-independent-state" / "decisions.json").is_file()
    )

    for feature in sorted(specs.iterdir()):
        match = FEATURE_DIR.fullmatch(feature.name)
        if not feature.is_dir() or not match or (legacy_context and feature.name in LEGACY_FEATURES):
            continue
        if feature.is_symlink() or not feature.resolve().is_relative_to(root):
            _issue(issues, "INVALID_FEATURE", feature, "Feature must be inside repository")
            continue
        artifacts = [feature / name for name in ("spec.md", "plan.md", "tasks.md")]
        present = [path for path in artifacts if path.is_file()]
        if not present:
            continue
        if not artifacts[0].is_file():
            _issue(issues, "MISSING_SPEC", feature, "Feature has PLAN or TASKS without SPEC")
            continue
        states = {path: _document_state(path, issues) for path in present}
        required = {
            path for path, state in states.items()
            if state in {"APPROVED", "IN_PROGRESS", "COMPLETED", "SUPERSEDED"}
        }
        ledger = feature / "decisions.json"
        if not ledger.is_file():
            _issue(issues, "MISSING_LEDGER", ledger, "New feature has no decision record")
            continue
        try:
            data = json.loads(ledger.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            _issue(issues, "INVALID_JSON", ledger, str(exc))
            continue
        if not isinstance(data, dict) or data.get("schema_version") != 1 or not isinstance(data.get("events"), list):
            _issue(issues, "INVALID_LEDGER", ledger, "Expected schema_version 1 and events list")
            continue

        ids: set[str] = set()
        approvals: dict[Path, dict] = {}
        for index, event in enumerate(data["events"]):
            label = f"event {index + 1}"
            if not isinstance(event, dict):
                _issue(issues, "INVALID_EVENT", ledger, f"{label} must be an object")
                continue
            event_id = event.get("id")
            if not isinstance(event_id, str) or not re.fullmatch(r"DECISION-\d{3,}", event_id):
                _issue(issues, "INVALID_EVENT", ledger, f"{label} has invalid id")
            elif event_id in ids:
                _issue(issues, "DUPLICATE_ID", ledger, event_id)
            else:
                ids.add(event_id)
            for field in ("actor", "date", "decision", "scope", "source"):
                if not isinstance(event.get(field), str) or not event[field].strip():
                    _issue(issues, "INVALID_EVENT", ledger, f"{label} missing {field}")
            try:
                date.fromisoformat(event["date"])
            except (KeyError, TypeError, ValueError):
                _issue(issues, "INVALID_EVENT", ledger, f"{label} has invalid date")
            if event.get("kind") not in {"APPROVAL", "DECISION", "REVOCATION", "SUPERSESSION"}:
                _issue(issues, "INVALID_EVENT", ledger, f"{label} has invalid kind")
                continue
            artifact = _artifact_path(root, feature, event.get("artifact"))
            if artifact is None:
                _issue(issues, "INVALID_ARTIFACT", ledger, f"{label} has invalid artifact")
                continue
            predecessor = event.get("supersedes")
            if predecessor is not None:
                active = approvals.get(artifact)
                if active is None or active.get("id") != predecessor:
                    _issue(issues, "INVALID_SUPERSESSION", ledger, f"{label} has no active predecessor")
                    continue
                del approvals[artifact]
            if event["kind"] in {"REVOCATION", "SUPERSESSION"}:
                if predecessor is None:
                    _issue(issues, "INVALID_SUPERSESSION", ledger, f"{label} needs supersedes")
                continue
            if event["kind"] != "APPROVAL":
                continue
            digest = event.get("artifact_sha256")
            if not isinstance(digest, str) or not HEX_DIGEST.fullmatch(digest):
                _issue(issues, "INVALID_EVENT", ledger, f"{label} has invalid digest")
                continue
            if artifact in approvals:
                _issue(issues, "CONFLICTING_APPROVAL", ledger, f"{label} duplicates {artifact.name}")
                continue
            approvals[artifact] = event
        for artifact, event in approvals.items():
            label = event["id"]
            actual = hashlib.sha256(canonical_bytes(artifact)).hexdigest()
            if actual != event["artifact_sha256"]:
                _issue(issues, "HASH_MISMATCH", artifact, f"{label} approved different content")
        for artifact in required - approvals.keys():
            _issue(issues, "MISSING_APPROVAL", artifact, "Gate state has no approval event")
    _audit_projection(root, issues)
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Check repository SDD approval state")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    issues = audit_repository(args.root)
    for issue in issues:
        print(f"{issue.code}: {issue.path}: {issue.detail}")
    print("HARNESS STATE: PASS" if not issues else f"HARNESS STATE: FAIL ({len(issues)})")
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
