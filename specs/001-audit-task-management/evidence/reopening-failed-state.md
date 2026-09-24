# Fixture validation — FINDING-001

SIMULATED ARTIFACT; actual test results from the isolated copy.
Observed UTC: 2026-09-24 16:52:48 UTC
Type: IMPLEMENTATION. Severity: MEDIUM. Status: OPEN.
Requirement: FR-002. Acceptance: AC-003. Owner: TASK-001.
Cause: deliberately injected reverse iteration, authorized by PLAN §11.3 / TASK-004.
Evidence: reopening-failed.txt, exit 1, 11 tests, 4 failures (TEST-001/003/005/011).
Fixture source SHA-256: 841660c2f3adf22e7a7da961b40d9d59bb9dcc0f4693ce68d141877e18380bbe
Unchanged tests SHA-256: f158bfac7d3e4db109805a00c67760480cfb8c049726e7bc5dc2e1e14838d512

Fixture SPEC COMPLIANCE: FAIL
Fixture FEATURE STATUS: NOT_VALIDATED
Prior PASS does not apply to the altered source. Other requirement results
are not inferred from the old evidence. No new Harness audit finding is claimed.
Required action: /implement §17.1; reopen affected fixture tasks before correction.
