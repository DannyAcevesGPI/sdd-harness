# Tareas: Orquestador de subagentes con modelo y effort por tarea

**ID:** TASKS-012
**SPEC relacionada:** SPEC-012
**PLAN relacionado:** PLAN-012
**Estado:** IN_REVIEW
**Versión:** 0.1.0
**Fecha:** 2026-10-28

# 1. Precondiciones

- [x] SPEC y PLAN `APPROVED`, sin aclaraciones bloqueantes; MUST cubiertos y orden general definido.
- [x] Checker de estado en PASS.

# 2. Objetivo

Dividir PLAN-012 en TASK pequeñas, trazables, verificables, con alcance, dependencias, DoD y evidencia.

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

## TASK-001 — ADR-002 y command de orquestación

**Estado:** TODO
**Tipo:** DOCUMENTATION
**Prioridad:** P1

### Objetivo

Documentar la decisión arquitectónica y el protocolo que sigue el agente principal en modo orquestado para `/implement` y `/validate`.

### Trazabilidad

**Requisitos:** FR-001, FR-005, FR-011, FR-012, BR-003.
**Criterios de aceptación:** AC-001, AC-005, AC-011, AC-015.
**Decisiones del plan:** DEC-001, DEC-002, DEC-003, DEC-010; ADR-002.

### Dependencias

**Depende de:** ninguna.

### Alcance permitido

Crear: `docs/decisions/ADR-002-subagent-orchestration.md`, `.spec/commands/orchestrate.md`. Modificar: ninguna. Reutilizar: `docs/decisions/ADR-001-model-effort-runtime-adapters.md`, `docs/agents/subagents.md`. No modificar: SPEC-012, PLAN-012, otros commands.

### Implementación esperada

ADR-002 con contexto, decisión (DEC-001 a DEC-003), alternativas y consecuencias. Command con: activación opcional, bootstrap y checker, ciclo `next → dispatch → decidir DONE/BLOCKED`, detención ante `stop_reason` o gate humano, prohibición de autoaprobar, procedimiento de `/validate` orquestado (veredicto solo del orquestador) y requisito de permisos headless configurados por el usuario sin flags de omisión.

### Pruebas requeridas

- Revisión documental contra DEC-001 a DEC-003 y DEC-010; `python3 src/check_harness_state.py` en PASS.

### TDD

**Aplicabilidad:** NO APLICA
**Caso RED previsto:** No aplica; documentación sin conducta automatizable.
**Evidencia GREEN esperada:** Revisión de correspondencia registrada y checker PASS.
**Si no aplica:** La revisión documental es la verificación apropiada para ADR y command.

### Validaciones

- [ ] Objetivo, requisitos y AC cubiertos; TEST y regresión relevantes en PASS.
- [ ] Controles de calidad, seguridad y alcance respetados.

### Evidencia esperada

`specs/012-subagent-orchestrator/evidence/task-001.md` con la revisión de correspondencia.

### Definition of Done

- [ ] Resultado cumple SPEC, PLAN y TASK; pruebas requeridas en PASS.
- [ ] RED/GREEN válidos o motivo/alternativa suficiente; sin bloqueos.
- [ ] Evidencia disponible y enlazada.

## TASK-002 — Grafo de tareas, detención y oleadas

**Estado:** TODO
**Tipo:** FEATURE
**Prioridad:** P1

### Objetivo

Parsear TASKS y calcular unidades listas, motivo de detención y oleadas paralelas sin retrabajo.

### Trazabilidad

**Requisitos:** FR-005, FR-010, NFR-004, BR-003.
**Criterios de aceptación:** AC-005, AC-014.
**Decisiones del plan:** DEC-008.

### Dependencias

**Depende de:** ninguna.

### Alcance permitido

Crear: `src/task_graph.py`, `tests/test_task_graph.py`. Modificar: ninguna. Reutilizar: formato de `.spec/templates/tasks.template.md`. No modificar: `src/check_harness_state.py`.

### Implementación esperada

`parse(tasks_path)` → por TASK: ID, estado, tipo, dependencias y rutas permitidas (`Crear`/`Modificar` entre comillas invertidas, normalizadas y rechazando absolutas o con `..`). `ready_units` excluye dependientes directos o transitivos de una `BLOCKED`. `next_wave(max_parallel)` agrupa solo TASK con rutas declaradas y disjuntas; una TASK sin rutas va sola. `stop_reason`: `COMPLETED`, `BLOCKED`, `NEEDS_CLARIFICATION`, `CYCLE`.

### Pruebas requeridas

- `TEST-001` — Parseo de una TASKS de ejemplo: estados, tipo, dependencias y rutas.
- `TEST-002` — Dependientes de una TASK `BLOCKED` no están listos; `stop_reason = BLOCKED` cuando no queda nada ejecutable (AC-005).
- `TEST-003` — Tres TASK listas, dos disjuntas y una que comparte ruta: oleada con las dos disjuntas y la tercera después (AC-014).
- `TEST-004` — Ciclo de dependencias → `CYCLE`; rutas con `..` o absolutas rechazadas.

### TDD

**Aplicabilidad:** OBLIGATORIO para conducta automatizable
**Caso RED previsto:** `python3 -m unittest tests.test_task_graph` falla porque `src/task_graph.py` no existe o carece de la función.
**Evidencia GREEN esperada:** Mismo comando en PASS y suite completa en PASS; detalle en `evidence/task-002.md`.
**Si no aplica:** —

### Validaciones

- [ ] Objetivo, requisitos y AC cubiertos; TEST y regresión relevantes en PASS.
- [ ] Controles de calidad, seguridad y alcance respetados.

### Evidencia esperada

RED/GREEN y resultado de suite en `specs/012-subagent-orchestrator/evidence/task-002.md`.

### Definition of Done

- [ ] Resultado cumple SPEC, PLAN y TASK; pruebas requeridas en PASS.
- [ ] RED/GREEN válidos o motivo/alternativa suficiente; sin bloqueos.
- [ ] Evidencia disponible y enlazada.

## TASK-003 — Catálogo de modelos, niveles y pisos

**Estado:** TODO
**Tipo:** FEATURE
**Prioridad:** P1

### Objetivo

Cargar y validar `harness-models.json` y seleccionar nivel de modelo por unidad con los pisos de BR-002.

### Trazabilidad

**Requisitos:** FR-003, FR-004, BR-001, BR-002.
**Criterios de aceptación:** AC-003, AC-004.
**Decisiones del plan:** DEC-003.

### Dependencias

**Depende de:** ninguna.

### Alcance permitido

Crear: `src/model_catalog.py`, `tests/test_model_catalog.py`. Modificar: ninguna. Reutilizar: `src/effort_policy.py`. No modificar: `src/effort_policy.py`.

### Implementación esperada

`load_catalog(root)` con validación de esquema e identificadores (catálogo inválido → ignorado con aviso). `select_tier(effort, unit_kind)` con mapeo `low→economy`, `medium→standard`, `high→advanced` y pisos (`SECURITY`/`MIGRATION` → `advanced`; validación → `standard`; revisión de seguridad → `advanced`). `resolve_model(catalog, runtime, tier)` con nivel superior más cercano, luego inferior sin violar piso, o `None` con `model_status`.

### Pruebas requeridas

- `TEST-005` — Mapeo effort→nivel y pisos por tipo de unidad (AC-003, BR-002).
- `TEST-006` — Sin catálogo o sin runtime → `None` y `not-selected-no-catalog` (AC-004).
- `TEST-007` — Catálogo inválido (JSON roto, esquema desconocido, identificador con espacios) se ignora con aviso.
- `TEST-008` — Nivel faltante: elige superior más cercano; nunca baja de piso.

### TDD

**Aplicabilidad:** OBLIGATORIO para conducta automatizable
**Caso RED previsto:** `python3 -m unittest tests.test_model_catalog` falla por módulo inexistente.
**Evidencia GREEN esperada:** Mismo comando y suite completa en PASS; detalle en `evidence/task-003.md`.
**Si no aplica:** —

### Validaciones

- [ ] Objetivo, requisitos y AC cubiertos; TEST y regresión relevantes en PASS.
- [ ] Controles de calidad, seguridad y alcance respetados.

### Evidencia esperada

RED/GREEN en `specs/012-subagent-orchestrator/evidence/task-003.md`.

### Definition of Done

- [ ] Resultado cumple SPEC, PLAN y TASK; pruebas requeridas en PASS.
- [ ] RED/GREEN válidos o motivo/alternativa suficiente; sin bloqueos.
- [ ] Evidencia disponible y enlazada.

## TASK-004 — Constructor de comandos reutilizable en el ejecutor

**Estado:** TODO
**Tipo:** TECHNICAL
**Prioridad:** P1

### Objetivo

Extraer `build_command` en `run_task.py` con modelo opcional, salida estructurada y rechazo de flags de omisión de permisos, sin cambiar la CLI pública.

### Trazabilidad

**Requisitos:** FR-003, FR-011, SEC-003, NFR-002.
**Criterios de aceptación:** AC-010, AC-011.
**Decisiones del plan:** DEC-002; ADR-001.

### Dependencias

**Depende de:** ninguna.

### Alcance permitido

Crear: ninguna. Modificar: `src/run_task.py`, `tests/test_run_task.py`. Reutilizar: `_command` y adaptadores existentes. No modificar: interfaz y salida de `python3 src/run_task.py`.

### Implementación esperada

`build_command(agent, executable, model | None, level, structured=False)`: con `model=None` omite `--model` (en OpenCode no aplica variante y lo informa); con `structured=True` añade `--output-format json` (Claude), `--json` (Codex) o `--format json` (OpenCode). Lista cerrada de flags prohibidos verificada antes de devolver el comando. `_command` delega en él.

### Pruebas requeridas

- `TEST-009` — Modelo `None` omite `--model` en los tres runtimes; con modelo, se conserva el comando actual.
- `TEST-010` — `structured=True` añade el flag JSON de cada runtime.
- `TEST-011` — Ningún comando construido contiene flags de omisión de permisos (AC-010); pruebas existentes de `run_task` siguen en PASS (AC-011).

### TDD

**Aplicabilidad:** OBLIGATORIO para conducta automatizable
**Caso RED previsto:** `python3 -m unittest tests.test_run_task` falla porque `build_command` no existe.
**Evidencia GREEN esperada:** Mismo comando y suite completa en PASS; detalle en `evidence/task-004.md`.
**Si no aplica:** —

### Validaciones

- [ ] Objetivo, requisitos y AC cubiertos; TEST y regresión relevantes en PASS.
- [ ] Controles de calidad, seguridad y alcance respetados.

### Evidencia esperada

RED/GREEN y regresión de `run_task` en `specs/012-subagent-orchestrator/evidence/task-004.md`.

### Definition of Done

- [ ] Resultado cumple SPEC, PLAN y TASK; pruebas requeridas en PASS.
- [ ] RED/GREEN válidos o motivo/alternativa suficiente; sin bloqueos.
- [ ] Evidencia disponible y enlazada.

## TASK-005 — Paquete de delegación, redacción y contrato de resultado

**Estado:** TODO
**Tipo:** SECURITY
**Prioridad:** P1

### Objetivo

Construir el paquete mínimo de delegación con redacción de secretos y parsear el bloque `harness-result`.

### Trazabilidad

**Requisitos:** FR-002, FR-007, NFR-003, SEC-004.
**Criterios de aceptación:** AC-002, AC-007, AC-010.
**Decisiones del plan:** DEC-004, DEC-005.

### Dependencias

**Depende de:** TASK-002.

### Alcance permitido

Crear: `src/delegation.py`, `tests/test_delegation.py`. Modificar: ninguna. Reutilizar: `src/task_graph.py`. No modificar: `src/task_graph.py`.

### Implementación esperada

`build_packet(feature_dir, unit)` con todos los campos de DEC-004 a partir de `tasks.md`, solo los IDs citados de `spec.md` y DEC de `plan.md`; sin parámetro de historial. `redact(text)` para los patrones de DEC-004. `parse_result(text)` extrae el último bloque `harness-result`, valida esquema y trunca textos; ausencia o JSON inválido → `INVALID_RESULT`.

### Pruebas requeridas

- `TEST-012` — El paquete contiene objetivo, feature/fase, ID, fuentes, rutas permitidas, límites, evidencia, escalamiento y contrato (AC-002).
- `TEST-013` — El paquete incluye solo los requisitos/AC citados y la firma no acepta historial (AC-002).
- `TEST-014` — Secretos sintéticos (`sk-…`, `ghp_…`, `AKIA…`, `password = …`) quedan redactados (AC-010).
- `TEST-015` — `parse_result` acepta un bloque válido, trunca textos largos y devuelve `INVALID_RESULT` ante ausencia o JSON inválido (AC-007).

### TDD

**Aplicabilidad:** OBLIGATORIO para conducta automatizable
**Caso RED previsto:** `python3 -m unittest tests.test_delegation` falla por módulo inexistente.
**Evidencia GREEN esperada:** Mismo comando y suite completa en PASS; detalle en `evidence/task-005.md`.
**Si no aplica:** —

### Validaciones

- [ ] Objetivo, requisitos y AC cubiertos; TEST y regresión relevantes en PASS.
- [ ] Controles de calidad, seguridad y alcance respetados.

### Evidencia esperada

RED/GREEN en `specs/012-subagent-orchestrator/evidence/task-005.md`.

### Definition of Done

- [ ] Resultado cumple SPEC, PLAN y TASK; pruebas requeridas en PASS.
- [ ] RED/GREEN válidos o motivo/alternativa suficiente; sin bloqueos.
- [ ] Evidencia disponible y enlazada.

## TASK-006 — Verificación por snapshot y archivos protegidos

**Estado:** TODO
**Tipo:** SECURITY
**Prioridad:** P0

### Objetivo

Detectar mutaciones de los subagentes y rechazar cambios fuera de alcance, sobre archivos de gate o sin la evidencia exigida.

### Trazabilidad

**Requisitos:** FR-006, SEC-001, SEC-002, BR-003.
**Criterios de aceptación:** AC-006, AC-009.
**Decisiones del plan:** DEC-006.

### Dependencias

**Depende de:** TASK-005.

### Alcance permitido

Crear: ninguna. Modificar: `src/delegation.py`, `tests/test_delegation.py`. Reutilizar: `git ls-files`, `hashlib`. No modificar: archivos del repositorio durante la verificación (sin revertir).

### Implementación esperada

`snapshot(repo)` con SHA-256 de archivos de `git ls-files -co --exclude-standard`. `verify(before, after, unit, result)` → `PASS` o `REJECTED` con motivos: ruta fuera de las permitidas (más `specs/<feature>/evidence/<task-id>*.md`), ruta protegida de DEC-006, evidencia exigida ausente o `files_changed` declarado distinto del observado.

### Pruebas requeridas

- `TEST-016` — Cambio solo en rutas permitidas y evidencia presente → `PASS`.
- `TEST-017` — Cambio en ruta no permitida o evidencia ausente → `REJECTED` con ruta y motivo (AC-006).
- `TEST-018` — Cambio en `decisions.json` o en `spec/plan/tasks.md` → `REJECTED` (AC-009).
- `TEST-019` — Cambios previos del usuario sin modificar no cuentan como mutación del subagente; `files_changed` falso se detecta.

### TDD

**Aplicabilidad:** OBLIGATORIO para conducta automatizable
**Caso RED previsto:** `python3 -m unittest tests.test_delegation` falla porque `snapshot`/`verify` no existen (repos git temporales).
**Evidencia GREEN esperada:** Mismo comando y suite completa en PASS; detalle en `evidence/task-006.md`.
**Si no aplica:** —

### Validaciones

- [ ] Objetivo, requisitos y AC cubiertos; TEST y regresión relevantes en PASS.
- [ ] Controles de calidad, seguridad y alcance respetados.

### Evidencia esperada

RED/GREEN y casos negativos en `specs/012-subagent-orchestrator/evidence/task-006.md`.

### Definition of Done

- [ ] Resultado cumple SPEC, PLAN y TASK; pruebas requeridas en PASS.
- [ ] RED/GREEN válidos o motivo/alternativa suficiente; sin bloqueos.
- [ ] Evidencia disponible y enlazada.

## TASK-007 — Helper `next`/`dispatch`, registro y tokens

**Estado:** TODO
**Tipo:** FEATURE
**Prioridad:** P1

### Objetivo

Exponer `orchestrate.py next` y `dispatch` para una unidad: selección de modelo y effort, ejecución headless, fallback de modelo, resultado compacto, uso de tokens y registro de delegaciones.

### Trazabilidad

**Requisitos:** FR-001, FR-003, FR-004, FR-007, FR-008, NFR-003, NFR-004.
**Criterios de aceptación:** AC-001, AC-003, AC-004, AC-007, AC-008.
**Decisiones del plan:** DEC-001, DEC-002, DEC-003, DEC-005, DEC-007.

### Dependencias

**Depende de:** TASK-002, TASK-003, TASK-004, TASK-006.

### Alcance permitido

Crear: `src/orchestrate.py`, `tests/test_orchestrate.py`. Modificar: ninguna. Reutilizar: `src/task_graph.py`, `src/model_catalog.py`, `src/delegation.py`, `src/run_task.py`, `src/effort_policy.py`. No modificar: `tasks.md`, `decisions.json` ni `validation.md` de ninguna feature.

### Implementación esperada

`next` imprime el JSON del contrato de PLAN §8. `dispatch` valida que la unidad esté lista, toma snapshot, arma paquete, construye comando estructurado, ejecuta, extrae texto final y uso de tokens del JSON de cada CLI (tolerante: ausente → `null`), reintenta una vez sin `--model` solo ante rechazo explícito de modelo, parsea resultado, verifica, añade línea al log y devuelve solo el JSON compacto. Errores de entrada → código 2.

### Pruebas requeridas

- `TEST-020` — `next` sobre TASKS de ejemplo devuelve oleada con IDs trazables o `stop_reason` (AC-001).
- `TEST-021` — `dispatch` con CLI falso en `PATH` temporal produce resultado compacto con modelo y effort solicitados/aplicados (AC-001, AC-003).
- `TEST-022` — Sin catálogo no se pasa `--model`; rechazo explícito de modelo → un reintento sin `--model` y `model_status=default-fallback` (AC-004).
- `TEST-023` — La salida del helper no contiene la salida cruda del CLI falso (AC-007).
- `TEST-024` — Cada intento añade una línea con los campos de DEC-007; sin uso reportado → `tokens=null`, `tokens_available=false` (AC-008).
- `TEST-025` — Unidad sin ID trazable o no lista → código 2 sin ejecutar CLI.

### TDD

**Aplicabilidad:** OBLIGATORIO para conducta automatizable
**Caso RED previsto:** `python3 -m unittest tests.test_orchestrate` falla por módulo inexistente.
**Evidencia GREEN esperada:** Mismo comando y suite completa en PASS; detalle en `evidence/task-007.md`.
**Si no aplica:** —

### Validaciones

- [ ] Objetivo, requisitos y AC cubiertos; TEST y regresión relevantes en PASS.
- [ ] Controles de calidad, seguridad y alcance respetados.

### Evidencia esperada

RED/GREEN en `specs/012-subagent-orchestrator/evidence/task-007.md`.

### Definition of Done

- [ ] Resultado cumple SPEC, PLAN y TASK; pruebas requeridas en PASS.
- [ ] RED/GREEN válidos o motivo/alternativa suficiente; sin bloqueos.
- [ ] Evidencia disponible y enlazada.

## TASK-008 — Oleadas paralelas y escalamiento único

**Estado:** TODO
**Tipo:** FEATURE
**Prioridad:** P2

### Objetivo

Ejecutar en paralelo las unidades de una oleada y reintentar una vez con nivel superior en fallos elegibles.

### Trazabilidad

**Requisitos:** FR-009, FR-010.
**Criterios de aceptación:** AC-013, AC-014.
**Decisiones del plan:** DEC-008, DEC-009.

### Dependencias

**Depende de:** TASK-007.

### Alcance permitido

Crear: ninguna. Modificar: `src/orchestrate.py`, `tests/test_orchestrate.py`. Reutilizar: `concurrent.futures`. No modificar: módulos de TASK-002 a TASK-006.

### Implementación esperada

`dispatch` con varias unidades de la misma oleada usa hasta `--max-parallel` procesos; tras la oleada ejecuta la suite del proyecto una vez y, si falla, marca las unidades para repetir en serie. Escalamiento según DEC-009, con ambos intentos en el log y sin reintento para errores de runner, autenticación, permisos, red, cuota, violación de rutas, `BLOCKED` o `NEEDS_CLARIFICATION`.

### Pruebas requeridas

- `TEST-026` — Dos unidades disjuntas se ejecutan de forma concurrente con CLI falsos (AC-014).
- `TEST-027` — `INCOMPLETE` → un reintento con nivel y effort superiores; dos líneas de log (AC-013).
- `TEST-028` — Error de autenticación o violación de ruta → sin reintento (AC-013).

### TDD

**Aplicabilidad:** OBLIGATORIO para conducta automatizable
**Caso RED previsto:** Nuevos casos de `tests.test_orchestrate` fallan porque `dispatch` no paraleliza ni escala.
**Evidencia GREEN esperada:** Mismo comando y suite completa en PASS; detalle en `evidence/task-008.md`.
**Si no aplica:** —

### Validaciones

- [ ] Objetivo, requisitos y AC cubiertos; TEST y regresión relevantes en PASS.
- [ ] Controles de calidad, seguridad y alcance respetados.

### Evidencia esperada

RED/GREEN en `specs/012-subagent-orchestrator/evidence/task-008.md`.

### Definition of Done

- [ ] Resultado cumple SPEC, PLAN y TASK; pruebas requeridas en PASS.
- [ ] RED/GREEN válidos o motivo/alternativa suficiente; sin bloqueos.
- [ ] Evidencia disponible y enlazada.

## TASK-009 — `/validate` orquestado

**Estado:** TODO
**Tipo:** FEATURE
**Prioridad:** P1

### Objetivo

Añadir `validate-checks` y el despacho de unidades `VALIDATION-XXX` de solo lectura.

### Trazabilidad

**Requisitos:** FR-012, BR-002, BR-003.
**Criterios de aceptación:** AC-015.
**Decisiones del plan:** DEC-010.

### Dependencias

**Depende de:** TASK-008.

### Alcance permitido

Crear: ninguna. Modificar: `src/orchestrate.py`, `tests/test_orchestrate.py`. Reutilizar: `src/check_harness_state.py`, `src/audit_tasks.py`. No modificar: `validation.md` de ninguna feature.

### Implementación esperada

`validate-checks` ejecuta pruebas, checker y auditoría de TASKS y devuelve resumen compacto. `dispatch` acepta unidades `VALIDATION-XXX` (revisión de AC con piso `standard`, revisión de seguridad con `advanced`), trata cualquier mutación como `REJECTED` y nunca produce líneas `SPEC COMPLIANCE`/`FEATURE STATUS`.

### Pruebas requeridas

- `TEST-029` — `validate-checks` devuelve nombre, comando, código y resumen de cada comprobación (AC-015).
- `TEST-030` — Unidad de validación que modifica un archivo → `REJECTED`; la salida del helper no contiene veredicto (AC-015).

### TDD

**Aplicabilidad:** OBLIGATORIO para conducta automatizable
**Caso RED previsto:** Nuevos casos de `tests.test_orchestrate` fallan porque el subcomando no existe.
**Evidencia GREEN esperada:** Mismo comando y suite completa en PASS; detalle en `evidence/task-009.md`.
**Si no aplica:** —

### Validaciones

- [ ] Objetivo, requisitos y AC cubiertos; TEST y regresión relevantes en PASS.
- [ ] Controles de calidad, seguridad y alcance respetados.

### Evidencia esperada

RED/GREEN en `specs/012-subagent-orchestrator/evidence/task-009.md`.

### Definition of Done

- [ ] Resultado cumple SPEC, PLAN y TASK; pruebas requeridas en PASS.
- [ ] RED/GREEN válidos o motivo/alternativa suficiente; sin bloqueos.
- [ ] Evidencia disponible y enlazada.

## TASK-010 — Adopción y guías

**Estado:** TODO
**Tipo:** CONFIGURATION
**Prioridad:** P2

### Objetivo

Incluir el modo orquestado en la adopción y enlazarlo desde las guías y commands existentes, conservando el flujo sin orquestador.

### Trazabilidad

**Requisitos:** FR-011, NFR-002, BR-001.
**Criterios de aceptación:** AC-011.
**Decisiones del plan:** DEC-001, DEC-003; ADR-002.

### Dependencias

**Depende de:** TASK-001, TASK-009.

### Alcance permitido

Crear: ninguna. Modificar: `src/adopt_harness.py`, `tests/test_adopt_harness.py`, `docs/agents/subagents.md`, `docs/agents/model-effort.md`, `AGENTS.md`, `.spec/commands/implement.md`, `.spec/commands/validate.md`. Reutilizar: listas `BASE_FILES`/`SPEC_FILES`. No modificar: otros commands, standards ni templates.

### Implementación esperada

La adopción copia `src/task_graph.py`, `src/model_catalog.py`, `src/delegation.py`, `src/orchestrate.py` (y sus pruebas) y `.spec/commands/orchestrate.md`, sin copiar `harness-models.json`. Guías: niveles de modelo, catálogo, permisos headless y uso de `/orchestrate`. Una referencia breve al modo opcional en `AGENTS.md`, `implement.md` y `validate.md`.

### Pruebas requeridas

- `TEST-031` — La adopción incluye los nuevos archivos y no copia `harness-models.json`; pruebas existentes de adopción en PASS (AC-011).

### TDD

**Aplicabilidad:** OBLIGATORIO para conducta automatizable
**Caso RED previsto:** `python3 -m unittest tests.test_adopt_harness` falla porque la adopción no incluye los nuevos archivos.
**Evidencia GREEN esperada:** Mismo comando, suite completa y checker en PASS; revisión documental en `evidence/task-010.md`.
**Si no aplica:** Las guías se verifican por revisión documental.

### Validaciones

- [ ] Objetivo, requisitos y AC cubiertos; TEST y regresión relevantes en PASS.
- [ ] Controles de calidad, seguridad y alcance respetados.

### Evidencia esperada

RED/GREEN y revisión de guías en `specs/012-subagent-orchestrator/evidence/task-010.md`.

### Definition of Done

- [ ] Resultado cumple SPEC, PLAN y TASK; pruebas requeridas en PASS.
- [ ] RED/GREEN válidos o motivo/alternativa suficiente; sin bloqueos.
- [ ] Evidencia disponible y enlazada.

## TASK-011 — Feature sintética y benchmark

**Estado:** TODO
**Tipo:** TEST
**Prioridad:** P1

### Objetivo

Crear la feature de referencia y el script que compara tokens entre línea base y modo orquestado.

### Trazabilidad

**Requisitos:** NFR-001.
**Criterios de aceptación:** AC-012.
**Decisiones del plan:** DEC-011; Q-TECH-001.

### Dependencias

**Depende de:** TASK-009.

### Alcance permitido

Crear: `src/benchmark_orchestration.py`, `tests/test_benchmark_orchestration.py`, `tests/fixtures/orchestration_benchmark/`. Modificar: ninguna. Reutilizar: `src/orchestrate.py`, `src/run_task.py`. No modificar: `src/orchestrate.py`.

### Implementación esperada

Fixture con SPEC/PLAN/TASKS aprobados y 4 TASK (documental, mecánica, funcional con pruebas, seguridad). El script copia el fixture a dos directorios temporales, ejecuta línea base y orquestado, suma `input + output + cache_creation + cache_read` y el desglose sin cache, calcula la reducción y emite PASS si es ≥ 30 % y ambas ejecuciones completan TASKS.

### Pruebas requeridas

- `TEST-032` — Con CLI falsos que reportan uso fijo, el cálculo de totales, desglose sin cache y reducción es correcto (AC-012).
- `TEST-033` — Uso no disponible o TASKS incompletas → resultado no concluyente, nunca PASS.

### TDD

**Aplicabilidad:** OBLIGATORIO para conducta automatizable
**Caso RED previsto:** `python3 -m unittest tests.test_benchmark_orchestration` falla por módulo inexistente.
**Evidencia GREEN esperada:** Mismo comando y suite completa en PASS; detalle en `evidence/task-011.md`.
**Si no aplica:** La ejecución real del benchmark va en TASK-012.

### Validaciones

- [ ] Objetivo, requisitos y AC cubiertos; TEST y regresión relevantes en PASS.
- [ ] Controles de calidad, seguridad y alcance respetados.

### Evidencia esperada

RED/GREEN en `specs/012-subagent-orchestrator/evidence/task-011.md`.

### Definition of Done

- [ ] Resultado cumple SPEC, PLAN y TASK; pruebas requeridas en PASS.
- [ ] RED/GREEN válidos o motivo/alternativa suficiente; sin bloqueos.
- [ ] Evidencia disponible y enlazada.

## TASK-012 — Smokes reales y ejecución del benchmark

**Estado:** TODO
**Tipo:** TEST
**Prioridad:** P1

### Objetivo

Demostrar con CLI y modelos reales la delegación de punta a punta por runtime y medir NFR-001.

### Trazabilidad

**Requisitos:** NFR-001, NFR-002, FR-003, FR-004, SEC-003.
**Criterios de aceptación:** AC-003, AC-004, AC-010, AC-012.
**Decisiones del plan:** DEC-002, DEC-011.

### Dependencias

**Depende de:** TASK-010, TASK-011.

### Alcance permitido

Crear: `specs/012-subagent-orchestrator/evidence/smokes.md`, `specs/012-subagent-orchestrator/evidence/benchmark.md`. Modificar: ninguna. Reutilizar: `src/orchestrate.py`, `src/benchmark_orchestration.py`, `harness-models.json` declarado por el usuario. No modificar: configuración global ni permisos de los CLI.

### Implementación esperada

Por runtime (Claude Code, Codex, OpenCode): delegar una TASK mecánica del fixture y registrar modelo/effort solicitados y aplicados, tokens y verificación. Ejecutar `python3 src/benchmark_orchestration.py --agent claude` y registrar totales, desglose sin cache, reducción y veredicto. Sin secretos ni salida cruda en la evidencia.

### Pruebas requeridas

- Smoke real por runtime con resultado y limitaciones documentadas.
- Benchmark real con reducción ≥ 30 % para PASS de AC-012.

### TDD

**Aplicabilidad:** NO APLICA
**Caso RED previsto:** No aplica; ejecución real con proveedores externos y consumo de tokens.
**Evidencia GREEN esperada:** `evidence/smokes.md` y `evidence/benchmark.md` con comandos, resultados y fecha.
**Si no aplica:** Depende de credenciales, modelos y permisos del usuario; se verifica con ejecución real documentada (PLAN §11.2). Sin catálogo o permisos headless del usuario, la TASK queda `BLOCKED`.

### Validaciones

- [ ] Objetivo, requisitos y AC cubiertos; TEST y regresión relevantes en PASS.
- [ ] Controles de calidad, seguridad y alcance respetados.

### Evidencia esperada

`specs/012-subagent-orchestrator/evidence/smokes.md` y `specs/012-subagent-orchestrator/evidence/benchmark.md`.

### Definition of Done

- [ ] Resultado cumple SPEC, PLAN y TASK; pruebas requeridas en PASS.
- [ ] RED/GREEN válidos o motivo/alternativa suficiente; sin bloqueos.
- [ ] Evidencia disponible y enlazada.

# 7. Tareas técnicas

TASK-004 se apoya en DEC-002/ADR-001 y soporta FR-003, FR-011, SEC-003 y AC-010/AC-011. TASK-004 no depende de TASK-003 (PLAN §21 los ordena en secuencia): `build_command` recibe un identificador de modelo, no tipos de nivel, así que pueden ejecutarse en paralelo sin cambio estructural.

# 8. Grafo de dependencias

```text
TASK-001 ───────────────────────────────────────────────┐
TASK-002 ──► TASK-005 ──► TASK-006 ──┐                  │
TASK-002 ────────────────────────────┤                  │
TASK-003 ────────────────────────────┼──► TASK-007 ──► TASK-008 ──► TASK-009 ──┬──► TASK-010 ──┐
TASK-004 ────────────────────────────┘                                         └──► TASK-011 ──┴──► TASK-012
```

Paralelos posibles: {TASK-001, TASK-002, TASK-003, TASK-004} y {TASK-010, TASK-011}, con rutas disjuntas. FILE CONFLICT secuenciado: `src/delegation.py` (TASK-005 → TASK-006) y `src/orchestrate.py` (TASK-007 → TASK-008 → TASK-009).

# 9. Orden sugerido de ejecución

| Orden | Tarea | Depende de | Estado |
|------:|-------|------------|--------|
| 1 | TASK-001 | — | TODO |
| 2 | TASK-002 | — | TODO |
| 3 | TASK-003 | — | TODO |
| 4 | TASK-004 | — | TODO |
| 5 | TASK-005 | TASK-002 | TODO |
| 6 | TASK-006 | TASK-005 | TODO |
| 7 | TASK-007 | TASK-002, TASK-003, TASK-004, TASK-006 | TODO |
| 8 | TASK-008 | TASK-007 | TODO |
| 9 | TASK-009 | TASK-008 | TODO |
| 10 | TASK-010 | TASK-001, TASK-009 | TODO |
| 11 | TASK-011 | TASK-009 | TODO |
| 12 | TASK-012 | TASK-010, TASK-011 | TODO |

La tabla registra progreso; el grafo de dependencias manda sobre el orden sugerido.

# 10. Bloqueos

Ninguno al generar TASKS. Riesgo conocido: TASK-012 requiere `harness-models.json` y permisos headless configurados por el usuario (RISK-003 de PLAN-012).

# 11. Descubrimientos fuera de alcance

Ninguno.

# 12. Matriz de trazabilidad

| Tarea | Requisito | Criterio | Decisión | Prueba |
|-------|-----------|----------|----------|--------|
| TASK-001 | FR-001, FR-005, FR-011, FR-012, BR-003 | AC-001, AC-005, AC-011, AC-015 | DEC-001, DEC-002, DEC-003, DEC-010, ADR-002 | Revisión documental |
| TASK-002 | FR-005, FR-010, NFR-004, BR-003 | AC-005, AC-014 | DEC-008 | TEST-001 a TEST-004 |
| TASK-003 | FR-003, FR-004, BR-001, BR-002 | AC-003, AC-004 | DEC-003 | TEST-005 a TEST-008 |
| TASK-004 | FR-003, FR-011, SEC-003, NFR-002 | AC-010, AC-011 | DEC-002, ADR-001 | TEST-009 a TEST-011 |
| TASK-005 | FR-002, FR-007, NFR-003, SEC-004 | AC-002, AC-007, AC-010 | DEC-004, DEC-005 | TEST-012 a TEST-015 |
| TASK-006 | FR-006, SEC-001, SEC-002, BR-003 | AC-006, AC-009 | DEC-006 | TEST-016 a TEST-019 |
| TASK-007 | FR-001, FR-003, FR-004, FR-007, FR-008, NFR-003, NFR-004 | AC-001, AC-003, AC-004, AC-007, AC-008 | DEC-001, DEC-002, DEC-003, DEC-005, DEC-007 | TEST-020 a TEST-025 |
| TASK-008 | FR-009, FR-010 | AC-013, AC-014 | DEC-008, DEC-009 | TEST-026 a TEST-028 |
| TASK-009 | FR-012, BR-002, BR-003 | AC-015 | DEC-010 | TEST-029, TEST-030 |
| TASK-010 | FR-011, NFR-002, BR-001 | AC-011 | DEC-001, DEC-003, ADR-002 | TEST-031 |
| TASK-011 | NFR-001 | AC-012 | DEC-011 | TEST-032, TEST-033 |
| TASK-012 | NFR-001, NFR-002, FR-003, FR-004, SEC-003 | AC-003, AC-004, AC-010, AC-012 | DEC-002, DEC-011 | Smokes y benchmark reales |

Todos los MUST que requieren implementación tienen TASK; ninguna tarea huérfana. Cobertura de AC: AC-001 (T-001, T-007), AC-002 (T-005), AC-003 (T-003, T-007, T-012), AC-004 (T-003, T-007, T-012), AC-005 (T-001, T-002), AC-006 (T-006), AC-007 (T-005, T-007), AC-008 (T-007), AC-009 (T-006), AC-010 (T-004, T-005, T-012), AC-011 (T-004, T-010), AC-012 (T-011, T-012), AC-013 (T-008), AC-014 (T-002, T-008), AC-015 (T-001, T-009).

# 13. Cambios durante implementación

Cambio de requisito → revisar SPEC; diseño → PLAN; trabajo/dependencias → TASKS. Detener trabajo afectado, evaluar downstream, recuperar aprobación de cada contenido autorizado modificado y comprobar gates antes de continuar. Estado/evidencia sin cambio de trabajo no exige aprobación nueva.

# 14. Criterios para comenzar implementación

- [ ] SPEC/PLAN/TASKS aprobados; MUST, AC, dependencias, alcance, TEST y DoD cubiertos.
- [x] Sin tareas huérfanas, ciclos, dudas o bloqueos impeditivos; checker PASS.

# 15. Estado del documento

**Estado actual:** IN_REVIEW

`DRAFT → IN_REVIEW → APPROVED → IN_PROGRESS → COMPLETED`. La primera TASK inicia `IN_PROGRESS`; todas las requeridas `DONE`, sin bloqueos y con evidencia permiten `COMPLETED`. Esto no valida la feature. Tras finding de implementación, `COMPLETED → IN_PROGRESS` y reapertura según `/implement` §17.1, sin nueva aprobación si el trabajo autorizado no cambia.

## Aprobación

Solo aprobación humana explícita permite `APPROVED`; ejecución inicial requiere ese estado y ledger/checker PASS.

**Aprobado por:** [PENDIENTE]
**Fecha de aprobación:** [PENDIENTE]
**Decisión explícita y alcance:** [PENDIENTE; contenido de la decisión humana.]
**Registro durable:** `specs/012-subagent-orchestrator/decisions.json` con huella normalizada.
