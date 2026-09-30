# Tareas: Historial de cambios del Harness

**ID:** TASKS-005
**SPEC relacionada:** SPEC-005
**PLAN relacionado:** PLAN-005
**Estado:** COMPLETED
**Versión:** 0.1.0
**Fecha:** 2026-09-30

---

# 1. Precondiciones

- [x] SPEC-005 existe y está `APPROVED`.
- [x] PLAN-005 existe y está `APPROVED`.
- [x] No hay aclaraciones bloqueantes.
- [x] Los requisitos MUST tienen cobertura técnica.
- [x] El orden general de implementación está definido.

# 2. Objetivo

Publicar un changelog breve, verificable y accesible desde la documentación de
entrada, con evidencia de cumplimiento de los criterios de aceptación.

# 3. Estados de tarea

TODO → IN_PROGRESS → BLOCKED/DONE.

# 4. Prioridades

P0 crítica; P1 alta; P2 normal; P3 baja.

# 5. Convención de identificadores

Tareas: TASK-001 a TASK-003. Verificaciones: TEST-001 a TEST-003.

---

# 6. Tareas

## TASK-001 — Redactar el historial

**Estado:** DONE
**Prioridad:** P1
**Tipo:** DOCUMENTATION

### Objetivo

Crear `CHANGELOG.md` con hitos comprobados y pauta para entradas futuras.

### Trazabilidad

**Requisitos:** FR-001, FR-003, NFR-001, BR-001
**Criterios:** AC-001, AC-003
**Decisiones:** DEC-001, DEC-003

### Dependencias

Ninguna.

### Alcance permitido

- Crear: `CHANGELOG.md`.
- Reutilizar: Git, `specs/*/validation.md`, `docs/audit-history.md`.
- No modificar: `src/`, `tests/`, `.spec/`, `handoff.md`.

### Implementación esperada

Ordenar hitos de más reciente a más antiguo, describir solo hechos respaldados,
enlazar evidencia dedicada y añadir una pauta corta de mantenimiento.

### Pruebas requeridas

- TEST-001 — Orden, respaldo y enlaces de las entradas históricas.
- TEST-003 — Pauta futura clara, sin historial duplicado.

### Definition of Done

- [x] `CHANGELOG.md` existe y cubre AC-001 y AC-003.
- [x] TEST-001 y TEST-003 en PASS.
- [x] Evidencia disponible; alcance y estándares respetados.

---

## TASK-002 — Enlazar el changelog

**Estado:** DONE
**Prioridad:** P1
**Tipo:** DOCUMENTATION

### Objetivo

Hacer localizable `CHANGELOG.md` desde ambos puntos de entrada.

### Trazabilidad

**Requisitos:** FR-002
**Criterios:** AC-002
**Decisiones:** DEC-002

### Dependencias

TASK-001.

### Alcance permitido

- Modificar: `README.md`, `docs/index.md`.
- Reutilizar: `CHANGELOG.md`.
- No modificar: `src/`, `tests/`, `.spec/`, `handoff.md`.

### Implementación esperada

Agregar enlaces relativos breves y funcionales, sin copiar entradas del historial.

### Pruebas requeridas

- TEST-002 — Enlaces desde README e índice resuelven a `CHANGELOG.md`.

### Definition of Done

- [x] Ambos puntos de entrada enlazan el changelog.
- [x] TEST-002 en PASS.
- [x] Evidencia disponible; alcance y estándares respetados.

---

## TASK-003 — Verificar y registrar evidencia

**Estado:** DONE
**Prioridad:** P1
**Tipo:** TEST

### Objetivo

Comprobar todos los criterios y conservar resultados en la feature.

### Trazabilidad

**Requisitos:** FR-001, FR-002, FR-003, NFR-001
**Criterios:** AC-001, AC-002, AC-003
**Decisiones:** DEC-001, DEC-002, DEC-003

### Dependencias

TASK-001 y TASK-002.

### Alcance permitido

- Crear: `specs/005-harness-changelog/evidence/implementation.md`.
- Modificar: `specs/005-harness-changelog/tasks.md` para estados y evidencia.
- Reutilizar: Git, changelog, README, índice y validaciones existentes.
- No modificar: código de aplicación, tests existentes, Constitución.

### Implementación esperada

Verificar respaldo de cada entrada, orden descendente, enlaces, pauta futura y
formato; registrar comandos y resultados sin copiar salidas extensas.

### Pruebas requeridas

- TEST-001, TEST-002 y TEST-003 — Evidencia documental reproducible.

### Definition of Done

- [x] Todas las verificaciones en PASS.
- [x] `git diff --check` sin errores.
- [x] Evidencia dedicada disponible, sin bloqueos ni cambios fuera de alcance.

---

# 7. Tareas técnicas

TASK-003 es TEST, derivada de PLAN-005 §11. Soporta AC-001 a AC-003 y los
requisitos asociados; no introduce funcionalidad nueva.

# 8. Grafo de dependencias

TASK-001 → TASK-002 → TASK-003.

No hay ciclos ni candidatas independientes a paralelización.

# 9. Orden sugerido de ejecución

| Orden | Tarea | Depende de | Estado |
|------:|-------|------------|--------|
| 1 | TASK-001 | — | DONE |
| 2 | TASK-002 | TASK-001 | DONE |
| 3 | TASK-003 | TASK-001, TASK-002 | DONE |

# 10. Bloqueos

Ninguno conocido.

# 11. Descubrimientos fuera de alcance

Ninguno al preparar estas tareas.

# 12. Matriz de trazabilidad

| Tarea | Requisito | Criterio | Decisión | Prueba |
|-------|-----------|----------|----------|--------|
| TASK-001 | FR-001, FR-003, NFR-001, BR-001 | AC-001, AC-003 | DEC-001, DEC-003 | TEST-001, TEST-003 |
| TASK-002 | FR-002 | AC-002 | DEC-002 | TEST-002 |
| TASK-003 | FR-001, FR-002, FR-003, NFR-001 | AC-001, AC-002, AC-003 | DEC-001, DEC-002, DEC-003 | TEST-001, TEST-002, TEST-003 |

Todos los requisitos MUST y criterios tienen cobertura; no hay tareas huérfanas.

# 13. Cambios durante implementación

Si aparece un cambio funcional, regresar a SPEC. Si cambia diseño o alcance de
archivos de forma estructural, regresar a PLAN y recuperar los gates afectados.

# 14. Criterios para comenzar implementación

- [x] SPEC y PLAN están `APPROVED`.
- [x] Tareas, dependencias, verificaciones y alcance definidos.
- [x] No hay tareas huérfanas, ciclos, aclaraciones ni bloqueos.
- [x] Aprobación humana explícita de TASKS-005.

# 15. Estado del documento

**Estado actual:** COMPLETED
**Aprobado por:** usuario en esta conversación
**Fecha de aprobación:** 2026-09-30
