# FINDING-004 — Resolución

**Fecha:** 2026-10-28  
**TASK:** TASK-003 (reabierta `DONE → TODO → IN_PROGRESS → DONE`)  
**TEST:** TEST-008 (`test_script_entrypoint_runs_dry_run_from_repository_root`)  
**Requisito/AC:** FR-001, AC-001

## RED

`PATH=/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest tests.test_run_task.RunTaskTests.test_script_entrypoint_runs_dry_run_from_repository_root`
→ `FAILED (failures=1)`. Causa: la prueba resolvía el CLI `claude` real del
`PATH` y el entorno del runner no lo tiene (ver `finding-004.md`).

## Cambio

Solo `tests/test_run_task.py`: la prueba crea un ejecutable `claude` falso en un
directorio temporal y lo antepone al `PATH` del subproceso. Las aserciones
(código 0 y `--effort low` en la salida) no cambian. Sin cambios en `src/`.

## GREEN

- Mismo comando → `Ran 1 test`, `OK`.
- Suite completa con `PATH` del runner:
  `PATH=/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest discover -s tests`
  → `Ran 72 tests`, `OK`.
- Suite completa con `PATH` de desarrollo (CLI reales instalados) → `Ran 72 tests`, `OK`.
- `python3 src/check_harness_state.py` → `HARNESS STATE: PASS`.

## Efecto en la validación

FINDING-004 queda RESOLVED. La validación de SPEC-011 sigue BLOCKED por
FINDING-002 (smokes reales y benchmark), independiente de esta corrección.
