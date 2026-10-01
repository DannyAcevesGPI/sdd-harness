# SPEC-008 - Implementation evidence

Fecha: 2026-09-30. Los datos de aprobación en tests son fixtures sintéticos;
no autorizan gates reales.

## Gates

- SPEC-008 v0.2.0: DECISION-003.
- PLAN-008 v0.1.0: DECISION-004.
- TASKS-008 v0.1.0: DECISION-005.
- `python3 src/check_harness_state.py`: `HARNESS STATE: PASS` tras las
  transiciones operativas de TASKS. No se cambió ninguna huella aprobada.

## Tareas y pruebas

| Task | Test | Resultado / archivo |
|------|------|---------------------|
| TASK-001 | TEST-001 | AGENTS y commands permiten ledger/proyecciones antes de implement; revisión cruzada PASS |
| TASK-002 | TEST-002/003/004 | `tests/test_adopt_harness.py`: base, colisión, symlink, fuente incompleta, padre ocupado y exclusión de `.env`/historia sintética PASS |
| TASK-003 | TEST-005 | Feature `001` temporal: DRAFT sin ledger FAIL, ledger vacío PASS, APPROVED sin evento FAIL, fixture aprobado PASS, contenido cambiado FAIL; slug histórico exacto también exige ledger |
| TASK-004 | TEST-006/007/008 | `tests/test_check_harness_state.py`: proyección válida, ausente, obsoleta, legado y huella de tabla de cuatro columnas PASS |
| TASK-005 | TEST-009 | `.github/workflows/harness.yml`: tests y checker en push/PR, `contents: read`; checker con contenido cambiado devuelve exit 1 y `HASH_MISMATCH` |
| TASK-006 | TEST-010 | README 41 líneas, AGENTS 176, handoff 158; referencia larga en `docs/reference.md`, enlaces principales revisados |
| TASK-007 | TEST-011 | Suite completa y checker local PASS; trazabilidad en `tasks.md` sección 5 |

## RED / GREEN

- TEST-002/003/004: el primer intento falló con `ModuleNotFoundError`;
  **no cuenta como RED TDD**. En la revisión se agregó un caso conductual:
  eliminar `.spec/commands/validate.md` de una fuente completa no provocaba
  `ValueError` (RED). Una allowlist explícita de `.spec/` lo rechaza (GREEN).
  Colisiones, symlinks y padre ocupado siguen cubiertos en GREEN.
- TEST-005: tras exigir proyecciones en el checker, el primer ciclo aislado
  falló por `STALE_HANDOFF` y `STALE_INDEX`. Tras actualizar el fixture para
  proyectar cada fase, pasó. Se añadió además un RED válido: la primera
  feature del destino con slug `001-audit-task-management` no emitía
  `MISSING_LEDGER` por una exención global de legado. Se acotó la exención al
  contexto histórico del repo fuente y el caso pasó a GREEN.
- TEST-002: la comprobacion de rutas del quickstart instalado falló en RED
  porque enlazaba `docs/reference.md`, excluido del paquete portable. Se
  retiraron enlaces de historia local y la misma prueba pasó en GREEN.
- TEST-008: la tabla `| Orden | Tarea | Depende de | Estado |` produjo FAIL
  al cambiar `TODO` por `IN_PROGRESS`; tras normalizar su cuarta columna al
  valor canónico `TODO`, el test pasó sin editar DECISION-005. Cambiar una
  dependencia sigue cambiando la huella.
- TEST-006/007: los tests de bloque ausente/obsoleto y enlace faltante
  fallaron antes de agregar `_audit_projection`; pasaron después. El test de
  enlace sobrante/bloque duplicado también pasó de RED a GREEN.
- TEST-001/009/010/011: verificación documental o de orquestación; no
  aplica RED de comportamiento productivo independiente.

## Comandos locales y límites

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest discover -s tests
38 tests, OK
python3 src/check_harness_state.py
HARNESS STATE: PASS
git diff --check
sin errores
```

No se ejecutó el job remoto de GitHub Actions en esta sesión. La validación
local verifica los mismos comandos y el caso negativo, no demuestra ejecución
remota. No hay secretos ni dependencia de red para los tests locales.
