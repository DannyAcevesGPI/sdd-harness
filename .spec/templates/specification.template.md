# Especificación: [Nombre de la funcionalidad]

**ID:** SPEC-[XXX]  
**Estado:** DRAFT  
**Versión:** 0.1.0  
**Fecha:** [YYYY-MM-DD]

---

# 1. Resumen

## 1.1 Descripción

[Descripción breve de la funcionalidad y del resultado esperado.]

## 1.2 Problema

[Describir el problema que se busca resolver.

Explicar la necesidad desde la perspectiva del negocio, usuario
o sistema.

Evitar describir todavía cómo se implementará.]

## 1.3 Objetivo

[Describir qué deberá conseguir esta funcionalidad.]

---

# 2. Alcance

## 2.1 Incluido

Esta especificación incluye:

- [Elemento incluido]
- [Elemento incluido]
- [Elemento incluido]

## 2.2 Fuera de alcance

Esta especificación NO incluye:

- [Elemento fuera de alcance]
- [Elemento fuera de alcance]

Los elementos fuera de alcance no deberán implementarse como parte
de esta especificación.

---

# 3. Actores

## ACT-001 — [Nombre del actor]

**Descripción:**

[Quién o qué interactúa con el sistema.]

**Responsabilidades o necesidades:**

- [Necesidad]
- [Necesidad]

---

# 4. Requisitos funcionales

## FR-001 — [Nombre del requisito]

**Descripción:**

El sistema deberá [comportamiento observable].

**Prioridad:** [MUST | SHOULD | COULD]

**Origen:**

[Problema, necesidad o decisión que origina el requisito.]

---

## FR-002 — [Nombre del requisito]

**Descripción:**

El sistema deberá [comportamiento observable].

**Prioridad:** [MUST | SHOULD | COULD]

**Origen:**

[Origen del requisito.]

---

# 5. Requisitos no funcionales

## NFR-001 — [Nombre]

**Categoría:**

[Rendimiento | Disponibilidad | Escalabilidad | Usabilidad |
Observabilidad | Mantenibilidad | Otra]

**Descripción:**

[Requisito medible o verificable.]

**Métrica o condición:**

[Cómo podrá comprobarse.]

---

# 6. Requisitos de seguridad

## SEC-001 — [Nombre]

**Descripción:**

[Control o comportamiento de seguridad requerido.]

**Riesgo mitigado:**

[Descripción breve del riesgo.]

---

# 7. Reglas de negocio

## BR-001 — [Nombre]

**Regla:**

[Regla de negocio que debe cumplirse.]

**Ejemplo:**

[Ejemplo cuando ayude a eliminar ambigüedad.]

---

# 8. Criterios de aceptación

## AC-001 — [Nombre]

**Relacionado con:** FR-001

### Given

[Estado inicial o precondición.]

### When

[Acción realizada.]

### Then

[Resultado observable esperado.]

---

## AC-002 — [Nombre]

**Relacionado con:** FR-001

### Given

[Precondición.]

### When

[Acción.]

### Then

[Resultado esperado.]

---

# 9. Casos límite y escenarios de error

## EDGE-001 — [Escenario]

**Condición:**

[Situación límite o excepcional.]

**Comportamiento esperado:**

[Qué deberá hacer el sistema.]

---

# 10. Datos involucrados

Esta sección describe los conceptos de información necesarios desde
la perspectiva funcional.

No define todavía el modelo físico de base de datos.

## [Entidad o concepto]

Información requerida:

- [Campo o concepto]
- [Campo o concepto]
- [Campo o concepto]

Reglas relevantes:

- [Regla]
- [Restricción]

---

# 11. Dependencias

La funcionalidad depende de:

- [Sistema, funcionalidad o condición]
- [Dependencia]

Si no existen dependencias conocidas:

Ninguna.

---

# 12. Restricciones

Restricciones conocidas:

- [Restricción técnica]
- [Restricción de negocio]
- [Restricción legal]
- [Restricción operativa]

Una restricción técnica solamente deberá incluirse cuando ya exista
una decisión explícita que deba respetarse.

---

# 13. Suposiciones

## ASM-001

[Suposición.]

## ASM-002

[Suposición.]

Las suposiciones que afecten significativamente al comportamiento
deberán confirmarse antes de la implementación.

---

# 14. Preguntas abiertas y necesidades de aclaración

Cuando exista información insuficiente, ambigua o contradictoria,
deberá marcarse explícitamente utilizando:

[NEEDS CLARIFICATION]

El agente no deberá inventar una respuesta ni convertir una suposición
en requisito sin indicarlo.

---

## Q-001 — [Título de la pregunta]

**Estado:** [NEEDS CLARIFICATION]

**Pregunta:**

[Pregunta concreta que debe resolverse.]

**Contexto:**

[Explicar por qué apareció la duda.]

**Impacto:**

[Qué requisito, comportamiento o decisión depende de esta respuesta.]

**Bloqueante:** [YES | NO]

**Opciones conocidas:**

1. [Opción A]
2. [Opción B]
3. [Opción C]

**Respuesta:**

[PENDIENTE]

**Resuelto por:**

[PENDIENTE]

**Fecha de resolución:**

[PENDIENTE]

---

# 14.1 Ciclo de vida de una aclaración

Una aclaración podrá utilizar los siguientes estados:

[NEEDS CLARIFICATION]
→ [CLARIFIED]

Cuando una aclaración sea resuelta:

1. Registrar la respuesta.
2. Identificar quién resolvió la pregunta.
3. Registrar la fecha.
4. Actualizar los requisitos afectados.
5. Actualizar los criterios de aceptación afectados.
6. Cambiar el estado a `[CLARIFIED]`.

Resolver una pregunta no sustituye la actualización de la
especificación.

La respuesta deberá reflejarse en las secciones correspondientes
de la SPEC.

---

# 15. Matriz inicial de trazabilidad

| Requisito | Criterios de aceptación | Prioridad |
|-----------|-------------------------|-----------|
| FR-001 | AC-001, AC-002 | MUST |
| FR-002 | AC-003 | SHOULD |
| SEC-001 | AC-004 | MUST |

Esta matriz deberá mantenerse consistente con el resto
de la especificación.

---

# 16. Criterios para avanzar a planificación

La especificación podrá avanzar a `plan.md` solamente cuando:

- [ ] El problema está claramente definido.
- [ ] El alcance está definido.
- [ ] Los elementos fuera de alcance están definidos.
- [ ] Los actores relevantes están identificados.
- [ ] Los requisitos funcionales están identificados.
- [ ] Los requisitos MUST tienen criterios de aceptación.
- [ ] Los requisitos de seguridad relevantes están identificados.
- [ ] Las reglas de negocio relevantes están documentadas.
- [ ] Los principales casos límite están considerados.
- [ ] Las restricciones conocidas están documentadas.
- [ ] Las suposiciones importantes están documentadas.
- [ ] No existen elementos `[NEEDS CLARIFICATION]` marcados como bloqueantes.
- [ ] Las aclaraciones resueltas fueron incorporadas a los requisitos correspondientes.
- [ ] Las decisiones obtenidas durante la aclaración quedaron documentadas.
- [ ] Los requisitos son verificables.
- [ ] No se han introducido decisiones técnicas innecesarias.

---

# 17. Estado de aprobación

**Estado actual:**

DRAFT

Estados permitidos:

DRAFT
→ IN_REVIEW
→ APPROVED
→ SUPERSEDED

## Aprobación

La transición a `APPROVED` requiere aprobación humana explícita.

Los agentes pueden preparar y revisar la SPEC, pero no podrán
autoaprobarla.

**Aprobado por:**

[PENDIENTE]

**Fecha de aprobación:**

[PENDIENTE]

**Decisión explícita y alcance:**

[PENDIENTE; registrar el contenido de la decisión humana, no solo "en chat"]

**Registro durable:**

`specs/<feature-id>/decisions.json` deberá contener el evento y la huella del
contenido autorizado antes de avanzar a PLAN. Véase
`docs/state-reconstruction.md`.

La implementación no podrá comenzar mientras la especificación
no se encuentre en estado:

APPROVED
