# Validation Report - Adopcion portable del Harness

**Validation ID:** VALIDATION-008  
**SPEC:** SPEC-008 v0.2.0  
**PLAN:** PLAN-008 v0.1.0  
**TASKS:** TASKS-008 v0.1.0  
**Status:** COMPLETED  
**Result:** PASS  
**Date:** 2026-09-30  
**Validated by:** Codex, agente verificador

# 1. Objetivo y artefactos

Validar adopcion desde cero, gates sin chat, proyecciones, CI local y entrada
documental corta contra SPEC-008. Artefactos: `spec.md`, `plan.md`, `tasks.md`,
`decisions.json`, implementacion del worktree `v1` y
`evidence/implementation.md`. No hay ADR ni migracion.

# 2. Precondiciones

| Check | Resultado | Evidencia |
|-------|-----------|-----------|
| SPEC/PLAN APPROVED y TASKS COMPLETED | PASS | Artefactos y DECISION-003/004/005 |
| TASK-001 a TASK-007 DONE | PASS | `tasks.md` y evidencia dedicada |
| Sin bloqueos ni aclaraciones abiertas | PASS | TASKS y SPEC |
| Gates y huellas vigentes | PASS | `python3 src/check_harness_state.py` |
| Implementacion presente | PASS | `src/`, `tests/`, docs y workflow |

# 3. Cobertura de requisitos

| Requisito | AC | Implementacion / evidencia | Resultado |
|-----------|----|---------------------------|-----------|
| FR-001, BR-001 | AC-001 | `AGENTS.md`, commands, TEST-001 | PASS |
| FR-002, BR-002 | AC-002, AC-007 | `src/adopt_harness.py`, TEST-002/003/004 | PASS |
| FR-003 | AC-003 | TEST-005, repo temporal y slug historico exacto | PASS |
| FR-004 | AC-004 | workflow, suite local y checker negativo | PASS |
| FR-005 | AC-005 | checker, TEST-006/007/008, handoff/indice | PASS |
| FR-006 | AC-006 | README, referencia, indice y conteos | PASS |
| NFR-001 | AC-006 | AGENTS 176, handoff 158, README 41 lineas | PASS |
| NFR-002 | AC-002 | destino limpio y checker de feature 001 | PASS |
| SEC-001 | AC-003, AC-007 | allowlist, symlink y fixture `.env` sintetico | PASS |

Se verificaron individualmente los siete AC; todos PASS. El workflow remoto
no se ejecuto en esta sesion. AC-004 exige que el job falle ante checker FAIL:
el workflow ejecuta el checker sin `continue-on-error` y el test negativo
comprueba exit 1 con `HASH_MISMATCH`. Es evidencia local del contrato; la
primera ejecucion real de CI sigue pendiente de observacion.

# 4. Pruebas y TDD

| TEST | Tipo | Relacion | Resultado |
|------|------|----------|-----------|
| TEST-001 | OTHER | FR-001, AC-001 | PASS |
| TEST-002/003/004 | INTEGRATION/SECURITY | FR-002, SEC-001, AC-002/007 | PASS |
| TEST-005 | INTEGRATION | FR-003, AC-003 | PASS |
| TEST-006/007/008 | UNIT/INTEGRATION | FR-005, AC-005 | PASS |
| TEST-009 | OTHER | FR-004, AC-004 | PASS local |
| TEST-010 | OTHER | FR-006, AC-006 | PASS |
| TEST-011 | REGRESSION | Todos | PASS |

TDD: TEST-002/003/004 tiene RED conductual por command obligatorio omitido y
GREEN con allowlist fija; el `ModuleNotFoundError` inicial no se conto como
RED. TEST-005 tiene RED por exencion de legado aplicada al mismo slug en un
proyecto nuevo, GREEN tras acotarla al contexto historico. TEST-006/007/008
tienen RED por proyecciones no comprobadas y por estado de tabla de cuatro
columnas que cambiaba la huella; GREEN con diagnostico y normalizacion. Ver
detalle en `evidence/implementation.md`. TEST-001/009/010/011 son revision
normativa, orquestacion o consolidacion sin comportamiento productivo nuevo;
la alternativa fue inspeccion y ejecucion local. No hubo refactor posterior.

La suite contiene assertions de resultado, exit codes, archivos instalados,
omisiones de copia y hash. No hay tests saltados ni mocks que oculten gates.

# 5. Quality gates y seguridad

| Gate | Resultado | Evidencia |
|------|-----------|-----------|
| Unit/integration/regression | PASS | 38 tests, `unittest discover -s tests` |
| Durable state | PASS | `HARNESS STATE: PASS` |
| Diff/format basico | PASS | `git diff --check` sin errores |
| Enlaces Markdown principales | PASS | Revision local de destinos en README/docs/CHANGELOG |
| Lint/types/build/E2E | NOT_APPLICABLE | No configurados; repo documental + Python stdlib |
| GitHub Actions remoto | NOT_RUN | Requiere push/PR; no sustituye los checks locales |

SEC-001 PASS: solo se copian rutas fijas, no `specs/`, `.env`, handoff local
ni validaciones historicas; se rechazan symlinks/colisiones antes de copiar.
No hay secretos reales en fixtures. El workflow usa `contents: read`, no
escritura ni aprobaciones automatizadas. Hallazgos SEC abiertos: 0.

# 6. Alcance, arquitectura y regresion

Cambios autorizados: `AGENTS.md`, commands, docs/README/CHANGELOG/handoff,
`src/adopt_harness.py`, `src/check_harness_state.py`, tests, workflow y
artefactos SPEC-008. `docs/reference.md` conserva el README largo.
Dependencias nuevas: ninguna. Migraciones: ninguna. No se altero
`src/audit_tasks.py` ni historia validada. DEC-001 a DEC-005 implementadas;
sin desviacion arquitectonica ni cambio no autorizado significativo.
La suite existente y el checker pasan: regresiones conocidas 0.

# 7. Tareas, trazabilidad y findings

TASK-001 a TASK-007: objetivo, alcance, pruebas y evidencia revisados; DoD
PASS para cada una. La matriz de la seccion 3 y `tasks.md` seccion 5 cubren
FR-001 a FR-006, NFR-001/002, SEC-001 y AC-001 a AC-007 sin huerfanos.
Gaps bloqueantes: 0. Findings abiertos: 0. Discoveries bloqueantes: 0.
La ejecucion remota de CI es una observacion pendiente, no un PASS remoto.

# 8. Gate final

- [x] Requisitos MUST y AC: PASS.
- [x] TDD aplicable y alternativas documentales: evidencia suficiente.
- [x] Tests, checks locales y SEC-001: PASS.
- [x] TASKS COMPLETED; sin regresiones, gaps o findings bloqueantes.
- [x] Alcance y arquitectura compatibles con PLAN-008.

**Validation Status:** COMPLETED  
**SPEC Compliance:** PASS  
**Feature Status:** VALIDATED

SPEC COMPLIANCE: PASS
FEATURE STATUS: VALIDATED
