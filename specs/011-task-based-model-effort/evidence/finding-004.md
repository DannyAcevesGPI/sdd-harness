# FINDING-004 — Prueba de entrada de script depende del CLI instalado

**Detectado:** 2026-10-28 en GitHub Actions tras integrar SPEC-011 en `v1`  
**Tipo:** IMPLEMENTATION (aislamiento de prueba)  
**Requisito/AC:** FR-001, AC-001; TASK-003; TEST-008

## Descripción

`test_script_entrypoint_runs_dry_run_from_repository_root` ejecuta
`src/run_task.py --dry-run` como subproceso real. El modo dry-run resuelve el
ejecutable del agente con `shutil.which`, así que la prueba solo pasa si el CLI
`claude` real está en el `PATH`. En la máquina de desarrollo existe; en el
runner de GitHub Actions no. El resto de casos de `tests/test_run_task.py`
sustituye `shutil.which` y no tiene esta dependencia. El código productivo es
correcto: devolver error ante un CLI ausente es el comportamiento especificado.

## Evidencia inicial

- Workflow "Harness checks": ejecuciones 40779993540 (`v1`, `4db1b3c`) y
  40780588117 (`plan-012-subagent-orchestrator`, `93e3de8`) en FAILURE en el
  paso "Unit and adoption tests"; la ejecución previa sin código de SPEC-011
  (`4818987`) estaba en SUCCESS.
- Reproducción local con el `PATH` mínimo del runner:
  `PATH=/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest discover -s tests`
  → `Ran 72 tests`, `FAILED (failures=1)`;
  `AssertionError: 2 != 0 : Runner error: CLI not found: claude`.

## Resolución prevista

Reabrir TASK-003 dentro del alcance aprobado (`tests/test_run_task.py`). La
prueba debe proveer un ejecutable `claude` falso en un directorio temporal
antepuesto al `PATH` del subproceso, sin cambiar sus aserciones. No hay cambio
de código productivo ni de trabajo autorizado.
