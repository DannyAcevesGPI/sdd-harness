# Tareas: [Nombre de la funcionalidad]

**ID:** TASKS-[XXX]  
**SPEC relacionada:** SPEC-[XXX]  
**PLAN relacionado:** PLAN-[XXX]  
**Estado:** DRAFT  
**Versión:** 0.1.0  
**Fecha:** [YYYY-MM-DD]

---

# 1. Precondiciones

Antes de generar estas tareas deberá verificarse:

- [ ] Existe una SPEC asociada.
- [ ] La SPEC se encuentra en estado `APPROVED`.
- [ ] Existe un PLAN asociado.
- [ ] El PLAN se encuentra en estado `APPROVED`.
- [ ] No existen `[NEEDS CLARIFICATION]` bloqueantes.
- [ ] Los requisitos MUST tienen cobertura técnica.
- [ ] El orden general de implementación está definido.

Si alguna precondición obligatoria no se cumple:

**TASK GENERATION STATUS: BLOCKED**

No deberán generarse tareas basadas en decisiones todavía
no resueltas.

---

# 2. Objetivo

Este documento divide el plan técnico aprobado en unidades
de trabajo pequeñas, trazables, verificables y ejecutables.

Cada tarea deberá:

- tener un objetivo específico;
- estar relacionada con requisitos o necesidades técnicas;
- identificar su alcance;
- definir dependencias;
- definir criterios de finalización;
- producir evidencia verificable.

---

# 3. Estados de tarea

Estados permitidos:

TODO
→ IN_PROGRESS
→ BLOCKED
→ DONE

Una tarea solamente podrá marcarse como `DONE` cuando cumpla
todos sus criterios de finalización.

`BLOCKED` deberá incluir la razón del bloqueo.

Para corregir un defecto de implementación detectado en validación,
una tarea `DONE` podrá reabrirse a `TODO` mediante el procedimiento de
la sección 17.1 de `/implement`. Deberá vincularse al finding y conservarse
la evidencia anterior. Su ejecución volverá a pasar por `IN_PROGRESS`.

`CANCELLED` es una anotación histórica de un identificador retirado,
no un estado de tarea activa. El retiro deberá seguir la revisión de
TASKS y los approval gates aplicables; no permite omitir trabajo requerido
por SPEC o PLAN ni liberar el identificador para reutilización.

---

# 4. Prioridades

Prioridades permitidas:

P0 — Bloqueante o crítica.
P1 — Alta.
P2 — Normal.
P3 — Baja.

La prioridad no sustituye las dependencias entre tareas.

---

# 5. Convención de identificadores

Las tareas deberán utilizar identificadores únicos:

TASK-001
TASK-002
TASK-003

Las pruebas podrán utilizar:

TEST-001
TEST-002
TEST-003

Las tareas no deberán renumerarse una vez utilizadas como
referencia en otros artefactos.

---

# 6. Tareas

## TASK-001 — [Nombre de la tarea]

**Estado:** TODO  
**Prioridad:** P1

### Objetivo

[Resultado concreto que deberá producir esta tarea.]

### Trazabilidad

**Requisitos:**

- FR-[XXX]
- SEC-[XXX]

**Criterios de aceptación:**

- AC-[XXX]

**Decisiones del plan:**

- DEC-[XXX]

### Dependencias

**Depende de:**

- Ninguna

o:

- TASK-[XXX]

### Alcance permitido

Crear:

- [archivo/módulo]

Modificar:

- [archivo/módulo]

Reutilizar:

- [archivo/módulo]

No modificar:

- [archivo/módulo o área cuando sea relevante]

### Implementación esperada

[Descripción breve del cambio técnico que deberá realizarse.]

Esta sección describe el resultado esperado, no código detallado.

### Pruebas requeridas

- TEST-[XXX] — [Comportamiento]
- TEST-[XXX] — [Comportamiento]

### Validaciones

- [ ] Código implementado.
- [ ] Requisitos asociados cubiertos.
- [ ] Pruebas requeridas implementadas.
- [ ] Pruebas relevantes en PASS.
- [ ] No existen errores de linting relacionados.
- [ ] No existen errores de tipos relacionados.
- [ ] No se modificó alcance no autorizado.

### Evidencia esperada

- Archivos modificados.
- Pruebas ejecutadas.
- Resultado de las pruebas.
- Requisitos satisfechos.

### Definition of Done

La tarea se considera `DONE` cuando:

- [ ] El objetivo fue cumplido.
- [ ] La implementación respeta el PLAN.
- [ ] La implementación respeta la SPEC.
- [ ] Las pruebas requeridas pasan.
- [ ] No existen bloqueos pendientes.
- [ ] La evidencia está disponible.

---

# 7. Tareas técnicas

Una tarea podrá no relacionarse directamente con un requisito
funcional cuando sea necesaria para implementar el plan.

En ese caso deberá indicar explícitamente:

**Tipo:** TECHNICAL

y deberá mantener una justificación trazable hacia el PLAN.

La tarea técnica deberá relacionarse con al menos una fuente
autorizada del PLAN, por ejemplo:

- una decisión `DEC-[XXX]`;
- una necesidad técnica documentada en el PLAN;
- un NFR;
- un SEC;
- infraestructura necesaria documentada en el PLAN.

Además deberá referenciar al menos un requisito o criterio de aceptación
real que soporte, directamente o mediante una cadena explícita del PLAN.
La referencia únicamente a DEC, ADR o infraestructura no sustituye esta
obligación del Artículo IV de la Constitution.

Cuando corresponda, también deberá indicar las tareas que dependen de ella.

Una relación únicamente con otra tarea no será suficiente para
justificar una tarea técnica.

No deberán crearse requisitos funcionales artificiales únicamente
para justificar trabajo técnico.

Ejemplo:

TASK-002 — Crear migración de Task

Tipo: TECHNICAL

Derivada de:

DEC-003

Soporta mediante DEC-003:

FR-001 / AC-001

Necesaria para:

TASK-004
TASK-005

No deberán existir tareas técnicas sin justificación.

---

# 8. Grafo de dependencias

Las dependencias entre tareas deberán ser explícitas.

Ejemplo:

TASK-001
   │
   ▼
TASK-002
   │
   ├─────────┐
   ▼         ▼
TASK-003   TASK-004
   │         │
   └────┬────┘
        ▼
     TASK-005

No deberá iniciarse una tarea si alguna dependencia obligatoria
permanece incompleta.

Se deberán evitar dependencias circulares.

---

# 9. Orden sugerido de ejecución

| Orden | Tarea | Depende de | Estado |
|------:|-------|------------|--------|
| 1 | TASK-001 | — | TODO |
| 2 | TASK-002 | TASK-001 | TODO |
| 3 | TASK-003 | TASK-002 | TODO |
| 4 | TASK-004 | TASK-002 | TODO |
| 5 | TASK-005 | TASK-003, TASK-004 | TODO |

El orden podrá ajustarse mientras se respeten las dependencias
y el PLAN aprobado.

---

# 10. Bloqueos

Si durante la preparación o ejecución de una tarea aparece una
ambigüedad que afecte su correcta implementación deberá utilizarse:

[NEEDS CLARIFICATION]

Ejemplo:

## BLOCK-001

**Tarea:** TASK-004

**Estado:** [NEEDS CLARIFICATION]

**Pregunta:**

[Pregunta.]

**Impacto:**

[Qué parte de la tarea no puede continuar.]

**Bloqueante:** YES

**Origen probable:**

[SPEC | PLAN | TASK | EXTERNAL]

La tarea afectada deberá pasar a:

BLOCKED

No deberá inventarse una decisión para continuar.

Cuando la aclaración sea resuelta:

1. actualizar el artefacto fuente correspondiente;
2. actualizar la tarea si es necesario;
3. registrar la resolución;
4. cambiar la tarea a `TODO` o `IN_PROGRESS`;
5. continuar.

---

# 11. Descubrimientos fuera de alcance

Durante la implementación podrán descubrirse problemas o mejoras
no pertenecientes a la tarea actual.

Deberán registrarse como:

DISCOVERY-[XXX]

Ejemplo:

## DISCOVERY-001

**Detectado durante:** TASK-004

**Descripción:**

[Problema o mejora detectada.]

**Impacto:**

[LOW | MEDIUM | HIGH]

**Acción recomendada:**

[Crear nueva SPEC | Crear tarea futura | Revisar arquitectura]

El descubrimiento no deberá implementarse automáticamente si está
fuera del alcance aprobado.

---

# 12. Matriz de trazabilidad

| Tarea | Requisito | Criterio | Decisión | Prueba |
|-------|-----------|----------|----------|--------|
| TASK-001 | FR-001 | AC-001 | DEC-001 | TEST-001 |
| TASK-002 | FR-001 | AC-002 | DEC-002 | TEST-002 |
| TASK-003 | SEC-001 | AC-003 | DEC-003 | TEST-003 |

Toda tarea deberá tener una justificación trazable.

Todo requisito MUST deberá estar cubierto por al menos una tarea
cuando requiera implementación.

---

# 13. Cambios durante implementación

Si una tarea requiere modificar el PLAN:

STOP

La implementación afectada deberá detenerse.

Después:

1. documentar el motivo;
2. actualizar el PLAN;
3. evaluar el impacto downstream;
4. actualizar únicamente las tareas afectadas cuando sea necesario;
5. si un artefacto previamente aprobado fue modificado,
   recuperar su approval gate;
6. verificar nuevamente las precondiciones aplicables;
7. continuar únicamente cuando los gates requeridos vuelvan a cumplirse.

Si el cambio afecta requisitos:

STOP

Deberá regresarse a la SPEC.

Después:

1. actualizar la SPEC;
2. recuperar la aprobación de la SPEC modificada;
3. evaluar el impacto sobre PLAN;
4. actualizar PLAN solamente cuando resulte afectado;
5. actualizar TASKS solamente cuando resulte afectado;
6. recuperar los approval gates de todo artefacto aprobado
   que haya sido modificado;
7. revisar si evidencia o validación previa quedó invalidada;
8. continuar únicamente cuando los gates aplicables vuelvan
   a cumplirse.


---

# 14. Criterios para comenzar implementación

La implementación podrá comenzar solamente cuando:

- [ ] La SPEC está `APPROVED`.
- [ ] El PLAN está `APPROVED`.
- [ ] Las tareas están definidas.
- [ ] Todos los requisitos MUST tienen tareas asociadas.
- [ ] Las dependencias entre tareas están identificadas.
- [ ] Las pruebas requeridas están identificadas.
- [ ] Las tareas tienen alcance definido.
- [ ] No existen tareas huérfanas.
- [ ] No existen dependencias circulares.
- [ ] No existen `[NEEDS CLARIFICATION]` bloqueantes.
- [ ] No existen bloqueos conocidos que impidan comenzar.

---

# 15. Estado del documento

Estados permitidos:

DRAFT
→ IN_REVIEW
→ APPROVED
→ IN_PROGRESS
→ COMPLETED

Transiciones de ejecución:

`APPROVED → IN_PROGRESS`

El documento deberá pasar a `IN_PROGRESS` cuando comience
la ejecución de la primera tarea requerida.

`IN_PROGRESS → COMPLETED`

El documento solamente podrá pasar a `COMPLETED` cuando:

- todas las tareas requeridas se encuentren en `DONE`;
- no exista ninguna tarea requerida en `BLOCKED`;
- no exista ninguna tarea requerida pendiente de ejecución;
- la evidencia requerida por las tareas esté disponible.

`COMPLETED` no significa que la feature esté validada.

La feature solamente podrá alcanzar `VALIDATED` mediante
el proceso de validación final.

`COMPLETED → IN_PROGRESS`

Esta transición permite corregir defectos de implementación encontrados
en validación mediante el procedimiento de la sección 17.1 de `/implement`.
Deberán reabrirse las tareas afectadas, conservarse la evidencia previa y
repetirse las verificaciones afectadas antes de cerrar nuevamente TASKS
y repetir `/validate`.

La actualización de estados y evidencia sin cambiar el trabajo autorizado
no requiere una nueva aprobación. Si cambia dicho trabajo, deberán
recuperarse los approval gates aplicables antes de ejecutar la corrección.

**Estado actual:**

DRAFT

La ejecución inicial no deberá comenzar mientras este documento
no se encuentre en estado `APPROVED`. Una ejecución ya iniciada o
reabierta podrá continuar en `IN_PROGRESS` únicamente si cumple las
precondiciones y los approval gates aplicables de `/implement`.

## Aprobación

La transición a `APPROVED` requiere aprobación humana explícita.

Los agentes pueden preparar y revisar TASKS, pero no podrán
autoaprobar el documento.

**Aprobado por:**

[PENDIENTE]

**Fecha de aprobación:**

[PENDIENTE]
