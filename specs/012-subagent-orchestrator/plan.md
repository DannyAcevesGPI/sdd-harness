# Plan Técnico: Orquestador de subagentes con modelo y effort por tarea

**ID:** PLAN-012
**SPEC relacionada:** SPEC-012
**Estado:** APPROVED
**Versión:** 0.2.0
**Fecha:** 2026-10-28

# 1. Precondiciones

- [x] SPEC existe, está `APPROVED`, sin aclaraciones bloqueantes y con MUST→AC.
- [x] Alcance y restricciones conocidos; checker de estado en PASS.

# 2. Resumen técnico

## 2.1 Objetivo

Añadir un modo orquestado opcional para `/implement` y `/validate`. El agente principal sigue un command de orquestación y delega cada unidad a un subagente headless lanzado por CLI con modelo y effort por unidad. Un helper Python determinista calcula el orden, prepara paquetes mínimos, verifica resultados y registra consumo.

## 2.2 Enfoque

- Reutilizar la política de effort (`src/effort_policy.py`) y los adaptadores CLI (`src/run_task.py`) de SPEC-011 en lugar de crear otro mecanismo de ejecución.
- Pasar a código determinista todo lo que no requiere razonamiento: leer TASKS, calcular dependencias y oleadas paralelas, armar paquetes, comparar archivos modificados, ejecutar pruebas y checker y sumar tokens. El LLM orquestador solo lee resultados JSON compactos y decide (NFR-003).
- Biblioteca estándar de Python y `unittest`, como el resto de `src/`; sin dependencias nuevas.

# 3. Requisitos cubiertos

| Requisito | Tipo | Cobertura en el plan |
|-----------|------|----------------------|
| FR-001 | Funcional | `.spec/commands/orchestrate.md` + `orchestrate.py next/dispatch` (DEC-001, DEC-002) |
| FR-002 | Funcional | `delegation.build_packet` desde artefactos, sin entrada de conversación (DEC-004) |
| FR-003 | Funcional | `model_catalog.select_tier` + effort de SPEC-011; log solicitado/aplicado (DEC-003) |
| FR-004 | Funcional | Catálogo `harness-models.json` opcional; sin catálogo no se pasa `--model`; fallback único ante modelo no disponible (DEC-003) |
| FR-005 | Funcional | `task_graph.ready_units` y motivo de detención (DEC-008) |
| FR-006 | Funcional | `delegation.verify` por snapshot de archivos y evidencia exigida (DEC-006) |
| FR-007 | Funcional | Contrato `harness-result` y salida compacta de `dispatch` (DEC-005) |
| FR-008 | Funcional | `evidence/orchestration-log.jsonl` append-only (DEC-007) |
| FR-009 | Funcional (SHOULD) | Un reintento con nivel superior en fallos elegibles (DEC-009) |
| FR-010 | Funcional (SHOULD) | Oleadas con rutas disjuntas; resto en serie (DEC-008) |
| FR-011 | Funcional | Modo solo vía `/orchestrate`; `run_task.py` conserva su CLI (DEC-001) |
| FR-012 | Funcional | `orchestrate.py validate-checks` + unidades de revisión; veredicto del orquestador (DEC-010) |
| NFR-001 | No funcional | `benchmark_orchestration.py` sobre feature sintética; meta ≥ 30 % (DEC-011) |
| NFR-002 | No funcional | Adaptadores Claude Code / Codex / OpenCode; smokes reales (DEC-002) |
| NFR-003 | No funcional | El helper no reenvía la salida cruda; solo JSON compacto (DEC-005) |
| NFR-004 | No funcional | Toda unidad lleva `TASK-XXX` o `VALIDATION-XXX`; el log lo exige (DEC-007) |
| SEC-001 | Seguridad | Verificación de rutas permitidas; violación → `REJECTED` (DEC-006) |
| SEC-002 | Seguridad | Archivos de gate protegidos; cualquier cambio → `REJECTED` (DEC-006) |
| SEC-003 | Seguridad | Lista de flags prohibidos en el constructor de comandos; sin escritura de config (DEC-002) |
| SEC-004 | Seguridad | Redacción de patrones de secreto en paquete y log; no se guarda salida cruda (DEC-004, DEC-007) |
| BR-001 | Regla | Solo modelos del catálogo; no hay catálogo por defecto (DEC-003) |
| BR-002 | Regla | Pisos por tipo de unidad (DEC-003) |
| BR-003 | Regla | El helper no escribe estados de gate; el command se detiene en gates (DEC-001, DEC-006) |

# 4. Contexto técnico existente

## Stack actual

Python 3 con biblioteca estándar; pruebas con `unittest` (`python3 -m unittest discover -s tests`, 72 pruebas en PASS). Sin dependencias de terceros. CLI instalados en el entorno: Claude Code 2.1.312, codex-cli 0.162.1, opencode v2.2.0.

## Componentes existentes relacionados

- `src/effort_policy.py`: clasificación determinista `low/medium/high` con motivo.
- `src/run_task.py`: adaptadores `_command`, detección de effort no soportado y reintento único sin override; validación de rutas de tarea sin symlinks.
- `src/check_harness_state.py`: checker de gates y proyecciones.
- `src/audit_tasks.py`: auditoría de TASKS.
- `.spec/templates/tasks.template.md`: cada TASK declara `**Estado:**`, `**Tipo:**`, `**Depende de:**` y «Alcance permitido» con rutas entre comillas invertidas (`Crear:`/`Modificar:`), formato comprobado en TASKS-011.
- `docs/agents/subagents.md`: contrato mínimo de delegación.
- `docs/decisions/ADR-001-model-effort-runtime-adapters.md`.
- `src/adopt_harness.py`: lista `BASE_FILES`/`SPEC_FILES` copiada al adoptar.

## Restricciones técnicas existentes

- Los CLI exponen salida estructurada: `claude -p --output-format json`, `codex exec --json` (JSONL), `opencode run --format json`. Qué campos de uso reporta cada uno se confirma en implementación (RISK-002).
- El Harness no cambia configuración global ni gestiona credenciales (ADR-001).
- La validación de SPEC-011 está BLOCKED por smokes reales y benchmark (GAP-001/GAP-002).

# 5. Decisiones técnicas

## DEC-001 — Orquestador híbrido: command LLM + helper determinista

**Decisión:** Crear `.spec/commands/orchestrate.md` como protocolo del agente principal en modo orquestado y `src/orchestrate.py` como helper CLI con subcomandos `next`, `dispatch` y `validate-checks`. El agente invoca el helper, lee su JSON y decide: marcar `DONE`/`BLOCKED`, detenerse o continuar. El helper no modifica `tasks.md`, `decisions.json` ni `validation.md`; el orquestador actualiza los estados según el command.
**Justificación:** Mantiene la responsabilidad del agente principal (FR-001, BR-003) y saca del contexto LLM el trabajo mecánico (NFR-003, NFR-001). El modo se activa solo con `/orchestrate` (FR-011).
**Requisitos relacionados:** FR-001, FR-005, FR-011, NFR-003, BR-003; AC-001, AC-005, AC-011.
**Alternativas consideradas:** (a) Orquestador 100 % script que también decide `DONE`: contradice FR-001 y quita juicio sobre bloqueos. (b) Solo instrucciones sin helper: el LLM tendría que leer TASKS completas, comparar archivos y sumar tokens, lo que gasta los tokens que se quieren ahorrar.
**Consecuencias:** Dos piezas que mantener; la frontera queda explícita (el helper informa, el orquestador decide).
**Requiere ADR:** YES (ADR-002)

## DEC-002 — Subagentes como procesos CLI headless

**Decisión:** Cada subagente es una invocación headless del CLI activo (`claude -p`, `codex exec`, `opencode run`) construida con los adaptadores de `run_task.py`. Se extrae un constructor reutilizable `build_command(agent, executable, model | None, level, structured: bool)` que con `model=None` omite `--model` y con `structured=True` añade el formato JSON de cada CLI. La CLI pública de `run_task.py` no cambia. El constructor rechaza flags de omisión de permisos (`--dangerously-skip-permissions`, `--dangerously-bypass-approvals-and-sandbox`, `--yolo` y equivalentes) y no escribe configuración.
**Justificación:** Es el único mecanismo común a los tres runtimes que permite fijar modelo y effort por invocación y obtener uso de tokens (FR-003, NFR-002, EDGE-001). El contexto de cada subagente arranca vacío (FR-002).
**Requisitos relacionados:** FR-002, FR-003, NFR-002, SEC-003; AC-002, AC-003, AC-010.
**Alternativas consideradas:** Subagentes nativos del runtime (p. ej. Agent tool de Claude Code): no existen igual en Codex/OpenCode, no exponen effort por invocación ni uso de tokens de forma portable.
**Consecuencias:** Los permisos de edición de los subagentes son los que el usuario configuró para su CLI en modo headless; si faltan, la unidad termina `BLOCKED` con mensaje claro (RISK-003). La guía documenta cómo configurarlos sin flags de omisión.
**Requiere ADR:** YES (ADR-002)

## DEC-003 — Niveles de modelo, catálogo y pisos

**Decisión:** Niveles comunes `economy`, `standard` y `advanced`. Por defecto el nivel deriva del effort de SPEC-011 (`low→economy`, `medium→standard`, `high→advanced`), con pisos: TASK de tipo `SECURITY` o `MIGRATION` → `advanced`; unidades de `/validate` → al menos `standard`; revisión de seguridad de `/validate` → `advanced` (BR-002). El catálogo es `harness-models.json` en la raíz del proyecto, declarado por el usuario y versionable:

```json
{"schema_version": 1, "runtimes": {"claude": {"economy": "<modelo>", "standard": "<modelo>", "advanced": "<modelo>"}}}
```

Sin archivo o sin entrada para el runtime, no se pasa `--model` (modelo configurado en el runtime) y se informa `model_status=not-selected-no-catalog`. Si falta el nivel pedido, se usa el nivel superior declarado más cercano y, si no hay, el inferior más cercano, sin bajar de un piso de BR-002; si nada cumple el piso, no se pasa `--model` y se informa. Un catálogo inválido (JSON mal formado, esquema desconocido, identificador con espacios o caracteres de control) se ignora por completo, con aviso (EDGE-003). Si el runtime rechaza explícitamente el modelo por no disponible, se hace un único reintento sin `--model` (`model_status=default-fallback`); otros errores no se reintentan por esta vía. El Harness no distribuye catálogo por defecto ni lo copia al adoptar.
**Justificación:** Cumple Q-002 (BR-001), FR-003, FR-004 y BR-002 con un mapeo determinista y explicable.
**Requisitos relacionados:** FR-003, FR-004, BR-001, BR-002; AC-003, AC-004.
**Alternativas consideradas:** Clasificador separado de modelo: duplica señales de `effort_policy`. Catálogo dentro de `.spec/`: `.spec` es normativo y se copia en la adopción.
**Consecuencias:** Modelo y effort se mueven juntos salvo por los pisos; la razón de selección queda en el log para revisarla.
**Requiere ADR:** NO (incluido en ADR-002)

## DEC-004 — Paquete de delegación mínimo

**Decisión:** `delegation.build_packet(feature_dir, unit)` arma un texto con: ID y objetivo de la unidad; feature y fase; sección completa de la TASK; texto solo de los FR/NFR/SEC/BR/AC que la TASK cita (extraído de `spec.md`); DEC citadas (de `plan.md`); rutas permitidas; límites de mutación (archivos protegidos de DEC-006); evidencia esperada (ruta `specs/<feature>/evidence/<task-id>.md` y RED/GREEN cuando TDD aplica); criterios de escalamiento (`BLOCKED` o `[NEEDS CLARIFICATION]`) y el contrato de resultado (DEC-005). La función no recibe historial de conversación. Antes de enviarlo, se aplica la redacción de patrones de secreto (claves tipo `sk-…`, `ghp_…`, `AKIA…`, asignaciones `token|secret|password|api_key = <valor largo>`).
**Justificación:** FR-002 con contexto mínimo, que es la principal fuente de ahorro, más SEC-004.
**Requisitos relacionados:** FR-002, SEC-004, NFR-003; AC-002, AC-010.
**Alternativas consideradas:** Enviar SPEC/PLAN completos: más tokens y más contexto irrelevante.
**Consecuencias:** El subagente puede leer otros archivos del repo por su cuenta si lo necesita; el paquete solo fija el punto de partida.
**Requiere ADR:** NO

## DEC-005 — Contrato de resultado compacto

**Decisión:** El subagente termina su respuesta con un bloque ```` ```harness-result ```` en JSON: `status` (`DONE`, `INCOMPLETE`, `BLOCKED`, `NEEDS_CLARIFICATION`), `files_changed`, `commands` (`cmd`, `exit_code`, `summary`), `evidence`, `tests` (`id`, `red`, `green`), `findings`, `blocks`, cada texto truncado a un máximo fijo. `dispatch` extrae el texto final del JSON del CLI, parsea el bloque y devuelve al orquestador solo `{unit, attempt, tier, model, effort, result, verification, tokens}`. La salida cruda no se imprime ni se guarda. Un bloque ausente o inválido produce `result.status = INVALID_RESULT`.
**Justificación:** FR-007 y NFR-003; también hace verificable FR-006.
**Requisitos relacionados:** FR-006, FR-007, NFR-003; AC-007.
**Alternativas consideradas:** Resumen libre: no verificable. `--output-schema` de Codex: no es portable.
**Consecuencias:** Un subagente que no respeta el contrato no puede pasar a `DONE`.
**Requiere ADR:** NO

## DEC-006 — Verificación por snapshot y archivos protegidos

**Decisión:** Antes de cada oleada, `delegation.snapshot(repo)` guarda el SHA-256 de cada archivo rastreado o no ignorado (`git ls-files -co --exclude-standard`). Después, los cambios son las rutas con hash nuevo, distinto o eliminado. Cada cambio debe pertenecer a las rutas permitidas de la unidad: `Crear`/`Modificar` de la TASK más `specs/<feature>/evidence/<task-id>*.md`. Rutas protegidas, rechazadas siempre: `specs/*/decisions.json`, `specs/*/{spec,plan,tasks,validation}.md`, `.spec/**`, `AGENTS.md`, `handoff.md` y `harness-models.json`. También se rechaza si falta la evidencia exigida o si `files_changed` declarado no coincide con lo observado. Resultado: `verification.status` = `PASS` o `REJECTED` con motivos y rutas. El helper no revierte cambios (no destructivo); el orquestador marca `BLOCKED` e informa.
**Justificación:** SEC-001, SEC-002, FR-006, BR-003, sin depender de la honestidad del subagente.
**Requisitos relacionados:** FR-006, SEC-001, SEC-002, BR-003; AC-006, AC-009.
**Alternativas consideradas:** `git diff` contra HEAD: confunde los cambios previos del usuario. Un worktree por subagente: aísla mejor, pero añade merges y coste. Queda como evolución si RISK-004 se materializa.
**Consecuencias:** En paralelo, la atribución funciona porque las rutas son disjuntas (DEC-008); un cambio fuera de todas las rutas permitidas rechaza la oleada completa.
**Requiere ADR:** NO

## DEC-007 — Registro de delegaciones

**Decisión:** Una línea JSON por intento en `specs/<feature>/evidence/orchestration-log.jsonl`, solo por append: `date`, `unit`, `attempt`, `runtime`, `tier_requested`, `tier_reason`, `model_requested`, `model_status`, `effort_requested`, `effort_status`, `result_status`, `verification_status`, `tokens` (`input`, `output`, `cache_creation`, `cache_read`, `total`) o `null`, `tokens_available`, `packet_chars`, `duration_s`. No incluye prompts, salida cruda ni secretos; los campos de texto pasan por la misma redacción de DEC-004. Rechaza unidades sin ID `TASK-XXX`/`VALIDATION-XXX`.
**Justificación:** FR-008, NFR-004 y EDGE-005: una sesión nueva reconstruye el avance desde `tasks.md` + log.
**Requisitos relacionados:** FR-008, NFR-004, SEC-004; AC-008.
**Alternativas consideradas:** Guardar en `decisions.json`: mezcla gates con telemetría.
**Consecuencias:** El log crece con cada intento; es pequeño (una línea por intento).
**Requiere ADR:** NO

## DEC-008 — Orden, detención y oleadas paralelas

**Decisión:** `task_graph.parse(tasks.md)` obtiene por TASK: estado, tipo, dependencias y rutas permitidas. `ready_units` devuelve las TASK `TODO` cuyas dependencias están todas `DONE`; las que dependen, directa o transitivamente, de una `BLOCKED` se excluyen. `next` agrupa las listas en una oleada: entran en paralelo solo las que tienen rutas declaradas y disjuntas entre sí; una TASK sin rutas parseables va sola. Límite de concurrencia `--max-parallel` (por defecto 2). `next` informa `stop_reason` cuando no hay unidades: `COMPLETED`, `BLOCKED`, `NEEDS_CLARIFICATION` o `CYCLE`. Tras cada oleada con más de una unidad, el helper ejecuta una vez la suite de pruebas del proyecto para detectar interferencias antes de aceptar resultados.
**Justificación:** FR-005, FR-010 (paralelo sin retrabajo, Q-003), EDGE-004.
**Requisitos relacionados:** FR-005, FR-010, BR-003; AC-005, AC-014.
**Alternativas consideradas:** Paralelismo libre: riesgo de retrabajo, excluido por Q-003.
**Consecuencias:** El paralelismo depende de que TASKS declare rutas; `/tasks` debe hacerlo (ya lo exige la plantilla).
**Requiere ADR:** NO

## DEC-009 — Escalamiento único

**Decisión:** Si `result.status` es `INCOMPLETE` o la verificación falla solo por evidencia o pruebas faltantes, se hace un reintento con el nivel siguiente (`economy→standard→advanced`) y effort un nivel mayor, hasta `high`. No se reintenta si: el runner devuelve error (código 2), la salida coincide con patrones de autenticación, permisos, red, límite de uso o cuota, hay violación de rutas o archivos protegidos, o el estado es `BLOCKED`/`NEEDS_CLARIFICATION`. Si la unidad ya está en `advanced`/`high`, no hay reintento. Ambos intentos van al log.
**Justificación:** FR-009 con coste acotado.
**Requisitos relacionados:** FR-009; AC-013.
**Alternativas consideradas:** Reintentos múltiples: gasto no acotado.
**Consecuencias:** Una mala clasificación inicial cuesta como máximo un intento extra.
**Requiere ADR:** NO

## DEC-010 — `/validate` orquestado

**Decisión:** `orchestrate.py validate-checks --feature <id>` ejecuta sin LLM las comprobaciones deterministas (`python3 -m unittest discover -s tests`, `python3 src/check_harness_state.py`, `python3 src/audit_tasks.py` cuando aplique) y devuelve resumen compacto. Luego `dispatch` lanza unidades de revisión `VALIDATION-XXX`: revisión de AC por grupos (nivel `standard`) y revisión de seguridad (nivel `advanced`). Son de solo lectura: cualquier cambio de archivo es `REJECTED`. El orquestador consolida en `validation.md` según la plantilla y emite `SPEC COMPLIANCE` y `FEATURE STATUS`. El helper nunca genera esas líneas.
**Justificación:** FR-012 y la guía de subagentes (un subagente no sustituye la validación final). Ejecutar las pruebas sin LLM evita gastar tokens.
**Requisitos relacionados:** FR-012, BR-002, BR-003; AC-015.
**Alternativas consideradas:** Un solo subagente de validación completo: pierde la consolidación por el orquestador.
**Consecuencias:** El command de orquestación incluye un procedimiento de validación.
**Requiere ADR:** NO

## DEC-011 — Medición de tokens y benchmark

**Decisión:** Tokens totales = `input + output + cache_creation + cache_read` tal como los reporta el CLI, sumados sobre todas las invocaciones (orquestador + subagentes, o el agente único). Feature de referencia: una feature sintética fija en `tests/fixtures/orchestration_benchmark/` (proyecto mínimo con SPEC/PLAN/TASKS aprobados y 4 TASK: una documental, una mecánica, una funcional con pruebas y una de seguridad). `src/benchmark_orchestration.py` copia el fixture a un directorio temporal dos veces y ejecuta: (a) línea base: una invocación headless con el modelo `standard` del catálogo y effort `medium` que implementa todas las TASK; (b) orquestado: invocación headless del orquestador con el mismo modelo siguiendo `/orchestrate`, más sus subagentes. Toma los tokens del JSON de cada CLI y del log. Pasa si `(base − orquestado) / base ≥ 0,30` y ambas ejecuciones terminan TASKS. Runtime principal: Claude Code; Codex/OpenCode solo si reportan uso. Resultado en `specs/012-subagent-orchestrator/evidence/benchmark.md`.
**Justificación:** NFR-001 / AC-012 con la meta de Q-001; fixture reproducible en lugar de re-ejecutar una feature real con estado irrepetible.
**Requisitos relacionados:** NFR-001; AC-012.
**Alternativas consideradas:** Re-ejecutar TASKS de SPEC-010/011: depende del estado del repo y es más caro. Contar solo `input + output` sin cache: ver Q-TECH-001.
**Consecuencias:** El benchmark consume tokens reales y se ejecuta de forma explícita, no en la suite de `unittest`.
**Requiere ADR:** NO

# 6. Arquitectura propuesta

## 6.1 Componentes involucrados

| Componente | Responsabilidad | Cambio |
|------------|-----------------|--------|
| `.spec/commands/orchestrate.md` | Protocolo del orquestador para `/implement` y `/validate` | CREATE |
| `src/task_graph.py` | Parsear TASKS, dependencias, rutas, oleadas y motivo de detención | CREATE |
| `src/model_catalog.py` | Cargar/validar `harness-models.json`, nivel y pisos | CREATE |
| `src/delegation.py` | Paquete, redacción, parseo de resultado, snapshot y verificación | CREATE |
| `src/orchestrate.py` | CLI `next`, `dispatch`, `validate-checks`; ejecución, escalamiento, log y uso de tokens | CREATE |
| `src/benchmark_orchestration.py` | Benchmark NFR-001 | CREATE |
| `src/run_task.py` | Extraer `build_command` con modelo opcional y salida estructurada | MODIFY |
| `src/effort_policy.py` | Clasificación de effort | REUSE |
| `src/adopt_harness.py` | Copiar nuevos archivos al adoptar | MODIFY |
| `docs/decisions/ADR-002-subagent-orchestration.md` | Decisión DEC-001/DEC-002/DEC-003 | CREATE |
| `docs/agents/subagents.md`, `docs/agents/model-effort.md` | Enlazar modo orquestado, niveles de modelo y catálogo | MODIFY |
| `AGENTS.md`, `.spec/commands/implement.md`, `.spec/commands/validate.md` | Una referencia al modo orquestado opcional | MODIFY |

## 6.2 Flujo principal

1. El usuario invoca `/orchestrate implement SPEC-XXX`. El orquestador hace bootstrap y comprueba con el checker que SPEC/PLAN/TASKS estén aprobados.
2. `orchestrate.py next --feature <id>` → JSON con la oleada (IDs, nivel, effort, motivo) o `stop_reason`.
3. El orquestador marca la oleada `IN_PROGRESS` y llama `orchestrate.py dispatch --feature <id> TASK-A [TASK-B]`.
4. El helper toma el snapshot, arma los paquetes, lanza los CLI (en paralelo si hay varias unidades), parsea `harness-result`, verifica, escala si corresponde, registra el log y devuelve JSON compacto.
5. El orquestador marca `DONE` cada unidad con `verification.status = PASS` y `result.status = DONE`; en otro caso `BLOCKED` con motivo. Vuelve a 2.
6. Ante `stop_reason`, informa y se detiene; ante gate humano, se detiene (BR-003).
7. `/orchestrate validate SPEC-XXX`: `validate-checks`, luego `dispatch` de unidades `VALIDATION-XXX`; el orquestador redacta `validation.md` y emite el veredicto.

## 6.3 Dependencias entre componentes

`orchestrate` → `task_graph`, `model_catalog`, `delegation`, `run_task.build_command`, `effort_policy`. `model_catalog` → `effort_policy` (tipos). `delegation` no depende de `orchestrate`. `benchmark_orchestration` → `orchestrate` (lectura de log y uso). Sin ciclos.

# 7. Modelo de datos

No hay base de datos. Persistencia en archivos:

## 7.1 Entidades afectadas

### Catálogo `harness-models.json`

`schema_version` = 1; `runtimes.<claude|codex|opencode>.<economy|standard|advanced>` = identificador de modelo sin espacios ni caracteres de control. Opcional y declarado por el usuario.

### Log `evidence/orchestration-log.jsonl`

Campos de DEC-007; una línea por intento; solo append.

## 7.2 Relaciones

`unit` del log → `TASK-XXX` de `tasks.md` o `VALIDATION-XXX` de `validation.md`.

## 7.3 Restricciones

Esquema validado al leer; entradas inválidas se ignoran con aviso (catálogo) o se rechazan (log sin ID).

## 7.4 Migraciones

**¿Requiere migración?:** NO. No hay cambios destructivos.

# 8. Interfaces y contratos

No hay API HTTP. Contratos CLI:

- `python3 src/orchestrate.py next --feature <feature-id> [--max-parallel N]` → `{"wave": [{"unit", "tier", "effort", "reason"}], "stop_reason": null | "COMPLETED" | "BLOCKED" | "NEEDS_CLARIFICATION" | "CYCLE"}`.
- `python3 src/orchestrate.py dispatch --feature <feature-id> --agent <claude|codex|opencode> UNIT...` → lista de resultados compactos (DEC-005). Código 0 si se procesaron todas las unidades (aunque alguna sea `REJECTED`) y 2 ante error de entrada o runner.
- `python3 src/orchestrate.py validate-checks --feature <feature-id>` → `{"checks": [{"name", "command", "exit_code", "summary"}]}`.
- `python3 src/benchmark_orchestration.py --agent claude [--keep]` → informe con tokens base, orquestado, reducción y PASS/FAIL.
- Contrato `harness-result` de DEC-005; catálogo de DEC-003.
- `python3 src/run_task.py`: interfaz sin cambios (FR-011).

Errores: feature inexistente, TASKS no aprobado, unidad no `TODO` o no lista, agente desconocido → código 2 con mensaje sin datos sensibles.

# 9. Validación de entradas

Entradas no confiables: `harness-models.json` (esquema e identificadores), `tasks.md` (rutas permitidas normalizadas: relativas, sin `..`, sin absolutas, dentro del repo, sin symlinks, reutilizando la regla de `run_task._read_task`), salida de los CLI (JSON tolerante; campos ausentes → no disponible) y bloque `harness-result` (esquema, tipos y truncado). Argumentos CLI validados con `argparse` y listas cerradas.

# 10. Seguridad

## Requisitos relacionados

SEC-001 → AC-006; SEC-002 → AC-009; SEC-003 y SEC-004 → AC-010.

## Autenticación

No aplica al Harness; cada CLI usa la autenticación que configuró el usuario. El Harness no solicita ni lee credenciales.

## Autorización

Límite confiable: el helper verifica las mutaciones (DEC-006) y el orquestador decide. Los subagentes heredan solo los permisos de su CLI; el constructor prohíbe flags de omisión de permisos (DEC-002).

## Datos sensibles

Paquetes y log redactados; la salida cruda de los subagentes se descarta (DEC-004, DEC-005, DEC-007).

## Secretos

Ningún valor real en código, pruebas, fixtures ni evidencia. Las pruebas usan cadenas sintéticas con forma de secreto para verificar la redacción.

## Riesgos relevantes

Mutación fuera de alcance → snapshot + `REJECTED` (TEST de AC-006). Autoaprobación → archivos protegidos (AC-009). Escalada de permisos → lista de flags prohibidos (AC-010). Fuga en log → redacción (AC-010).

# 11. Estrategia de pruebas

## Unitarias

`task_graph` (parseo, dependencias, bloqueo transitivo, oleadas, ciclo), `model_catalog` (mapeo, pisos, catálogo ausente/inválido, nivel faltante), `delegation` (campos del paquete, redacción, parseo de resultado, snapshot y verificación con repos git temporales), `run_task.build_command` (modelo opcional, flags estructurados, flags prohibidos).

## Integración

`orchestrate.py` con CLI falsos en un `PATH` temporal (patrón de `tests/test_run_task.py`): ejecución de una oleada, paralelo, escalamiento, fallback de modelo, log, salida compacta, unidades de validación de solo lectura.

## End-to-End

Smokes reales por runtime (Claude Code, Codex, OpenCode) con el fixture: una TASK mecánica delegada de punta a punta. Benchmark NFR-001 (DEC-011). No forman parte de la suite `unittest` porque consumen tokens reales.

## Seguridad

Casos negativos de AC-006, AC-009 y AC-010 en unitarias e integración.

## 11.1 Mapeo inicial

| Criterio | Tipo de prueba previsto |
|----------|-------------------------|
| AC-001 | Integración: `next` + `dispatch` con CLI falso; unidad con ID trazable |
| AC-002 | Unitaria: campos del paquete; la firma no acepta historial |
| AC-003 | Unitaria + integración: niveles y pisos; log con solicitado/aplicado |
| AC-004 | Unitaria + integración: sin catálogo no hay `--model`; modelo rechazado → un reintento |
| AC-005 | Unitaria: dependientes de una `BLOCKED` excluidos; `stop_reason` |
| AC-006 | Integración (git temporal): ruta no permitida o evidencia faltante → `REJECTED` |
| AC-007 | Integración: stdout del helper sin salida cruda del CLI falso |
| AC-008 | Integración: líneas del log con campos y `tokens=null` cuando no hay uso |
| AC-009 | Integración: cambio en `decisions.json` o en estado de gate → `REJECTED` |
| AC-010 | Unitaria: sin flags prohibidos; redacción de secretos sintéticos; sin escritura de config |
| AC-011 | Regresión: suite existente + `run_task.py` sin cambios + checker PASS |
| AC-012 | Benchmark real (`benchmark_orchestration.py`); aritmética probada con CLI falso |
| AC-013 | Integración: `INCOMPLETE` → un reintento superior; error de auth sin reintento |
| AC-014 | Unitaria: oleadas con rutas disjuntas; integración: ejecución concurrente |
| AC-015 | Integración: `validate-checks` y unidades de solo lectura; el helper no emite veredicto |

## 11.2 Estrategia TDD

| Criterio | Automatizable | Caso y comando/nivel | RED viable antes de cambio | Motivo y alternativa si no aplica |
|----------|---------------|----------------------|----------------------------|----------------------------------|
| AC-001 a AC-011, AC-013 a AC-015 | YES | `python3 -m unittest tests.test_<módulo>`; unitarias/integración con CLI falsos | YES (módulos inexistentes o función faltante) | — |
| AC-012 | NO (en suite) | `python3 src/benchmark_orchestration.py --agent claude` | NO | Consume tokens reales y depende del proveedor; la aritmética y el parseo sí se prueban con TDD; el resultado real va a evidencia |
| Smokes reales NFR-002 | NO (en suite) | Ejecución manual documentada por runtime | NO | Dependen de credenciales y CLI del usuario; evidencia en `evidence/` |
| Docs (command, guía, ADR) | NO | Revisión documental + checker PASS | NO | Documentación sin conducta automatizable |

Preparar casos no autoriza modificar pruebas antes de `/implement`.

# 12. Observabilidad

## Logs

Resumen por unidad en stderr (`unit`, `tier`, `model_status`, `effort_status`, `result`, `verification`), sin contenido de prompts ni salida cruda.

## Métricas

Tokens por intento y total por feature en el log; reducción en el benchmark.

## Auditoría

`orchestration-log.jsonl` y transiciones de TASK en `tasks.md` hechas por el orquestador.

## Health checks

N/A.

# 13. Impacto en el repositorio

## Archivos o módulos a crear

`.spec/commands/orchestrate.md`, `src/task_graph.py`, `src/model_catalog.py`, `src/delegation.py`, `src/orchestrate.py`, `src/benchmark_orchestration.py`, `tests/test_task_graph.py`, `tests/test_model_catalog.py`, `tests/test_delegation.py`, `tests/test_orchestrate.py`, `tests/test_benchmark_orchestration.py`, `tests/fixtures/orchestration_benchmark/**`, `docs/decisions/ADR-002-subagent-orchestration.md`, `specs/012-subagent-orchestrator/evidence/**`.

## Archivos o módulos a modificar

`src/run_task.py`, `tests/test_run_task.py`, `src/adopt_harness.py`, `tests/test_adopt_harness.py`, `docs/agents/subagents.md`, `docs/agents/model-effort.md`, `AGENTS.md`, `.spec/commands/implement.md`, `.spec/commands/validate.md`, `docs/index.md`, `handoff.md`.

## Elementos a reutilizar

`src/effort_policy.py`, adaptadores y validación de rutas de `src/run_task.py`, `src/check_harness_state.py`, `src/audit_tasks.py`, patrón de CLI falsos de `tests/test_run_task.py`.

## Elementos a eliminar

Ninguno.

# 14. Dependencias

## Nuevas dependencias

| Dependencia | Propósito | Justificación/seguridad |
|-------------|-----------|------------------------|
| Ninguna | — | Biblioteca estándar (`json`, `subprocess`, `concurrent.futures`, `hashlib`, `re`) |

# 15. Configuración

`harness-models.json` (opcional, sin secretos; solo identificadores de modelo). `--max-parallel` por argumento. Sin variables de entorno nuevas. Los permisos headless de cada CLI los configura el usuario en su runtime; la guía lo documenta sin flags de omisión.

# 16. Migración y compatibilidad

Sin cambios de formato en artefactos SDD existentes. `run_task.py` conserva su CLI y salida. Proyectos adoptados reciben los nuevos archivos; sin catálogo, el modo orquestado no cambia de modelo.

## Breaking changes

**¿Existen?:** NO

# 17. Manejo de errores

- CLI ausente o error de ejecución → unidad `BLOCKED` (`runner_error`), sin reintento.
- Autenticación, permisos, red, límite de uso o cuota → `BLOCKED` con categoría, sin reintento.
- Resultado inválido → `INVALID_RESULT`; elegible para un reintento solo si no hubo mutación fuera de límites.
- Catálogo inválido → aviso y comportamiento sin catálogo.
- `tasks.md` no parseable o ciclo de dependencias → `stop_reason` y código 2; el orquestador lo eleva a TASKS.
- Uso de tokens ausente → `tokens=null`, `tokens_available=false`.

# 18. Riesgos técnicos

## RISK-001 — Meta del 30 % no alcanzada

**Descripción:** En una feature pequeña, la sobrecarga del orquestador puede reducir el ahorro.
**Impacto:** HIGH
**Probabilidad:** MEDIUM
**Mitigación:** El trabajo mecánico va al helper, no al LLM; paquetes mínimos; niveles bajos para tareas mecánicas. Si el benchmark no alcanza la meta, se registra FAIL honesto y se vuelve a PLAN; no se ajusta la métrica en silencio.

## RISK-002 — Uso de tokens no reportado por algún CLI

**Descripción:** OpenCode, o versiones futuras de los otros CLI, pueden no exponer el uso en su JSON.
**Impacto:** MEDIUM
**Probabilidad:** MEDIUM
**Mitigación:** Parsers tolerantes → `tokens_available=false` (EDGE-002); NFR-001 se mide en Claude Code; la TASK de smokes confirma los campos de cada CLI.

## RISK-003 — Subagentes headless sin permiso de edición

**Descripción:** Sin permisos configurados, `claude -p`/`codex exec` no pueden escribir archivos.
**Impacto:** MEDIUM
**Probabilidad:** HIGH
**Mitigación:** Detección del rechazo → `BLOCKED` con instrucción clara; la guía documenta la configuración del usuario (allowlists) sin flags de omisión.

## RISK-004 — Interferencia entre subagentes en paralelo

**Descripción:** Con rutas disjuntas, las pruebas de un subagente pueden ver los cambios a medio hacer de otro.
**Impacto:** MEDIUM
**Probabilidad:** MEDIUM
**Mitigación:** Concurrencia por defecto de 2; suite completa tras la oleada; ante fallo, se repite en serie. Worktree por subagente como evolución documentada.

## RISK-005 — Clasificación de nivel incorrecta

**Descripción:** Las reglas por palabras clave pueden subestimar una tarea.
**Impacto:** LOW
**Probabilidad:** MEDIUM
**Mitigación:** Pisos por tipo de TASK, escalamiento único y motivo en el log.

## RISK-006 — Validación dependiente de SPEC-011

**Descripción:** SPEC-011 sigue BLOCKED por smokes y benchmark; SPEC-012 reutiliza sus adaptadores.
**Impacto:** MEDIUM
**Probabilidad:** MEDIUM
**Mitigación:** Los smokes reales de SPEC-012 ejercitan los mismos adaptadores; su evidencia puede servir a GAP-001 de SPEC-011 si cubre lo que exige.

# 19. Aclaraciones técnicas

## Q-TECH-001 — Contabilidad de tokens en cache

**Estado:** [CLARIFIED]
**Pregunta:** ¿Los tokens leídos de cache (`cache_read`) cuentan igual que el resto para la meta del 30 %?
**Impacto:** DEC-011, AC-012. Contarlos favorece al modo orquestado, porque un agente único relee su contexto acumulado en cada turno; excluirlos mide solo tokens nuevos.
**Bloqueante:** NO. Propuesta por defecto: contarlos (DEC-011) y reportar también el desglose sin cache.
**Respuesta:** De acuerdo con la propuesta: `cache_read` cuenta en el total para la meta del 30 % y el informe incluye además el desglose sin cache. Usuario responsable del proyecto, 2026-10-28.

# 20. ADR requeridos

| ADR | Decisión | Estado |
|-----|----------|--------|
| ADR-002 | Orquestación híbrida con subagentes CLI headless, niveles de modelo y catálogo del usuario (DEC-001 a DEC-003) | PENDING |

# 21. Orden de implementación

1. ADR-002 y `.spec/commands/orchestrate.md` (base documental).
2. `task_graph` y `model_catalog`, independientes entre sí.
3. `run_task.build_command`, que depende de 2 para los tipos de nivel.
4. `delegation`: paquete, redacción, contrato de resultado, snapshot y verificación.
5. `orchestrate.py`: `next`, `dispatch` (paralelo, escalamiento, fallback de modelo, log, tokens) y `validate-checks`.
6. Adopción y guías (`adopt_harness`, `subagents.md`, `model-effort.md`, `AGENTS.md`, referencias en `implement`/`validate`).
7. Fixture y `benchmark_orchestration.py`.
8. Smokes reales por runtime y ejecución del benchmark, con evidencia.

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
**Fecha de aprobación:** 2026-10-28
**Decisión explícita y alcance:** «Apruebo PLAN-012, Q-TECH-001 de acuerdo con tu propuesta», respecto a PLAN-012 v0.2.0 con Q-TECH-001 resuelta según la propuesta; autoriza preparar TASKS-012.
**Registro durable:** `specs/012-subagent-orchestrator/decisions.json` con huella antes de TASKS.
