# FINDING-001 — Script de entrada no importa policy en invocación directa

**Detectado:** 2026-10-27 durante `/validate` previo al reporte final  
**Tipo:** IMPLEMENTATION  
**Requisito/AC:** FR-001, AC-001; TASK-003; TEST-005 a TEST-008

## Descripción

La documentación indica ejecutar `python3 src/run_task.py`, pero el módulo
importaba `src.effort_policy` como paquete. La ejecución directa establece
`src/` como ruta de importación y terminaba con `ModuleNotFoundError` antes de
validar argumentos o despachar al CLI.

## Evidencia inicial

`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_run_task.py' -v`
falló en `test_script_entrypoint_runs_dry_run_from_repository_root` con código
1 y `ModuleNotFoundError: No module named 'src'`. El resto de los ocho casos
permaneció PASS.

## Resolución

Reabrir TASK-003 dentro del alcance aprobado. Añadir una prueba de entrada de
script directo y soportar tanto la importación por paquete como la ejecución
documentada. Conservar esta evidencia y el resultado desfavorable inicial.
