# Validation Report

## Metadata

**Validation ID:** VALIDATION-002  
**SPEC:** SPEC-011  
**PLAN:** PLAN-011  
**TASKS:** TASKS-011  
**Status:** BLOCKED  
**Result:** BLOCKED  
**Date:** 2026-11-03  
**Validated by:** Harness implementation agent

# 1. Objetivo

Repetir la validación de SPEC-011 v0.1.0 con evidencia real de runtime, ahora
que el usuario autorizó consumo y la combinación Claude Code +
`claude-sonnet-5-5`. VALIDATION-001 se conserva en
`evidence/validation-attempt-001.md` y `evidence/validation-attempt-002.md`
(estado final de VALIDATION-001, con FINDING-003/004).

El resultado sigue BLOCKED. TEST-015 y el benchmark NFR-001 pasan, pero
TEST-016 (Codex) sigue NOT_RUN y TEST-017 (OpenCode) sigue BLOCKED por
decisión del usuario. Tampoco hay evidencia real con los proveedores DeepSeek
y GLM que exige NFR-002.

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

`src/effort_policy.py`, `src/run_task.py` y `src/adopt_harness.py`, más las
pruebas y la documentación enlazadas en `evidence/task-001.md` a
`evidence/task-006-compatibility.md`. Evidencia real nueva en
`evidence/validation-002-real-runtime.md`. Esta validación no modificó código.

# 3. Precondition Check

| Gate | Result | Evidence |
|------|--------|----------|
| SPEC/PLAN aprobados, ledger y huellas vigentes | PASS | `decisions.json`; `PYTHONDONTWRITEBYTECODE=1 python3 src/check_harness_state.py` → PASS (2026-11-03) |
| TASKS COMPLETED y TASK requeridas DONE | PASS | `tasks.md`; checker PASS |
| Sin bloqueos pendientes e implementación presente | BLOCKED | Implementación presente; TEST-016 NOT_RUN y TEST-017 BLOCKED en `evidence/validation-002-real-runtime.md` |

# 4. Functional Requirement Coverage

| FR | AC | TASK/cambio | TEST/evidencia | Result |
|----|----|-------------|----------------|--------|
| FR-001 | AC-001 | TASK-002/003; `src/effort_policy.py`, `src/run_task.py` | TEST-001..008 y TEST-015; `evidence/task-002.md`, `evidence/task-003.md`, `evidence/validation-002-real-runtime.md` | PASS |
| FR-002 | AC-002 | TASK-004; fallback controlado | TEST-009..011; `evidence/task-004.md`; firma real de Claude en `evidence/validation-002-real-runtime.md` | BLOCKED |
| FR-003 | AC-003 | TASK-003/005/006; adaptadores y adopción | TEST-005..017; `evidence/task-006-compatibility.md`, `evidence/validation-002-real-runtime.md` | BLOCKED |

FR-001 queda demostrado con el CLI real: la policy clasificó low/medium/high y
el runner aplicó el control nativo `--effort` en Claude Code. FR-002 sigue
bloqueado porque ningún runtime real produjo un rechazo de nivel: Claude Code
aceptó los tres niveles de la policy y Codex/OpenCode no se ejecutaron. FR-003
exige los tres runtimes.

# 5. Non-Functional Requirement Coverage

| NFR | AC | Evidencia/métrica | Result |
|-----|----|------------------|--------|
| NFR-001 | AC-001 | Conjunto reproducible de 3 tareas frente a `medium` fijo, con clase, nivel, resultado y duración registrados; 3/3 correctas en ambas configuraciones. No se declara mejora (n=1). `evidence/validation-002-real-runtime.md` | PASS |
| NFR-002 | AC-001, AC-003 | Solo Claude Code/Anthropic verificado en real; faltan Codex, OpenCode, DeepSeek y GLM. `evidence/task-006-compatibility.md` | BLOCKED |

NFR-001 se evalúa con la condición que fija PLAN-011 §3: registrar la
comparación sin afirmar mejoras de calidad no demostradas. Esa condición se
cumple.

# 6. Security Requirement Coverage

SPEC-011 no define requisitos `SEC-[XXX]` específicos, así que la matriz SEC
de SPEC es NOT_APPLICABLE. Se revisaron entradas, archivos de tarea, manejo de
errores, subprocess, logs, permisos y límites externos conforme a
`.spec/standards/security.md`; evidencia en `evidence/task-003.md` y
`evidence/task-004.md`. Las ejecuciones reales usaron tareas sintéticas y no
leyeron ni modificaron credenciales ni configuración.

# 7. Acceptance Criteria Validation

| AC | TEST/verificación y evidencia | Result |
|----|-------------------------------|--------|
| AC-001 | TEST-001..008; TEST-015 PASS con Claude Code real; `evidence/validation-002-real-runtime.md` | PASS |
| AC-002 | TEST-009..011 simulados PASS; sin rechazo real observado; TEST-016/017 sin completar | BLOCKED |
| AC-003 | TEST-015 PASS; TEST-016 NOT_RUN; TEST-017 BLOCKED; `evidence/task-006-compatibility.md` | BLOCKED |

## AC-001 — Selección y aplicación para una tarea

**Related requirements:** FR-001  
**Given:** Tarea y combinación runtime/modelo.  
**When:** Se inicia por runner.  
**Then:** Se clasifica y pasa el control nativo correspondiente.  
**Evidence:** `evidence/validation-002-real-runtime.md`: `effort=low|medium|high status=applied` con `claude-sonnet-5-5`, rc=0, salidas correctas.  
**Result:** PASS

## AC-002 — Runtime sin capacidad de ajuste

**Related requirements:** FR-002  
**Given:** El runtime/modelo no admite el nivel solicitado.  
**When:** El runner procesa la tarea.  
**Then:** Reintenta una vez sin override e informa el fallback.  
**Evidence:** Contrato simulado PASS en `evidence/task-004.md`. Claude Code real no rechaza niveles: avisa por stderr y degrada él mismo (DISCOVERY-001). No hay rechazo real observado en Codex/OpenCode.  
**Result:** BLOCKED

## AC-003 — Runtimes y proveedores requeridos

**Related requirements:** FR-003  
**Given:** Claude Code, Codex u OpenCode con un proveedor/modelo compatible.  
**When:** Se ejecuta la tarea por el runner.  
**Then:** Se aplica el control disponible o se usa fallback.  
**Evidence:** Claude Code real PASS; Codex NOT_RUN; OpenCode BLOCKED (`evidence/task-006-compatibility.md`).  
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
| TEST-008 | CONTRACT | FR-001, AC-001 | Mismo comando; validación y CLI ausente; `evidence/task-003.md`, `evidence/finding-004-resolution.md` | PASS |
| TEST-009 | CONTRACT | FR-002, AC-002 | `python3 -m unittest discover -s tests -p 'test_run_task.py' -v`; `evidence/task-004.md` | PASS |
| TEST-010 | SECURITY | FR-002, AC-002 | Mismo comando; errores ajenos no reintentan aunque stdout contenga frase de effort; `evidence/task-004.md` | PASS |
| TEST-011 | CONTRACT | FR-002, AC-002 | Mismo comando; máximo un retry; `evidence/task-004.md` | PASS |
| TEST-012 | INTEGRATION | FR-001, AC-001 | `python3 -m unittest discover -s tests -p 'test_adopt_harness.py' -v`; `evidence/task-005.md` | PASS |
| TEST-013 | INTEGRATION | FR-001, AC-001 | Mismo comando; colisiones sin copia parcial; `evidence/task-005.md` | PASS |
| TEST-014 | OTHER | FR-003, AC-003 | Mismo comando; rutas y documentación de adopción; `evidence/task-005.md` | PASS |
| TEST-015 | E2E | FR-003, AC-001..003 | Smoke Claude Code + `claude-sonnet-5-5`; `evidence/validation-002-real-runtime.md` | PASS |
| TEST-016 | E2E | FR-003, AC-001..003 | Smoke Codex CLI; modelo no indicado; `evidence/validation-002-real-runtime.md` | NOT_RUN |
| TEST-017 | E2E | FR-003, AC-001..003 | Smoke OpenCode; BLOCKED por decisión del usuario; `evidence/validation-002-real-runtime.md` | BLOCKED |

## 8.1 TDD Evidence Review

| TASK / TEST | Aplicabilidad | RED y causa | GREEN / refactor | Motivo y alternativa si N/A | Resultado |
|-------------|---------------|-------------|------------------|-----------------------------|-----------|
| TASK-001 | NO APLICA | N/A | Revisión de contenido | Documentación y ADR; revisión manual registrada en `evidence/task-001.md` | PASS |
| TASK-002 / TEST-001..004 | OBLIGATORIO | RED por policy inicial que siempre devolvía medium | 6 tests PASS | N/A | PASS |
| TASK-003 / TEST-005..008 | OBLIGATORIO | RED contractual, FINDING-001 de importación directa y FINDING-004 de dependencia del CLI instalado | Tests PASS; `evidence/task-003.md`, `evidence/finding-001-resolution.md`, `evidence/finding-004-resolution.md` | N/A | PASS |
| TASK-004 / TEST-009..011 | OBLIGATORIO | RED de fallback, límite de retries y falso positivo desde stdout | 10 tests PASS; reapertura en `evidence/task-004.md` | N/A | PASS |
| TASK-005 / TEST-012..014 | OBLIGATORIO | RED por archivos no incluidos en allowlist | 11 tests PASS | N/A | PASS |
| TASK-006 / TEST-015..017 | NO APLICA | N/A | Integración real manual | Smoke real con servicio externo; TEST-015 PASS; TEST-016/017 sin completar | BLOCKED |

# 9. Evidence Quality Review

- [x] Aserciones significativas, tests requeridos habilitados, dobles representativos de los contratos.
- [x] Pruebas verifican conducta y AC; no se debilitó evidencia para PASS.
- [x] Smoke real con tareas de respuesta verificable y línea de estado del runner registrada.

Limitación: el benchmark es n=1 por celda y solo cubre un runtime. Sirve para
registrar la comparación que pide PLAN-011, no para afirmar una mejora.

# 10. Quality Gates

| Gate | Result | Evidence |
|------|--------|----------|
| Format/Lint/Types | NOT_APPLICABLE | El repo no configura formatter, linter ni tipos para estos scripts Python. |
| Unit/Integration/Contract/E2E/Security | BLOCKED | Suite completa 72/72 PASS (2026-11-03); TEST-015 PASS; TEST-016 NOT_RUN; TEST-017 BLOCKED. |
| Build | NOT_APPLICABLE | No hay build ni empaquetado Python configurado. |

# 11. Security Validation

La policy es local y no maneja credenciales. El runner valida agente/modelo,
restringe archivos a rutas regulares dentro del cwd, rechaza symlinks, usa
argumentos de lista sin shell, no registra el contenido de la tarea y no
cambia permisos del CLI. OpenCode recibe un archivo temporal con modo `0600`
que se elimina al salir. Se heredan la autenticación y los permisos del
runtime elegido. En la ejecución real, la línea de estado del runner no incluyó
el contenido de la tarea.

## Findings

No hay SEC-FINDING abiertos aplicables.

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

Ninguna; no se cambió configuración de usuario ni de CLI.

# 13. Scope Deviations

| ID | Change | Classification | Reason | Blocking |
|----|--------|----------------|--------|----------|
| DEV-001 | Corrección de import para el punto de entrada como script | AUTHORIZED | Defecto local de TASK-003 descubierto al verificar el comando documentado; evidencia en `finding-001.md` | NO |

# 14. Architecture Validation

Conforme a PLAN-011 y ADR-001: policy determinista separada, wrapper delgado,
adaptadores por CLI, subprocess sin shell, sin persistencia ni dependencias
nuevas, y autenticación/permisos delegados al runtime.

## Architecture Deviations

Ninguna. La opción nativa `--effort` de Claude Code queda verificada en real;
la de Codex y OpenCode solo con contratos simulados.

# 15. Regression Validation

| TEST/flujo | Resultado | Evidencia |
|------------|-----------|-----------|
| Suite completa: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests` | PASS, 72 tests | Ejecución del 2026-11-03 |
| `PYTHONDONTWRITEBYTECODE=1 python3 src/check_harness_state.py` | PASS | Ejecución del 2026-11-03 |
| Runner real con Claude Code | PASS | `evidence/validation-002-real-runtime.md` |

# 16. Task Validation

| TASK | DoD y evidencia | Result |
|------|----------------|--------|
| TASK-001 | `evidence/task-001.md` | PASS |
| TASK-002 | `evidence/task-002.md` | PASS |
| TASK-003 | `evidence/task-003.md`, `evidence/finding-001-resolution.md`, `evidence/finding-004-resolution.md` | PASS |
| TASK-004 | `evidence/task-004.md` | PASS |
| TASK-005 | `evidence/task-005.md` | PASS |
| TASK-006 | `evidence/task-006-compatibility.md`, `evidence/validation-002-real-runtime.md` | PASS |

# 17. Discoveries

| ID | Hallazgo | Blocking | Acción |
|----|----------|----------|--------|
| DISCOVERY-001 | Claude Code 2.1.317 no falla ante un `--effort` desconocido: devuelve rc=0, escribe `Warning: Unknown --effort value '<x>' — ignoring it and using the default effort…` y usa el valor por defecto. El fallback del runner solo se activa con rc≠0, y su regex no reconoce ese texto. Si un modelo o runtime futuro degradara así un nivel que la policy sí emite, el runner informaría `status=applied` cuando el nivel se ignoró (riesgo para BR-001). | NON_BLOCKING | No se observó con los niveles de la policy (`low`, `medium` y `high` aceptados en `claude-sonnet-5-5` y `claude-haiku-5-5`). Proponer en una feature futura que se detecte el warning con rc=0 y se reporte como fallback. No se implementa ahora. |

# 18. Final Traceability Matrix

| Requirement | AC | Plan | Task | Implementation | Test/Evidence | Result |
|-------------|----|------|------|----------------|---------------|--------|
| FR-001 | AC-001 | DEC-001/002 | TASK-002/003/006 | `src/effort_policy.py`, `src/run_task.py` | TEST-001..008, TEST-015; `evidence/validation-002-real-runtime.md` | PASS |
| FR-002 | AC-002 | DEC-003/004 | TASK-004 | `src/run_task.py` fallback | TEST-009..011; `evidence/task-004.md`; sin rechazo real | BLOCKED |
| FR-003 | AC-003 | DEC-001/003/004 | TASK-003/005/006 | adaptadores y adopción | TEST-005..017; `evidence/task-006-compatibility.md` | BLOCKED |
| NFR-001 | AC-001 | RISK-003 | TASK-006 | métrica de duración del runner | benchmark frente a `medium`; `evidence/validation-002-real-runtime.md` | PASS |
| NFR-002 | AC-001/003 | RISK-001 | TASK-003/006 | adaptadores y tests de contrato | TEST-005..017; `evidence/task-006-compatibility.md` | BLOCKED |
| BR-001 | AC-001/002 | DEC-003 | TASK-002/004 | clases y fallback seguro | TEST-001..011, TEST-015; DISCOVERY-001 | PASS |

# 19. Traceability Gaps

## Gaps

| ID | Type | Artifact | Description | Blocking |
|----|------|----------|-------------|----------|
| GAP-001 | ENVIRONMENT / INTEGRATION | `evidence/task-006-compatibility.md` | PARCIAL: Claude Code + Anthropic verificado. Faltan Codex (modelo no indicado), OpenCode (BLOCKED por decisión del usuario; error de plugins) y los proveedores DeepSeek y GLM. | YES |
| GAP-002 | PERFORMANCE | `evidence/validation-002-real-runtime.md` | RESUELTO: benchmark real frente a `medium` fijo registrado para NFR-001. | NO |

# 20. Validation Findings

## FINDING-001 — Import del runner en ejecución directa

**Type:** IMPLEMENTATION  
**Severity:** MEDIUM  
**Related artifacts:** TASK-003, TEST-008  
**Description:** El script no importaba la policy al ejecutarse directamente.  
**Evidence:** `evidence/finding-001.md`, `evidence/finding-001-resolution.md`  
**Status:** RESOLVED  
**Required action:** Corregido y probado con test de regresión.

## FINDING-002 — Smokes reales pendientes

**Type:** ENVIRONMENT  
**Severity:** HIGH  
**Related artifacts:** FR-002, FR-003, NFR-002, AC-002, AC-003, TEST-016, TEST-017  
**Description:** Se demostró la compatibilidad real solo con Claude Code + `claude-sonnet-5-5`. Falta Codex, OpenCode y modelos DeepSeek/GLM. La parte de benchmark de este finding quedó resuelta (GAP-002).  
**Evidence:** `evidence/task-006-compatibility.md`, `evidence/validation-002-real-runtime.md`  
**Status:** OPEN  
**Required action:** Indicar un modelo para Codex, desbloquear OpenCode (`Location plugins did not finish activating`) y aportar al menos una combinación DeepSeek y una GLM en un runtime que las soporte; después repetir `/validate`.

## FINDING-003 — Falso fallback por frase del prompt

**Type:** IMPLEMENTATION  
**Severity:** MEDIUM  
**Related artifacts:** TASK-004, TEST-010  
**Description:** Una frase de effort en stdout podía activar el fallback aunque stderr comunicara un error ajeno.  
**Evidence:** `evidence/finding-003.md`, `evidence/task-004.md`  
**Status:** RESOLVED  
**Required action:** El reconocimiento usa solo stderr y el test de regresión pasa.

## FINDING-004 — Prueba de entrada de script depende del CLI instalado

**Type:** IMPLEMENTATION  
**Severity:** MEDIUM  
**Related artifacts:** TASK-003, TEST-008  
**Description:** `test_script_entrypoint_runs_dry_run_from_repository_root` requería el CLI `claude` real en `PATH` y fallaba en GitHub Actions.  
**Evidence:** `evidence/finding-004.md`, `evidence/finding-004-resolution.md`  
**Status:** RESOLVED  
**Required action:** TASK-003 se reabrió; la prueba usa un CLI falso en `PATH`; suite 72/72 PASS con y sin CLIs instalados.

# 21. Findings Summary

| Severity | Open | Resolved |
|----------|-----:|---------:|
| HIGH | 1 | 0 |
| MEDIUM | 0 | 3 |
| LOW | 0 | 0 |

Blocking findings: 1.

# 22. Requirement Summary

| Grupo | PASS | FAIL | BLOCKED |
|-------|-----:|-----:|--------:|
| FR | 1 | 0 | 2 |
| NFR | 1 | 0 | 1 |
| SEC | 0 | 0 | 0 |
| AC | 1 | 0 | 2 |

# 23. Test Summary

| Tipo | PASS | FAIL | BLOCKED |
|------|-----:|-----:|--------:|
| Unit | 4 | 0 | 0 |
| Integration | 2 | 0 | 0 |
| Contract | 4 | 0 | 0 |
| E2E | 1 | 0 | 2 |
| Security | 3 | 0 | 0 |
| Other | 1 | 0 | 0 |
| Regression (suite) | 72 | 0 | 0 |

De los E2E, TEST-016 es NOT_RUN y TEST-017 está BLOCKED; ninguno cuenta como
PASS.

# 24. Final Gate

- [ ] MUST, AC, TEST, calidad y SEC obligatorios en PASS; evidencia TDD aplicable válida o N/A justificado con alternativa.
- [x] TASKS COMPLETED, todas las TASK requeridas DONE y evidencia de tarea disponible.
- [ ] Sin regresiones, gaps, cambios no autorizados, desviaciones arquitectónicas ni findings OPEN bloqueantes.

# 25. Final Result

**Validation Status:** BLOCKED  
**SPEC Compliance:** BLOCKED  
**Feature Status:** NOT_VALIDATED

FR-001, AC-001, NFR-001 y BR-001 pasan con evidencia real. FR-002, FR-003,
AC-002, AC-003 y NFR-002 siguen bloqueados por runtimes y proveedores sin
verificar. No se declara conformidad ni feature validada.

# 26. Required Next Action

1. Indicar un modelo para Codex y ejecutar TEST-016.
2. Resolver `ServiceUnavailableError: Location plugins did not finish activating`
   en OpenCode y ejecutar TEST-017.
3. Aportar al menos una combinación DeepSeek y una GLM (por ejemplo, en
   OpenCode) para NFR-002.
4. Repetir `/validate`. DISCOVERY-001 puede encauzarse por separado con
   `/specify`.

# 27. Approval

**Validated by:** Harness implementation agent  
**Date:** 2026-11-03  
**Notes:** Resultado BLOCKED; no equivale a aprobación humana ni a cierre funcional.
