# Evidencia TASK-004

**Fecha:** 2026-10-27  
**Trazabilidad:** FR-002, FR-003, BR-001 → AC-002, AC-003 → TEST-009 a TEST-011

## Archivos

- `src/run_task.py` — detección específica por runtime, eliminación del override para retry único y estado de aplicación/fallback/no confirmado.
- `tests/test_run_task.py` — casos de rechazo de effort, errores ajenos y límite de un retry.

## TDD

- RED: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_run_task.py' -v` — `TEST-009` y `TEST-011` fallaron: no hubo retry y el rechazo final no completó la secuencia prevista. Los casos existentes y `TEST-010` permanecieron PASS.
- GREEN: mismo comando — 8 tests PASS; retry exactamente una vez sin override.

## Seguridad y resultado

- Solo patrones acotados de rechazo del parámetro activan el fallback; errores de autenticación, permiso, red y modelo no repiten.
- El resumen reporta `applied` solo con salida exitosa; errores sin clasificación de incompatibilidad reportan `not-confirmed`.
- No se añaden flags de permisos ni se imprime el entorno.

## Estado

TEST-009 a TEST-011: PASS en pruebas simuladas. TASK-004: DONE.

## Reapertura y resolución de FINDING-003

Durante `/validate` se comprobó que un mensaje parecido a error de effort en
stdout podía provocar fallback pese a un diagnóstico ajeno en stderr. Se
conservó el reporte anterior en `evidence/validation-attempt-002.md` y se
reabrió TASK-004 conforme a `/implement` §17.1.

- RED: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_run_task.py' -v` — el nuevo caso falló porque se hicieron dos invocaciones; los nueve casos previos pasaron.
- GREEN: mismo comando — 10 tests PASS después de reconocer incompatibilidad solo en stderr.
- Regresión completa: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v` — 72 tests PASS.
- FINDING-003: RESOLVED; el retry conserva su límite de una ejecución y exige código de salida no-cero.
