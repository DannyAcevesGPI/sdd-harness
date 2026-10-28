# Evidencia TASK-003

**Fecha:** 2026-10-27  
**Trazabilidad:** FR-001, FR-003, NFR-002 → AC-001, AC-003 → TEST-005 a TEST-008

## Archivos

- `src/run_task.py` — validación, selección de policy, argumentos nativos, proceso sin shell, salida separada, duración y `--dry-run` redactado.
- `tests/test_run_task.py` — contratos simulados de Claude Code, Codex CLI y OpenCode; entradas adversariales y errores.

## TDD

- RED inicial de importación (`ImportError` porque aún no existía `src.run_task`) fue un fallo de estructura del test y no se usa como evidencia RED.
- RED con el módulo mínimo: los tests de dry-run, validación, CLI ausente y despacho no cumplieron los contratos esperados. Algunos casos señalaron también expectativas de prueba que se ajustaron al ejecutable absoluto que devuelve `shutil.which`.
- GREEN: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_run_task.py' -v` — 5 tests PASS.
- Regresión policy: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_effort_policy.py' -v` — 6 tests PASS.

## Verificaciones

- Los tres adaptadores preservan el identificador de modelo recibido y envían effort en el formato previsto: `--effort` para Claude, `model_reasoning_effort` para Codex y variante `#<level>` para OpenCode.
- Los prompts se tratan como datos. Codex y Claude los reciben por stdin; OpenCode usa archivo temporal con permisos `0600` y lo elimina al terminar. No se activa shell ni flags de permisos.
- `--dry-run` no imprime el texto de tarea. CLI faltante e inputs inválidos devuelven error controlado.
- Los tests usan procesos falsos; no demuestran compatibilidad real de versión/modelo. OpenCode CLI local no pudo consultarse porque su invocación requería escritura de log fuera del sandbox y la solicitud de escalación fue cancelada.

## Estado

TEST-005 a TEST-008: PASS en pruebas de contrato simuladas. TASK-003: DONE.

## Reapertura y resolución de FINDING-001

La primera ejecución del comando documentado encontró una regresión no cubierta
por la suite inicial: ejecución como script no resolvía `src.effort_policy`.
Se conservó el RED en `evidence/finding-001.md`, se reabrió TASK-003 conforme
a `/implement` §17.1 y se añadió
`test_script_entrypoint_runs_dry_run_from_repository_root`.

- RED: el test nuevo falló con `ModuleNotFoundError: No module named 'src'`;
  los ocho tests anteriores pasaron.
- GREEN: la suite `test_run_task.py` terminó con 9 tests PASS.
- Comando de entrada documentado en `evidence/finding-001-resolution.md`:
  exit 0, `status=would-apply`, sin iniciar el CLI.

FINDING-001: RESOLVED; TASK-003 vuelve a DONE.
