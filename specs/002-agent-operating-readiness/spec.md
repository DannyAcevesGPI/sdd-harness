# Especificación: Preparación operativa para agentes, subagentes y hooks

**ID:** SPEC-002
**Estado:** APPROVED
**Versión:** 0.1.0
**Fecha:** 2026-09-30

---

# 1. Resumen

## 1.1 Descripción

Esta feature prepara el Harness para operar con instrucciones de agente más
compactas, delegación mediante subagentes y puntos de extensión mediante hooks,
sin debilitar las reglas SDD ya aprobadas.

## 1.2 Problema

`AGENTS.md` concentra actualmente instrucciones extensas del Harness. Esto
dificulta su uso como contexto operativo ligero y todavía no define cómo un
agente principal debe delegar trabajo a subagentes ni cómo deben incorporarse
hooks sin romper trazabilidad, gates o autoridad humana.

## 1.3 Objetivo

Reducir la carga operativa de `AGENTS.md` y definir las condiciones observables
que permitan preparar el repositorio para subagentes y hooks, manteniendo la
Constitución como fuente normativa superior y preservando el estado estable del
Harness.

---

# 2. Alcance

## 2.1 Incluido

Esta especificación incluye:

- Compactar `AGENTS.md` por debajo del límite acordado de slots.
- Mantener en `AGENTS.md` una ruta clara hacia la Constitución, standards,
  commands y artefactos SDD.
- Definir expectativas funcionales para uso de subagentes dentro del Harness.
- Definir expectativas funcionales para incorporación futura de hooks.
- Preservar los gates de aprobación humana y la regla de no implementar sin
  artefactos aprobados.

## 2.2 Fuera de alcance

Esta especificación NO incluye:

- Implementar código de aplicación en `src/`.
- Modificar la feature `001-audit-task-management`.
- Instalar dependencias, configurar servicios externos o ejecutar hooks reales.
- Crear una plataforma automática de workflow SDD.
- Cambiar la Constitución sin una decisión humana explícita y una evaluación de
  propagación.

Los elementos fuera de alcance no deberán implementarse como parte de esta
especificación.

---

# 3. Actores

## ACT-001 — Agente principal

**Descripción:**

Agente que inicia trabajo en el repositorio y debe respetar el Harness.

**Responsabilidades o necesidades:**

- Entender rápidamente el bootstrap obligatorio.
- Identificar cuándo debe leer artefactos SDD completos.
- Coordinar subagentes sin perder autoridad, trazabilidad ni gates.

## ACT-002 — Subagente

**Descripción:**

Agente delegado para realizar inspecciones o trabajos acotados.

**Responsabilidades o necesidades:**

- Recibir alcance explícito y artefactos relevantes.
- No saltarse las restricciones SDD por estar delegado.
- Devolver evidencia útil al agente principal.

## ACT-003 — Mantenedor humano

**Descripción:**

Persona con autoridad para aprobar artefactos y decisiones del Harness.

**Responsabilidades o necesidades:**

- Revisar y aprobar cambios de SPEC, PLAN y TASKS cuando aplique.
- Entender qué cambia en el modo de operación de agentes.

---

# 4. Requisitos funcionales

## FR-001 — Compactar instrucciones operativas

**Descripción:**

El Harness deberá disponer de un `AGENTS.md` compacto que conserve las reglas
operativas mínimas necesarias y remita a las fuentes normativas completas.

**Prioridad:** MUST

**Origen:**

Solicitud humana: "bajar el AGENTS.md a menos de 200 slots".

---

## FR-002 — Preservar bootstrap y ruteo SDD

**Descripción:**

El `AGENTS.md` compacto deberá seguir obligando al agente a leer la Constitución,
determinar feature, fase, artefactos, command y standards antes de trabajo
significativo.

**Prioridad:** MUST

**Origen:**

Constitución y regla fundamental del Harness.

---

## FR-003 — Preparar uso de subagentes

**Descripción:**

El Harness deberá definir cómo el agente principal puede usar subagentes sin
delegar aprobación humana, romper trazabilidad ni omitir lectura de fuentes
autoritativas.

**Prioridad:** MUST

**Origen:**

Solicitud humana: "Preparar para usar subagentes".

---

## FR-004 — Preparar uso de hooks

**Descripción:**

El Harness deberá definir criterios para incorporar hooks como apoyo operativo,
sin convertirlos en autoridad de aprobación ni sustituto de validación SDD.

**Prioridad:** MUST

**Origen:**

Solicitud humana: "Preparar para hooks".

---

# 5. Requisitos no funcionales

## NFR-001 — Mantenibilidad documental

**Categoría:** Mantenibilidad

**Descripción:**

Las instrucciones compactas deberán reducir duplicación con la Constitución y los
commands, de forma que los cambios futuros tengan menor riesgo de divergencia.

**Métrica o condición:**

Revisión textual demuestra que `AGENTS.md` resume o referencia reglas, pero no
redefine silenciosamente fuentes superiores.

---

## NFR-002 — Compatibilidad con Harness estable

**Categoría:** Compatibilidad

**Descripción:**

Los cambios deberán preservar el estado estable 1.0.0 salvo que el plan aprobado
determine explícitamente una nueva versión o estado.

**Métrica o condición:**

La validación no identifica contradicciones con `handoff.md` sección 44,
Constitución, standards o commands.

---

# 6. Requisitos de seguridad

## SEC-001 — Hooks sin exposición de secretos

**Descripción:**

La preparación para hooks deberá mantener la prohibición de almacenar, imprimir o
propagar secretos en documentación, comandos, logs o evidencia.

**Riesgo mitigado:**

Exposición accidental de credenciales o tokens al automatizar verificaciones.

---

## SEC-002 — Delegación sin elevación de autoridad

**Descripción:**

La preparación para subagentes deberá impedir que un subagente apruebe artefactos
o tome decisiones humanas requeridas por el Harness.

**Riesgo mitigado:**

Bypass de gates de aprobación y pérdida de control humano.

---

# 7. Reglas de negocio

## BR-001 — AGENTS.md no sustituye fuentes superiores

**Regla:**

`AGENTS.md` podrá resumir instrucciones, pero no deberá contradecir ni reemplazar
Constitución, standards, commands o artefactos aprobados.

**Ejemplo:**

Si `AGENTS.md` dice "leer la Constitución", la regla completa sigue viviendo en
`.spec/constitution.md`.

---

## BR-002 — Delegación mantiene responsabilidad principal

**Regla:**

El agente principal conserva responsabilidad de integrar hallazgos, verificar
trazabilidad y respetar gates, aun cuando use subagentes.

**Ejemplo:**

Un subagente puede inspeccionar archivos, pero no puede declarar una SPEC
`APPROVED`.

---

# 8. Criterios de aceptación

## AC-001 — Límite de slots verificable

**Relacionado con:** FR-001

### Given

Existe la decisión humana de que "slot" significa línea para `AGENTS.md`.

### When

Se revisa el `AGENTS.md` actualizado.

### Then

El documento queda por debajo de 200 líneas.

---

## AC-002 — Bootstrap preservado

**Relacionado con:** FR-002

### Given

Un agente inicia trabajo significativo en el repositorio.

### When

Lee el `AGENTS.md` actualizado.

### Then

Encuentra instrucciones explícitas para leer `.spec/constitution.md`, detectar
feature/fase/artefactos/command/standards y respetar el mutation boundary.

---

## AC-003 — Subagentes acotados

**Relacionado con:** FR-003, SEC-002

### Given

El agente principal delega trabajo a un subagente.

### When

La delegación se realiza bajo las instrucciones actualizadas.

### Then

El alcance, fuentes autorizadas, límites de mutación y evidencia esperada quedan
definidos sin transferir aprobaciones humanas al subagente.

---

## AC-004 — Hooks acotados

**Relacionado con:** FR-004, SEC-001

### Given

El Harness se prepara para hooks.

### When

Se revisan las instrucciones actualizadas.

### Then

Los hooks quedan descritos como apoyo verificable y no como sustituto de SPEC,
PLAN, TASKS, validación, aprobación humana o revisión de seguridad.

---

## AC-005 — No contradicción normativa

**Relacionado con:** NFR-001, NFR-002, BR-001

### Given

Se comparan las instrucciones actualizadas contra las fuentes superiores.

### When

Se ejecuta la validación documental.

### Then

No se identifican contradicciones bloqueantes ni pérdida de reglas obligatorias.

---

# 9. Casos límite y escenarios de error

## EDGE-001 — Límite de líneas no verificable

**Condición:**

El límite "menos de 200 slots" vuelve a usarse sin conservar la definición
operacional aprobada.

**Comportamiento esperado:**

La SPEC no avanza a PLAN hasta recuperar una definición medible.

---

## EDGE-002 — Hook con resultado no determinista

**Condición:**

Un hook propuesto produce resultados dependientes de red, tiempo o estado externo.

**Comportamiento esperado:**

El PLAN deberá clasificarlo como riesgo o excluirlo de gates obligatorios hasta
que pueda controlarse o documentarse adecuadamente.

---

# 10. Datos involucrados

## Instrucciones de agente

Información requerida:

- Reglas mínimas de bootstrap.
- Ruta a fuentes normativas completas.
- Límites de delegación.
- Límites de hooks.

Reglas relevantes:

- No contradicción con fuentes superiores.
- Trazabilidad de cambios documentales.

---

# 11. Dependencias

La funcionalidad depende de:

- `.spec/constitution.md`
- `.spec/standards/`
- `.spec/commands/`
- `AGENTS.md`
- `handoff.md`
- Decisión humana sobre la definición de "slot".

---

# 12. Restricciones

Restricciones conocidas:

- No modificar código de aplicación durante `/specify`, `/plan` o `/tasks`.
- No autoaprobar SPEC, PLAN o TASKS.
- No tratar subagentes ni hooks como autoridad humana.
- No degradar la trazabilidad del Harness estable.

---

# 13. Suposiciones

## ASM-001

La preparación para subagentes y hooks puede resolverse inicialmente mediante
instrucciones y artefactos del Harness, sin instalar software externo.

## ASM-002

La compactación de `AGENTS.md` deberá priorizar referencias a fuentes
autoritativas sobre duplicación extensa de contenido.

---

# 14. Preguntas abiertas y necesidades de aclaración

## Q-001 — Definición de slot

**Estado:** [CLARIFIED]

**Pregunta:**

¿Qué significa "slot" para el límite de `AGENTS.md`: línea, sección, bloque de
instrucción, token aproximado u otra unidad?

**Contexto:**

El `AGENTS.md` actual tiene 935 líneas y 26 secciones numeradas. Sin una unidad
medible, no se puede verificar AC-001.

**Impacto:**

Afecta FR-001 y AC-001, y podría cambiar el grado de compactación permitido.

**Bloqueante:** YES

**Opciones conocidas:**

1. Menos de 200 líneas.
2. Menos de 200 bloques/instrucciones operativas.
3. Menos de 200 tokens aproximados.

**Respuesta:**

El límite de "menos de 200 slots" significa menos de 200 líneas en `AGENTS.md`.

**Resuelto por:**

Decisión humana del usuario en conversación del 2026-09-30.

**Fecha de resolución:**

2026-09-30

---

## Q-002 — Alcance inicial de hooks

**Estado:** [NEEDS CLARIFICATION]

**Pregunta:**

¿La preparación para hooks debe limitarse a instrucciones/documentación o debe
crear archivos de configuración concretos para una herramienta específica?

**Contexto:**

La solicitud pide "Preparar para hooks", pero no identifica herramienta ni tipo
de hook.

**Impacto:**

Afecta el PLAN y las TASKS; no impide definir el comportamiento general.

**Bloqueante:** NO

**Opciones conocidas:**

1. Solo reglas e instrucciones del Harness.
2. Estructura documental para hooks futuros.
3. Configuración concreta de una herramienta por definir.

**Respuesta:**

PENDIENTE

**Resuelto por:**

PENDIENTE

**Fecha de resolución:**

PENDIENTE

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

Resolver una pregunta no sustituye la actualización de la especificación.

La respuesta deberá reflejarse en las secciones correspondientes de la SPEC.

---

# 15. Matriz inicial de trazabilidad

| Requisito | Criterios de aceptación | Prioridad |
|-----------|-------------------------|-----------|
| FR-001 | AC-001 | MUST |
| FR-002 | AC-002, AC-005 | MUST |
| FR-003 | AC-003 | MUST |
| FR-004 | AC-004 | MUST |
| NFR-001 | AC-005 | MUST |
| NFR-002 | AC-005 | MUST |
| SEC-001 | AC-004 | MUST |
| SEC-002 | AC-003 | MUST |
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

Los agentes pueden preparar y revisar la SPEC, pero no podrán autoaprobarla.

**Aprobado por:**

Usuario, mediante respuesta "De acuerdo" en conversación del 2026-09-30.

**Fecha de aprobación:**

2026-09-30

La implementación no podrá comenzar mientras la especificación no se encuentre
en estado:

APPROVED
