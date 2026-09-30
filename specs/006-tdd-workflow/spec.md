# Especificación: TDD en el flujo SDD

**ID:** SPEC-006
**Estado:** APPROVED
**Versión:** 0.1.0
**Fecha:** 2026-09-30

---

# 1. Resumen

## 1.1 Descripción

Integrar Test-Driven Development (TDD) en el trabajo del SDD Harness para que
el desarrollo de comportamiento comprobable use pruebas tempranas y conserve
evidencia de los ciclos de implementación.

## 1.2 Problema

El Harness exige pruebas relacionadas con requisitos, pero actualmente no
define cuándo deben escribirse: `/implement` declara TDD como no obligatorio.
Esto permite completar una feature sin comprobar que la prueba habría fallado
antes del cambio de código.

## 1.3 Objetivo

Establecer una política TDD coherente con los gates SPEC → PLAN → TASKS →
IMPLEMENT → VALIDATE, con aplicación clara para comportamiento automatizable,
excepciones justificadas y evidencia revisable.

---

# 2. Alcance

## 2.1 Incluido

- Exigir para cambios de comportamiento automatizable el ciclo prueba fallida → implementación mínima →
  prueba exitosa → refactorización con pruebas en verde.
- Explicar cómo PLAN y TASKS preparan casos de prueba derivados de requisitos y
  criterios de aceptación.
- Explicar cómo `/implement` y `/validate` registran y revisan la evidencia TDD.
- Documentar el uso de TDD para proyectos que adopten el Harness.
- Registrar la política obligatoria decidida en Q-001.

## 2.2 Fuera de alcance

- Reescribir retroactivamente features ya validadas o inventar evidencia RED.
- Imponer un framework o lenguaje de pruebas.
- Exigir pruebas automatizadas para cambios puramente documentales o criterios
  que solo puedan validarse manualmente con justificación.
- Crear hooks o herramientas ejecutables de automatización TDD.
- Cambiar los gates de aprobación humana definidos en la Constitución.

---

# 3. Actores

## ACT-001 — Mantenedor o desarrollador

Necesita saber cuándo aplicar TDD y qué evidencia conservar por tarea.

## ACT-002 — Agente de desarrollo

Necesita ejecutar TDD dentro de las tareas aprobadas sin implementar antes de
SPEC, PLAN y TASKS.

## ACT-003 — Validador

Necesita distinguir evidencia real de RED/GREEN y excepciones justificadas.

---

# 4. Requisitos funcionales

## FR-001 — Política TDD explícita

**Descripción:** El Harness deberá exigir TDD para todo cambio nuevo de
comportamiento que pueda probarse automáticamente, incluidas correcciones de
defectos reproducibles, y declarar claramente sus límites de aplicación.

**Prioridad:** MUST
**Origen:** Solicitud humana de integrar TDD.

## FR-002 — Preparación trazable

**Descripción:** Para comportamiento cubierto por TDD, PLAN y TASKS deberán
preparar casos verificables derivados de requisitos y criterios de aceptación
antes de modificar la implementación.

**Prioridad:** MUST
**Origen:** Trazabilidad existente del Harness y necesidad de orientar el ciclo.

## FR-003 — Ciclo TDD durante implementación

**Descripción:** Para los cambios cubiertos, el flujo deberá exigir una prueba
relevante que falle por el comportamiento faltante antes de modificar el código
productivo, una implementación mínima que la haga pasar y una refactorización
posterior con pruebas en verde cuando sea necesaria.

**Prioridad:** MUST
**Origen:** Significado operativo de TDD solicitado.

## FR-004 — Evidencia y excepciones

**Descripción:** El flujo deberá exigir evidencia mínima del ciclo RED/GREEN y
una justificación para cambios donde no hay comportamiento nuevo automatizable
o la verificación solo puede ser manual. Una prueba fallida por entorno deberá
tratarse como bloqueo, no como RED ni como excepción aprobada automáticamente.

**Prioridad:** MUST
**Origen:** Necesidad de validación verificable y casos no automatizables.

## FR-005 — Guía de adopción

**Descripción:** La documentación de adopción deberá explicar cómo aplicar la
política TDD en proyectos nuevos sin imponer stack ni duplicar comandos largos.

**Prioridad:** MUST
**Origen:** Reutilización del Harness en otros proyectos.

---

# 5. Requisitos no funcionales

## NFR-001 — Brevedad operativa

**Categoría:** Mantenibilidad
**Descripción:** La guía operativa deberá ser breve y enlazar detalle solo donde
corresponda, conservando `AGENTS.md` bajo 200 líneas y `handoff.md` como estado
vivo.
**Métrica o condición:** Ambas restricciones se mantienen después del cambio.

---

# 6. Requisitos de seguridad

No se agregan controles nuevos. La evidencia TDD no debe incluir secretos,
datos personales reales ni salidas sensibles, según el estándar vigente.

---

# 7. Reglas de negocio

## BR-001 — Gate SDD antes de TDD

**Regla:** El ciclo TDD se ejecuta durante `/implement`, después de aprobar
SPEC, PLAN y TASKS. Preparar casos en PLAN o TASKS no autoriza modificar código
de pruebas antes del gate de implementación.

## BR-002 — Excepciones acotadas

**Regla:** Los cambios de comportamiento automatizable no pueden omitir TDD por
preferencia o conveniencia. Si el entorno impide ejecutar la prueba requerida,
la tarea queda bloqueada hasta resolverlo. Documentación, validación
exclusivamente manual y refactors sin comportamiento nuevo requieren evidencia
adecuada a su naturaleza, con motivo explícito para no usar RED/GREEN.

---

# 8. Criterios de aceptación

## AC-001 — Política consistente

**Relacionado con:** FR-001

### Given

Un agente consulta las reglas y commands aplicables.

### When

Determina cómo desarrollar comportamiento automatizable.

### Then

Encuentra TDD obligatorio para cambios de comportamiento automatizable y una
lista explícita de casos fuera de ese alcance.

## AC-002 — Casos antes de código

**Relacionado con:** FR-002, BR-001

### Given

Existe una feature con SPEC, PLAN y TASKS aprobados.

### When

Se inicia una tarea de comportamiento comprobable.

### Then

Los casos de prueba están relacionados con requisitos y criterios, y su código
solo se modifica en `/implement`.

## AC-003 — Ciclo verificable

**Relacionado con:** FR-003, FR-004

### Given

Una tarea aplica TDD.

### When

Se implementa y valida.

### Then

Hay evidencia de RED causado por comportamiento faltante antes del cambio
productivo, GREEN tras implementación y pruebas en verde tras refactorización
cuando la hubo. Una falla de infraestructura no cuenta como RED.

## AC-004 — Excepción explícita

**Relacionado con:** FR-004, BR-002

### Given

Un cambio no admite TDD razonablemente.

### When

Se documenta la excepción.

### Then

Se registra motivo, verificación alternativa y resultado; `/validate` no la
interpreta como PASS sin evidencia suficiente. Si la prueba automatizable está
bloqueada por entorno, la tarea no avanza como excepción.

## AC-005 — Adopción

**Relacionado con:** FR-005, NFR-001

### Given

Un equipo adopta el Harness en otro proyecto.

### When

Consulta su guía de adopción.

### Then

Puede aplicar la política TDD a su stack sin cargar `AGENTS.md` ni `handoff.md`
con instrucciones extensas.

---

# 9. Casos límite y escenarios de error

## EDGE-001 — Prueba falla por entorno

Una falla por infraestructura no demuestra RED válido; debe identificarse la
causa antes de avanzar.

## EDGE-002 — Comportamiento existente

Si la prueba ya pasa antes del cambio, se revisa si el caso expresa una
necesidad nueva o si hace falta otro caso, sin fabricar RED artificial.

## EDGE-003 — Documentación o validación manual

Se usan verificaciones adecuadas al cambio y se registra por qué no aplica
un ciclo TDD automatizado.

---

# 10. Datos involucrados

Casos de prueba, resultados RED/GREEN, referencias a requisitos, tareas y
evidencia. No se requiere persistencia nueva.

# 11. Dependencias

Constitución, standards y commands SDD existentes; guía de adopción.

# 12. Restricciones

- No relajar aprobaciones, trazabilidad ni integridad de pruebas.
- No imponer herramientas de pruebas ajenas al stack del proyecto adoptante.
- No incluir secretos en evidencia.

# 13. Suposiciones

## ASM-001

La política aplicará prospectivamente a trabajo nuevo; las features ya
validadas conservarán su evidencia histórica.

---

# 14. Preguntas abiertas y necesidades de aclaración

## Q-001 — Grado de obligatoriedad

**Estado:** [CLARIFIED]
**Pregunta:** ¿TDD será obligatorio para código con comportamiento automatizable,
recomendado con excepciones justificadas o solo una guía opcional?
**Contexto:** `/implement` hoy lo declara no obligatorio; cambiar esa regla
afecta gates y evidencia futura.
**Impacto:** FR-001, FR-003, FR-004, AC-001, AC-003 y AC-004.
**Bloqueante:** YES
**Opciones conocidas:** Obligatorio; recomendado con excepciones; opcional.
**Respuesta:** Opción 1. TDD obligatorio para código con comportamiento
automatizable. Los casos fuera de ese alcance requieren motivo y verificación
alternativa; fallas de entorno bloquean la tarea.
**Resuelto por:** usuario en esta conversación
**Fecha de resolución:** 2026-09-30
**Artefactos afectados:** FR-001, FR-003, FR-004, BR-002, AC-001, AC-003, AC-004.

---

# 15. Matriz inicial de trazabilidad

| Requisito | Criterios de aceptación | Prioridad |
|-----------|-------------------------|-----------|
| FR-001 | AC-001 | MUST |
| FR-002, BR-001 | AC-002 | MUST |
| FR-003 | AC-003 | MUST |
| FR-004 | AC-003, AC-004 | MUST |
| FR-005, NFR-001 | AC-005 | MUST |
| BR-002 | AC-004 | MUST |

---

# 16. Criterios para avanzar a planificación

- [x] Problema, actores, alcance y límites identificados.
- [x] Requisitos y criterios iniciales trazables.
- [x] Q-001 resuelta e incorporada a requisitos y criterios.
- [x] Aprobación humana explícita de la SPEC.

# 17. Estado de aprobación

**Estado actual:** APPROVED
**Resultado:** APPROVED
**Aprobado por:** usuario en esta conversación
**Fecha de aprobación:** 2026-09-30
