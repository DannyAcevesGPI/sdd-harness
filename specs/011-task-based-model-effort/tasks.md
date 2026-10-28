# Tareas: Ajuste de reasoning effort interoperable por tarea

**ID:** TASKS-011
**SPEC relacionada:** SPEC-011
**PLAN relacionado:** PLAN-011
**Estado:** COMPLETED
**Versión:** 0.1.0
**Fecha:** 2026-10-27

# 1. Precondiciones

- [x] SPEC y PLAN `APPROVED`, sin aclaraciones bloqueantes; MUST cubiertos y orden general definido.
- [x] Checker de estado en PASS antes de generar TASKS.

# 2. Objetivo

Dividir PLAN-011 en tareas trazables para producir una política común, invocaciones seguras para los tres CLIs, fallback controlado, adopción portable y evidencia de compatibilidad.

# 3. Estados de tarea

`TODO → IN_PROGRESS → BLOCKED/DONE`; BLOCKED requiere motivo. `DONE → TODO` solo para reapertura según `/implement` §17.1, conservando finding/evidencia. `CANCELLED` reserva un ID retirado, no es estado activo; requiere revisión y gates si cambia trabajo autorizado.
La línea `**Estado:**` de cada ficha es la fuente operativa: no agregarle
otros campos. La tabla §9 la repite una vez por TASK. `COMPLETED` exige todas
las fichas `DONE` y la misma información en la tabla.

# 4. Prioridades

`P0` crítica/bloqueante, `P1` alta, `P2` normal, `P3` baja; no sustituyen dependencias.

# 5. Convención de identificadores

`TASK-[XXX]`, `TEST-[XXX]` únicos y estables; no renumerar ni reutilizar.

# 6. Tareas

## TASK-001 — Documentar la política y el límite de integración

**Estado:** DONE
**Tipo:** DOCUMENTATION
**Prioridad:** P1

### Objetivo

Crear la guía de política de effort y ADR-001 aprobado en PLAN antes de implementar el ejecutor.

### Trazabilidad

**Requisitos:** FR-001, NFR-001, NFR-002.
**Criterios de aceptación:** AC-001, AC-003.
**Decisiones del plan:** DEC-001, DEC-002, DEC-003; ADR-001.

### Dependencias

**Depende de:** ninguna.

### Alcance permitido

Crear: `docs/agents/model-effort.md`, `docs/decisions/ADR-001-model-effort-runtime-adapters.md`. Modificar: ninguna. Reutilizar: `PLAN-011`. No modificar: SPEC-011 ni PLAN-011.

### Implementación esperada

Documentar clases `low`, `medium`, `high`, señales para selección, decisión por defecto `medium`, controles de cada runtime, límites de soporte, fallback previsto y motivo para ejecutar tareas mediante el nuevo punto de entrada.

### Pruebas requeridas

- Revisión documental de correspondencia entre guía, PLAN-011 y ADR-001.

### TDD

**Aplicabilidad:** NO APLICA
**Caso RED previsto:** No aplica; tarea documental sin comportamiento automatizable.
**Evidencia GREEN esperada:** Revisar que las decisiones documentadas correspondan exactamente a DEC-001 a DEC-004 y no amplíen el alcance.
**Si no aplica:** La revisión de contenido y enlaces es la verificación apropiada para documentación/ADR.

### Validaciones

- [x] Guía y ADR reflejan las decisiones aprobadas y declaran los límites sin prometer soporte no verificado.
- [x] No se modifica implementación.

### Evidencia esperada

Enlaces a los dos documentos y revisión de consistencia registrada en `evidence/task-001.md`.

### Definition of Done

- [x] Resultado cumple SPEC, PLAN y TASK; pruebas requeridas en PASS.
- [x] Justificación de no aplicar TDD documentada; sin bloqueos.
- [x] Evidencia disponible y enlazada.

## TASK-002 — Implementar clasificación determinista de tareas

**Estado:** DONE
**Tipo:** FEATURE
**Prioridad:** P1

### Objetivo

Implementar la política pura que asigna `low`, `medium` o `high` y una razón breve a una descripción de tarea.

### Trazabilidad

**Requisitos:** FR-001, NFR-001, BR-001.
**Criterios de aceptación:** AC-001.
**Decisiones del plan:** DEC-002.

### Dependencias

**Depende de:** TASK-001.

### Alcance permitido

Crear: `src/effort_policy.py`, `tests/test_effort_policy.py`. Modificar: ninguna. Reutilizar: estándar Python y `unittest`. No modificar: adaptadores CLI ni documentación de adopción.

### Implementación esperada

Usar reglas explícitas y repetibles para trabajos pequeños/mecánicos (`low`), rutinarios con varios pasos (`medium`) y seguridad, arquitectura, migración, depuración compleja o alto impacto (`high`). Ante ambigüedad/conflicto usar `medium`. Mantener la función independiente de procesos, red y proveedor.

### Pruebas requeridas

- `TEST-001` — tarea mecánica y acotada → `low`.
- `TEST-002` — tarea rutinaria de varios pasos → `medium`.
- `TEST-003` — tarea de seguridad, arquitectura o migración → `high`.
- `TEST-004` — entrada ambigua o señales contradictorias → `medium`.

### TDD

**Aplicabilidad:** OBLIGATORIO para comportamiento automatizable
**Caso RED previsto:** Añadir `TEST-001` a `TEST-004` y ejecutar `python3 -m unittest discover -s tests -p 'test_effort_policy.py' -v`; registrar que fallan por el módulo/reglas ausentes.
**Evidencia GREEN esperada:** Ejecutar el mismo comando y registrar PASS para cada clase, fallback y casos de borde.
**Si no aplica:** No aplica.

### Validaciones

- [x] Todos los casos de policy son deterministas y no dependen del modelo, runtime o idioma del sistema.
- [x] La selección y su razón coinciden con la guía de TASK-001.

### Evidencia esperada

Resultado RED y GREEN de `TEST-001` a `TEST-004` en `evidence/task-002.md`.

### Definition of Done

- [ ] Resultado cumple SPEC, PLAN y TASK; pruebas requeridas en PASS.
- [ ] RED/GREEN válidos; sin bloqueos.
- [ ] Evidencia disponible y enlazada.

## TASK-003 — Implementar el ejecutor y adaptadores CLI

**Estado:** DONE
**Tipo:** FEATURE
**Prioridad:** P1

### Objetivo

Ejecutar una tarea mediante Claude Code, Codex CLI u OpenCode con el nivel seleccionado antes de iniciar el proceso.

### Trazabilidad

**Requisitos:** FR-001, FR-003, NFR-002, BR-001.
**Criterios de aceptación:** AC-001, AC-003.
**Decisiones del plan:** DEC-001, DEC-003, DEC-004; ADR-001.

### Dependencias

**Depende de:** TASK-002.

### Alcance permitido

Crear: `src/run_task.py`, `tests/test_run_task.py`. Modificar: ninguna. Reutilizar: `src/effort_policy.py`, `subprocess`, CLI instalados. No modificar: autenticación ni configuración persistente de los CLIs.

### Implementación esperada

Validar agente/modelo/entrada y construir invocaciones como lista de argumentos sin `shell=True`. Traducir el nivel a las opciones nativas aprobadas en PLAN-011. Incluir `--dry-run` redactado, separar stdout/stderr y conservar los códigos de salida. No activar opciones de autoaprobación ni alterar permisos. El texto no debe convertirse en opciones de CLI ni registrarse en salida diagnóstica.

### Pruebas requeridas

- `TEST-005` — cada agente recibe el modelo, el nivel y el prompt/archivo en el formato previsto.
- `TEST-006` — dry-run muestra agente y opciones sin revelar el texto de tarea.
- `TEST-007` — metacaracteres, espacios y texto con prefijo de opción se tratan como datos, sin evaluación de shell.
- `TEST-008` — agente/modelo/archivo inválido o ejecutable ausente falla de forma controlada.

### TDD

**Aplicabilidad:** OBLIGATORIO para comportamiento automatizable
**Caso RED previsto:** Añadir `TEST-005` a `TEST-008` con ejecutables falsos temporales y ejecutar `python3 -m unittest discover -s tests -p 'test_run_task.py' -v`; registrar las fallas iniciales de contrato.
**Evidencia GREEN esperada:** Ejecutar el mismo comando; confirmar argv/stdin capturados, salida separada, redacción y códigos de error.
**Si no aplica:** No aplica.

### Validaciones

- [x] La invocación no usa shell y no cambia la política de permisos de ningún CLI.
- [x] Los tres adaptadores preservan modelo y proveedor elegidos por el usuario.
- [x] El resultado indica el nivel pedido y si el CLI aceptó el override.

### Evidencia esperada

RED/GREEN de `TEST-005` a `TEST-008` en `evidence/task-003.md`.

### Definition of Done

- [x] Resultado cumple SPEC, PLAN y TASK; pruebas requeridas en PASS.
- [x] RED/GREEN válidos; sin bloqueos.
- [x] Evidencia disponible y enlazada.

## TASK-004 — Implementar fallback y tratamiento seguro de errores

**Estado:** DONE
**Tipo:** SECURITY
**Prioridad:** P1

### Objetivo

Permitir continuar con el valor predeterminado únicamente cuando el runtime rechaza explícitamente el nivel por falta de soporte.

### Trazabilidad

**Requisitos:** FR-002, FR-003, BR-001.
**Criterios de aceptación:** AC-002, AC-003.
**Decisiones del plan:** DEC-003, DEC-004; ADR-001.

### Dependencias

**Depende de:** TASK-003.

### Alcance permitido

Crear: ninguno. Modificar: `src/run_task.py`, `tests/test_run_task.py`. Reutilizar: ejecutor y adaptadores de TASK-003. No modificar: niveles de policy ni archivos de configuración de usuario.

### Implementación esperada

Reconocer de forma acotada el error de nivel no soportado, ejecutar un único retry sin override y comunicar fallback. No reintentar errores de autenticación, permiso, red, timeout, modelo inexistente u otros errores genéricos. No imprimir entorno o credenciales.

### Pruebas requeridas

- `TEST-009` — rechazo por effort no soportado antes de ejecutar → un retry por defecto y mensaje de fallback.
- `TEST-010` — error de auth/permisos/red/modelo → sin retry y código/diagnóstico seguro.
- `TEST-011` — segundo rechazo → termina sin ciclo de reintentos.

### TDD

**Aplicabilidad:** OBLIGATORIO para comportamiento automatizable
**Caso RED previsto:** Añadir `TEST-009` a `TEST-011` y ejecutar `python3 -m unittest discover -s tests -p 'test_run_task.py' -v`; usar fake CLI para reproducir cada secuencia de salida y estado.
**Evidencia GREEN esperada:** Ejecutar el mismo comando y confirmar exactamente cero o un retry según el error, con resultado final reportado correctamente.
**Si no aplica:** No aplica.

### Validaciones

- [x] Solo la condición de incompatibilidad explícita inicia fallback.
- [x] Se conserva la salida y se informa cuándo el nivel predeterminado fue usado.
- [x] No se filtran secretos ni se amplían permisos.

### Evidencia esperada

RED/GREEN de `TEST-009` a `TEST-011` en `evidence/task-004.md`.

### Definition of Done

- [x] Resultado cumple SPEC, PLAN y TASK; pruebas requeridas en PASS.
- [x] RED/GREEN válidos; sin bloqueos.
- [x] Evidencia disponible y enlazada.

## TASK-005 — Integrar adopción y documentación de uso

**Estado:** DONE
**Tipo:** FEATURE
**Prioridad:** P1

### Objetivo

Distribuir el ejecutor y la política al adoptar el Harness, e indicar cómo usarlo desde cada CLI y sus límites.

### Trazabilidad

**Requisitos:** FR-001, FR-002, FR-003, NFR-002.
**Criterios de aceptación:** AC-001, AC-002, AC-003.
**Decisiones del plan:** DEC-001, DEC-003, DEC-004.

### Dependencias

**Depende de:** TASK-001, TASK-003 y TASK-004.

### Alcance permitido

Crear: ninguno. Modificar: `src/adopt_harness.py`, `tests/test_adopt_harness.py`, `AGENTS.md`, `docs/quickstart.md`, `docs/adoption.md`, `docs/index.md`. Reutilizar: lista explícita de archivos reutilizables en `adopt_harness.py`. No modificar: comandos/templates SDD ni SPEC/PLAN aprobados.

### Implementación esperada

Agregar ejecutor, policy, tests y guía a los archivos que se copian al adoptar; documentar comandos, clasificación, fallback, requisitos previos y que el ajuste automático requiere invocar el runner. Mantener el uso directo de CLIs claramente descrito como ejecución con configuración nativa.

### Pruebas requeridas

- `TEST-012` — adopción limpia copia todos los archivos requeridos y el checker de destino reconoce el Harness.
- `TEST-013` — colisión/archivo faltante conserva rechazo sin copia parcial.
- `TEST-014` — enlaces y comandos documentados apuntan a archivos y opciones existentes.

### TDD

**Aplicabilidad:** OBLIGATORIO para comportamiento automatizable
**Caso RED previsto:** Ajustar `TEST-012` a `TEST-014` en `tests/test_adopt_harness.py` y ejecutar `python3 -m unittest discover -s tests -p 'test_adopt_harness.py' -v`; registrar el fallo por lista de archivos/documentación incompleta.
**Evidencia GREEN esperada:** Ejecutar el mismo comando y validar adopción completa, rechazo seguro de colisiones y enlaces documentados.
**Si no aplica:** No aplica.

### Validaciones

- [x] La adopción incluye cada archivo nuevo necesario y no incluye configuración o secretos del CLI.
- [x] Las instrucciones de Claude Code, Codex y OpenCode concuerdan con los adaptadores.
- [x] El quickstart deja claro el punto de entrada.

### Evidencia esperada

RED/GREEN de `TEST-012` a `TEST-014` en `evidence/task-005.md`, junto con lista de rutas distribuidas.

### Definition of Done

- [x] Resultado cumple SPEC, PLAN y TASK; pruebas requeridas en PASS.
- [x] RED/GREEN válidos; sin bloqueos.
- [x] Evidencia disponible y enlazada.

## TASK-006 — Verificar compatibilidad de los tres CLIs

**Estado:** DONE
**Tipo:** TEST
**Prioridad:** P2

### Objetivo

Confirmar que las opciones nativas generadas por los adaptadores corresponden a las versiones instaladas de Claude Code, Codex CLI y OpenCode, y registrar los casos disponibles de proveedor/modelo.

### Trazabilidad

**Requisitos:** FR-003, NFR-002.
**Criterios de aceptación:** AC-001, AC-002, AC-003.
**Decisiones del plan:** DEC-001, DEC-003, DEC-004; ADR-001.

### Dependencias

**Depende de:** TASK-003, TASK-004 y TASK-005.

### Alcance permitido

Crear: `specs/011-task-based-model-effort/evidence/task-006-compatibility.md`. Modificar: ninguno. Reutilizar: CLIs ya instalados y configuración/credenciales aportados por el usuario. No modificar: credenciales, configuración global, permisos o modelo seleccionado.

### Implementación esperada

Ejecutar una verificación mínima con cada CLI disponible y registrar agente, versión, modelo/proveedor probado, nivel aplicado o fallback y resultado. Usar solo configuraciones ya existentes; no instalar ni actualizar CLIs. Si una llamada real requiere autenticación, permiso, conexión o gasto no disponible, registrar `BLOCKED`/`NOT_RUN` y causa sin simular PASS.

### Pruebas requeridas

- `TEST-015` — smoke de Claude Code con nivel aceptado o fallback reportado.
- `TEST-016` — smoke de Codex CLI con nivel aceptado o fallback reportado.
- `TEST-017` — smoke de OpenCode con variante aceptada o fallback reportado.

### TDD

**Aplicabilidad:** NO APLICA
**Caso RED previsto:** No aplica; son verificaciones de integración manual que dependen de CLIs, modelos, credenciales y disponibilidad externa.
**Evidencia GREEN esperada:** Registrar por cada smoke la versión, combinación y resultado real, o una causa explícita de bloqueo/NOT_RUN.
**Si no aplica:** No se puede reproducir el comportamiento de una cuenta real con una prueba local determinista; las integraciones simuladas ya cubren los contratos.

### Validaciones

- [x] No instalar, actualizar, autenticar ni cambiar configuración para ejecutar los smokes.
- [x] Resultado identifica con claridad qué combinaciones se probaron y cuáles no.
- [x] La evidencia no contiene tokens, prompts sensibles ni datos de entorno.

### Evidencia esperada

Matriz y resultados en `evidence/task-006-compatibility.md`; enlazados desde la validación final.

### Definition of Done

- [x] Cada smoke ejecutado tiene resultado; los no ejecutados tienen motivo concreto.
- [x] No se alteró configuración ni se guardaron secretos.
- [x] Evidencia disponible y enlazada.

# 7. Tareas técnicas

TASK-001 se justifica por DEC-001/DEC-002 y FR-001/AC-001; TASK-003 y TASK-004 implementan las decisiones de adaptadores/fallback y se trazan a FR/AC reales. Ninguna tarea se apoya solo en otra tarea.

# 8. Grafo de dependencias

```text
TASK-001 → TASK-002 → TASK-003 → TASK-004 → TASK-005 → TASK-006
```

# 9. Orden sugerido de ejecución

| Orden | Tarea | Depende de | Estado |
|------:|-------|------------|--------|
| 1 | TASK-001 | — | DONE |
| 2 | TASK-002 | TASK-001 | DONE |
| 3 | TASK-003 | TASK-002 | DONE |
| 4 | TASK-004 | TASK-003 | DONE |
| 5 | TASK-005 | TASK-001, TASK-003, TASK-004 | DONE |
| 6 | TASK-006 | TASK-003, TASK-004, TASK-005 | DONE |

# 10. Bloqueos

Ninguno conocido durante la descomposición.

# 11. Descubrimientos fuera de alcance

Ninguno.

# 12. Matriz de trazabilidad

| Tarea | Requisito | Criterio | Decisión | Prueba |
|-------|-----------|----------|----------|--------|
| TASK-001 | FR-001, NFR-001 | AC-001, AC-003 | DEC-001, DEC-002, ADR-001 | Revisión documental |
| TASK-002 | FR-001, NFR-001, BR-001 | AC-001 | DEC-002 | TEST-001 a TEST-004 |
| TASK-003 | FR-001, FR-003, NFR-002 | AC-001, AC-003 | DEC-001, DEC-003, DEC-004, ADR-001 | TEST-005 a TEST-008 |
| TASK-004 | FR-002, FR-003, BR-001 | AC-002, AC-003 | DEC-003, DEC-004, ADR-001 | TEST-009 a TEST-011 |
| TASK-005 | FR-001, FR-002, FR-003, NFR-002 | AC-001 a AC-003 | DEC-001, DEC-003, DEC-004 | TEST-012 a TEST-014 |
| TASK-006 | FR-003, NFR-002 | AC-001 a AC-003 | DEC-001, DEC-003, DEC-004, ADR-001 | TEST-015 a TEST-017 |

# 13. Cambios durante implementación

Cambio de requisito → revisar SPEC; diseño → PLAN; trabajo/dependencias → TASKS. Detener trabajo afectado, evaluar downstream, recuperar aprobación de cada contenido autorizado modificado y comprobar gates antes de continuar. Estado/evidencia sin cambio de trabajo no exige aprobación nueva.

# 14. Criterios para comenzar implementación

- [x] SPEC/PLAN/TASKS aprobados; MUST, AC, dependencias, alcance, TEST y DoD cubiertos.
- [x] Sin tareas huérfanas, ciclos, dudas o bloqueos impeditivos; checker PASS.

# 15. Estado del documento

**Estado actual:** COMPLETED

`DRAFT → IN_REVIEW → APPROVED → IN_PROGRESS → COMPLETED`. La primera TASK inicia `IN_PROGRESS`; todas las requeridas `DONE`, sin bloqueos y con evidencia permiten `COMPLETED`. Esto no valida la feature. Tras finding de implementación, `COMPLETED → IN_PROGRESS` y reapertura según `/implement` §17.1, sin nueva aprobación si el trabajo autorizado no cambia.

## Aprobación

Solo aprobación humana explícita permite `APPROVED`; ejecución inicial requiere ese estado y ledger/checker PASS.

**Aprobado por:** Usuario responsable del proyecto
**Fecha de aprobación:** 2026-10-27
**Decisión explícita y alcance:** «Esta aprobada», respecto a TASKS-011 v0.1.0; autoriza ejecutar TASK-001 a TASK-006 según dependencias.
**Registro durable:** `specs/011-task-based-model-effort/decisions.json` con huella normalizada.
