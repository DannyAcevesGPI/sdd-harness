# Tareas: Adopción portable del Harness

**ID:** TASKS-008  
**SPEC relacionada:** SPEC-008 v0.2.0  
**PLAN relacionado:** PLAN-008 v0.1.0  
**Estado:** COMPLETED  
**Versión:** 0.1.0  
**Fecha:** 2026-09-30

---

# 1. Precondiciones

- [x] SPEC y PLAN están APPROVED, con eventos y huellas vigentes.
- [x] Requisitos MUST y AC tienen cobertura técnica en PLAN.
- [x] No hay aclaraciones bloqueantes; orden y dependencias definidos.
- [x] TASKS cuenta con aprobación humana explícita.

# 2. Objetivo y reglas de ejecución

Implementar DEC-001 a DEC-005 en unidades verificables. Ninguna tarea se
ejecutará antes de aprobar este documento. Para código automatizable, guardar
RED antes del cambio productivo y GREEN después, por TEST, en
`specs/008-portable-harness-adoption/evidence/`. El checker y toda evidencia
de gates deben seguir siendo reproducibles sin el chat.

# 3. Tareas

## TASK-001 — Alinear permisos de metadata por fase

**Tipo:** DOCUMENTATION  
**Estado:** DONE  
**Prioridad:** P1  
**Trazabilidad:** FR-001, BR-001, AC-001, DEC-001.  
**Depende de:** ninguna.

**Alcance:** modificar `AGENTS.md`, los commands de SPEC/clarify/plan/tasks y,
si sus reglas se contradicen, implement/validate y templates afectados.
Reutilizar `docs/state-reconstruction.md`; no modificar código de aplicación.

**Resultado:** ledger vacío permitido al crear SPEC; eventos humanos y
proyecciones de solo estado/enlaces permitidos en cada fase, sin extender el
permiso a cambios sustantivos ni autoaprobación.

**TEST-001:** revisión cruzada de reglas y simulación documental del primer
gate; no aplica TDD porque el resultado es normativo. Verificar que ninguna
regla restante exija escribir código antes de `/implement`.

**DONE cuando:** reglas coherentes, AC-001 revisado, alcance respetado y
evidencia de revisión enlazada.

## TASK-002 — Crear adoptador con base reusable única

**Tipo:** FEATURE / SECURITY  
**Estado:** DONE  
**Prioridad:** P1  
**Trazabilidad:** FR-002, NFR-002, SEC-001, BR-002, AC-002, AC-007, DEC-002.  
**Depende de:** TASK-001.

**Alcance:** crear `src/adopt_harness.py`, `tests/test_adopt_harness.py` y
actualizar `docs/adoption.md`; reutilizar `.spec/`, `AGENTS.md`, herramientas
de `src/` y tests del Harness. No copiar `specs/`, `handoff.md` local,
auditorías ni estado histórico.

**Resultado:** CLI que lista/copía allowlist única a destino explícito,
valida fuente, colisiones, rutas y symlinks antes de mutar, e inicializa
handoff e índice sin historia. Documentar Python y adaptación local.

**TEST-002:** base completa y ejecutable en destino. **TEST-003:** colisión,
fuente faltante y symlink inseguro fallan sin copia parcial. **TEST-004:**
historia/secretos sintéticos no llegan al destino. TDD obligatorio: primero
RED de estos casos, después GREEN con `unittest discover`; guardar salidas.

**DONE cuando:** TEST-002/003/004 pasan, seguridad de rutas revisada,
documentación corresponde a la allowlist y evidencia RED/GREEN está enlazada.

## TASK-003 — Probar primer ciclo en repositorio aislado

**Tipo:** TEST  
**Estado:** DONE  
**Prioridad:** P1  
**Trazabilidad:** FR-003, FR-002, BR-001, AC-002, AC-003, DEC-002.  
**Depende de:** TASK-002.

**Alcance:** ampliar `tests/test_adopt_harness.py`; reutilizar CLI y
`src/check_harness_state.py`. No añadir aprobaciones reales ni cambiar
artefactos de SPEC-008 como parte del fixture.

**Resultado:** test de integración en directorio temporal: instalación,
feature 001 nueva, ledger vacío, aprobación sintética con huella canónica,
diagnóstico PASS; corrupción o falta de evento produce FAIL. Los datos
sintéticos deben identificarse como fixture, no como decisión humana.

**TEST-005:** ciclo positivo y negativo sin historial heredado. TDD
obligatorio: RED frente a soporte faltante, GREEN al completar el flujo;
guardar comandos, resultados y archivos de fixture relevantes.

**DONE cuando:** TEST-005 pasa de forma determinista y evidencia RED/GREEN
permite reconstruir el smoke test sin chat.

## TASK-004 — Verificar handoff e índice contra artefactos

**Tipo:** FEATURE / TEST  
**Estado:** DONE  
**Prioridad:** P1  
**Trazabilidad:** FR-005, BR-001, AC-005, DEC-003, RISK-001.  
**Depende de:** TASK-001, TASK-002.

**Alcance:** modificar `src/check_harness_state.py`,
`tests/test_check_harness_state.py`, `handoff.md`, `docs/index.md` y
`docs/state-reconstruction.md`; no editar ledgers históricos ni inferir
aprobación humana desde el resumen.

**Resultado:** bloque JSON versionado de estado vivo; checker de solo lectura
compara fase, siguiente gate, validadas y enlaces con artefactos. Diagnostica
ausente, malformado y obsoleto con ruta/causa. Preservar la normalización de
huellas: cambios solo de estado/checklist no deben ser contenido distinto;
cambios de trabajo aprobado sí deben fallar.

**TEST-006:** proyección válida y desactualizada. **TEST-007:** bloque
inválido, enlaces ausentes y legacy compatible. **TEST-008:** huella canónica
estable para cambios operativos y sensible a contenido. TDD obligatorio:
RED por caso antes del código, GREEN con suite y checker; guardar evidencia.

**DONE cuando:** TEST-006/007/008 pasan, el repo actual pasa el checker y
la proyección no se convierte en fuente de aprobación.

## TASK-005 — Ejecutar controles en CI

**Tipo:** CONFIGURATION  
**Estado:** DONE  
**Prioridad:** P1  
**Trazabilidad:** FR-004, BR-001, AC-004, DEC-004.  
**Depende de:** TASK-003, TASK-004.

**Alcance:** crear `.github/workflows/harness.yml`; actualizar
`docs/adoption.md` para distinguir workflow opcional de núcleo portable.
No añadir credenciales, autoescritura ni aprobación automática.

**Resultado:** GitHub Actions ejecuta suite y checker en PR/push, con permisos
mínimos y versiones oficiales verificadas. Fallo de cualquier control deja
job en FAIL; se documenta ejecución local si CI no está disponible.

**TEST-009:** inspección del workflow, ejecución local equivalente y prueba
negativa del checker. TDD no aplica al archivo de orquestación; la lógica
invocada ya tiene tests RED/GREEN. Guardar evidencia de checks y límites.

**DONE cuando:** workflow invoca ambos comandos, no usa secretos ni gates
humanos, y TEST-009 queda documentado.

## TASK-006 — Reducir entrada documental sin perder referencia

**Tipo:** DOCUMENTATION  
**Estado:** DONE  
**Prioridad:** P2  
**Trazabilidad:** FR-006, NFR-001, AC-006, DEC-005.  
**Depende de:** TASK-001, TASK-002.

**Alcance:** modificar `README.md`, `docs/quickstart.md`, `docs/index.md`,
`docs/adoption.md`, `CHANGELOG.md`; crear `docs/reference.md`. Conservar
contenido útil del README, sin duplicar evidencia en el handoff.

**Resultado:** README de 300 líneas o menos con entrada y enlaces claros;
detalle largo consultable bajo demanda, guía de adopción completa y enlaces
funcionales.

**TEST-010:** conteo, revisión de enlaces y recorrido documental de nuevo
proyecto. TDD no aplica a reubicación de texto; guardar conteo y revisión.

**DONE cuando:** información preservada, TEST-010 documentado, índice y
quickstart coherentes y sin enlaces rotos.

## TASK-007 — Regresión, trazabilidad y evidencia final

**Tipo:** TEST  
**Estado:** DONE  
**Prioridad:** P1  
**Trazabilidad:** FR-001 a FR-006, NFR-001/002, SEC-001, AC-001 a AC-007,
DEC-001 a DEC-005.  
**Depende de:** TASK-003, TASK-004, TASK-005, TASK-006.

**Alcance:** ejecutar suite completa, checker y controles documentales;
registrar `specs/008-portable-harness-adoption/evidence/implementation.md`.
Actualizar solo estado/enlaces operativos de handoff e índice. No crear PASS
ficticio ni sustituir `/validate`.

**TEST-011:** regresión y mapa requisito -> AC -> tarea -> prueba/evidencia.
TDD no aplica a esta consolidación: los cambios automatizables ya tienen
RED/GREEN en TASK-002/003/004. Registrar salidas reales y fallos pendientes.

**DONE cuando:** todas las tareas previas están DONE, TEST-011 pasa, ningún
gap bloqueante queda abierto y la evidencia permite ejecutar `/validate`.

# 4. Grafo, orden y conflictos

| Orden | Tarea | Depende de | Estado |
|------:|-------|-----------|--------|
| 1 | TASK-001 | ninguna | DONE |
| 2 | TASK-002 | TASK-001 | DONE |
| 3 | TASK-003 | TASK-002 | DONE |
| 4 | TASK-004 | TASK-001, TASK-002 | DONE |
| 5 | TASK-005 | TASK-003, TASK-004 | DONE |
| 6 | TASK-006 | TASK-001, TASK-002 | DONE |
| 7 | TASK-007 | TASK-003, TASK-004, TASK-005, TASK-006 | DONE |

TASK-003 y TASK-004 pueden avanzar en paralelo tras TASK-002. TASK-004 y
TASK-006 comparten `docs/index.md`; TASK-002/005/006 comparten
`docs/adoption.md`: coordinar o ejecutar sus ediciones secuencialmente.
No hay ciclos ni tareas huérfanas.

# 5. Matriz de cobertura

| Requisito / criterio | Tarea | Evidencia prevista |
|----------------------|-------|--------------------|
| FR-001, BR-001, AC-001 | TASK-001, 003 | TEST-001, 005 |
| FR-002, NFR-002, BR-002, AC-002 | TASK-002, 003 | TEST-002, 005 |
| FR-003, AC-003 | TASK-003 | TEST-005 |
| FR-004, AC-004 | TASK-005 | TEST-009 |
| FR-005, AC-005 | TASK-004 | TEST-006, 007, 008 |
| FR-006, NFR-001, AC-006 | TASK-006 | TEST-010 |
| SEC-001, AC-007 | TASK-002 | TEST-003, 004 |

DEC-001 a DEC-005 tienen TASK-001, 002, 004, 005 y 006 respectivamente.
La evidencia consolidada corresponde a TASK-007 / TEST-011.

# 6. Bloqueos y discoveries

No hay bloqueos conocidos ni preguntas Q-TASK pendientes. Discovery fuera de
alcance durante implementación se documentará en la evidencia y no se
implementará sin revisión del artefacto dueño.

# 7. Estado y aprobación

**Estado actual:** COMPLETED  
**Aprobado por:** Usuario responsable del proyecto  
**Fecha de aprobación:** 2026-09-30  
**Registro durable:** DECISION-005 en `decisions.json`.

La decisión humana "Aprobado" corresponde a TASKS-008 v0.1.0. Autoriza
iniciar `/implement` conforme al orden y alcance de estas tareas.
