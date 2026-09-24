# Validation Report

## Metadata

**Validation ID:** VALIDATION-[XXX]

**SPEC:** SPEC-[XXX]

**PLAN:** PLAN-[XXX]

**TASKS:** TASKS-[XXX]

**Status:** DRAFT

**Result:** PENDING

**Date:** YYYY-MM-DD

**Validated by:** [PENDING]

---

# 1. Objetivo

Validar que la implementación final cumple la especificación
aprobada y que existe evidencia suficiente para demostrarlo.

La validación deberá reconstruir la trazabilidad completa:

Requirement
→ Acceptance Criterion
→ Plan
→ Task
→ Implementation
→ Test
→ Evidence

Este documento representa el gate final de la feature.

---

# 2. Artefactos validados

## Specification

**ID:** SPEC-[XXX]

**Version:** [X.Y.Z]

**Status:** APPROVED

**Path:**

specs/<feature-id>/spec.md

---

## Plan

**ID:** PLAN-[XXX]

**Version:** [X.Y.Z]

**Status:** APPROVED

**Path:**

specs/<feature-id>/plan.md

---

## Tasks

**ID:** TASKS-[XXX]

**Version:** [X.Y.Z]

**Status:** COMPLETED

**Path:**

specs/<feature-id>/tasks.md

---

## Implementation

**Reference:**

[Branch / commit / working tree / other reference]

---

# 3. Precondition Check

| Check | Result | Evidence |
|---|---|---|
| SPEC exists | PENDING | |
| SPEC is APPROVED | PENDING | |
| PLAN exists | PENDING | |
| PLAN is APPROVED | PENDING | |
| TASKS exists | PENDING | |
| Required TASKS are DONE | PENDING | |
| TASKS document is COMPLETED | PENDING | |
| No blocking clarification exists | PENDING | |
| No known blocking issue exists | PENDING | |
| Implementation exists | PENDING | |

Allowed results:

- PASS
- FAIL
- BLOCKED
- NOT_APPLICABLE

If a mandatory precondition cannot be satisfied:

VALIDATION STATUS: BLOCKED

---

# 4. Functional Requirement Coverage

| Requirement | Priority | Acceptance Criteria | Evidence | Result |
|---|---|---|---|---|
| FR-001 | MUST | AC-001 | TEST-001 | PENDING |

Allowed results:

- PASS
- FAIL
- BLOCKED
- NOT_APPLICABLE

Every MUST requirement shall reach PASS before final validation
can result in PASS.

---

# 5. Non-Functional Requirement Coverage

| Requirement | Category | Evidence | Result |
|---|---|---|---|
| NFR-001 | [Category] | [Evidence] | PENDING |

Non-functional requirements shall use measurable or otherwise
verifiable evidence appropriate to the requirement.

---

# 6. Security Requirement Coverage

| Requirement | Acceptance Criteria | Evidence | Result |
|---|---|---|---|
| SEC-001 | AC-004 | TEST-004 | PENDING |

Every mandatory security requirement shall have explicit evidence.

A mandatory security requirement in FAIL prevents final PASS.

---

# 7. Acceptance Criteria Validation

## AC-001 — [Título]

**Related requirements:**

- FR-[XXX]

### Given

[Initial condition]

### When

[Action]

### Then

[Expected behavior]

### Evidence

- TEST-[XXX]
- [Other evidence]

### Result

PENDING

---

# 8. Test Results

| Test | Type | Related Requirement | Related AC | Result |
|---|---|---|---|---|
| TEST-001 | UNIT | FR-001 | AC-001 | PENDING |
| TEST-002 | INTEGRATION | FR-002 | AC-002 | PENDING |
| TEST-004 | SECURITY | SEC-001 | AC-004 | PENDING |

Supported test types include:

- UNIT
- INTEGRATION
- CONTRACT
- E2E
- SECURITY
- REGRESSION
- OTHER

Supported results:

- PASS
- FAIL
- BLOCKED
- NOT_RUN
- NOT_APPLICABLE

FAIL, BLOCKED and NOT_RUN do not constitute evidence of compliance.

---

# 9. Evidence Quality Review

Verify that evidence is meaningful.

- [ ] Tests contain meaningful assertions.
- [ ] Required tests are not skipped.
- [ ] Mocks do not remove the behavior being validated.
- [ ] Tests verify behavior rather than implementation details only.
- [ ] Acceptance criteria have sufficient evidence.
- [ ] Evidence corresponds to the current SPEC.
- [ ] No evidence was weakened to obtain PASS.

Findings:

[None / findings]

---

# 10. Quality Gates

| Gate | Result | Evidence |
|---|---|---|
| Format | PENDING | |
| Lint | PENDING | |
| Type Check | PENDING | |
| Unit Tests | PENDING | |
| Integration Tests | PENDING | |
| Contract Tests | PENDING | |
| E2E Tests | PENDING | |
| Security Checks | PENDING | |
| Build | PENDING | |

Use NOT_APPLICABLE when a gate does not exist or does not apply,
with justification when necessary.

---

# 11. Security Validation

Review when applicable:

- authentication;
- authorization;
- ownership;
- input validation;
- sensitive data;
- secrets;
- destructive operations;
- file uploads;
- external integrations;
- logging;
- error exposure;
- data access.

## Findings

| ID | Requirement | Finding | Severity | Status |
|---|---|---|---|---|
| SEC-FINDING-001 | SEC-[XXX] | [Finding] | LOW / MEDIUM / HIGH | OPEN |

Estados permitidos para un security finding:

OPEN
MITIGATED
ACCEPTED
NOT_APPLICABLE

Semántica:

- `OPEN`: el finding permanece sin resolver.
- `MITIGATED`: se aplicó una mitigación y existe evidencia suficiente
  para evaluar su efectividad.
- `ACCEPTED`: el riesgo fue aceptado mediante la autoridad
  correspondiente.
- `NOT_APPLICABLE`: se determinó justificadamente que el finding
  no aplica.

`ACCEPTED` no constituye por sí mismo evidencia de cumplimiento
de un requisito de seguridad y no permite automáticamente
un resultado `PASS`.

`MITIGATED` requiere evidencia suficiente.

Si la aceptación o resolución implica una excepción, cambio de
requisito, cambio de alcance o cambio técnico, deberá actualizarse
el artefacto propietario correspondiente y recuperarse los approval
gates aplicables antes de continuar.

Si no hay hallazgos:

No se identificaron hallazgos de seguridad que impidan el acceso.

---

# 12. Scope Validation

## Files Created

- [path]

## Files Modified

- [path]

## Files Removed

- [path]

## Dependencies Added

- [dependency]

## Migrations

- [migration]

## Configuration Changes

- [change]

Each change shall be classified as:

AUTHORIZED
MINOR_DEVIATION
UNAUTHORIZED_CHANGE

---

# 13. Scope Deviations

| ID | Change | Classification | Justification | Blocking |
|---|---|---|---|---|
| DEV-001 | [Change] | [Classification] | [Reason] | YES / NO |

A significant UNAUTHORIZED_CHANGE prevents final PASS until
resolved or incorporated through the SDD process.

---

# 14. Architecture Validation

Verify implementation against:

- approved PLAN;
- architecture standard;
- applicable ADRs.

Checklist:

- [ ] Component boundaries respected.
- [ ] Responsibilities respected.
- [ ] Dependency direction respected.
- [ ] Contracts respected.
- [ ] Data model matches approved design.
- [ ] Integrations match approved design.
- [ ] ADR decisions respected.
- [ ] No unapproved architecture introduced.

## Architecture Deviations

[None / findings]

---

# 15. Regression Validation

Relevant existing tests:

- [TEST / suite]

Result:

PENDING

Known regressions:

[None / list]

An unresolved confirmed regression prevents final PASS unless
the previous behavior was explicitly superseded by an approved SPEC.

---

# 16. Task Validation

| Task | Objective Completed | Tests | Evidence | DoD | Result |
|---|---|---|---|---|---|
| TASK-001 | PENDING | PENDING | PENDING | PENDING | PENDING |

A TASK marked DONE without sufficient evidence shall be considered
a validation failure until corrected.

---

# 17. Discoveries

| Discovery | Description | Classification | Action |
|---|---|---|---|
| DISCOVERY-001 | [Description] | BLOCKING / NON_BLOCKING | [Action] |

Blocking discoveries shall be resolved before final PASS.

Non-blocking discoveries may be moved to future work.

---

# 18. Final Traceability Matrix

| Requirement | Acceptance | Plan | Task | Implementation | Test | Evidence | Result |
|---|---|---|---|---|---|---|---|
| FR-001 | AC-001 | DEC-001 | TASK-001 | [path/reference] | TEST-001 | [evidence] | PENDING |
| SEC-001 | AC-004 | DEC-002 | TASK-002 | [path/reference] | TEST-004 | [evidence] | PENDING |

Every mandatory traceability chain shall terminate in sufficient
evidence and PASS.

---

# 19. Traceability Gaps

Check for:

- Requirement without Acceptance Criterion.
- Acceptance Criterion without implementation coverage.
- Acceptance Criterion without evidence.
- Required PLAN item without TASK.
- TASK without justification.
- Implementation without TASK.
- Required behavior without test or equivalent evidence.
- Test without relevant behavior.

## Gaps

| ID | Type | Artifact | Description | Blocking |
|---|---|---|---|---|
| GAP-001 | [Type] | [Reference] | [Description] | YES / NO |

If none:

No traceability gaps identified.

---

# 20. Validation Findings

All relevant validation problems shall be recorded.

## FINDING-001 — [Title]

**Type:**

IMPLEMENTATION
TASK
PLAN
SPEC
SECURITY
REGRESSION
TRACEABILITY
SCOPE
ARCHITECTURE
ENVIRONMENT

**Severity:**

LOW
MEDIUM
HIGH

**Related artifacts:**

- [Artifact]

**Description:**

[Finding]

**Evidence:**

[Evidence]

**Status:**

OPEN

**Required action:**

[Action]

---

# 21. Findings Summary

| Severity | Open | Resolved |
|---|---:|---:|
| HIGH | 0 | 0 |
| MEDIUM | 0 | 0 |
| LOW | 0 | 0 |

Blocking findings:

0

---

# 22. Requirement Summary

Functional Requirements:

PASS: 0
FAIL: 0
BLOCKED: 0

Non-Functional Requirements:

PASS: 0
FAIL: 0
BLOCKED: 0

Security Requirements:

PASS: 0
FAIL: 0
BLOCKED: 0

Acceptance Criteria:

PASS: 0
FAIL: 0
BLOCKED: 0

---

# 23. Test Summary

Unit:

PASS: 0
FAIL: 0
BLOCKED: 0

Integration:

PASS: 0
FAIL: 0
BLOCKED: 0

Contract:

PASS: 0
FAIL: 0
BLOCKED: 0

E2E:

PASS: 0
FAIL: 0
BLOCKED: 0

Security:

PASS: 0
FAIL: 0
BLOCKED: 0

Regression:

PASS: 0
FAIL: 0
BLOCKED: 0

---

# 24. Final Gate

Final validation may result in PASS only when:

- [ ] All MUST requirements are PASS.
- [ ] All mandatory acceptance criteria are PASS.
- [ ] Required tests are PASS.
- [ ] Mandatory quality gates are PASS.
- [ ] Mandatory security requirements are PASS.
- [ ] No known regression remains unresolved.
- [ ] No blocking traceability gap exists.
- [ ] No significant unauthorized change exists.
- [ ] No blocking architecture deviation exists.
- [ ] No blocking finding remains OPEN.
- [ ] No required TASK remains incomplete.
- [ ] Evidence is sufficient.

---

# 25. Final Result

**Validation Status:**

DRAFT

**SPEC Compliance:**

PENDING

Allowed final results:

PASS
FAIL
BLOCKED

**Feature Status:**

NOT_VALIDATED

When final result is PASS:

Feature Status:

VALIDATED

---

# 26. Required Next Action

If PASS:

No corrective action required.

If implementation defect:

Return to:

/implement

Apply the reopening procedure in `/implement`, section 17.1, before code
changes: link the finding, reopen TASKS and affected tasks, retain previous
evidence and recheck preconditions. Complete TASKS again and repeat
`/validate` after the correction; reopening alone does not establish PASS.

If task decomposition defect:

Return to:

/tasks

If technical design defect:

Return to:

/plan

If requirement defect or ambiguity:

Return to:

/specify
or
/clarify

If external blocker:

Resolve blocker and repeat:

/validate

---

# 27. Approval

**Validated by:**

[Human / authorized validator]

**Date:**

YYYY-MM-DD

**Notes:**

[Optional notes]
