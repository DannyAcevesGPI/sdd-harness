# Especificación: Guía de adopción del Harness para nuevos proyectos

**ID:** SPEC-004
**Estado:** APPROVED
**Versión:** 0.1.0
**Fecha:** 2026-09-30

---

# 1. Resumen

## 1.1 Descripción

Esta feature documenta cómo usar el SDD Harness actual desde cero en otros
proyectos, mediante una guía dedicada y una referencia breve en el README.

## 1.2 Problema

El Harness ya está optimizado para este repositorio, pero falta una guía clara
para adoptarlo en proyectos nuevos sin cargar historial interno, evidencia local
o decisiones específicas de este repo.

## 1.3 Objetivo

Proveer instrucciones reutilizables para copiar, inicializar, adaptar y operar el
Harness en otro proyecto manteniendo el flujo SDD, los gates humanos y la
estrategia de evidencia dedicada.

---

# 2. Alcance

## 2.1 Incluido

Esta especificación incluye:

- Crear una guía dedicada para adopción en nuevos proyectos.
- Agregar una referencia breve en `README.md`.
- Explicar qué archivos copiar, cuáles adaptar y cuáles no copiar.
- Explicar cómo iniciar una primera feature desde cero.
- Explicar cómo mantener `AGENTS.md`, `handoff.md`, `docs/` y `specs/`.
- Incluir recomendaciones para proyectos con stacks distintos.

## 2.2 Fuera de alcance

Esta especificación NO incluye:

- Crear una herramienta automática de instalación.
- Publicar paquete, plantilla remota o GitHub template.
- Cambiar reglas SDD del Harness.
- Modificar código de aplicación o pruebas.
- Borrar evidencia existente de este repositorio.

Los elementos fuera de alcance no deberán implementarse como parte de esta
especificación.

---

# 3. Actores

## ACT-001 — Mantenedor que adopta el Harness

**Descripción:**

Persona que quiere usar el Harness en otro repositorio.

**Responsabilidades o necesidades:**

- Saber qué copiar.
- Saber qué adaptar al proyecto destino.
- Evitar copiar evidencia o historial que no corresponde.

## ACT-002 — Agente de desarrollo

**Descripción:**

Agente que trabajará dentro del nuevo proyecto usando el Harness.

**Responsabilidades o necesidades:**

- Tener instrucciones de bootstrap claras.
- Saber cómo iniciar SPEC/PLAN/TASKS/IMPLEMENT/VALIDATE.

---

# 4. Requisitos funcionales

## FR-001 — Guía de adopción

**Descripción:**

El repositorio deberá incluir una guía dedicada que explique cómo instalar y usar
el Harness actual en proyectos nuevos.

**Prioridad:** MUST

**Origen:**

Solicitud humana: documentar el uso del Harness actual para próximos proyectos.

---

## FR-002 — Referencia desde README

**Descripción:**

El README deberá incluir una referencia breve hacia la guía de adopción.

**Prioridad:** MUST

**Origen:**

Solicitud humana: documentarlo como documento o en README.

---

## FR-003 — Separación entre plantilla y evidencia local

**Descripción:**

La guía deberá distinguir qué artefactos forman parte del Harness reusable y qué
artefactos son evidencia/historial local que no debe copiarse ciegamente.

**Prioridad:** MUST

**Origen:**

Necesidad de reutilización segura entre proyectos.

---

## FR-004 — Flujo desde cero

**Descripción:**

La guía deberá explicar cómo iniciar una primera feature en un proyecto destino,
incluyendo SPEC, approval, PLAN, approval, TASKS, approval, IMPLEMENT y VALIDATE.

**Prioridad:** MUST

**Origen:**

Necesidad de operación desde cero.

---

# 5. Requisitos no funcionales

## NFR-001 — Brevedad operativa

**Categoría:** Mantenibilidad

**Descripción:**

La guía deberá ser suficientemente breve y escaneable para uso frecuente.

**Métrica o condición:**

La guía deberá quedar bajo 250 líneas.

---

## NFR-002 — Stack agnóstico

**Categoría:** Portabilidad

**Descripción:**

La guía deberá funcionar para proyectos con distintos lenguajes, frameworks y
herramientas, sin imponer stack.

**Métrica o condición:**

La guía debe indicar que standards/planes se adaptan al repositorio destino.

---

# 6. Requisitos de seguridad

## SEC-001 — No copiar secretos ni evidencia sensible

**Descripción:**

La guía deberá advertir que no deben copiarse secretos, logs sensibles ni
evidencia propia de otro proyecto al adoptar el Harness.

**Riesgo mitigado:**

Filtración de secretos o contexto privado entre repositorios.

---

# 7. Reglas de negocio

## BR-001 — El Harness es proceso, no stack

**Regla:**

La adopción del Harness no debe imponer framework, lenguaje, base de datos o
infraestructura.

**Ejemplo:**

Un proyecto Python, TypeScript o móvil puede usar el mismo flujo SDD ajustando
PLAN y TASKS al stack real.

---

## BR-002 — Nuevo proyecto, nuevo handoff

**Regla:**

Cada proyecto destino debe iniciar su propio `handoff.md`, evidencia y specs, en
vez de copiar el estado vivo de este repositorio como si fuera propio.

**Ejemplo:**

Se puede copiar la estructura y reglas, pero no afirmar que el proyecto destino
tiene AUDIT-01 a AUDIT-10 PASS salvo que lo haya validado.

---

# 8. Criterios de aceptación

## AC-001 — Guía dedicada existe

**Relacionado con:** FR-001

### Given

El repositorio contiene documentación de adopción.

### When

Un mantenedor busca cómo usar el Harness en otro proyecto.

### Then

Encuentra una guía dedicada con pasos de copia, inicialización y operación.

---

## AC-002 — README enlaza la guía

**Relacionado con:** FR-002

### Given

Un usuario lee `README.md`.

### When

Busca cómo adoptar el Harness en otro proyecto.

### Then

Encuentra una referencia breve hacia la guía dedicada.

---

## AC-003 — Plantilla y evidencia separadas

**Relacionado con:** FR-003, SEC-001, BR-002

### Given

Un usuario sigue la guía.

### When

Decide qué copiar al proyecto destino.

### Then

Puede distinguir artefactos reutilizables de evidencia/historial local que no
debe copiarse sin adaptación.

---

## AC-004 — Primera feature explicada

**Relacionado con:** FR-004

### Given

Un proyecto destino ya copió el Harness base.

### When

Quiere iniciar su primera feature.

### Then

La guía describe el flujo SPEC → PLAN → TASKS → IMPLEMENT → VALIDATE con gates
humanos.

---

## AC-005 — Portabilidad documentada

**Relacionado con:** NFR-002, BR-001

### Given

El proyecto destino usa un stack distinto.

### When

Lee la guía.

### Then

Entiende que el Harness no impone stack y que el PLAN debe detectar el contexto
real del repositorio.

---

# 9. Casos límite y escenarios de error

## EDGE-001 — Proyecto destino ya tiene AGENTS.md

**Condición:**

El proyecto destino ya contiene instrucciones de agente.

**Comportamiento esperado:**

La guía debe recomendar fusionar instrucciones preservando las reglas SDD y las
decisiones propias del proyecto.

---

## EDGE-002 — Proyecto destino contiene secretos o evidencia sensible

**Condición:**

Al adoptar el Harness, existen logs, tokens o credenciales en el proyecto destino.

**Comportamiento esperado:**

La guía debe advertir que no se versionen ni copien secretos en evidencia.

---

# 10. Datos involucrados

## Documentación de adopción

Información requerida:

- Archivos base a copiar.
- Archivos a inicializar.
- Archivos que no deben copiarse como estado propio.
- Flujo operativo.
- Reglas de seguridad.

Reglas relevantes:

- No imponer stack.
- No copiar secretos.
- No fabricar estado validado.

---

# 11. Dependencias

La funcionalidad depende de:

- `README.md`
- `docs/index.md`
- `docs/quickstart.md`
- `AGENTS.md`
- `handoff.md`
- `.spec/`

---

# 12. Restricciones

Restricciones conocidas:

- No modificar código de aplicación.
- No modificar normas SDD.
- No crear instalador automático.

---

# 13. Suposiciones

## ASM-001

La primera versión de adopción puede ser documental y manual.

## ASM-002

Una guía dedicada bajo `docs/` es preferible a expandir demasiado el README.

---

# 14. Preguntas abiertas y necesidades de aclaración

No existen aclaraciones bloqueantes.

---

# 15. Matriz inicial de trazabilidad

| Requisito | Criterios de aceptación | Prioridad |
|-----------|-------------------------|-----------|
| FR-001 | AC-001 | MUST |
| FR-002 | AC-002 | MUST |
| FR-003 | AC-003 | MUST |
| FR-004 | AC-004 | MUST |
| NFR-001 | AC-001 | MUST |
| NFR-002 | AC-005 | MUST |
| SEC-001 | AC-003 | MUST |
| BR-001 | AC-005 | MUST |
| BR-002 | AC-003 | MUST |

---

# 16. Criterios para avanzar a planificación

La especificación podrá avanzar a `plan.md` solamente cuando:

- [x] El problema está claramente definido.
- [x] El alcance está definido.
- [x] Los elementos fuera de alcance están definidos.
- [x] Los actores relevantes están identificados.
- [x] Los requisitos funcionales están identificados.
- [x] Los requisitos MUST tienen criterios de aceptación.
- [x] Los requisitos de seguridad relevantes están identificados.
- [x] Las reglas de negocio relevantes están documentadas.
- [x] Los principales casos límite están considerados.
- [x] Las restricciones conocidas están documentadas.
- [x] Las suposiciones importantes están documentadas.
- [x] No existen elementos `[NEEDS CLARIFICATION]` marcados como bloqueantes.
- [x] Las aclaraciones resueltas fueron incorporadas a los requisitos correspondientes.
- [x] Las decisiones obtenidas durante la aclaración quedaron documentadas.
- [x] Los requisitos son verificables.
- [x] No se han introducido decisiones técnicas innecesarias.

---

# 17. Estado de aprobación

**Estado actual:**

APPROVED

Estados permitidos:

DRAFT
→ IN_REVIEW
→ APPROVED
→ SUPERSEDED

## Aprobación

La transición a `APPROVED` requiere aprobación humana explícita.

**Aprobado por:**

Usuario, mediante respuesta "Aprobado" en conversación del 2026-09-30.

**Fecha de aprobación:**

2026-09-30

La implementación no podrá comenzar mientras la especificación no se encuentre
en estado:

APPROVED
