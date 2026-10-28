# Especificación: Orquestador de subagentes con modelo y effort por tarea

**ID:** SPEC-012
**Estado:** APPROVED
**Versión:** 0.3.0
**Fecha:** 2026-10-28

# 1. Resumen

## 1.1 Descripción

El agente principal del Harness actúa como orquestador: reconstruye el estado SDD, decide el siguiente paso y delega cada unidad de trabajo a un subagente con contexto mínimo, modelo y reasoning effort adecuados a esa unidad. Los subagentes ejecutan y devuelven un resultado compacto que el orquestador verifica antes de integrarlo.

## 1.2 Problema

Hoy un solo agente acumula en su contexto todo el bootstrap, las lecturas de archivos, la ejecución de tareas y la evidencia de una feature, con un mismo modelo y effort para trabajo simple y complejo. Esto eleva el consumo de tokens, satura la ventana de contexto en features largas y dificulta llevar un proyecto hasta `FEATURE STATUS: VALIDATED` sin reiniciar sesiones.

## 1.3 Objetivo

Reducir el consumo de tokens necesario para completar una feature y mejorar la continuidad del flujo SDD, manteniendo gates, trazabilidad y autoridad humana sin cambios.

# 2. Alcance

## 2.1 Incluido

- Rol de orquestador para el agente principal y rol de ejecutor acotado para subagentes.
- Paquete de delegación con contexto mínimo y límites de mutación por unidad de trabajo.
- Selección de modelo y reasoning effort por subagente según tipo y complejidad de la tarea.
- Avance de las TASK aprobadas en orden de dependencias hasta completar TASKS, un bloqueo o una aclaración.
- Ejecución paralela de TASK independientes cuando no genere retrabajo.
- Delegación de las verificaciones de `/validate` con consolidación del reporte por el orquestador.
- Resultado compacto de subagente y verificación del orquestador antes de marcar `DONE`.
- Registro durable de modelo, effort y consumo por delegación.
- Medición comparativa del consumo de tokens frente a una línea base.

## 2.2 Fuera de alcance

- Aprobar SPEC, PLAN o TASKS, o cambiar gates SDD y la autoridad humana.
- Usar modelos o proveedores no declarados por el usuario.
- Gestionar autenticación, claves, facturación o cuotas de proveedores.
- Modificar el contenido aprobado de SPEC-011; esta feature lo reutiliza.
- Optimización automática basada en evaluación de calidad de las respuestas.
- Orquestar `/specify`, `/clarify`, `/plan` y `/tasks`; esas fases siguen el flujo habitual del agente principal.

# 3. Actores

## ACT-001 — Usuario responsable del proyecto

**Descripción:** Persona que aprueba gates y configura runtimes y modelos.
**Responsabilidades o necesidades:** Completar features con menos consumo, conocer qué modelo y effort se usó y conservar el control de aprobaciones.

## ACT-002 — Agente orquestador

**Descripción:** Agente principal de la sesión.
**Responsabilidades o necesidades:** Reconstruir estado, delegar, verificar e integrar resultados; responsable de bootstrap, gates y trazabilidad.

## ACT-003 — Subagente ejecutor

**Descripción:** Agente lanzado por el orquestador para una unidad de trabajo.
**Responsabilidades o necesidades:** Ejecutar solo lo delegado con el contexto recibido y devolver resultado y evidencia.

# 4. Requisitos funcionales

## FR-001 — Rol de orquestador

**Descripción:** En modo orquestado, durante `/implement` y `/validate`, el agente principal debe determinar fase, gate y siguiente acción desde los artefactos del repositorio y delegar a subagentes la ejecución de las unidades de trabajo, sin ejecutar él mismo el trabajo delegado.
**Prioridad:** MUST
**Origen:** Petición del usuario del 2026-10-28.

## FR-002 — Paquete de delegación mínimo

**Descripción:** Cada delegación debe incluir objetivo, feature y fase, TASK o ID trazable, fuentes a consultar, archivos permitidos, límites de mutación, evidencia esperada y criterios de escalamiento, según `docs/agents/subagents.md`, y limitarse al contexto que la unidad necesita, sin transferir la conversación completa del orquestador.
**Prioridad:** MUST
**Origen:** Petición del usuario (reducción de tokens) y guía de subagentes vigente.

## FR-003 — Modelo y effort por subagente

**Descripción:** Para cada delegación, el Harness debe determinar un nivel de modelo y un nivel de reasoning effort acordes con el tipo y complejidad de la unidad, aplicarlos mediante los controles del runtime activo e informar el modelo y effort solicitados y los efectivamente aplicados.
**Prioridad:** MUST
**Origen:** Petición del usuario del 2026-10-28; extiende la política de effort de SPEC-011.

## FR-004 — Catálogo de modelos y fallback

**Descripción:** El Harness solo debe asignar modelos incluidos en el catálogo que el usuario declara en un archivo del proyecto; si ese catálogo no existe, no cambia de modelo y usa el configurado en el runtime. Si el modelo o el effort seleccionado no está disponible en la combinación activa, debe continuar con la configuración predeterminada del runtime e informar la limitación, sin afirmar un cambio no confirmado.
**Prioridad:** MUST
**Origen:** Restricciones de SPEC-011, Artículo X de la Constitución y aclaración Q-002 del 2026-10-28.

## FR-005 — Ejecución de TASKS hasta un punto de detención

**Descripción:** Durante `/implement`, el orquestador debe delegar las TASK aprobadas en el orden de dependencias definido hasta que TASKS quede `COMPLETED`, una TASK quede `BLOCKED` o surja `[NEEDS CLARIFICATION]`, y entonces informar el estado y la siguiente acción.
**Prioridad:** MUST
**Origen:** Petición del usuario (terminar un proyecto con el Harness).

## FR-006 — Verificación antes de integrar

**Descripción:** El orquestador debe marcar una TASK como `DONE` solo tras comprobar que el resultado del subagente incluye la evidencia exigida y que los archivos modificados están dentro de los límites de la delegación; en caso contrario debe rechazarlo o marcarla `BLOCKED` con motivo.
**Prioridad:** MUST
**Origen:** Constitución, Artículos V, VI y XII; guía de subagentes.

## FR-007 — Resultado compacto

**Descripción:** Cada subagente debe devolver un resultado estructurado con estado, archivos modificados, comandos y resultado, evidencia, hallazgos y bloqueos; el orquestador debe conservar ese resultado y no el registro completo de la ejecución del subagente.
**Prioridad:** MUST
**Origen:** Petición del usuario (reducción de tokens).

## FR-008 — Registro de consumo por delegación

**Descripción:** Para cada delegación, el Harness debe registrar en la evidencia de la feature la TASK, modelo y effort solicitados y aplicados, resultado y tokens consumidos cuando el runtime los reporte, o indicar que no están disponibles.
**Prioridad:** MUST
**Origen:** Necesario para verificar NFR-001.

## FR-009 — Escalamiento ante fallo

**Descripción:** Si un subagente no completa una unidad por insuficiencia de razonamiento, el orquestador puede reintentarla una sola vez con un nivel de modelo o effort superior del catálogo, registrando ambos intentos; fallos de autenticación, permisos, red o límites no se reintentan por esta vía.
**Prioridad:** SHOULD
**Origen:** Petición del usuario (adaptar modelos a la tarea).

## FR-010 — Ejecución paralela sin retrabajo

**Descripción:** El orquestador debe delegar en paralelo las TASK listas que no dependan entre sí ni modifiquen archivos en común; cuando el paralelismo pueda causar retrabajo (dependencias, archivos compartidos o resultado de una TASK necesario para otra), debe ejecutarlas en serie.
**Prioridad:** SHOULD
**Origen:** Aclaración Q-003 del 2026-10-28.

## FR-011 — Modo opcional y compatible

**Descripción:** El flujo SDD sin orquestador debe seguir funcionando sin cambios; el modo orquestado es una opción del usuario.
**Prioridad:** MUST
**Origen:** Portabilidad del Harness (SPEC-008, SPEC-011).

## FR-012 — Orquestación de `/validate`

**Descripción:** Durante `/validate`, el orquestador debe delegar a subagentes las verificaciones (pruebas, comprobación de AC, revisión de seguridad y trazabilidad) y consolidar sus resultados en el reporte de validación; el veredicto `SPEC COMPLIANCE` y `FEATURE STATUS` lo emite el orquestador, no un subagente.
**Prioridad:** MUST
**Origen:** Aclaración Q-004 del 2026-10-28; guía de subagentes (un subagente no sustituye la validación final).

# 5. Requisitos no funcionales

## NFR-001 — Reducción de consumo de tokens

**Categoría:** Rendimiento
**Descripción:** Completar la implementación de una feature de referencia en modo orquestado debe consumir al menos 30 % menos tokens totales que la línea base de un solo agente con modelo y effort uniformes.
**Métrica o condición:** (tokens línea base − tokens orquestado) / tokens línea base ≥ 0,30, medido sobre las mismas TASK; la feature de referencia y el procedimiento de medición se definen en PLAN (Q-001).

## NFR-002 — Portabilidad

**Categoría:** Compatibilidad
**Descripción:** El modo orquestado debe estar disponible en los runtimes y proveedores cubiertos por SPEC-011.
**Métrica o condición:** Claude Code, Codex y OpenCode con modelos de Anthropic, DeepSeek, GLM u otros compatibles; donde un runtime no ofrezca un control, aplica FR-004.

## NFR-003 — Contexto acotado del orquestador

**Categoría:** Mantenibilidad
**Descripción:** El contexto del orquestador no debe crecer con el contenido completo de los archivos leídos o generados por subagentes.
**Métrica o condición:** Por delegación, el orquestador retiene solo el resultado compacto de FR-007; verificable en el registro de FR-008.

## NFR-004 — Trazabilidad de delegaciones

**Categoría:** Observabilidad
**Descripción:** Toda delegación debe ser trazable a una TASK o ID del Harness.
**Métrica o condición:** No existen delegaciones registradas sin ID trazable.

# 6. Requisitos de seguridad

## SEC-001 — Límite de mutación del subagente

**Descripción:** Un subagente solo puede modificar los archivos autorizados por su delegación; cualquier modificación fuera de ese límite se detecta, se reporta y impide `DONE`.
**Riesgo mitigado:** Cambios no autorizados o scope creep fuera de la TASK.

## SEC-002 — Integridad de aprobaciones

**Descripción:** Un subagente no puede crear, alterar ni retirar eventos `APPROVAL` o `REVOCATION` ni cambiar estados de SPEC, PLAN o TASKS a `APPROVED`.
**Riesgo mitigado:** Autoaprobación o elusión de gates humanos.

## SEC-003 — Mínimo privilegio

**Descripción:** Un subagente no recibe más permisos que los configurados por el usuario para el runtime; el Harness no activa omisión de permisos ni cambia configuración global.
**Riesgo mitigado:** Escalada de privilegios mediante delegación.

## SEC-004 — Secretos fuera de delegaciones y registros

**Descripción:** Paquetes de delegación, resultados, registros de consumo y evidencia no contienen secretos ni credenciales.
**Riesgo mitigado:** Exposición de secretos en archivos versionados o logs.

# 7. Reglas de negocio

## BR-001 — Catálogo declarado por el usuario

**Regla:** El usuario declara en un archivo del proyecto qué modelos puede usar cada nivel en cada runtime; el Harness no trae catálogo por defecto ni incorpora modelos por su cuenta. Sin catálogo declarado no hay cambio de modelo.

## BR-002 — Piso para trabajo de alto impacto

**Regla:** Unidades de seguridad, arquitectura, validación final o resolución de conflictos de gate no se asignan al nivel de modelo más bajo del catálogo.

## BR-003 — Gates humanos

**Regla:** El orquestador se detiene en cada gate que requiere aprobación humana y no lo infiere de silencio ni de resultados de subagentes.

# 8. Criterios de aceptación

## AC-001 — Orquestación desde artefactos

**Relacionado con:** FR-001, NFR-004

### Given

Una feature con SPEC, PLAN y TASKS `APPROVED` y modo orquestado habilitado.

### When

El usuario inicia la ejecución en modo orquestado.

### Then

El orquestador identifica fase y siguiente TASK desde los artefactos y la delega a un subagente con un ID trazable, sin implementarla él mismo.

## AC-002 — Contenido del paquete de delegación

**Relacionado con:** FR-002

### Given

Una TASK aprobada lista para ejecución.

### When

El orquestador la delega.

### Then

El paquete contiene todos los campos de FR-002 y no incluye el historial completo de la conversación del orquestador.

## AC-003 — Selección y aplicación de modelo y effort

**Relacionado con:** FR-003, BR-002

### Given

Un catálogo con al menos dos niveles de modelo y dos TASK de complejidad distinta, una de ellas de seguridad.

### When

El orquestador delega ambas.

### Then

Cada delegación registra modelo y effort solicitados y aplicados; la TASK de seguridad no usa el nivel más bajo.

## AC-004 — Modelo fuera de catálogo o no disponible

**Relacionado con:** FR-004, BR-001

### Given

Un nivel seleccionado cuyo modelo no está en el catálogo o no está disponible en el runtime.

### When

El orquestador delega la unidad.

### Then

No se usa un modelo fuera del catálogo; la unidad se ejecuta con la configuración predeterminada y el resultado informa la limitación.

## AC-005 — Avance hasta punto de detención

**Relacionado con:** FR-005, BR-003

### Given

TASKS aprobadas con dependencias, una de las cuales resulta `BLOCKED`.

### When

El orquestador ejecuta en modo orquestado.

### Then

Delega en orden de dependencias, no inicia TASK que dependan de la bloqueada y se detiene informando el bloqueo y la siguiente acción.

## AC-006 — Rechazo de resultado fuera de límites

**Relacionado con:** FR-006, SEC-001

### Given

Un subagente que modifica un archivo no autorizado o no entrega la evidencia exigida.

### When

El orquestador verifica el resultado.

### Then

La TASK no pasa a `DONE`; queda rechazada o `BLOCKED` con el motivo y los archivos afectados.

## AC-007 — Resultado compacto retenido

**Relacionado con:** FR-007, NFR-003

### Given

Una delegación completada.

### When

El orquestador integra el resultado.

### Then

Conserva solo los campos estructurados de FR-007 y no el registro completo de la ejecución.

## AC-008 — Registro de consumo

**Relacionado con:** FR-008

### Given

Una o más delegaciones completadas o fallidas.

### When

Se revisa la evidencia de la feature.

### Then

Cada delegación aparece con TASK, modelo y effort solicitados y aplicados, resultado y tokens o la indicación de que no están disponibles.

## AC-009 — Integridad de aprobaciones

**Relacionado con:** SEC-002, BR-003

### Given

Un subagente cuyo resultado modifica eventos `APPROVAL`/`REVOCATION` o estados `APPROVED`.

### When

El orquestador verifica el resultado.

### Then

El cambio se rechaza, se reporta y no se integra.

## AC-010 — Permisos y secretos

**Relacionado con:** SEC-003, SEC-004

### Given

Una ejecución orquestada en cualquier runtime soportado.

### When

Se inspeccionan las invocaciones, paquetes, resultados y registros generados.

### Then

No hay opciones de omisión de permisos ni cambios de configuración global y no aparecen secretos.

## AC-011 — Flujo sin orquestador

**Relacionado con:** FR-011

### Given

El modo orquestado no está habilitado.

### When

Se ejecuta el flujo SDD habitual.

### Then

El comportamiento es el mismo que antes de esta feature y `python3 src/check_harness_state.py` da PASS.

## AC-012 — Reducción medida de tokens

**Relacionado con:** NFR-001

### Given

La feature de referencia y la línea base definidas en PLAN conforme a Q-001.

### When

Se ejecuta la implementación en modo orquestado y en línea base.

### Then

El consumo total orquestado es al menos 30 % menor que el de la línea base y la comparación queda en la evidencia.

## AC-013 — Escalamiento único

**Relacionado con:** FR-009

### Given

Un subagente que falla por insuficiencia de razonamiento.

### When

El orquestador reintenta.

### Then

Hay como máximo un reintento con nivel superior del catálogo y ambos intentos quedan registrados; un fallo de autenticación o permisos no se reintenta.

## AC-014 — Paralelo solo sin retrabajo

**Relacionado con:** FR-010, EDGE-004

### Given

Tres TASK listas: dos sin dependencias ni archivos en común y una tercera que comparte archivos con una de ellas.

### When

El orquestador las delega.

### Then

Las dos independientes se ejecutan en paralelo y la tercera en serie después de la que comparte archivos.

## AC-015 — Validación orquestada

**Relacionado con:** FR-012

### Given

Una feature con TASKS `COMPLETED` en modo orquestado.

### When

Se ejecuta `/validate`.

### Then

Las verificaciones se delegan y quedan registradas (FR-008); el reporte de validación consolida sus resultados y el veredicto final lo emite el orquestador.

# 9. Casos límite y escenarios de error

## EDGE-001 — Runtime sin subagentes nativos

**Condición:** El runtime activo no ofrece subagentes integrados.
**Comportamiento esperado:** El modo orquestado sigue siendo posible por los medios que defina PLAN, o se informa que no está disponible y el flujo continúa sin orquestador (FR-011).

## EDGE-002 — Runtime que no reporta tokens

**Condición:** El runtime no expone consumo de tokens.
**Comportamiento esperado:** Se registra «no disponible» (FR-008); esa combinación no sirve como evidencia de AC-012.

## EDGE-003 — Catálogo vacío o inválido

**Condición:** El usuario no declaró catálogo o declaró uno inconsistente.
**Comportamiento esperado:** No se cambia de modelo: se usa el modelo configurado en el runtime para todas las delegaciones (el effort sigue aplicándose según SPEC-011) y se informa; no se inventan modelos.

## EDGE-004 — Conflicto de archivos entre delegaciones paralelas

**Condición:** Dos TASK candidatas a paralelo tocan los mismos archivos.
**Comportamiento esperado:** Se ejecutan en serie.

## EDGE-005 — Sesión interrumpida

**Condición:** La sesión del orquestador termina a mitad de TASKS.
**Comportamiento esperado:** Una sesión nueva reconstruye el avance desde artefactos y registro (`docs/state-reconstruction.md`) sin depender del chat.

# 10. Datos involucrados

## Paquete de delegación

Información requerida: campos de FR-002. Reglas relevantes: sin secretos (SEC-004).

## Resultado de subagente

Información requerida: campos de FR-007.

## Registro de delegación

Información requerida: campos de FR-008, fecha e intento. Reglas relevantes: vive en la evidencia de la feature; no contiene prompts completos ni secretos.

## Catálogo de modelos

Información requerida: runtime, nivel y modelo permitido. Reglas relevantes: declarado por el usuario en un archivo del proyecto (BR-001); su ubicación y formato se definen en PLAN.

# 11. Dependencias

- SPEC-011: política de effort por tarea y ejecutor `src/run_task.py`. Su validación está BLOCKED por smokes reales y benchmark; la validación de SPEC-012 en runtimes reales comparte ese requisito.
- `docs/agents/subagents.md`: contrato vigente de delegación.
- Capacidades de subagentes, selección de modelo y reporte de tokens de cada runtime.

# 12. Restricciones

- Los gates, estados y autoridad humana de la Constitución no cambian.
- No afirmar modelo, effort o consumo no confirmados por el runtime.
- El Harness no solicita claves ni cambia configuración global o permisos del usuario.
- SPEC-011 excluye cambiar de modelo dentro de su propio alcance; SPEC-012 lo añade de forma explícita por petición del usuario sin modificar SPEC-011.

# 13. Suposiciones

## ASM-001

Las unidades delegables son las TASK de `/implement` y las verificaciones de `/validate` (Q-004).

## ASM-002

Los niveles de modelo se expresan como clases comunes portables (por ejemplo económico, estándar, avanzado), análogas a las clases de effort de SPEC-011; sus nombres finales se definen en PLAN.

# 14. Preguntas abiertas y necesidades de aclaración

## Q-001 — Meta de reducción de tokens

**Estado:** [CLARIFIED]
**Pregunta:** ¿Qué reducción mínima de tokens debe demostrar el modo orquestado y contra qué feature de referencia se mide?
**Contexto:** El objetivo principal es bajar consumo; NFR-001 de SPEC-011 quedó sin métrica y hoy bloquea su validación.
**Impacto:** NFR-001, AC-012.
**Bloqueante:** YES
**Opciones conocidas:** (a) ≥ 30 % menos tokens totales; (b) ≥ 20 %; (c) solo medir y reportar, sin umbral. Referencia: re-ejecutar las TASK de una feature ya validada o una feature sintética de prueba.
**Respuesta:** Opción (a): al menos 30 % menos tokens totales frente a la línea base. La elección de la feature de referencia y el procedimiento de medición son técnicos y se definen en PLAN. Propagado a NFR-001 y AC-012.
**Resuelto por:** Usuario responsable del proyecto
**Fecha de resolución:** 2026-10-28

## Q-002 — Origen del catálogo de modelos

**Estado:** [CLARIFIED]
**Pregunta:** ¿Quién define qué modelo corresponde a cada nivel en cada runtime?
**Contexto:** Cambiar de modelo afecta costo, calidad y proveedores; el Harness no debe inventar integraciones.
**Impacto:** FR-003, FR-004, BR-001, AC-003, AC-004.
**Bloqueante:** YES
**Opciones conocidas:** (a) el usuario declara el catálogo en un archivo del proyecto y sin él no se cambia de modelo; (b) el Harness trae un catálogo por defecto editable por el usuario.
**Respuesta:** Opción (a): el usuario declara el catálogo en un archivo del proyecto; sin él no se cambia de modelo. Propagado a FR-004, BR-001, EDGE-003 y Datos involucrados.
**Resuelto por:** Usuario responsable del proyecto
**Fecha de resolución:** 2026-10-28

## Q-003 — Paralelismo en esta feature

**Estado:** [CLARIFIED]
**Pregunta:** ¿La ejecución paralela de TASK independientes entra en esta versión?
**Contexto:** Mejora el tiempo, no necesariamente los tokens, y añade riesgo de conflictos.
**Impacto:** FR-010, EDGE-004.
**Bloqueante:** NO
**Opciones conocidas:** Mantener como COULD o moverla fuera de alcance.
**Respuesta:** Sí: ejecutar en paralelo cuando se pueda, salvo que cause retrabajo. Propagado a FR-010 (SHOULD), AC-014 y alcance.
**Resuelto por:** Usuario responsable del proyecto
**Fecha de resolución:** 2026-10-28

## Q-004 — Fases cubiertas

**Estado:** [CLARIFIED]
**Pregunta:** ¿El orquestador solo cubre `/implement` (y apoyo a `/validate`) o también delega redacción de SPEC, PLAN y TASKS?
**Contexto:** El mayor consumo está en implementación; la redacción de artefactos requiere juicio y contexto del usuario.
**Impacto:** FR-001, FR-005, ASM-001.
**Bloqueante:** NO
**Opciones conocidas:** Según ASM-001, o ampliar a redacción delegada.
**Respuesta:** El orquestador asume `/implement` y `/validate` (implementación y pruebas). Propagado a FR-001, FR-012, AC-015, ASM-001 y alcance.
**Resuelto por:** Usuario responsable del proyecto
**Fecha de resolución:** 2026-10-28

# 14.1 Ciclo de vida de una aclaración

`[NEEDS CLARIFICATION] → [CLARIFIED]`: registrar respuesta, responsable y fecha; actualizar FR/AC/SEC afectados. Resolver Q sin propagar su contenido no basta.

# 15. Matriz inicial de trazabilidad

| Requisito | Criterios de aceptación | Prioridad |
|-----------|-------------------------|-----------|
| FR-001 | AC-001 | MUST |
| FR-002 | AC-002 | MUST |
| FR-003 | AC-003 | MUST |
| FR-004 | AC-004 | MUST |
| FR-005 | AC-005 | MUST |
| FR-006 | AC-006 | MUST |
| FR-007 | AC-007 | MUST |
| FR-008 | AC-008 | MUST |
| FR-009 | AC-013 | SHOULD |
| FR-010 | AC-014 | SHOULD |
| FR-011 | AC-011 | MUST |
| FR-012 | AC-015 | MUST |
| NFR-001 | AC-012 | MUST |
| NFR-002 | AC-003, AC-004, AC-010 | MUST |
| NFR-003 | AC-007 | MUST |
| NFR-004 | AC-001 | MUST |
| SEC-001 | AC-006 | MUST |
| SEC-002 | AC-009 | MUST |
| SEC-003 | AC-010 | MUST |
| SEC-004 | AC-010 | MUST |
| BR-001 | AC-004 | MUST |
| BR-002 | AC-003 | MUST |
| BR-003 | AC-005, AC-009 | MUST |

# 16. Criterios para avanzar a planificación

- [x] Problema, alcance, actores, FR/NFR/SEC/BR y casos límite aplicables definidos.
- [x] MUST con AC verificables y matriz consistente; sin aclaraciones bloqueantes.
- [x] Suposiciones/restricciones visibles; no hay diseño innecesario.
- [x] SPEC aprobada por humano y decisión durable registrada.

# 17. Estado de aprobación

**Estado actual:** APPROVED

Estados: `DRAFT → IN_REVIEW → APPROVED → SUPERSEDED`.

## Aprobación

Solo decisión humana explícita permite `APPROVED`.

**Aprobado por:** Usuario responsable del proyecto
**Fecha de aprobación:** 2026-10-28
**Decisión explícita y alcance:** «Listo, he revisado y queda autorizada la spec», respecto a SPEC-012 v0.3.0; autoriza preparar PLAN-012.
**Registro durable:** `specs/012-subagent-orchestrator/decisions.json` con huella, según `docs/state-reconstruction.md`, antes de PLAN.
