# Resolución de FINDING-001

**Fecha:** 2026-10-27  
**TASK reabierta:** TASK-003  
**Prueba de regresión:** `test_script_entrypoint_runs_dry_run_from_repository_root`

## TDD

- RED previo al cambio: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_run_task.py' -v` — el nuevo test falló con `ModuleNotFoundError: No module named 'src'`; los ocho casos anteriores pasaron.
- GREEN: mismo comando — 9 tests PASS.
- Verificación de la interfaz documentada: `PYTHONDONTWRITEBYTECODE=1 python3 src/run_task.py --agent claude --model test-model --task 'fix typo' --dry-run` — exit 0; reportó `effort=low status=would-apply` y mostró el comando sin invocar el CLI.

## Cambio

`src/run_task.py` importa la policy relativa al ejecutarse como módulo y desde
`src/` al ejecutarse como script. No cambió el contrato de argumentos ni las
opciones de runtime.

## Resultado

FINDING-001: RESOLVED. La evidencia inicial desfavorable permanece en
`evidence/finding-001.md`.
