# AUDIT-08 fixture — reopened before correction

SIMULATED STATE; real TASKS remains IN_PROGRESS with real TASK-004 active.
Recorded UTC: 2026-09-24 16:52:48 UTC
Finding: FINDING-001 (see reopening-failed-state.md).
Fixture TASKS: COMPLETED → IN_PROGRESS
TASK-001: DONE → TODO → IN_PROGRESS
TASK-002: DONE → TODO (TEST-005 evidence invalidated by changed listing)
TASK-003: DONE → TODO (TEST-011/repeatability evidence invalidated)

Preflight TASK-001: no dependencies; correction restores approved ordering;
SPEC/PLAN/authorized work unchanged; no approval recovery needed for state/evidence.
The finding is the correction target, not an independent blocker. No independent
blocker exists. Original assertions and all prior logs remain available.
TASK-002 and TASK-003 cannot start until their dependencies are DONE.
