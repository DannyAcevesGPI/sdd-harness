# Tareas: Optimización de handoff y ventana de contexto

**ID:** TASKS-003
**SPEC relacionada:** SPEC-003
**PLAN relacionado:** PLAN-003
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

Dividir PLAN-003 en trabajo documental para compactar `handoff.md`, mover detalle
largo a `docs/`, crear quickstart e índice, y validar evidencia dedicada.

---

# 3. Estados de tarea

TODO → IN_PROGRESS → BLOCKED/DONE

---

# 4. Prioridades

P0 — Bloqueante o crítica. P1 — Alta. P2 — Normal. P3 — Baja.

---

# 5. Convención de identificadores

Tareas: TASK-001 a TASK-004.

Pruebas/evidencias: TEST-001 a TEST-006.

---

# 6. Tareas

## TASK-001 — Crear quickstart, índice y audit history compacto

**Estado:** DONE
**Prioridad:** P1
**Tipo:** DOCUMENTATION

### Objetivo

Crear la documentación de navegación que reemplazará el detalle largo embebido
en `handoff.md`.

### Trazabilidad

**Requisitos:** FR-004, FR-005, NFR-002, BR-002

**Criterios de aceptación:** AC-004, AC-006

**Decisiones del plan:** DEC-002

### Dependencias

**Depende de:** Ninguna

### Alcance permitido

Crear:

- `docs/quickstart.md`
- `docs/index.md`
- `docs/audit-history.md`

Modificar:

- Ninguno

Reutilizar:

- `AGENTS.md`
- `README.md`
- `specs/001-audit-task-management/`
- `specs/002-agent-operating-readiness/`

No modificar:

- `src/`
- `tests/`

### Implementación esperada

Documentar lectura mínima, rutas bajo demanda, resumen histórico compacto y
política de evidencia dedicada.

### Pruebas requeridas

- TEST-004 — Quickstart e índice existen y distinguen lectura obligatoria, bajo demanda y evidencia.
- TEST-006 — Evidencia futura queda documentada fuera de handoff.

### Definition of Done

- [x] Archivos creados.
- [x] TEST-004 y TEST-006 pasan.
- [x] No hay cambio de normas SDD.
- [x] Evidencia disponible.

---

## TASK-002 — Reescribir handoff como estado vivo

**Estado:** DONE
**Prioridad:** P0
**Tipo:** DOCUMENTATION

### Objetivo

Compactar `handoff.md` a menos de 200 líneas y convertirlo en estado vivo con
enlaces a evidencia.

### Trazabilidad

**Requisitos:** FR-001, FR-002, FR-003, NFR-001, NFR-002, BR-001, BR-002

**Criterios de aceptación:** AC-001, AC-002, AC-003, AC-005

**Decisiones del plan:** DEC-001, DEC-002

### Dependencias

**Depende de:** TASK-001

### Alcance permitido

Crear:

- Ninguno

Modificar:

- `handoff.md`

Reutilizar:

- `docs/index.md`
- `docs/quickstart.md`
- `docs/audit-history.md`
- `specs/001-audit-task-management/validation.md`
- `specs/002-agent-operating-readiness/validation.md`

No modificar:

- `src/`
- `tests/`

### Implementación esperada

Reemplazar el handoff extenso con un documento breve que indique estado actual,
features validadas, findings, next IDs, rutas de evidencia y regla de no repetir
audits cerrados sin evidencia nueva.

### Pruebas requeridas

- TEST-001 — `handoff.md` menor a 200 líneas y sin cuerpos detallados AUDIT-01 a AUDIT-10.
- TEST-002 — Estado vigente preservado.
- TEST-003 — SPEC-002 visible.
- TEST-005 — Seguridad y trazabilidad preservadas.

### Definition of Done

- [x] `handoff.md` queda bajo 200 líneas.
- [x] Rutas de evidencia preservadas.
- [x] No se fabrican nuevos PASS.
- [x] TEST-001, TEST-002, TEST-003 y TEST-005 pasan.

---

## TASK-003 — Registrar evidencia dedicada de SPEC-003

**Estado:** DONE
**Prioridad:** P1
**Tipo:** TEST

### Objetivo

Registrar evidencia de implementación en archivo dedicado, no en `handoff.md`.

### Trazabilidad

**Requisitos:** FR-005, NFR-002, BR-002

**Criterios de aceptación:** AC-006, AC-005

**Decisiones del plan:** DEC-002

### Dependencias

**Depende de:** TASK-001, TASK-002

### Alcance permitido

Crear:

- `specs/003-context-window-optimization/evidence/implementation.md`

Modificar:

- `specs/003-context-window-optimization/tasks.md` para estados/evidencia durante implementación.

Reutilizar:

- Outputs de verificaciones documentales.

No modificar:

- `handoff.md` salvo si la evidencia revela una corrección necesaria dentro de TASK-002.

### Implementación esperada

Documentar comandos, resultados y matriz TEST-001 a TEST-006.

### Pruebas requeridas

- TEST-006 — Evidencia dedicada existe y handoff solo enlaza/resume.

### Definition of Done

- [x] Evidencia dedicada creada.
- [x] TEST-006 pasa.
- [x] TASKS registra evidencia.

---

## TASK-004 — Verificación final de implementación

**Estado:** DONE
**Prioridad:** P0
**Tipo:** TEST

### Objetivo

Ejecutar verificaciones documentales, seguridad básica y regresión existente.

### Trazabilidad

**Requisitos:** Todos

**Criterios de aceptación:** AC-001 a AC-006

**Decisiones del plan:** DEC-001, DEC-002

### Dependencias

**Depende de:** TASK-001, TASK-002, TASK-003

### Alcance permitido

Crear:

- Ninguno adicional

Modificar:

- `specs/003-context-window-optimization/tasks.md` para cierre de estados.

Reutilizar:

- `handoff.md`
- `docs/quickstart.md`
- `docs/index.md`
- `docs/audit-history.md`
- `src/audit_tasks.py`
- `tests/test_audit_tasks.py`

No modificar:

- Código de aplicación.
- Pruebas existentes.

### Implementación esperada

Verificar conteo de líneas, rutas, ausencia de secretos, no creación de
dependencias y regresión `unittest`.

### Pruebas requeridas

- TEST-001 — Handoff corto.
- TEST-002 — Estado vigente.
- TEST-003 — SPEC-002 visible.
- TEST-004 — Quickstart e índice.
- TEST-005 — Seguridad y trazabilidad.
- TEST-006 — Evidencia dedicada.

### Definition of Done

- [x] TEST-001 a TEST-006 pasan.
- [x] Regresión existente PASS.
- [x] No hay cambios no autorizados.
- [x] Evidencia disponible.

---

# 7. Tareas técnicas

TASK-003 y TASK-004 son TEST/DOCUMENTATION derivados de PLAN-003 §11 y AC-001 a
AC-006. No introducen comportamiento de aplicación.

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

Ninguno.

---

# 12. Matriz de trazabilidad

| Tarea | Requisito | Criterio | Decisión | Prueba |
|-------|-----------|----------|----------|--------|
| TASK-001 | FR-004, FR-005, NFR-002, BR-002 | AC-004, AC-006 | DEC-002 | TEST-004, TEST-006 |
| TASK-002 | FR-001, FR-002, FR-003, NFR-001, NFR-002, BR-001, BR-002 | AC-001, AC-002, AC-003, AC-005 | DEC-001, DEC-002 | TEST-001, TEST-002, TEST-003, TEST-005 |
| TASK-003 | FR-005, NFR-002, BR-002 | AC-005, AC-006 | DEC-002 | TEST-005, TEST-006 |
| TASK-004 | Todos | AC-001 a AC-006 | DEC-001, DEC-002 | TEST-001 a TEST-006 |

Todo requisito MUST tiene cobertura.

---

# 13. Cambios durante implementación

Si una tarea requiere modificar SPEC o PLAN, detener, actualizar el artefacto
propietario y recuperar approval gates.

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

Usuario, mediante respuesta "Aprobado" en conversación del 2026-09-30.

**Fecha de aprobación:**

2026-09-30
