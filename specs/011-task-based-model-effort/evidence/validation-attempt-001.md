# Validation Report

## Metadata

**Validation ID:** VALIDATION-001  
**SPEC:** SPEC-011  
**PLAN:** PLAN-011  
**TASKS:** TASKS-011  
**Status:** BLOCKED  
**Result:** BLOCKED  
**Date:** 2026-10-27  
**Validated by:** Harness implementation agent

# 1. Objetivo

Validar SPEC-011 v0.1.0 contra la implementación y evidencia local. La
validación queda BLOCKED porque no se completaron smokes reales en runtimes y
combinaciones modelo/proveedor; no se presume PASS a partir de CLIs falsos.

# 2. Artefactos validados

## Specification

**ID:** SPEC-011  
**Version:** 0.1.0  
**Status:** APPROVED  
**Path:** `spec.md`

## Plan

**ID:** PLAN-011  
**Version:** 0.1.0  
**Status:** APPROVED  
**Path:** `plan.md`

## Tasks

**ID:** TASKS-011  
**Version:** 0.1.0  
**Status:** COMPLETED  
**Path:** `tasks.md`

## Implementation

`src/effort_policy.py`, `src/run_task.py`, `src/adopt_harness.py`, pruebas y
documentación enlazadas en `evidence/task-001.md` a `evidence/task-006-compatibility.md`.
FINDING-001 se corrigió y se conserva su historial en
`evidence/finding-001.md` y `evidence/finding-001-resolution.md`.

# 3. Precondition Check

| Gate | Result | Evidence |
|------|--------|----------|
| SPEC/PLAN aprobados, ledger y huellas vigentes | PASS | `decisions.json`; `PYTHONDONTWRITEBYTECODE=1 python3 src/check_harness_state.py` |
| TASKS COMPLETED y TASK requeridas DONE | PASS | `tasks.md`; checker PASS |
| Sin bloqueos pendientes e implementación presente | BLOCKED | Implementación presente; TEST-015/016 NOT_RUN y TEST-017 BLOCKED en `evidence/task-006-compatibility.md` |

# 4. Functional Requirement Coverage

| FR | AC | TASK/cambio | TEST/evidencia | Result |
|----|----|-------------|----------------|--------|
| FR-001 | AC-001 | TASK-002/003; `src/effort_policy.py`, `src/run_task.py` | TEST-001..008; `evidence/task-002.md`, `evidence/task-003.md` | BLOCKED |
| FR-002 | AC-002 | TASK-004; fallback controlado | TEST-009..011; `evidence/task-004.md` | BLOCKED |
| FR-003 | AC-003 | TASK-003/005/006; adaptadores y adopción | TEST-005..017; `evidence/task-003.md`, `evidence/task-005.md`, `evidence/task-006-compatibility.md` | BLOCKED |

Los contratos automatizados simulados pasan. Los requisitos funcionales
incluyen comportamiento con las combinaciones reales requeridas y no pueden
cerrarse con esos dobles solamente.

# 5. Non-Functional Requirement Coverage

| NFR | AC | Evidencia/métrica | Result |
|-----|----|------------------|--------|
| NFR-001 | AC-001 | La policy es determinista; falta comparación reproducible de duración/resultado frente a `medium` en runtimes reales. `evidence/task-003.md` | BLOCKED |
| NFR-002 | AC-001, AC-003 | Contratos simulados para los tres adaptadores; sin matriz de smoke real por CLI/modelo/proveedor. `evidence/task-006-compatibility.md` | BLOCKED |

# 6. Security Requirement Coverage

SPEC-011 no define requisitos `SEC-[XXX]` específicos. NOT_APPLICABLE para la
matriz SEC de SPEC. Se revisaron entradas, archivos de tarea, manejo de
errores, subprocess, logs, permisos y límites externos conforme a
`.spec/standards/security.md`; evidencia en `evidence/task-003.md` y
`evidence/task-004.md`.

# 7. Acceptance Criteria Validation

| AC | TEST/verificación y evidencia | Result |
|----|-------------------------------|--------|
| AC-001 | TEST-001..008; `evidence/task-002.md`, `evidence/task-003.md`; smoke real TEST-015/016 NOT_RUN y TEST-017 BLOCKED | BLOCKED |
| AC-002 | TEST-009..011; `evidence/task-004.md`; runtime real TEST-015..017 sin completar | BLOCKED |
| AC-003 | TEST-005..008; `evidence/task-003.md`; TEST-015..017; `evidence/task-006-compatibility.md` | BLOCKED |

## AC-001 — Selección y aplicación para una tarea

**Related requirements:** FR-001  
**Given:** Tarea y combinación runtime/modelo.  
**When:** Se inicia por runner.  
**Then:** Se clasifica y pasa el control nativo correspondiente.  
**Evidence:** Contratos simulados PASS; smokes reales pendientes en `evidence/task-006-compatibility.md`.  
**Result:** BLOCKED

## AC-002 — Runtime sin capacidad de ajuste

**Related requirements:** FR-002  
**Given:** El runtime/modelo no admite el nivel solicitado.  
**When:** El runner procesa la tarea.  
**Then:** Reintenta una vez sin override e informa el fallback.  
**Evidence:** Contrato de fallback simulado PASS en `evidence/task-004.md`; firmas reales de rechazo no verificadas con los tres CLIs.  
**Result:** BLOCKED

## AC-003 — Runtimes y proveedores requeridos

**Related requirements:** FR-003  
**Given:** Claude Code, Codex u OpenCode con un proveedor/modelo compatible.  
**When:** Se ejecuta la tarea por el runner.  
**Then:** Se aplica el control disponible o se usa fallback.  
**Evidence:** Contratos simulados PASS; combinaciones reales no verificadas en `evidence/task-006-compatibility.md`.  
**Result:** BLOCKED

# 8. Test Results

| TEST | Type | FR/AC/SEC | Command/evidence | Result |
|------|------|-----------|------------------|--------|
| TEST-001 | UNIT | FR-001, AC-001 | `python3 -m unittest discover -s tests -p 'test_effort_policy.py' -v`; `evidence/task-002.md` | PASS |
| TEST-002 | UNIT | FR-001, AC-001 | `python3 -m unittest discover -s tests -p 'test_effort_policy.py' -v`; `evidence/task-002.md` | PASS |
| TEST-003 | UNIT | FR-001, AC-001 | `python3 -m unittest discover -s tests -p 'test_effort_policy.py' -v`; `evidence/task-002.md` | PASS |
| TEST-004 | UNIT | FR-001, AC-001 | `python3 -m unittest discover -s tests -p 'test_effort_policy.py' -v`; `evidence/task-002.md` | PASS |
| TEST-005 | CONTRACT | FR-001, FR-003, AC-001/003 | `python3 -m unittest discover -s tests -p 'test_run_task.py' -v`; `evidence/task-003.md` | PASS |
| TEST-006 | SECURITY | FR-001, AC-001 | Mismo comando; dry-run sin contenido de tarea; `evidence/task-003.md` | PASS |
| TEST-007 | SECURITY | FR-001, AC-001 | Mismo comando; metacaracteres tratados como datos; `evidence/task-003.md` | PASS |
| TEST-008 | CONTRACT | FR-001, AC-001 | Mismo comando; validación y CLI ausente; `evidence/task-003.md` | PASS |
| TEST-009 | CONTRACT | FR-002, AC-002 | `python3 -m unittest discover -s tests -p 'test_run_task.py' -v`; `evidence/task-004.md` | PASS |
| TEST-010 | SECURITY | FR-002, AC-002 | Mismo comando; errores ajenos no reintentan; `evidence/task-004.md` | PASS |
| TEST-011 | CONTRACT | FR-002, AC-002 | Mismo comando; máximo un retry; `evidence/task-004.md` | PASS |
| TEST-012 | INTEGRATION | FR-001, AC-001 | `python3 -m unittest discover -s tests -p 'test_adopt_harness.py' -v`; `evidence/task-005.md` | PASS |
| TEST-013 | INTEGRATION | FR-001, AC-001 | Mismo comando; colisiones sin copia parcial; `evidence/task-005.md` | PASS |
| TEST-014 | OTHER | FR-003, AC-003 | Mismo comando; rutas y documentación de adopción; `evidence/task-005.md` | PASS |
| TEST-015 | E2E | FR-003, AC-001..003 | Smoke Claude Code; `evidence/task-006-compatibility.md` | NOT_RUN |
| TEST-016 | E2E | FR-003, AC-001..003 | Smoke Codex CLI; `evidence/task-006-compatibility.md` | NOT_RUN |
| TEST-017 | E2E | FR-003, AC-001..003 | Smoke OpenCode; `evidence/task-006-compatibility.md` | BLOCKED |

## 8.1 TDD Evidence Review

| TASK / TEST | Aplicabilidad | RED y causa | GREEN / refactor | Motivo y alternativa si N/A | Resultado |
|-------------|---------------|-------------|------------------|-----------------------------|-----------|
| TASK-001 | NO APLICA | N/A | Revisión de contenido | Documentación y ADR; revisión manual registrada en `evidence/task-001.md` | PASS |
| TASK-002 / TEST-001..004 | OBLIGATORIO | RED por policy inicial que siempre devolvía medium | 6 tests PASS | N/A | PASS |
| TASK-003 / TEST-005..008 | OBLIGATORIO | RED contractual y FINDING-001 de importación directa | 9 tests PASS; evidencia en `evidence/task-003.md` y `evidence/finding-001-resolution.md` | N/A | PASS |
| TASK-004 / TEST-009..011 | OBLIGATORIO | RED de fallback y límite de retries | 8 tests PASS | N/A | PASS |
| TASK-005 / TEST-012..014 | OBLIGATORIO | RED por archivos no incluidos en allowlist | 11 tests PASS | N/A | PASS |
| TASK-006 / TEST-015..017 | NO APLICA | N/A | Integración real no ejecutable/disponible; NOT_RUN/BLOCKED en evidencia | Smoke real requiere combinación de modelo y acceso local; simulados cubren contratos, no el servicio real | BLOCKED |

# 9. Evidence Quality Review

- [x] Aserciones significativas, tests requeridos habilitados, dobles representativos de los contratos.
- [x] Pruebas verifican conducta y AC; no se debilitó evidencia para PASS.

Finding resuelto: FINDING-001, corregido y probado con RED/GREEN conservados.
La evidencia del smoke real sigue incompleta y causa BLOCKED.

# 10. Quality Gates

| Gate | Result | Evidence |
|------|--------|----------|
| Format/Lint/Types | NOT_APPLICABLE | El repo no configura formatter/linter/tipos para estos scripts Python. |
| Unit/Integration/Contract/E2E/Security | BLOCKED | Suite completa 71 tests PASS; TEST-015/016 NOT_RUN y TEST-017 BLOCKED. |
| Build | NOT_APPLICABLE | No hay build ni empaquetado Python configurado. |

# 11. Security Validation

La policy es local y no maneja credenciales. El runner valida agente/modelo,
restringe archivos a rutas regulares dentro del cwd, rechaza symlinks, usa
argumentos de lista sin shell, no registra el contenido de tarea y no cambia
permisos del CLI. OpenCode recibe un archivo temporal con modo `0600` eliminado
al salir. Se heredan autenticación y permisos del runtime elegido.

## Findings

No hay SEC-FINDING abiertos aplicables. La compatibilidad no probada se registra
como bloqueo de validación funcional, no como finding de seguridad.

# 12. Scope Validation

## Files Created

`docs/agents/model-effort.md`, `docs/decisions/ADR-001-model-effort-runtime-adapters.md`, `src/effort_policy.py`, `src/run_task.py`, `tests/test_effort_policy.py`, `tests/test_run_task.py`, `specs/011-task-based-model-effort/evidence/` y este reporte.

## Files Modified

`AGENTS.md`, `docs/adoption.md`, `docs/index.md`, `docs/quickstart.md`, `handoff.md`, `src/adopt_harness.py`, `tests/test_adopt_harness.py`, `specs/011-task-based-model-effort/tasks.md`.

## Files Removed

Ninguno.

## Dependencies Added

Ninguna.

## Migrations

Ninguna.

## Configuration Changes

Ninguna; no se cambió configuración de usuario/CLI.

# 13. Scope Deviations

| ID | Change | Classification | Reason | Blocking |
|----|--------|----------------|--------|----------|
| DEV-001 | Corrección de import para el punto de entrada como script | AUTHORIZED | Defecto local de TASK-003 descubierto al verificar el comando documentado; evidencia `finding-001.md` | NO |

# 14. Architecture Validation

Conforme a PLAN-011 y ADR-001: policy determinista separada, wrapper delgado,
adaptadores por CLI, subprocess sin shell, sin persistencia ni dependencias
nuevas, y autenticación/permisos delegados al runtime.

## Architecture Deviations

Ninguna conocida. Las opciones nativas están verificadas con contratos
simulados; su aceptación real por combinación CLI/modelo sigue bloqueada.

# 15. Regression Validation

| TEST/flujo | Resultado | Evidencia |
|------------|-----------|-----------|
| Suite completa: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v` | PASS, 71 tests | Ejecución del 2026-10-27 |
| `PYTHONDONTWRITEBYTECODE=1 python3 src/check_harness_state.py` | PASS | Checker posterior al cierre de TASKS |
| Entrada directa del runner en dry-run | PASS | `evidence/finding-001-resolution.md` |

# 16. Task Validation

| TASK | DoD y evidencia | Result |
|------|----------------|--------|
| TASK-001 | `evidence/task-001.md` | PASS |
| TASK-002 | `evidence/task-002.md` | PASS |
| TASK-003 | `evidence/task-003.md`, `evidence/finding-001-resolution.md` | PASS |
| TASK-004 | `evidence/task-004.md` | PASS |
| TASK-005 | `evidence/task-005.md` | PASS |
| TASK-006 | `evidence/task-006-compatibility.md`; no-run reasons documentados según DoD | PASS |

# 17. Discoveries

| ID | Hallazgo | Blocking | Acción |
|----|----------|----------|--------|
| Ninguno | — | — | — |

# 18. Final Traceability Matrix

| Requirement | AC | Plan | Task | Implementation | Test/Evidence | Result |
|-------------|----|------|------|----------------|---------------|--------|
| FR-001 | AC-001 | DEC-001/002 | TASK-002/003 | `src/effort_policy.py`, `src/run_task.py` | TEST-001..008; `evidence/task-002.md`, `evidence/task-003.md` | BLOCKED |
| FR-002 | AC-002 | DEC-003/004 | TASK-004 | `src/run_task.py` fallback | TEST-009..011; `evidence/task-004.md` | BLOCKED |
| FR-003 | AC-003 | DEC-001/003/004 | TASK-003/005/006 | adaptadores y adopción | TEST-005..017; `evidence/task-003.md`, `evidence/task-005.md`, `evidence/task-006-compatibility.md` | BLOCKED |
| NFR-001 | AC-001 | RISK-003 | TASK-006 | métrica de duración disponible en runner | benchmark real pendiente; `evidence/task-006-compatibility.md` | BLOCKED |
| NFR-002 | AC-001/003 | RISK-001 | TASK-003/006 | adaptadores y tests de contrato | TEST-005..017; `evidence/task-006-compatibility.md` | BLOCKED |
| BR-001 | AC-001/002 | DEC-003 | TASK-002/004 | clases y fallback seguro | TEST-001..011; `evidence/task-002.md`, `evidence/task-004.md` | PASS local / integración BLOCKED |

# 19. Traceability Gaps

## Gaps

| ID | Type | Artifact | Description | Blocking |
|----|------|----------|-------------|----------|
| GAP-001 | ENVIRONMENT / INTEGRATION | `evidence/task-006-compatibility.md` | Falta ejecutar smoke real por CLI con modelo/proveedor configurado; OpenCode no pudo iniciarse y Claude/Codex no se invocaron por no disponer de combinación/consumo confirmado. | YES |
| GAP-002 | PERFORMANCE | `evidence/task-006-compatibility.md` | No hay benchmark real contra baseline fijo `medium` para NFR-001. | YES |

# 20. Validation Findings

## FINDING-001 — Import del runner en ejecución directa

**Type:** IMPLEMENTATION  
**Severity:** MEDIUM  
**Related artifacts:** TASK-003, TEST-008  
**Description:** El script no importaba la policy al ejecutarse directamente.  
**Evidence:** `evidence/finding-001.md`, `evidence/finding-001-resolution.md`  
**Status:** RESOLVED  
**Required action:** Corregido y probado con test de regresión.

## FINDING-002 — Smokes reales y benchmark pendientes

**Type:** ENVIRONMENT  
**Severity:** HIGH  
**Related artifacts:** FR-001..003, NFR-001..002, AC-001..003, TEST-015..017  
**Description:** No se pudo demostrar compatibilidad con solicitudes reales en las combinaciones de runtime/modelo requeridas ni medir la política frente a baseline.  
**Evidence:** `evidence/task-006-compatibility.md`  
**Status:** OPEN  
**Required action:** Proveer/confirmar combinaciones de modelo y disponibilidad para smokes y benchmark; resolver el acceso local de OpenCode y repetir `/validate`.

# 21. Findings Summary

| Severity | Open | Resolved |
|----------|-----:|---------:|
| HIGH | 1 | 0 |
| MEDIUM | 0 | 1 |
| LOW | 0 | 0 |

Blocking findings: 1.

# 22. Requirement Summary

| Grupo | PASS | FAIL | BLOCKED |
|-------|-----:|-----:|--------:|
| FR | 0 | 0 | 3 |
| NFR | 0 | 0 | 2 |
| SEC | 0 | 0 | 0 |
| AC | 0 | 0 | 3 |

# 23. Test Summary

| Tipo | PASS | FAIL | BLOCKED |
|------|-----:|-----:|--------:|
| Unit | 6 | 0 | 0 |
| Integration | 11 | 0 | 0 |
| Contract | 9 | 0 | 0 |
| E2E | 0 | 0 | 3 |
| Security | 3 | 0 | 0 |
| Regression | 71 | 0 | 0 |

De los tres E2E, TEST-015/016 son NOT_RUN y TEST-017 está BLOCKED; ninguno
cuenta como PASS.

# 24. Final Gate

- [ ] MUST, AC, TEST, calidad y SEC obligatorios en PASS; evidencia TDD aplicable válida o N/A justificado con alternativa.
- [x] TASKS COMPLETED, todas las TASK requeridas DONE y evidencia de tarea disponible.
- [ ] Sin regresiones, gaps, cambios no autorizados, desviaciones arquitectónicas ni findings OPEN bloqueantes.

# 25. Final Result

**Validation Status:** BLOCKED  
**SPEC Compliance:** BLOCKED  
**Feature Status:** NOT_VALIDATED

La evidencia local y suite automatizada pasan, pero permanecen TEST E2E sin
ejecutar y gaps bloqueantes de compatibilidad/performance. No se declara
conformidad ni feature validada.

# 26. Required Next Action

Resolver GAP-001 y GAP-002 con combinaciones modelo/proveedor disponibles,
ejecutar smokes reales y baseline de rendimiento sin cambiar credenciales ni
permisos; actualizar `evidence/task-006-compatibility.md` y repetir `/validate`.

# 27. Approval

**Validated by:** Harness implementation agent  
**Date:** 2026-10-27  
**Notes:** Resultado BLOCKED; no equivale a aprobación humana ni a cierre funcional.
