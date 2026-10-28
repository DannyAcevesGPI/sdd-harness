# Plan Técnico: Ajuste de reasoning effort interoperable por tarea

**ID:** PLAN-011
**SPEC relacionada:** SPEC-011
**Estado:** APPROVED
**Versión:** 0.1.0
**Fecha:** 2026-10-27

# 1. Precondiciones

- [x] SPEC existe, está `APPROVED`, sin aclaraciones bloqueantes y con MUST→AC.
- [x] Alcance y restricciones conocidos; checker de estado en PASS al iniciar PLAN.

# 2. Resumen técnico

## 2.1 Objetivo

Proveer un punto de entrada portable que clasifique la complejidad de una tarea, traduzca esa clase a un nivel común de effort y ejecute la tarea usando el control nativo del agente/modelo elegido.

## 2.2 Enfoque

El repositorio actual es un Harness documental con utilidades Python de biblioteca estándar; no contiene un orquestador ni integra directamente un runtime de modelos. Se añadirá un ejecutor opcional para Claude Code, Codex CLI y OpenCode. La política será común y determinista; cada adaptador traducirá el nivel común a la interfaz del CLI. El usuario seguirá autenticándose y configurando permisos en el CLI instalado.

# 3. Requisitos cubiertos

| Requisito | Tipo | Cobertura en el plan |
|-----------|------|----------------------|
| FR-001 | Funcional | Clasificador determinista de tareas más adaptadores que aplican el control nativo del CLI antes de ejecutar la tarea. |
| FR-002 | Funcional | Ante rechazo explícito por nivel no soportado, repetir una sola vez sin override y reportar uso del valor predeterminado. No reintentar errores ajenos al parámetro de effort. |
| FR-003 | Funcional | Adaptadores para Claude Code, Codex CLI y OpenCode; selección independiente del proveedor siempre que modelo y CLI lo soporten. |
| NFR-001 | Rendimiento | Evaluar un conjunto reproducible contra ejecución fija en `medium`; registrar clase, nivel aplicado, resultado y duración; no declarar mejora de calidad sin evidencia. |
| NFR-002 | Compatibilidad | Pruebas de contrato por adaptador con CLIs falsos y verificación manual en los tres CLIs cuando estén disponibles. |
| BR-001 | Negocio | La traducción verifica soporte y nunca reporta como aplicado un nivel rechazado. |
| AC-001 | Aceptación | Caso de integración simulado confirma clasificación, argumento nativo y ejecución con override. |
| AC-002 | Aceptación | Caso de integración simulado confirma reintento sin override, mensaje de fallback y ejecución completada. |
| AC-003 | Aceptación | Matriz por agente y proveedor/modelo configurado confirma adaptación o fallback sin impedir la tarea. |

# 4. Contexto técnico existente

## Stack actual

- Scripts Python sin dependencias externas.
- Pruebas con `unittest`.
- No hay empaquetado Python, aplicación de runtime, capa API, configuración de modelos ni credenciales en el repositorio.

## Componentes existentes relacionados

- `src/adopt_harness.py`: copia una lista explícita de archivos reutilizables a proyectos destino.
- `AGENTS.md`, `docs/quickstart.md` y `docs/adoption.md`: describen el flujo documental de agentes y su adopción.
- No existe una skill o adaptador de effort en el repositorio.

## Restricciones técnicas existentes

- La implementación debe seguir funcionando sin dependencias adicionales y no alterar autenticación, permisos o configuración persistente de los CLIs.
- Las interfaces de esfuerzo difieren por runtime y por modelo. OpenCode representa controles como variantes de modelo y documenta que no toda variante existe para todos los modelos; Codex usa una opción de reasoning effort y Claude Code expone un selector de effort.
- Referencias oficiales consultadas el 2026-10-27: [Claude Code CLI](https://code.claude.com/docs/en/cli-reference), [OpenCode Models](https://dev.opencode.ai/v2/docs/models/), [Codex Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference).

# 5. Decisiones técnicas

## DEC-001 — Ejecución por punto de entrada común

**Decisión:** Añadir `src/run_task.py`, invocado con agente, modelo y texto/archivo de tarea; ejecutará el CLI seleccionado como proceso hijo con el esfuerzo establecido antes de iniciar la tarea.
**Justificación:** Las instrucciones de una skill no pueden por sí solas garantizar que un runtime aplique un parámetro nativo a la solicitud ya iniciada. El CLI wrapper puede configurar el siguiente proceso/turno y reutiliza la autenticación existente.
**Requisitos relacionados:** FR-001, FR-003, AC-001, AC-003.
**Alternativas consideradas:** Solo documentar una recomendación; cambiar archivos de configuración global del usuario; crear tres integraciones dentro de runtimes distintos. La primera no aplica effort; la segunda modifica estado externo persistente; la tercera duplica distribución y mantenimiento.
**Consecuencias:** Las tareas deben entrar por el ejecutor para recibir selección automática; el uso directo del CLI conserva sus valores configurados y no obtiene el ajuste automático del Harness.
**Requiere ADR:** YES — ADR-001 sobre el límite del Harness y la invocación de runtimes externos.

## DEC-002 — Niveles comunes y clasificación transparente

**Decisión:** Usar clases `low`, `medium` y `high`; clasificar con reglas locales deterministas: tarea mecánica, pequeña y acotada → `low`; tarea rutinaria con varios pasos → `medium`; trabajo de seguridad, arquitectura, migraciones, depuración compleja o alto impacto → `high`. Ante señales contradictorias o falta de información, usar `medium`.
**Justificación:** Evita una llamada de clasificación adicional, mantiene la selección repetible y permite probar cada regla sin depender del proveedor.
**Requisitos relacionados:** FR-001, NFR-001, AC-001.
**Alternativas consideradas:** Clasificación con una llamada LLM adicional, que agrega latencia y costo; una sola configuración fija, que no satisface el ajuste por tarea.
**Consecuencias:** La heurística debe ser explícita, sencilla y revisable; no pretende estimar complejidad semántica perfecta.
**Requiere ADR:** NO.

## DEC-003 — Adaptadores nativos con fallback acotado

**Decisión:** Cada adaptador genera argumentos sin shell para su CLI; valida las capacidades disponibles cuando el CLI las expone. Si el CLI rechaza específicamente el nivel como no soportado antes de ejecutar la tarea, reintenta una vez sin override. Otros errores se devuelven sin retry.
**Justificación:** Los niveles y nombres no son uniformes entre runtimes/modelos; el fallback conserva uso de cualquier modelo que el CLI ya pueda ejecutar y evita repetir fallas no relacionadas.
**Requisitos relacionados:** FR-002, FR-003, BR-001, AC-002, AC-003.
**Alternativas consideradas:** Forzar niveles comunes sin validar, lo que puede fallar en modelos sin esa capacidad; editar configuración persistente, lo que amplía permisos y deja cambios laterales.
**Consecuencias:** Los patrones de error soportados deben documentarse y probarse por CLI; desconocidos requieren mensaje de error y no activan fallback.
**Requiere ADR:** NO.

## DEC-004 — Sin cambios de permiso ni credenciales

**Decisión:** El ejecutor conserva las políticas nativas del CLI, usa las credenciales ya configuradas y no activa flags de autoaprobación ni modos de permiso más amplios.
**Justificación:** El Harness solo necesita seleccionar effort y despachar la tarea.
**Requisitos relacionados:** FR-002, FR-003 y standard de seguridad.
**Alternativas consideradas:** No aplica.
**Consecuencias:** Una solicitud de permiso sigue siendo manejada por el CLI y su usuario.
**Requiere ADR:** NO.

# 6. Arquitectura propuesta

## 6.1 Componentes involucrados

| Componente | Responsabilidad | Cambio |
|------------|-----------------|--------|
| `src/effort_policy.py` | Clasificar tarea, resolver nivel común y producir razón breve | CREATE |
| `src/run_task.py` | Validar entradas, seleccionar adaptador, construir y ejecutar proceso, gestionar fallback y salida | CREATE |
| Adaptadores Claude Code, Codex y OpenCode | Traducir nivel común a argumentos propios | CREATE dentro de `src/run_task.py` o módulo compartido, según la división mínima de TASKS |
| `tests/test_effort_policy.py` | Verificar clasificación, conflictos y valor por defecto | CREATE |
| `tests/test_run_task.py` | Verificar comandos, ejecución, fallback, errores y seguridad con procesos simulados | CREATE |
| `src/adopt_harness.py` | Incluir nuevas utilidades y guías en adopción | MODIFY |
| `AGENTS.md`, `docs/quickstart.md`, `docs/adoption.md`, `docs/index.md` | Explicar el punto de entrada, límites y uso por agente | MODIFY |
| `docs/agents/model-effort.md` | Documentar política y soporte | CREATE |
| `docs/decisions/ADR-001-model-effort-runtime-adapters.md` | Registrar el límite entre política común y CLI externos | CREATE |

## 6.2 Flujo principal

1. El usuario indica agente, modelo y tarea (texto o archivo) al ejecutor.
2. El ejecutor valida agente, modelo, ruta y entradas; la tarea no se interpreta como shell.
3. La política común asigna `low`, `medium` o `high` y conserva una razón breve para informar el resultado.
4. El adaptador construye una lista de argumentos para el CLI sin shell y sin cambiar sus opciones de permiso.
5. El ejecutor transmite el texto al CLI y devuelve su salida/estado junto con la clase y el resultado del ajuste.
6. Si hay rechazo explícito de nivel no soportado, reintenta una vez sin el override y reporta el fallback.

## 6.3 Dependencias entre componentes

`run_task.py` depende de `effort_policy.py` y de uno de los CLI instalados por el usuario. Los adaptadores no comparten configuración persistente ni credenciales. `adopt_harness.py` distribuye utilidades y documentación; no ejecuta agentes al adoptar el Harness.

# 7. Modelo de datos

No aplica; no se agrega persistencia.

# 8. Interfaces y contratos

## CLI local del Harness

**Propósito:** Ejecutar una tarea con una selección de effort calculada antes de invocar el modelo.
**Requisito relacionado:** FR-001, FR-002, FR-003.

### Entrada

- Identificador de agente: `claude`, `codex` u `opencode`.
- Modelo, respetando el formato de identificación que acepta ese agente.
- Texto de tarea o ruta de archivo; no ambos si el contrato del comando no lo permite.
- Opciones informativas como `--dry-run` para inspeccionar argumentos sin ejecutar el CLI.

### Salida exitosa

Código de salida del CLI y un resumen en `stderr` con agente, clase, nivel solicitado y `applied` o `default-fallback`. La salida generada por el agente se conserva en `stdout`.

### Errores esperados

Entrada inválida, CLI ausente, error de ejecución, configuración de modelo inválida, rechazo de permiso o error del CLI. No exponer entorno ni valores de secretos.

# 9. Validación de entradas

- Validar agente contra una lista permitida y modelo/texto contra valores no vacíos.
- Resolver rutas de tarea bajo reglas de ruta segura; rechazar directorios, symlinks si se leen archivos y rutas fuera del directorio permitido definido en implementación.
- Invocar con `subprocess` en forma de lista, nunca con `shell=True`.
- No interpolar texto de tarea en comandos ni guardarlo en logs.
- El modo `--dry-run` muestra el ejecutable y flags, pero omite el contenido completo de la tarea.

# 10. Seguridad

## Requisitos relacionados

No hay SEC específico en SPEC-011; aplican las reglas de seguridad para entradas externas, secretos y agentes.

## Autenticación

El CLI elegido autentica mediante su configuración existente. El Harness no solicita ni lee credenciales.

## Autorización

El CLI y sus políticas mantienen la autorización y los permisos de herramientas; el adaptador no los amplía.

## Datos sensibles

El contenido de tarea se entrega al proveedor ya seleccionado por el usuario mediante el CLI. No se registra en logs ni archivos temporales persistentes.

## Secretos

No se aceptan ni almacenan secretos por el ejecutor. Las variables sensibles del proceso se heredan según configuración del CLI y no se imprimen.

## Riesgos relevantes

Una tarea puede contener texto que parezca una opción o comando; mitigación: argumento separado, lista de argumentos y lectura de contenido sin evaluación de shell.

# 11. Estrategia de pruebas

Pruebas unitarias para política, invocación simulada de cada CLI y documentación de una validación manual por runtime. No se requieren cuentas, claves ni llamadas reales a modelos en CI.

## Unitarias

Casos para categorías low/medium/high, señales contradictorias, entrada vacía, agente desconocido, argumento con espacios/metacaracteres y serialización de archivos.

## Integración

Ejecutables falsos en directorios temporales capturan argv/stdin y devuelven éxitos, errores de nivel no soportado y errores genéricos. Verificar que solo el error reconocido activa un único retry sin override.

## End-to-End

Validación manual opcional por CLI real con modelos configurados por el usuario, confirmando la etiqueta aplicada o fallback. No incluir credenciales en evidencia.

## Seguridad

Verificar que argv no evalúa shell, `--dry-run` redacta la tarea, errores no imprimen variables sensibles y no se añaden flags para elevar permisos.

## 11.1 Mapeo inicial

| Criterio | Tipo de prueba previsto |
|----------|-------------------------|
| AC-001 | Integración simulada para tres adaptadores, más smoke manual con cada CLI disponible |
| AC-002 | Integración simulada de rechazo compatible y fallback; caso negativo de error no relacionado |
| AC-003 | Tabla de contrato agente/modelo con nivel soportado y sin soporte |

## 11.2 Estrategia TDD

| Criterio | Automatizable | Caso y comando/nivel | RED viable antes de cambio | Motivo y alternativa si no aplica |
|----------|---------------|----------------------|----------------------------|----------------------------------|
| AC-001 | YES | `python3 -m unittest discover -s tests -p 'test_*effort*.py'` con CLIs falsos | YES | Los contratos argv/stdin y niveles esperados son comprobables sin servicios externos |
| AC-002 | YES | Mismo comando; fake CLI rechaza nivel y después acepta default | YES | El fallback y límite de retries son deterministas |
| AC-003 | YES | Mismo comando con matriz de runtimes/proveedores simulados | YES | La portabilidad de contrato se verifica sin credenciales; complementar con smoke manual |

Preparar casos no autoriza modificar pruebas antes de `/implement`.

# 12. Observabilidad

## Logs

Resumen a `stderr` con runtime, clase, nivel y aplicación/fallback; nunca contenido de tarea, entorno completo ni credenciales.

## Métricas

La salida incluye duración total y clase para permitir comparación manual. No se persisten métricas.

## Auditoría

No aplica; las decisiones no contienen datos persistidos.

## Health checks

El ejecutor informa CLI ausente antes de procesar la tarea.

# 13. Impacto en el repositorio

## Archivos o módulos a crear

- `src/effort_policy.py`
- `src/run_task.py`
- `tests/test_effort_policy.py`
- `tests/test_run_task.py`
- `docs/agents/model-effort.md`
- `docs/decisions/ADR-001-model-effort-runtime-adapters.md`

## Archivos o módulos a modificar

- `src/adopt_harness.py`
- `tests/test_adopt_harness.py`
- `AGENTS.md`
- `docs/quickstart.md`
- `docs/adoption.md`
- `docs/index.md`

## Elementos a reutilizar

- Python estándar, `argparse`, `subprocess`, `pathlib`, y `unittest`.
- Patrones de distribución explícita de `src/adopt_harness.py`.

## Elementos a eliminar

Ninguno.

# 14. Dependencias

## Nuevas dependencias

| Dependencia | Propósito | Justificación/seguridad |
|-------------|-----------|------------------------|
| Ninguna | — | Los procesos externos son CLIs que el usuario ya instaló y configuró. |

# 15. Configuración

Sin configuración persistente nueva. El agente y el modelo se indican en cada invocación; autenticación, proveedores y permisos permanecen en la configuración del CLI correspondiente.

# 16. Migración y compatibilidad

No se cambia formato persistido ni API existente. La adopción incluye el nuevo ejecutor y guía; los proyectos ya adoptados continúan usando sus instrucciones actuales hasta que copien/actualicen los archivos.

## Breaking changes

**¿Existen?:** NO

El ejecutor es opcional; la selección automática requiere invocarlo.

# 17. Manejo de errores

| Error | Tratamiento |
|-------|-------------|
| CLI no encontrado | Mensaje con instalación/configuración requerida; no procesa la tarea |
| Rechazo explícito de effort no soportado | Un solo retry con configuración nativa por defecto; informar fallback |
| Error de autenticación, permisos, red o modelo | Devolver estado del CLI sin retry automático ni exponer secretos |
| Política no puede clasificar con certeza | Elegir `medium` y reportar esa clase |

# 18. Riesgos técnicos

## RISK-001 — Cambios en opciones de los CLIs

**Descripción:** Los argumentos, modelos y variantes disponibles pueden cambiar entre versiones.
**Impacto:** MEDIUM
**Probabilidad:** MEDIUM
**Mitigación:** Adaptadores pequeños, errores sin fallback amplio, contratos falsos y documentación de versiones/capacidades probadas.

## RISK-002 — Heurística de complejidad imperfecta

**Descripción:** Las reglas pueden elegir demasiado o muy poco effort para una descripción ambigua.
**Impacto:** MEDIUM
**Probabilidad:** MEDIUM
**Mitigación:** `medium` como fallback, razón visible, reglas revisables y casos de evaluación representativos.

## RISK-003 — Costo y latencia

**Descripción:** La clasificación por reglas no genera una solicitud adicional, pero las reglas `high` pueden aumentar costo y tiempo de tareas mal clasificadas.
**Impacto:** MEDIUM
**Probabilidad:** MEDIUM
**Mitigación:** Mantener policy conservadora, comparar contra baseline `medium` y revisar mediciones antes de ajustar reglas.

# 19. Aclaraciones técnicas

Ninguna bloqueante. La selección aplica a nuevas invocaciones del ejecutor; cambiar el esfuerzo de una respuesta que ya está en curso queda fuera de los controles de CLI del plan.

# 20. ADR requeridos

| ADR | Decisión | Estado |
|-----|----------|--------|
| ADR-001 — `docs/decisions/ADR-001-model-effort-runtime-adapters.md` | Política común y adaptadores nativos con ejecución por CLI | PENDING |

# 21. Orden de implementación

1. Definir policy pura y casos de clasificación.
2. Construir adaptadores y contrato de ejecución aislado.
3. Implementar fallback limitado, salida y controles de seguridad.
4. Integrar distribución/adopción, instrucciones y documentación.
5. Ejecutar pruebas TDD y validación manual por CLI cuando estén disponibles.

# 22. Criterios para avanzar a Tasks

- [x] SPEC aprobada; MUST cubiertos; diseño, archivos, datos/contratos aplicables definidos.
- [x] Seguridad, pruebas/TDD, dependencias, compatibilidad, riesgos y ADR revisados.
- [x] Sin aclaraciones técnicas bloqueantes; aprobación humana de PLAN registrada.

# 23. Estado del plan

**Estado actual:** APPROVED

Estados: `DRAFT → IN_REVIEW → APPROVED → SUPERSEDED`.

## Aprobación

Solo aprobación humana explícita permite `APPROVED`.

**Aprobado por:** Usuario responsable del proyecto
**Fecha de aprobación:** 2026-10-27
**Decisión explícita y alcance:** «Lo revisé y apruebo el plan», respecto a PLAN-011 v0.1.0; autoriza preparar TASKS-011.
**Registro durable:** `specs/011-task-based-model-effort/decisions.json` con huella antes de TASKS.
