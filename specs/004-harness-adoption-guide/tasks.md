# Tareas: Guía de adopción del Harness para nuevos proyectos

**ID:** TASKS-004
**SPEC relacionada:** SPEC-004
**PLAN relacionado:** PLAN-004
**Estado:** COMPLETED
**Versión:** 0.1.0
**Fecha:** 2026-09-30

---

# 1. Precondiciones

- [x] Existe una SPEC asociada.
- [x] La SPEC se encuentra en estado `APPROVED`.
- [x] Existe un PLAN asociado.
- [x] El PLAN se encuentra en estado `APPROVED`.
- [x] No existen `[NEEDS CLARIFICATION]` bloqueantes.
- [x] Los requisitos MUST tienen cobertura técnica.
- [x] El orden general de implementación está definido.

---

# 2. Objetivo

Crear la guía reusable de adopción del Harness, enlazarla desde README e índice,
y validar que queda clara, portable y segura.

---

# 3. Estados de tarea

TODO → IN_PROGRESS → BLOCKED/DONE

---

# 4. Prioridades

P0 — Bloqueante o crítica. P1 — Alta. P2 — Normal. P3 — Baja.

---

# 5. Convención de identificadores

Tareas: TASK-001 a TASK-004.

Pruebas/evidencias: TEST-001 a TEST-005.

---

# 6. Tareas

## TASK-001 — Crear guía de adopción

**Estado:** DONE
**Prioridad:** P0
**Tipo:** DOCUMENTATION

### Objetivo

Crear `docs/adoption.md` con pasos para usar el Harness en proyectos nuevos.

### Trazabilidad

**Requisitos:** FR-001, FR-003, FR-004, NFR-001, NFR-002, SEC-001, BR-001, BR-002

**Criterios de aceptación:** AC-001, AC-003, AC-004, AC-005

**Decisiones del plan:** DEC-001

### Dependencias

**Depende de:** Ninguna

### Alcance permitido

Crear:

- `docs/adoption.md`

Modificar:

- Ninguno

Reutilizar:

- `AGENTS.md`
- `.spec/`
- `docs/quickstart.md`
- `handoff.md`

No modificar:

- `src/`
- `tests/`

### Implementación esperada

Documentar qué copiar, qué adaptar, qué no copiar, cómo iniciar la primera
feature, cómo manejar evidencia y cómo adaptar a cualquier stack.

### Pruebas requeridas

- TEST-001 — Guía dedicada existe y cubre adopción.
- TEST-003 — Distingue plantilla reusable de evidencia local y advierte sobre secretos.
- TEST-004 — Explica primera feature desde cero.
- TEST-005 — Explica portabilidad stack agnostic.

### Definition of Done

- [x] `docs/adoption.md` existe.
- [x] Guía queda bajo 250 líneas.
- [x] TEST-001, TEST-003, TEST-004 y TEST-005 pasan.
- [x] Evidencia disponible.

---

## TASK-002 — Enlazar guía desde README e índice

**Estado:** DONE
**Prioridad:** P1
**Tipo:** DOCUMENTATION

### Objetivo

Agregar referencias breves a `docs/adoption.md` desde `README.md` y `docs/index.md`.

### Trazabilidad

**Requisitos:** FR-002

**Criterios de aceptación:** AC-002

**Decisiones del plan:** DEC-002

### Dependencias

**Depende de:** TASK-001

### Alcance permitido

Crear:

- Ninguno

Modificar:

- `README.md`
- `docs/index.md`

Reutilizar:

- `docs/adoption.md`

No modificar:

- `.spec/constitution.md`
- `.spec/commands/`
- `.spec/standards/`
- `src/`
- `tests/`

### Implementación esperada

Agregar una sección breve en README y una entrada en docs index sin duplicar la
guía.

### Pruebas requeridas

- TEST-002 — README e índice enlazan la guía dedicada.

### Definition of Done

- [x] README enlaza la guía.
- [x] `docs/index.md` enlaza la guía.
- [x] TEST-002 pasa.
- [x] Evidencia disponible.

---

## TASK-003 — Registrar evidencia dedicada

**Estado:** DONE
**Prioridad:** P1
**Tipo:** TEST

### Objetivo

Registrar evidencia de implementación en la feature.

### Trazabilidad

**Requisitos:** NFR-001, SEC-001

**Criterios de aceptación:** AC-001, AC-003, AC-005

**Decisiones del plan:** DEC-001, DEC-002

### Dependencias

**Depende de:** TASK-001, TASK-002

### Alcance permitido

Crear:

- `specs/004-harness-adoption-guide/evidence/implementation.md`

Modificar:

- `specs/004-harness-adoption-guide/tasks.md` para estados y evidencia.

Reutilizar:

- Salidas de verificaciones documentales.

### Implementación esperada

Documentar TEST-001 a TEST-005, comandos y resultados.

### Pruebas requeridas

- TEST-001 a TEST-005 — Matriz de evidencia registrada.

### Definition of Done

- [x] Evidencia dedicada creada.
- [x] Resultados documentados.
- [x] No hay bloqueos.

---

## TASK-004 — Verificación final de implementación

**Estado:** DONE
**Prioridad:** P0
**Tipo:** TEST

### Objetivo

Ejecutar revisión documental, búsqueda de secretos y regresión existente.

### Trazabilidad

**Requisitos:** Todos

**Criterios de aceptación:** AC-001 a AC-005

**Decisiones del plan:** DEC-001, DEC-002

### Dependencias

**Depende de:** TASK-001, TASK-002, TASK-003

### Alcance permitido

Crear:

- Ninguno adicional

Modificar:

- `specs/004-harness-adoption-guide/tasks.md` para cierre.

Reutilizar:

- `docs/adoption.md`
- `README.md`
- `docs/index.md`
- `src/audit_tasks.py`
- `tests/test_audit_tasks.py`

No modificar:

- Código de aplicación.
- Pruebas existentes.

### Implementación esperada

Verificar conteo de líneas, enlaces, separación de evidencia, stack agnostic,
secretos y regresión.

### Pruebas requeridas

- TEST-001 — Guía dedicada existe y cubre adopción.
- TEST-002 — README e índice enlazan guía.
- TEST-003 — Plantilla y evidencia separadas; seguridad.
- TEST-004 — Primera feature explicada.
- TEST-005 — Portabilidad documentada.

### Definition of Done

- [x] TEST-001 a TEST-005 pasan.
- [x] Regresión existente PASS.
- [x] No hay cambios no autorizados.
- [x] Evidencia disponible.

---

# 7. Tareas técnicas

TASK-003 y TASK-004 son TEST/DOCUMENTATION derivados de PLAN-004 §11 y AC-001 a
AC-005. No introducen comportamiento de aplicación.

---

# 8. Grafo de dependencias

TASK-001 → TASK-002 → TASK-003 → TASK-004

No existen dependencias circulares.

---

# 9. Orden sugerido de ejecución

| Orden | Tarea | Depende de | Estado |
|------:|-------|------------|--------|
| 1 | TASK-001 | — | DONE |
| 2 | TASK-002 | TASK-001 | DONE |
| 3 | TASK-003 | TASK-001, TASK-002 | DONE |
| 4 | TASK-004 | TASK-001, TASK-002, TASK-003 | DONE |

---

# 10. Bloqueos

No existen bloqueos conocidos.

---

# 11. Descubrimientos fuera de alcance

Ninguno al generar tareas.

---

# 12. Matriz de trazabilidad

| Tarea | Requisito | Criterio | Decisión | Prueba |
|-------|-----------|----------|----------|--------|
| TASK-001 | FR-001, FR-003, FR-004, NFR-001, NFR-002, SEC-001, BR-001, BR-002 | AC-001, AC-003, AC-004, AC-005 | DEC-001 | TEST-001, TEST-003, TEST-004, TEST-005 |
| TASK-002 | FR-002 | AC-002 | DEC-002 | TEST-002 |
| TASK-003 | NFR-001, SEC-001 | AC-001, AC-003, AC-005 | DEC-001, DEC-002 | TEST-001, TEST-003, TEST-005 |
| TASK-004 | Todos | AC-001 a AC-005 | DEC-001, DEC-002 | TEST-001 a TEST-005 |

Todo requisito MUST tiene cobertura.

---

# 13. Cambios durante implementación

No se requirieron cambios de SPEC o PLAN durante la implementación.

---

# 14. Criterios para comenzar implementación

- [x] La SPEC está `APPROVED`.
- [x] El PLAN está `APPROVED`.
- [x] Las tareas están definidas.
- [x] Todos los requisitos MUST tienen tareas asociadas.
- [x] Las dependencias entre tareas están identificadas.
- [x] Las pruebas requeridas están identificadas.
- [x] Las tareas tienen alcance definido.
- [x] No existen tareas huérfanas.
- [x] No existen dependencias circulares.
- [x] No existen `[NEEDS CLARIFICATION]` bloqueantes.
- [x] No existen bloqueos conocidos que impidan comenzar.
- [x] TASKS está `APPROVED` por decisión humana explícita.

---

# 15. Estado del documento

Estados permitidos:

DRAFT → IN_REVIEW → APPROVED → IN_PROGRESS → COMPLETED

**Estado actual:**

COMPLETED

## Aprobación

La transición a `APPROVED` requiere aprobación humana explícita.

**Aprobado por:**

Usuario

**Fecha de aprobación:**

2026-09-30
