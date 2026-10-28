# Especificación: Ajuste de reasoning effort interoperable por tarea

**ID:** SPEC-011
**Estado:** APPROVED
**Versión:** 0.1.0
**Fecha:** 2026-10-27

# 1. Resumen

## 1.1 Descripción

El Harness debe ajustar el reasoning effort del modelo de acuerdo con el tipo y la complejidad de la tarea, buscando equilibrar rapidez y eficacia en distintos proveedores de modelos y runtimes de agentes.

## 1.2 Problema

Usar un nivel de effort uniforme puede emplear más tiempo y recursos de los necesarios en tareas sencillas, o aportar razonamiento insuficiente en tareas complejas.

## 1.3 Objetivo

Que las tareas reciban un nivel de reasoning effort adecuado en los entornos de agentes y proveedores de modelos requeridos, sin depender de un solo fabricante.

# 2. Alcance

## 2.1 Incluido

- Determinar el effort adecuado según la tarea que recibe el Harness.
- Aplicar el nivel mediante las capacidades disponibles en el runtime y modelo activos.
- Mantener compatibilidad con Claude Code, Codex y OpenCode, y con modelos de Anthropic, DeepSeek, GLM y otros proveedores.
- Continuar con el valor predeterminado del runtime/modelo y comunicar la limitación cuando la combinación activa no permita ajustar effort.

## 2.2 Fuera de alcance

- Cambiar de modelo o proveedor automáticamente.
- Optimizar el esfuerzo mediante evaluación automática de calidad, salvo decisión posterior respaldada por requisitos.
- Cambiar los gates SDD o la autoridad de aprobación humana.

# 3. Actores

## ACT-001 — Agente del Harness

**Descripción:** Agente que recibe y ejecuta tareas en el Harness.
**Responsabilidades o necesidades:** Aplicar un nivel de effort proporcional al trabajo y conocer si el runtime pudo aplicar el nivel seleccionado.

# 4. Requisitos funcionales

## FR-001 — Ajuste de effort según tarea

**Descripción:** Para cada tarea recibida, el Harness debe determinar un nivel de effort acorde con sus necesidades de razonamiento y aplicarlo mediante el control equivalente que ofrezcan el runtime y modelo activos.
**Prioridad:** MUST
**Origen:** Petición del usuario del 2026-10-27.

## FR-002 — Manejo de effort no disponible

**Descripción:** Si la combinación activa no expone un control de effort compatible, el Harness debe continuar la tarea con el comportamiento predeterminado de esa combinación e informar que no pudo ajustar el effort.
**Prioridad:** MUST
**Origen:** Requisito de interoperar con múltiples runtimes y modelos expresado por el usuario.

## FR-003 — Interoperabilidad de runtimes y proveedores

**Descripción:** El Harness debe ofrecer el comportamiento de esta funcionalidad en Claude Code, Codex y OpenCode, con modelos de Anthropic, DeepSeek, GLM y otros proveedores compatibles con el runtime activo.
**Prioridad:** MUST
**Origen:** Aclaración del usuario del 2026-10-27.

# 5. Requisitos no funcionales

## NFR-001 — Equilibrio entre rapidez y eficacia

**Categoría:** Rendimiento
**Descripción:** La política de selección debe apoyar el equilibrio solicitado entre rapidez y eficacia.
**Métrica o condición:** La condición medible queda pendiente de concretar en PLAN con el runtime y las métricas disponibles.

## NFR-002 — Portabilidad entre entornos

**Categoría:** Compatibilidad
**Descripción:** La selección de effort no debe depender de un único proveedor de modelos o runtime de agente.
**Métrica o condición:** La aceptación cubre los runtimes Claude Code, Codex y OpenCode y los proveedores/familias Anthropic, DeepSeek y GLM; otras combinaciones se admiten cuando el runtime las soporte.

# 6. Requisitos de seguridad

No se identifican requisitos de seguridad específicos en esta fase. La integración deberá reevaluarse en PLAN si transmite datos a un servicio externo o modifica permisos/configuración.

# 7. Reglas de negocio

## BR-001 — Compatibilidad del nivel

**Regla:** El nivel utilizado debe ser compatible con las capacidades declaradas por el modelo y runtime activos.
**Ejemplo:** No aplica en esta fase.

# 8. Criterios de aceptación

## AC-001 — Selección y aplicación para una tarea

**Relacionado con:** FR-001

### Given

Una tarea y una combinación de runtime/modelo que permite ajustar su control equivalente de effort.

### When

El Harness inicia la ejecución de la tarea.

### Then

El Harness determina un nivel apropiado y la ejecución lo aplica mediante el control disponible en esa combinación.

## AC-002 — Runtime sin capacidad de ajuste

**Relacionado con:** FR-002

### Given

Una combinación de runtime/modelo que no permite ajustar effort.

### When

El Harness procesa una tarea.

### Then

El Harness comunica que no pudo aplicar el ajuste y ejecuta la tarea con el valor predeterminado de esa combinación.

## AC-003 — Runtimes y proveedores requeridos

**Relacionado con:** FR-003

### Given

Claude Code, Codex u OpenCode configurado con un modelo de Anthropic, DeepSeek, GLM u otro proveedor compatible con ese runtime.

### When

Se ejecuta una tarea con la funcionalidad habilitada.

### Then

El Harness aplica el control equivalente de effort que exponga la combinación activa; si no expone uno, cumple AC-002 y la tarea sigue ejecutándose.

# 9. Casos límite y escenarios de error

## EDGE-001 — Modelo sin soporte para el nivel seleccionado

**Condición:** El nivel elegido no está soportado por el modelo activo.
**Comportamiento esperado:** No enviar una configuración incompatible; comunicar que no pudo ajustar effort y usar el valor predeterminado, conforme a AC-002.

## EDGE-002 — Tarea ambigua o con complejidad mixta

**Condición:** La tarea no permite determinar claramente las necesidades de razonamiento.
**Comportamiento esperado:** La política de selección se define en PLAN; la compatibilidad del runtime se rige por FR-002.

# 10. Datos involucrados

## Tarea de ejecución

Información requerida: contenido o clasificación de la tarea necesaria para escoger effort. Retención y registro de esa información no están definidos por esta SPEC.

## Configuración de reasoning effort

Información requerida: nivel elegido, nivel aplicado y resultado de aplicación, cuando sean disponibles en el entorno.

# 11. Dependencias

- Capacidad de configuración del runtime y modelo seleccionados.

# 12. Restricciones

- Respetar los niveles de reasoning effort soportados por el modelo activo.
- No afirmar que el effort cambió cuando el runtime no confirmó o no permite ese cambio.
- La disponibilidad y nombres de controles de effort dependen del modelo y runtime activos.

# 13. Suposiciones

## ASM-001

El Harness recibe tareas de forma que puede identificar al menos su tipo o necesidades de razonamiento. Confirmar en PLAN según el runtime real.

# 14. Preguntas abiertas y necesidades de aclaración

## Q-001 — Portabilidad entre runtimes y proveedores

**Estado:** [CLARIFIED]
**Pregunta:** ¿En qué runtimes y proveedores debe estar disponible el ajuste de effort?
**Contexto:** La propuesta inicial no definía si se limitaba a una integración concreta.
**Impacto:** FR-001, FR-002, FR-003, NFR-002, AC-001, AC-002 y AC-003.
**Bloqueante:** NO
**Opciones conocidas:** N/A; aclaración recibida.
**Respuesta:** El Harness debe poder usarse con cualquier modelo, incluidos los de Anthropic, DeepSeek y GLM, entre otros, y con Claude Code, Codex y OpenCode. Cuando una combinación no exponga un control de effort, continuará con su configuración predeterminada e informará la limitación.
**Resuelto por:** Usuario responsable del proyecto
**Fecha de resolución:** 2026-10-27

# 14.1 Ciclo de vida de una aclaración

`[NEEDS CLARIFICATION] → [CLARIFIED]`: registrar respuesta, responsable y fecha; actualizar FR/AC/SEC afectados. Resolver Q sin propagar su contenido no basta.

# 15. Matriz inicial de trazabilidad

| Requisito | Criterios de aceptación | Prioridad |
|-----------|-------------------------|-----------|
| FR-001 | AC-001 | MUST |
| FR-002 | AC-002 | MUST |
| FR-003 | AC-003 | MUST |

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
**Fecha de aprobación:** 2026-10-27
**Decisión explícita y alcance:** «Ok lo apruebo», respecto a SPEC-011 v0.1.0; autoriza preparar PLAN-011.
**Registro durable:** `specs/011-task-based-model-effort/decisions.json` con huella, según `docs/state-reconstruction.md`, antes de PLAN.
