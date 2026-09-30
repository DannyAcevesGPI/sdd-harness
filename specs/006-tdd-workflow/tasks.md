# Tareas: TDD en el flujo SDD

**ID:** TASKS-006
**SPEC relacionada:** SPEC-006
**PLAN relacionado:** PLAN-006
**Estado:** COMPLETED
**Versión:** 0.1.0
**Fecha:** 2026-09-30

---

# 1. Precondiciones

- [x] SPEC-006 y PLAN-006 están APPROVED.
- [x] No hay aclaraciones bloqueantes.
- [x] Todos los requisitos MUST tienen estrategia y criterios.
- [x] El orden general de implementación está definido.

# 2. Objetivo

Integrar una política TDD obligatoria para comportamiento automatizable en el
Harness, con ciclo, evidencia, excepciones y guía para proyectos adoptantes.

# 3. Estados de tarea

TODO → IN_PROGRESS → BLOCKED/DONE.

# 4. Prioridades

P0 crítica; P1 alta; P2 normal; P3 baja.

# 5. Convención de identificadores

Tareas: TASK-001 a TASK-005. Verificaciones: TEST-001 a TEST-005.

---

# 6. Tareas

## TASK-001 — Definir política TDD

**Estado:** DONE
**Prioridad:** P0
**Tipo:** DOCUMENTATION

### Objetivo

Hacer del estándar de testing la referencia para ámbito, ciclo RED/GREEN,
excepciones y bloqueos.

### Trazabilidad

**Requisitos:** FR-001, FR-003, FR-004, BR-002.
**Criterios:** AC-001, AC-003, AC-004.
**Decisiones:** DEC-001.

### Dependencias

Ninguna.

### Alcance permitido

- Modificar: `.spec/standards/testing.md`.
- Reutilizar: Constitución y SPEC-006.
- No modificar: `src/`, `tests/`, evidencia histórica.

### Implementación esperada

Definir TDD obligatorio para comportamiento automatizable, RED auténtico antes
de código productivo, GREEN, refactor opcional en verde, bloqueo por entorno y
excepciones acotadas con verificación alternativa.

### Pruebas requeridas

- TEST-001 — Política cubre los casos obligatorios, no aplicables y bloqueados.

### Definition of Done

- [x] El estándar expresa la política sin contradecir la Constitución.
- [x] TEST-001 PASS y evidencia disponible.
- [x] Alcance y estándares respetados; sin bloqueos.

---

## TASK-002 — Integrar TDD en commands

**Estado:** DONE
**Prioridad:** P1
**Tipo:** DOCUMENTATION

### Objetivo

Aplicar la política en PLAN, TASKS, IMPLEMENT y VALIDATE sin cambiar los gates
de aprobación.

### Trazabilidad

**Requisitos:** FR-001, FR-002, FR-003, FR-004, BR-001, BR-002.
**Criterios:** AC-001, AC-002, AC-003, AC-004.
**Decisiones:** DEC-002.

### Dependencias

TASK-001.

### Alcance permitido

- Modificar: `.spec/commands/plan.md`, `tasks.md`, `implement.md`,
  `validate.md` dentro de `.spec/commands/`.
- Reutilizar: `.spec/standards/testing.md`, SPEC-006 y PLAN-006.
- No modificar: `.spec/constitution.md`, `src/`, `tests/`.

### Implementación esperada

Exigir casos en PLAN/TASKS, iniciar RED solo durante `/implement`, registrar
GREEN y verificar evidencia o excepción en `/validate`. Sustituir la frase que
declara TDD opcional. La falla de entorno produce BLOCKED.

### Pruebas requeridas

- TEST-002 — Recorrido de gates y secuencia TDD por command.
- TEST-003 — Validación rechaza RED de infraestructura o evidencia omitida.

### Definition of Done

- [x] Los cuatro commands son coherentes con la política y los gates SDD.
- [x] TEST-002 y TEST-003 PASS; evidencia disponible.
- [x] Alcance y estándares respetados; sin bloqueos.

---

## TASK-003 — Adaptar templates de fase

**Estado:** DONE
**Prioridad:** P1
**Tipo:** DOCUMENTATION

### Objetivo

Permitir registrar aplicabilidad y evidencias TDD en artefactos futuros.

### Trazabilidad

**Requisitos:** FR-002, FR-004, NFR-001, BR-001, BR-002.
**Criterios:** AC-002, AC-003, AC-004.
**Decisiones:** DEC-003.

### Dependencias

TASK-001.

### Alcance permitido

- Modificar: `.spec/templates/plan.template.md`, `tasks.template.md`,
  `validation.template.md`.
- Reutilizar: standard de testing y commands existentes.
- No modificar: `specification.template.md`, artefactos SDD validados.

### Implementación esperada

Añadir campos cortos para casos previstos, RED/GREEN, motivo y verificación
alternativa; enlazar evidencia dedicada. No solicitar código de prueba antes de
`/implement` ni aceptar excepción como PASS por sí sola.

### Pruebas requeridas

- TEST-004 — Templates producen campos consistentes con commands y SPEC.

### Definition of Done

- [x] Tres templates permiten documentar política, ciclo y excepción.
- [x] TEST-004 PASS; evidencia disponible.
- [x] Alcance y estándares respetados; sin bloqueos.

---

## TASK-004 — Publicar guía y navegación

**Estado:** DONE
**Prioridad:** P1
**Tipo:** DOCUMENTATION

### Objetivo

Explicar el uso de TDD en proyectos adoptantes sin inflar el bootstrap.

### Trazabilidad

**Requisitos:** FR-001, FR-005, NFR-001.
**Criterios:** AC-001, AC-005.
**Decisiones:** DEC-004.

### Dependencias

TASK-001.

### Alcance permitido

- Crear: `docs/tdd.md`.
- Modificar: `docs/adoption.md`, `docs/index.md`, `AGENTS.md`.
- Reutilizar: `.spec/standards/testing.md` y `docs/quickstart.md`.
- No modificar: `handoff.md`, README, `src/`, `tests/`.

### Implementación esperada

Guía stack agnostic con ciclo y casos límite; enlaces breves en adopción e
índice; una referencia compacta en AGENTS.

### Pruebas requeridas

- TEST-005 — Guía y enlaces resuelven; AGENTS bajo 200 líneas.

### Definition of Done

- [x] Guía y enlaces disponibles, sin duplicación extensa.
- [x] TEST-005 PASS; evidencia disponible.
- [x] Alcance y estándares respetados; sin bloqueos.

---

## TASK-005 — Verificar consistencia y registrar evidencia

**Estado:** DONE
**Prioridad:** P1
**Tipo:** TEST

### Objetivo

Demostrar que la política TDD resultante satisface AC-001 a AC-005.

### Trazabilidad

**Requisitos:** FR-001 a FR-005, NFR-001, BR-001, BR-002.
**Criterios:** AC-001 a AC-005.
**Decisiones:** DEC-001 a DEC-004.

### Dependencias

TASK-002, TASK-003 y TASK-004.

### Alcance permitido

- Crear: `specs/006-tdd-workflow/evidence/implementation.md`.
- Modificar: `specs/006-tdd-workflow/tasks.md` para estados y evidencia.
- Reutilizar: los archivos de TASK-001 a TASK-004 y tests de regresión
  relevantes si el cambio afecta su interpretación.
- No modificar: código de aplicación, pruebas existentes, historial validado.

### Implementación esperada

Ejercitar caso TDD aplicable, excepción legítima y falla de entorno; comprobar
consistencia entre documentos, enlaces, conteo de AGENTS y `git diff --check`.
Registrar resultados breves y rutas de evidencia.

### Pruebas requeridas

- TEST-001 a TEST-005 — Matriz de verificaciones documentales.

### Definition of Done

- [x] TEST-001 a TEST-005 PASS y evidencia dedicada disponible.
- [x] Calidad, alcance y seguridad revisados; sin bloqueos.

---

# 7. Tareas técnicas

TASK-005 es TEST derivada de PLAN-006 §11; soporta todos los criterios y no
introduce nuevas decisiones de producto.

# 8. Grafo de dependencias

TASK-001 → TASK-002, TASK-003, TASK-004 → TASK-005.

TASK-002, TASK-003 y TASK-004 pueden ejecutarse en paralelo tras TASK-001;
no modifican los mismos archivos. No hay ciclos ni conflictos de archivo.

# 9. Orden sugerido de ejecución

| Orden | Tarea | Depende de | Estado |
|------:|-------|------------|--------|
| 1 | TASK-001 | — | DONE |
| 2 | TASK-002 | TASK-001 | DONE |
| 3 | TASK-003 | TASK-001 | DONE |
| 4 | TASK-004 | TASK-001 | DONE |
| 5 | TASK-005 | TASK-002, TASK-003, TASK-004 | DONE |

# 10. Bloqueos

Ninguno conocido.

# 11. Descubrimientos fuera de alcance

Ninguno al generar TASKS.

# 12. Matriz de trazabilidad

| Tarea | Requisito | Criterio | Decisión | Prueba |
|-------|-----------|----------|----------|--------|
| TASK-001 | FR-001, FR-003, FR-004, BR-002 | AC-001, AC-003, AC-004 | DEC-001 | TEST-001 |
| TASK-002 | FR-001, FR-002, FR-003, FR-004, BR-001, BR-002 | AC-001 a AC-004 | DEC-002 | TEST-002, TEST-003 |
| TASK-003 | FR-002, FR-004, NFR-001, BR-001, BR-002 | AC-002 a AC-004 | DEC-003 | TEST-004 |
| TASK-004 | FR-001, FR-005, NFR-001 | AC-001, AC-005 | DEC-004 | TEST-005 |
| TASK-005 | FR-001 a FR-005, NFR-001, BR-001, BR-002 | AC-001 a AC-005 | DEC-001 a DEC-004 | TEST-001 a TEST-005 |

Todos los requisitos MUST, reglas y criterios tienen cobertura; no hay tareas
huérfanas.

# 13. Cambios durante implementación

Si cambia comportamiento de la política, revisar SPEC y recuperar aprobación.
Si cambia diseño o alcance estructural, revisar PLAN y TASKS afectados antes
de continuar.

# 14. Criterios para comenzar implementación

- [x] SPEC y PLAN están APPROVED.
- [x] Tareas, dependencias, verificaciones y alcance definidos.
- [x] No hay tareas huérfanas, ciclos, aclaraciones ni bloqueos.
- [x] Aprobación humana explícita de TASKS-006.

# 15. Estado del documento

**Estado actual:** COMPLETED
**Aprobado por:** usuario en esta conversación
**Fecha de aprobación:** 2026-09-30
