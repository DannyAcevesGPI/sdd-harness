# Especificación: Estado reconstruible sin chat

**ID:** SPEC-007  
**Estado:** APPROVED  
**Versión:** 0.1.0  
**Fecha:** 2026-09-30

---

# 1. Resumen

## 1.1 Descripción

Una sesión nueva debe poder reconstruir el estado operativo y los gates SDD a
partir de los artefactos del repositorio, sin consultar conversaciones previas.

## 1.2 Problema

El Harness guarda SPEC, PLAN, TASKS y evidencia, pero ciertas aprobaciones se
atribuyen solo a "esta conversación". Además, el estado resumido puede quedar
desactualizado respecto de los artefactos. Una sesión nueva no puede distinguir
con certeza qué se aprobó, qué sigue pendiente y qué evidencia respalda cada
transición.

## 1.3 Objetivo

Hacer que las decisiones, aprobaciones y estado necesarios para continuar el
trabajo sean recuperables, verificables y enlazados desde archivos del repo. El
chat podrá transportar decisiones humanas, pero no será la única fuente para
reconstruirlas en sesiones posteriores.

---

# 2. Alcance

## 2.1 Incluido

- Registro persistente de decisiones y aprobaciones relevantes para gates SDD.
- Reconstrucción de fase, estado, bloqueos, siguiente acción y evidencia desde el
  repositorio.
- Reglas para detectar información ausente, contradictoria u obsoleta.
- Comprobación repetible de reconstrucción en una sesión sin contexto del chat.
- Tratamiento explícito y honesto de los registros históricos.

## 2.2 Fuera de alcance

- Eliminar la aprobación humana o modificar su autoridad.
- Usar el chat como registro permanente de decisiones.
- Crear un servicio externo de almacenamiento o exigir firmas criptográficas.
- Reabrir auditorías cerradas sin evidencia nueva.
- Cambiar el comportamiento de features ya validadas, salvo la documentación de
  su procedencia y estado.

---

# 3. Actores

## ACT-001 — Responsable humano

Emite decisiones y aprobaciones explícitas; puede verificar qué alcance quedó
registrado y corregir discrepancias.

## ACT-002 — Agente de una sesión nueva

Consulta el repositorio y determina qué trabajo está autorizado, pendiente o
bloqueado sin acceso a conversaciones anteriores.

---

# 4. Requisitos funcionales

## FR-001 — Aprobaciones persistentes

**Descripción:** Toda aprobación nueva de SPEC, PLAN o TASKS deberá dejar un
registro persistente que identifique quién aprobó, cuándo, qué artefacto y
versión/contenido aprobó, y el alcance de la decisión. Una mención genérica a
"esta conversación" no será evidencia suficiente por sí sola.

**Prioridad:** MUST  
**Origen:** Necesidad del usuario de independizar el estado del chat.

## FR-002 — Decisiones recuperables

**Descripción:** Toda decisión humana que afecte alcance, comportamiento,
prioridades, seguridad o un gate deberá conservar su resultado y vínculo al
artefacto afectado. El registro deberá permitir distinguir la decisión vigente
de una reemplazada, revocada o pendiente.

**Prioridad:** MUST  
**Origen:** Precedencia de decisiones humanas y reconstrucción entre sesiones.

## FR-003 — Reconstrucción operativa

**Descripción:** Una sesión nueva deberá poder identificar desde el repo la
feature activa, fase y estados de sus artefactos, aprobaciones necesarias,
bloqueos, siguiente acción autorizada y rutas de evidencia; también deberá
poder localizar las features validadas sin depender de un resumen incompleto.

**Prioridad:** MUST  
**Origen:** Petición explícita del usuario.

## FR-004 — Discrepancias visibles

**Descripción:** Si faltan registros, hay contradicciones entre estado resumido
y artefactos, o el contenido aprobado cambió, el Harness deberá señalar la
discrepancia y no presentar la autorización como verificada hasta resolverla en
el nivel dueño correspondiente.

**Prioridad:** MUST  
**Origen:** Evitar continuar trabajo basándose en estado implícito u obsoleto.

## FR-005 — Evidencia enlazada, no duplicada

**Descripción:** El estado vivo deberá permanecer compacto y enlazar los
registros y evidencias dedicados. La reconstrucción no deberá requerir leer todo
el historial de auditorías ni releer el chat.

**Prioridad:** MUST  
**Origen:** Modelo de `handoff.md` y optimización de contexto ya aprobados.

## FR-006 — Tratamiento del legado

**Descripción:** Las aprobaciones de SPEC-001 a SPEC-006 cuya prueba depende del
chat se identificarán como legado no verificable. No se inventarán respaldos ni
se alterará retrospectivamente el contenido autorizado. El registro completo
será exigible para decisiones y aprobaciones nuevas desde esta feature.

**Prioridad:** MUST  
**Origen:** Aprobaciones históricas referidas a la conversación.

---

# 5. Requisitos no funcionales

## NFR-001 — Reconstrucción acotada

**Categoría:** Mantenibilidad  
**Descripción:** Una sesión nueva podrá comenzar con los índices y artefactos
pertinentes, siguiendo vínculos bajo demanda; el estado vivo no se convertirá
en un duplicado del historial.  
**Métrica o condición:** El procedimiento de reconstrucción está documentado y
se ejecuta sin leer el chat ni todos los archivos de evidencia.

## NFR-002 — Registros revisables

**Categoría:** Observabilidad  
**Descripción:** Los registros y enlaces de estado serán legibles y auditables
en el repositorio.  
**Métrica o condición:** Un revisor puede comprobar para cada gate nuevo su
artefacto, aprobación y estado vigente desde archivos versionables.

---

# 6. Requisitos de seguridad

## SEC-001 — No registrar secretos

**Descripción:** Los registros de decisión, handoff y evidencia no deberán
incluir secretos, credenciales ni datos sensibles innecesarios.  
**Riesgo mitigado:** Exposición de información por documentación versionada.

---

# 7. Reglas de negocio

## BR-001 — Autoridad humana intacta

Un registro documenta una aprobación humana explícita; no la crea. Ningún
agente podrá autoaprobar SPEC, PLAN o TASKS por escribir o actualizar un archivo.

## BR-002 — Sin inferencias de aprobación

Un commit, un estado `APPROVED` sin procedencia suficiente o una validación
posterior no equivalen por sí solos a una aprobación humana verificable.

---

# 8. Criterios de aceptación

## AC-001 — Gate nuevo reconstruible

**Relacionado con:** FR-001, FR-002, BR-001

**Given** una aprobación humana explícita de un artefacto SDD nuevo, **when**
una sesión posterior examina solo el repo, **then** identifica la decisión,
persona/rol, fecha, artefacto y contenido aprobado, sin consultar el chat.

## AC-002 — Continuación sin chat

**Relacionado con:** FR-003, FR-005, NFR-001

**Given** una sesión nueva sin historial conversacional, **when** sigue el
bootstrap documentado, **then** identifica feature activa, fase, gates,
bloqueos, siguiente acción y evidencia por enlaces desde el repo.

## AC-003 — Cambio posterior a aprobación

**Relacionado con:** FR-004, BR-002

**Given** un artefacto aprobado cuyo contenido autorizado cambia, **when** se
reconstruye el estado, **then** la aprobación anterior no se aplica
silenciosamente al contenido nuevo y se indica qué gate debe recuperarse.

## AC-004 — Estado incompleto o contradictorio

**Relacionado con:** FR-003, FR-004

**Given** un resumen desactualizado o evidencia de aprobación ausente, **when**
una sesión nueva reconstruye el estado, **then** la discrepancia queda visible y
no se afirma falsamente que el siguiente paso está autorizado.

## AC-005 — Legado honesto

**Relacionado con:** FR-006

**Given** una aprobación de SPEC-001 a SPEC-006 cuyo respaldo depende del chat,
**when** se consulta su estado, **then** se identifica como legado no verificable
sin fabricar aprobación histórica ni presentarla como evidencia completa.

## AC-006 — Registros seguros

**Relacionado con:** SEC-001

**Given** registros y evidencia de decisiones, **when** se revisan para
versionarlos, **then** no contienen secretos ni datos sensibles innecesarios.

---

# 9. Casos límite y escenarios de error

## EDGE-001 — Aprobación ambigua

Una frase de aprobación sin artefacto o alcance inequívoco no habilita el gate;
se solicita aclaración y se registra el resultado.

## EDGE-002 — Decisiones en conflicto

Si dos registros vigentes se contradicen, se detiene la transición afectada,
se expone el conflicto y se resuelve conforme a la precedencia del Harness.

## EDGE-003 — Handoff atrasado

Un resumen desactualizado no oculta el estado de los artefactos; la sesión
señala la diferencia antes de continuar.

---

# 10. Datos involucrados

## Decisión o aprobación

Información requerida: decisión explícita, actor, fecha, artefacto y contenido
al que aplica, estado vigente y vínculo a su contexto/evidencia disponible.

## Estado operativo

Información requerida: feature, fase, estados, bloqueos, próximo paso y rutas
de evidencia. Los detalles históricos permanecen en artefactos dedicados.

---

# 11. Dependencias

- Flujo SDD, precedencia y gates de `.spec/constitution.md`.
- Índice documental y `handoff.md` existentes.
- Artefactos de `specs/001` a `specs/006` para el tratamiento de legado.

---

# 12. Restricciones

- Respetar la aprobación humana explícita y los límites de mutación por fase.
- Mantener `AGENTS.md` compacto y `handoff.md` como estado vivo, no historial.
- No convertir evidencia inferida de Git en una aprobación humana.

---

# 13. Suposiciones

Ninguna suposición adicional necesaria.

---

# 14. Preguntas abiertas y necesidades de aclaración

## Q-001 — Política para aprobaciones históricas

**Estado:** [CLARIFIED]  
**Pregunta:** ¿Cómo deben tratarse las aprobaciones de SPEC-001 a SPEC-006
cuya procedencia completa depende del chat?  
**Contexto:** El repositorio contiene estados aprobados y validaciones, pero
algunos campos de aprobación solo indican "usuario en esta conversación".  
**Impacto:** FR-006 y AC-005; determina la política de procedencia del legado.  
**Bloqueante:** YES

**Opciones conocidas:**

1. Marcar el legado como no verificable y exigir registro completo en adelante.
2. Reconstruir únicamente lo respaldado por archivos y Git, marcando vacíos.
3. Solicitar nueva aprobación humana de cada artefacto histórico.

**Respuesta:** Registrar el legado como no verificable cuando la prueba dependa
del chat y exigir registro completo desde ahora.  
**Resuelto por:** Usuario  
**Fecha de resolución:** 2026-09-30

---

# 15. Matriz inicial de trazabilidad

| Requisito | Criterios de aceptación | Prioridad |
|-----------|-------------------------|-----------|
| FR-001 | AC-001 | MUST |
| FR-002 | AC-001 | MUST |
| FR-003 | AC-002, AC-004 | MUST |
| FR-004 | AC-003, AC-004 | MUST |
| FR-005 | AC-002 | MUST |
| FR-006 | AC-005 | MUST |
| NFR-001 | AC-002 | MUST |
| NFR-002 | AC-001 | MUST |
| SEC-001 | AC-006 | MUST |
| BR-001 | AC-001 | MUST |
| BR-002 | AC-003 | MUST |

---

# 16. Criterios para avanzar a planificación

- [x] Problema, objetivo, alcance, actores y fuera de alcance definidos.
- [x] Requisitos MUST y seguridad tienen criterios de aceptación.
- [x] Casos límite y trazabilidad inicial documentados.
- [x] Q-001 resuelta e incorporada a FR-006 y AC-005.
- [x] Revisión y aprobación humana explícita de la SPEC.

---

# 17. Estado de aprobación

**Estado actual:** APPROVED  
**Resultado:** READY FOR PLANNING  
**Aprobado por:** Usuario responsable del proyecto  
**Fecha de aprobación:** 2026-09-30  
**Decisión explícita:** "Aprobado" en respuesta a la solicitud de aprobación
de SPEC-007 para preparar el PLAN.  
**Alcance aprobado:** Contenido de SPEC-007 versión 0.1.0, incluida la política
de legado no verificable de Q-001.

La aprobación de SPEC no autoriza implementación antes de aprobar PLAN y TASKS.
