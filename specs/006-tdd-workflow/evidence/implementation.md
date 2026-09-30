# Evidencia de implementación — SPEC-006

Fecha: 2026-09-30. Rama: `v1`. Referencia: working tree previo a commit.

## Alcance

- TASK-001: `.spec/standards/testing.md` define la política TDD.
- TASK-002: commands `plan`, `tasks`, `implement` y `validate` aplican la regla
  en su fase.
- TASK-003: templates `plan`, `tasks` y `validation` incluyen aplicabilidad y
  evidencia mínima.
- TASK-004: `docs/tdd.md`, `docs/adoption.md`, `docs/index.md` y `AGENTS.md`
  guían al equipo sin cargar el bootstrap.
- TASK-005: esta evidencia y verificaciones transversales.

No se modificaron `.spec/constitution.md`, `handoff.md`, `src/`, `tests/` ni
artefactos de features previamente validadas.

## Verificaciones

| ID | AC | Comprobación | Resultado |
|----|----|--------------|-----------|
| TEST-001 | AC-001, AC-003, AC-004 | Standard §21 exige TDD para comportamiento automatizable, RED auténtico antes del cambio, GREEN, refactor en verde; rechaza falla de entorno y define excepción acotada. | PASS |
| TEST-002 | AC-002, AC-003 | `/plan` prepara casos, `/tasks` asigna TEST IDs, `/implement` ejecuta ciclo solo tras gates, `/validate` revisa evidencia. | PASS |
| TEST-003 | AC-003, AC-004 | Recorrido documental de los escenarios de abajo: prueba ya verde no demuestra RED; falla de entorno queda BLOCKED; excepción legítima exige verificación. | PASS |
| TEST-004 | AC-002, AC-003, AC-004 | Templates de PLAN, TASKS y VALIDATE contienen campos coherentes para aplicabilidad, casos previstos, RED/GREEN y alternativa. | PASS |
| TEST-005 | AC-001, AC-005 | `AGENTS.md` tiene 167 líneas; guía de 49 líneas; adopción incluye `docs/tdd.md` en la base copiable; enlaces de adopción e índice resuelven; sin frase que declare TDD opcional. | PASS |

### Recorrido documental (TEST-002 y TEST-003)

| Caso | PLAN / TASKS | `/implement` | `/validate` esperado |
|------|--------------|--------------|----------------------|
| Comportamiento automatizable nuevo | AC y TEST previstos; gates aprobados | RED por assertion de comportamiento faltante antes de código productivo; GREEN después; refactor en verde si existe | PASS solo con evidencia RED/GREEN y pruebas requeridas PASS |
| Prueba ya verde | Caso previsto revisado | No se fabrica RED; se identifica comportamiento faltante real | No aceptar esa ejecución como evidencia RED |
| Falla de dependencia o entorno | TEST previsto | Fallo no es RED válido; BLOCK y TASK BLOCKED | BLOCKED mientras el test requerido no pueda ejecutarse |
| Documentación sin comportamiento automatizable | Motivo y verificación alternativa | Revisión documental aplicable | PASS solo si la alternativa demuestra el AC |

Este recorrido verifica las reglas documentadas; no afirma haber ejecutado
los ciclos de un proyecto de ejemplo. SPEC-006 modifica documentación de
proceso, por lo que no hay un comportamiento productivo nuevo al cual aplicar
RED/GREEN en esta feature.

## Comandos y resultados

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest discover -s tests -v`
  → 11 tests PASS. El espécimen Python existente no cambió.
- `git diff --check` → PASS.
- `wc -l AGENTS.md docs/tdd.md` → 167 y 49 líneas.
- Búsqueda de afirmaciones que declaren TDD opcional en `.spec/`, `docs/` y
  `AGENTS.md` → sin resultados.
- `test -f docs/tdd.md` → PASS; rutas relativas desde ambos documentos en
  `docs/` resuelven a ese archivo.

No se almacenaron secretos ni salidas extensas. Bloqueos, desviaciones y
discoveries: ninguno.
