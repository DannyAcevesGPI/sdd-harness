# Especificación: Gestión de tareas para AUDIT-08

**ID:** SPEC-001  
**Estado:** APPROVED  
**Versión:** 0.1.0  
**Fecha:** 2026-09-24

# 1. Resumen

## 1.1 Descripción

Feature de prueba propuesta para recorrer el Harness con implementación,
pruebas y evidencia reales: crear, listar y completar tareas propias.

## 1.2 Problema

AUDIT-07 verificó consistencia documental. Falta demostrar que una feature
puede recorrer los commands, approval gates y validación de forma ejecutable.

## 1.3 Objetivo

Producir una muestra pequeña que permita verificar trazabilidad funcional,
seguridad, errores, pruebas y cierre de TASKS antes de validar la feature.

**Origen:** solicitud humana «Sigamos con el AUDIT-08» y handoff §34.
La selección de esta feature y sus reglas fueron propuestas por el agente
y confirmadas por el usuario en Q-001. Esta aprobación corresponde al
ejercicio de auditoría. La implementación aún requiere PLAN y TASKS aprobados.

# 2. Alcance

## 2.1 Incluido — confirmado en Q-001

- Crear tareas con título y propietario.
- Listar las tareas propias, pendientes y completadas, en orden de creación.
- Completar una tarea propia sin afectar otras tareas.
- Rechazar entradas inválidas y operaciones sin identidad o sin permiso.
- Utilizar actores y datos sintéticos durante el ejercicio.

## 2.2 Fuera de alcance — confirmado en Q-001

- Interfaz web, servidor público, despliegue e integraciones externas.
- Registro de usuarios, contraseñas, sesiones o proveedor de autenticación real.
- Compartir, editar, eliminar, reasignar o reabrir tareas de la aplicación.
- Persistencia entre ejecuciones y ejecución concurrente.

La reapertura de TASKS del Harness es un proceso de auditoría distinto de
reabrir una tarea de esta aplicación.

# 3. Actores

## ACT-001 — Usuario identificado del ejercicio

Identidad sintética estable proporcionada por el entorno de prueba confiable.
Puede crear, listar y completar exclusivamente sus propias tareas.

## ACT-002 — Solicitante sin identidad

No puede ejecutar ninguna de las tres operaciones.

# 4. Requisitos funcionales

Los requisitos y reglas fueron confirmados mediante Q-001.
**Origen común:** muestra representativa aprobada para AUDIT-08.

## FR-001 — Crear tarea

**Prioridad:** MUST.
El sistema deberá crear una tarea pendiente con identificador único dentro
del ejercicio, título válido y propietario igual al actor identificado.
La tarea deberá estar disponible en operaciones posteriores del ejercicio.

## FR-002 — Listar tareas propias

**Prioridad:** MUST.
El sistema deberá devolver exclusivamente las tareas del actor identificado,
con identificador, título y estado, en orden de creación. Sin tareas propias,
deberá devolver una colección vacía.

## FR-003 — Completar tarea propia

**Prioridad:** MUST.
El propietario podrá completar una tarea pendiente. Completarla nuevamente
deberá mantenerla completada sin crear tareas ni producir un error.

# 5. Requisitos no funcionales

## NFR-001 — Ejercicio reproducible sin servicios externos

**Prioridad:** MUST. **Categoría:** Verificabilidad.
Las operaciones y su verificación deberán poder ejecutarse localmente con
datos sintéticos, sin credenciales ni servicios externos en ejecución.
**Condición verificable:** ejecutar dos veces la verificación desde un estado
vacío y obtener los mismos resultados de comportamiento; los valores exactos
de identificadores no necesitan coincidir entre ejecuciones.

# 6. Requisitos de seguridad

## SEC-001 — Identidad obligatoria

**Prioridad:** MUST.
Crear, listar o completar sin identidad válida deberá rechazarse sin devolver
datos de tareas ni modificar el estado. La identidad será un identificador
textual no vacío ni compuesto únicamente por espacios; no podrá elegirse un
propietario distinto al actor durante la creación.
**Riesgo mitigado:** acceso anónimo y suplantación del propietario en la creación.
El PLAN deberá definir el límite confiable del ejercicio; no se afirmará
autenticación de producción a partir de identidades de prueba.

## SEC-002 — Aislamiento entre propietarios

**Prioridad:** MUST.
Un actor no deberá ver tareas ajenas ni completarlas. Intentar completar una
tarea ajena o inexistente deberá producir el mismo resultado observable de
tarea no disponible, sin exponer su título, propietario o estado y sin mutación.
**Riesgo mitigado:** acceso horizontal y revelación de existencia de tareas ajenas.

# 7. Reglas de negocio

## BR-001 — Título válido

**Prioridad:** MUST.
El título deberá ser texto y contener al menos un carácter distinto de espacio.
Se eliminarán espacios exteriores antes de guardarlo. Títulos iguales estarán
permitidos y producirán tareas distintas. Un título inválido no creará tareas.

## BR-002 — Estados

**Prioridad:** MUST.
Estados funcionales: PENDING y COMPLETED. La transición permitida es
PENDING → COMPLETED; repetir la finalización conserva COMPLETED.

## BR-003 — Propiedad estable

**Prioridad:** MUST.
El propietario queda determinado por el actor de creación y no cambia.

# 8. Criterios de aceptación

## AC-001 — Creación válida y títulos repetidos

**Relacionado con:** FR-001, BR-001, BR-002, BR-003.
**Given:** un actor A identificado y un ejercicio vacío.
**When:** crea dos tareas con título `  Revisar informe  `.
**Then:** ambas pertenecen a A, tienen título `Revisar informe`, estado PENDING
e identificadores distintos; ambas pueden consultarse después.

## AC-002 — Título inválido

**Relacionado con:** FR-001, BR-001.
**Given:** un actor identificado y un conjunto de tareas existente.
**When:** intenta crear con título vacío, solo espacios o un valor no textual.
**Then:** cada intento se rechaza por entrada inválida y el conjunto permanece igual.

## AC-003 — Listado propio y orden

**Relacionado con:** FR-002, SEC-002.
**Given:** A y B tienen tareas intercaladas por orden de creación.
**When:** A lista sus tareas.
**Then:** recibe únicamente las propias, en orden de creación, con identificador,
título y estado; las completadas también aparecen.

## AC-004 — Listado vacío

**Relacionado con:** FR-002, SEC-002.
**Given:** A no tiene tareas y B sí.
**When:** A lista sus tareas.
**Then:** recibe una colección vacía.

## AC-005 — Finalización e idempotencia

**Relacionado con:** FR-003, BR-002, BR-003.
**Given:** A tiene dos tareas pendientes.
**When:** completa una y repite la misma operación.
**Then:** ambas operaciones son satisfactorias; la tarea elegida queda COMPLETED,
la otra permanece PENDING y no cambian títulos, propietarios ni cantidad de tareas.

## AC-006 — Operaciones sin identidad

**Relacionado con:** SEC-001.
**Given:** tareas existentes y una identidad ausente, vacía, solo espacios o no textual.
**When:** intenta crear con título válido, listar o completar una tarea existente.
**Then:** cada operación se rechaza por falta de identidad válida, sin revelar
datos de tareas ni alterar el estado.

## AC-007 — Finalización ajena o inexistente

**Relacionado con:** FR-003, SEC-002.
**Given:** una tarea de B y un actor A identificado.
**When:** A intenta completarla y después intenta completar un identificador inexistente.
**Then:** obtiene el mismo resultado de tarea no disponible en ambos casos,
sin datos de la tarea de B y sin cambios de estado.

## AC-008 — Propietario derivado del actor

**Relacionado con:** FR-001, SEC-001, BR-003.
**Given:** A es la identidad confiable de la operación.
**When:** crea una tarea mediante el contrato público definido por el PLAN.
**Then:** la tarea pertenece a A; el contrato no permite asignarla a B mediante
datos de creación. B no la ve en su listado.

## AC-009 — Repetibilidad local

**Relacionado con:** NFR-001.
**Given:** un entorno local con los prerrequisitos documentados en el PLAN.
**When:** se ejecuta dos veces la verificación de AC-001 a AC-008, comenzando cada
ejecución con datos sintéticos y estado vacío, sin servicios externos ni credenciales.
**Then:** ambas ejecuciones producen resultados satisfactorios para esos criterios.

# 9. Casos límite y escenarios de error

| ID | Condición | Comportamiento esperado |
|---|---|---|
| EDGE-001 | Título inválido | Rechazo sin crear ni modificar tareas; AC-002 |
| EDGE-002 | Actor sin tareas | Colección vacía; AC-004 |
| EDGE-003 | Tarea ya completada | Éxito sin cambios adicionales; AC-005 |
| EDGE-004 | Identidad inválida | Rechazo sin lectura ni mutación; AC-006 |
| EDGE-005 | Tarea ajena o inexistente | Mismo resultado no disponible; AC-007 |

Las entradas del identificador de tarea y la precedencia técnica de errores
se concretarán en el PLAN sin alterar los resultados funcionales anteriores.

# 10. Datos involucrados

- Actor: identificador sintético textual estable.
- Tarea: identificador único, título normalizado, propietario y estado.
- Orden de creación: deberá conservarse para el listado, sin imponer un campo físico.

No se requieren nombres reales, correos, contraseñas ni otros datos personales.

# 11. Dependencias

No hay features ni servicios externos requeridos. La identidad de prueba
proviene del entorno confiable del ejercicio; su contrato se definirá en el PLAN.

# 12. Restricciones

- Constitución, standards y gates del Harness vigentes.
- SPEC, PLAN y TASKS requieren aprobación humana explícita antes de implementación.
- Esta propuesta no selecciona lenguaje, framework, persistencia ni interfaz técnica.
- Los resultados de auditoría no convierten el Harness automáticamente en STABLE.

# 13. Suposiciones

No se utilizan suposiciones funcionales implícitas. El alcance y las reglas
fueron confirmados por el usuario en Q-001 sin modificaciones funcionales.

# 14. Preguntas abiertas y necesidades de aclaración

## Q-001 — Confirmación de la feature representativa

**Estado:** [CLARIFIED]  
**Bloqueante:** NO (bloqueo original resuelto)

**Pregunta:** ¿Se confirma esta feature de tareas y las reglas propuestas en
esta SPEC como muestra para AUDIT-08?

**Contexto:** se autorizó continuar la auditoría, pero no se eligió una feature
ni se aprobaron reglas funcionales específicas. Los ejemplos históricos del
Harness no constituyen esa decisión.

**Impacto:** alcance, FR-001 a FR-003, NFR-001, SEC-001/002, BR-001 a BR-003
y AC-001 a AC-009.

**Opciones conocidas:** confirmar esta propuesta o ajustar la muestra/reglas.
**Respuesta:** «Confirmo esa propuesta», en respuesta a la solicitud de
confirmación y aprobación de SPEC-001 v0.1.0 para avanzar a `/plan`.
**Resuelto por:** usuario humano.
**Fecha de resolución:** 2026-09-24.
**Propagación:** se confirmó el contenido funcional sin cambios; se actualizaron
las referencias a la propuesta pendiente y el estado de aprobación.

# 14.1 Ciclo de vida de una aclaración

Al recibir la decisión humana se registrarán respuesta, responsable y fecha;
se incorporarán los ajustes en requisitos, criterios y matriz antes de marcar
Q-001 [CLARIFIED]. La aprobación de la SPEC deberá ser explícita y referirse al
contenido resultante. No se reutiliza la aprobación de correcciones de AUDIT-07.

Revisión de `/clarify`: se revisaron actores, permisos, estados, errores,
datos, alcance y criterios. Q-001 quedó resuelta; no quedan aclaraciones
bloqueantes ni contradicciones identificadas. Las decisiones de implementación
quedan en PLAN. La revisión habilitó IN_REVIEW y la confirmación humana del
contenido presentado habilitó APPROVED; ambas transiciones se registran aquí.

# 15. Matriz inicial de trazabilidad

| Requisito o regla | Criterios de aceptación | Prioridad |
|---|---|---|
| FR-001 | AC-001, AC-002, AC-008 | MUST |
| FR-002 | AC-003, AC-004 | MUST |
| FR-003 | AC-005, AC-007 | MUST |
| NFR-001 | AC-009 | MUST |
| SEC-001 | AC-006, AC-008 | MUST |
| SEC-002 | AC-003, AC-004, AC-007 | MUST |
| BR-001 | AC-001, AC-002 | MUST |
| BR-002 | AC-001, AC-005 | MUST |
| BR-003 | AC-001, AC-005, AC-008 | MUST |

# 16. Criterios para avanzar a planificación

- [x] Problema, objetivo, actores y alcance propuesto documentados.
- [x] Requisitos propuestos verificables y criterios para cada MUST.
- [x] Seguridad, errores y casos límite identificados.
- [x] Matriz inicial consistente y sin selección tecnológica prematura.
- [x] Q-001 resuelta e incorporada; sin aclaraciones bloqueantes.
- [x] SPEC revisada y aprobada explícitamente por el humano.

# 17. Estado de aprobación

**Estado actual:** APPROVED.
**Resultado:** READY FOR PLAN.

Estados permitidos: DRAFT → IN_REVIEW → APPROVED → SUPERSEDED.
**Aprobado por:** usuario humano. **Fecha de aprobación:** 2026-09-24.
**Evidencia:** «Confirmo esa propuesta», respuesta a la solicitud explícita
de confirmar y aprobar SPEC-001 v0.1.0. No se modificaron requisitos ni
criterios respecto de la versión presentada para aprobación.

Siguiente fase autorizada: `/plan`. Esta aprobación no cubre PLAN, TASKS
ni implementación.
