# Evidencia TASK-005

**Fecha:** 2026-10-27  
**Trazabilidad:** FR-001 a FR-003, NFR-002 → AC-001 a AC-003 → TEST-012 a TEST-014

## Archivos

- `src/adopt_harness.py` — allowlist y índice inicial para el runner/policy.
- `tests/test_adopt_harness.py` — comprobación de distribución y documentación en proyecto limpio.
- `AGENTS.md`, `docs/quickstart.md`, `docs/adoption.md`, `docs/index.md` — punto de entrada, ejemplos de uso y límites.

## TDD

- RED: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_adopt_harness.py' -v` — `test_effort_runner_is_shipped_and_documented` falló porque los nuevos archivos aún no estaban en `reusable_files`.
- GREEN: mismo comando — 11 tests PASS, incluidos adopción limpia, checker de destino, colisiones sin copia parcial, rutas y documentación.

## Rutas distribuidas

- `src/effort_policy.py`, `src/run_task.py`
- `tests/test_effort_policy.py`, `tests/test_run_task.py`
- `docs/agents/model-effort.md`

No se copian credenciales ni configuración global de los CLIs. La guía especifica que Claude Code, Codex y OpenCode deben iniciarse por el runner para aplicar la política; ejecuciones directas conservan los valores nativos.

## Estado

TEST-012 a TEST-014: PASS en adopción temporal simulada. TASK-005: DONE.
