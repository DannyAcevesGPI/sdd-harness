# Tareas: Preparación operativa para agentes, subagentes y hooks

**ID:** TASKS-002
**SPEC relacionada:** SPEC-002
**PLAN relacionado:** PLAN-002
**Estado:** COMPLETED
**Versión:** 0.1.0
**Fecha:** 2026-09-30

---

# 1. Precondiciones

Antes de generar estas tareas se verificó:

- [x] Existe una SPEC asociada.
- [x] La SPEC se encuentra en estado `APPROVED`.
- [x] Existe un PLAN asociado.
- [x] El PLAN se encuentra en estado `APPROVED`.
- [x] No existen `[NEEDS CLARIFICATION]` bloqueantes.
- [x] Los requisitos MUST tienen cobertura técnica.
- [x] El orden general de implementación está definido.

---

# 2. Objetivo

Dividir PLAN-002 en trabajo documental trazable para compactar `AGENTS.md`,
preparar subagentes, preparar hooks y verificar que el Harness mantiene sus
gates y compatibilidad.

---

# 3. Estados de tarea

Estados permitidos:

TODO
→ IN_PROGRESS
→ BLOCKED
→ DONE

`CANCELLED` es anotación histórica, no estado activo.

---

# 4. Prioridades

Prioridades permitidas:

P0 — Bloqueante o crítica.
P1 — Alta.
P2 — Normal.
P3 — Baja.

---

# 5. Convención de identificadores

Tareas: TASK-001 a TASK-004.

Pruebas/evidencias: TEST-001 a TEST-005.

---

# 6. Tareas

## TASK-001 — Compactar AGENTS.md

**Estado:** DONE
**Prioridad:** P0
**Tipo:** DOCUMENTATION

### Objetivo

Reescribir `AGENTS.md` como índice operativo compacto de menos de 200 líneas,
preservando bootstrap, ruteo SDD, gates, mutation boundary y trazabilidad.

### Trazabilidad

**Requisitos:**

- FR-001
- FR-002
- NFR-001
- NFR-002
- BR-001

**Criterios de aceptación:**

- AC-001
- AC-002
- AC-005

**Decisiones del plan:**

- DEC-001

### Dependencias

**Depende de:**

- Ninguna

### Alcance permitido

Crear:

- Ninguno

Modificar:

- `AGENTS.md`

Reutilizar:

- `.spec/constitution.md`
- `.spec/commands/`
- `.spec/standards/`
- `handoff.md`
- `specs/002-agent-operating-readiness/spec.md`
- `specs/002-agent-operating-readiness/plan.md`

No modificar:

- `src/`
- `tests/`
- `specs/001-audit-task-management/`

### Implementación esperada

Sustituir la versión extensa de `AGENTS.md` por un documento menor a 200 líneas
que funcione como bootstrap y mapa hacia fuentes superiores, sin redefinirlas.

### Pruebas requeridas

- TEST-001 — Conteo de líneas confirma `AGENTS.md` menor a 200 líneas.
- TEST-002 — Revisión documental confirma bootstrap y mutation boundary.
- TEST-005 — Revisión de consistencia normativa sin contradicciones bloqueantes.

### Validaciones

- [x] `AGENTS.md` queda bajo el límite de 200 líneas.
- [x] Constitución y commands siguen siendo fuentes autoritativas referenciadas.
- [x] No se modifica código de aplicación ni feature validada.
- [x] Evidencia de conteo y revisión disponible.

### Evidencia esperada

- Salida de `wc -l AGENTS.md`.
- Extracto o checklist de revisión documental.
- Evidencia obtenida: `evidence/implementation.md`, TEST-001, TEST-002 y TEST-005.

### Definition of Done

La tarea se considera `DONE` cuando:

- [x] El objetivo fue cumplido.
- [x] La implementación respeta PLAN-002.
- [x] La implementación respeta SPEC-002.
- [x] TEST-001, TEST-002 y parte aplicable de TEST-005 pasan.
- [x] No existen bloqueos pendientes.
- [x] La evidencia está disponible.

---

## TASK-002 — Crear guía de subagentes

**Estado:** DONE
**Prioridad:** P1
**Tipo:** DOCUMENTATION

### Objetivo

Crear una guía documental que defina delegación a subagentes con alcance,
fuentes, límites, evidencia y prohibición de aprobar gates.

### Trazabilidad

**Requisitos:**

- FR-003
- SEC-002
- BR-002

**Criterios de aceptación:**

- AC-003

**Decisiones del plan:**

- DEC-002

### Dependencias

**Depende de:**

- TASK-001

### Alcance permitido

Crear:

- `docs/agents/subagents.md`

Modificar:

- `AGENTS.md` solamente si se requiere ajustar una referencia mínima.

Reutilizar:

- `.spec/constitution.md`
- `.spec/commands/`
- `specs/002-agent-operating-readiness/plan.md`

No modificar:

- `src/`
- `tests/`

### Implementación esperada

Documentar qué puede delegarse, qué no puede delegarse, qué debe recibir un
subagente y qué evidencia debe devolver. La aprobación humana no puede ser
delegada.

### Pruebas requeridas

- TEST-003 — Revisión documental confirma delegación acotada sin transferencia de aprobación.

### Validaciones

- [x] La guía define alcance, fuentes y límites de mutación.
- [x] La guía exige evidencia verificable.
- [x] La guía mantiene responsabilidad final en el agente principal.

### Evidencia esperada

- Checklist de revisión contra AC-003 y SEC-002.
- Evidencia obtenida: `evidence/implementation.md`, TEST-003.

### Definition of Done

La tarea se considera `DONE` cuando:

- [x] El objetivo fue cumplido.
- [x] TEST-003 pasa.
- [x] No se introducen nuevas decisiones técnicas.
- [x] La evidencia está disponible.

---

## TASK-003 — Crear guía de hooks

**Estado:** DONE
**Prioridad:** P1
**Tipo:** DOCUMENTATION

### Objetivo

Crear una guía documental para hooks como apoyo operativo futuro, sin hooks
ejecutables ni dependencias nuevas.

### Trazabilidad

**Requisitos:**

- FR-004
- SEC-001
- NFR-002

**Criterios de aceptación:**

- AC-004

**Decisiones del plan:**

- DEC-003

### Dependencias

**Depende de:**

- TASK-001

### Alcance permitido

Crear:

- `docs/agents/hooks.md`

Modificar:

- `AGENTS.md` solamente si se requiere ajustar una referencia mínima.

Reutilizar:

- `.spec/standards/security.md`
- `.spec/commands/validate.md`
- `specs/002-agent-operating-readiness/plan.md`

No modificar:

- `.git/hooks/`
- `src/`
- `tests/`

### Implementación esperada

Documentar categorías recomendadas de hooks, límites de autoridad, manejo de
secretos, evidencia y condiciones para futura automatización.

### Pruebas requeridas

- TEST-004 — Revisión documental confirma que hooks no sustituyen SPEC, PLAN, TASKS, validación, aprobación humana ni seguridad.

### Validaciones

- [x] No se crean hooks ejecutables.
- [x] No se agregan dependencias.
- [x] Se prohíbe exponer secretos en comandos, logs o evidencia.

### Evidencia esperada

- Checklist de revisión contra AC-004 y SEC-001.
- Evidencia obtenida: `evidence/implementation.md`, TEST-004.

### Definition of Done

La tarea se considera `DONE` cuando:

- [x] El objetivo fue cumplido.
- [x] TEST-004 pasa.
- [x] No se modifica configuración ejecutable.
- [x] La evidencia está disponible.

---

## TASK-004 — Verificar consistencia, línea base y regresión

**Estado:** DONE
**Prioridad:** P0
**Tipo:** TEST

### Objetivo

Ejecutar verificaciones documentales y regresión existente para confirmar que
SPEC-002/PLAN-002 se cumplen y que la feature validada no fue afectada.

### Trazabilidad

**Requisitos:**

- FR-001
- FR-002
- FR-003
- FR-004
- NFR-001
- NFR-002
- SEC-001
- SEC-002
- BR-001
- BR-002

**Criterios de aceptación:**

- AC-001
- AC-002
- AC-003
- AC-004
- AC-005

**Decisiones del plan:**

- DEC-001
- DEC-002
- DEC-003

### Dependencias

**Depende de:**

- TASK-001
- TASK-002
- TASK-003

### Alcance permitido

Crear:

- Evidencia dentro de `specs/002-agent-operating-readiness/evidence/` si se decide registrar salidas en archivos.

Modificar:

- `specs/002-agent-operating-readiness/tasks.md` para estados y evidencia.

Reutilizar:

- `AGENTS.md`
- `docs/agents/subagents.md`
- `docs/agents/hooks.md`
- `src/audit_tasks.py`
- `tests/test_audit_tasks.py`

No modificar:

- Código de aplicación.
- Pruebas existentes.

### Implementación esperada

Verificar conteo de líneas, presencia de reglas obligatorias, coherencia con
fuentes superiores, ausencia de secretos evidentes y regresión de `unittest`.

### Pruebas requeridas

- TEST-001 — `AGENTS.md` menor a 200 líneas.
- TEST-002 — Bootstrap y mutation boundary presentes.
- TEST-003 — Subagentes acotados sin aprobación delegada.
- TEST-004 — Hooks acotados sin sustituir gates ni seguridad.
- TEST-005 — Consistencia normativa y regresión existente PASS.

### Validaciones

- [x] Conteo de líneas PASS.
- [x] Revisión documental PASS.
- [x] Regresión existente PASS con `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest discover -s tests -v`.
- [x] No hay cambios no autorizados en `src/`, `tests/` o feature 001.

### Evidencia esperada

- Salidas o resumen de comandos ejecutados.
- Matriz final de TEST-001 a TEST-005.
- Evidencia obtenida: `evidence/implementation.md`.

### Definition of Done

La tarea se considera `DONE` cuando:

- [x] El objetivo fue cumplido.
- [x] TEST-001 a TEST-005 pasan.
- [x] No existen bloqueos pendientes.
- [x] La evidencia está disponible.

---

# 7. Tareas técnicas

TASK-004 es de tipo TEST y se justifica por PLAN-002 §11, AC-001 a AC-005 y
NFR-002. No introduce comportamiento nuevo; verifica el trabajo documental
aprobado.

---

# 8. Grafo de dependencias

TASK-001
   │
   ├─────────┐
   ▼         ▼
TASK-002   TASK-003
   │         │
   └────┬────┘
        ▼
     TASK-004

No existen dependencias circulares.

---

# 9. Orden sugerido de ejecución

| Orden | Tarea | Depende de | Estado |
|------:|-------|------------|--------|
| 1 | TASK-001 | — | DONE |
| 2 | TASK-002 | TASK-001 | DONE |
| 3 | TASK-003 | TASK-001 | DONE |
| 4 | TASK-004 | TASK-001, TASK-002, TASK-003 | DONE |

TASK-002 y TASK-003 podrían ejecutarse en paralelo después de TASK-001, pero
ambas pueden tocar referencias mínimas en `AGENTS.md`; si lo hacen, ejecutarlas
secuencialmente para evitar conflicto.

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
| TASK-001 | FR-001, FR-002, NFR-001, NFR-002, BR-001 | AC-001, AC-002, AC-005 | DEC-001 | TEST-001, TEST-002, TEST-005 |
| TASK-002 | FR-003, SEC-002, BR-002 | AC-003 | DEC-002 | TEST-003 |
| TASK-003 | FR-004, SEC-001, NFR-002 | AC-004 | DEC-003 | TEST-004 |
| TASK-004 | Todos | AC-001 a AC-005 | DEC-001 a DEC-003 | TEST-001 a TEST-005 |

Todo requisito MUST tiene cobertura.

---

# 13. Cambios durante implementación

Si una tarea requiere modificar el PLAN o la SPEC, detener el trabajo afectado,
actualizar el artefacto propietario y recuperar approval gates aplicables.

---

# 14. Criterios para comenzar implementación

La implementación podrá comenzar solamente cuando:

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

DRAFT
→ IN_REVIEW
→ APPROVED
→ IN_PROGRESS
→ COMPLETED

**Estado actual:**

COMPLETED

## Aprobación

La transición a `APPROVED` requiere aprobación humana explícita.

Los agentes pueden preparar y revisar TASKS, pero no podrán autoaprobar el
documento.

**Aprobado por:**

Usuario, mediante respuesta "Aprobado" en conversación del 2026-09-30.

**Fecha de aprobación:**

2026-09-30
