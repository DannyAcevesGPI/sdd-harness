# Smokes reales y benchmark — VALIDATION-002

**Fecha:** 2026-11-03  
**Trazabilidad:** FR-001..003, NFR-001, NFR-002, BR-001 → AC-001..003 → TEST-015..017, GAP-001, GAP-002, FINDING-002  
**Autorización:** el usuario responsable autorizó el consumo real el 2026-11-03,
indicó `claude-sonnet-5-5` para Claude Code y pidió dejar OpenCode como BLOCKED.
No indicó modelo para Codex.

## Entorno

| CLI | Versión | Modelo | Proveedor |
|-----|---------|--------|-----------|
| Claude Code | `2.1.317` | `claude-sonnet-5-5` | Anthropic |
| Codex CLI | `codex-cli 0.162.1` | no indicado | — |
| OpenCode | `opencode v2.2.0` | — | — |

No se leyeron ni modificaron credenciales ni configuración de CLI. Las
ejecuciones se hicieron desde un directorio temporal fuera del repo, con tareas
sintéticas sin datos sensibles.

## TEST-015 — Smoke Claude Code (runner real)

Comando: `python3 src/run_task.py --agent claude --model claude-sonnet-5-5 --task "<tarea>"`

| Tarea | Esperado | Salida | Línea de estado del runner | rc |
|-------|----------|--------|---------------------------|----|
| T1 `Corrige typo en la palabra 'harnes'…` | `harness` | `harness` | `effort=low status=applied duration=6.98s reason=small mechanical task signal detected` | 0 |
| T2 `Cuenta las vocales de 'spec driven development'…` | `7` | `7` | `effort=medium status=applied duration=10.92s reason=no decisive complexity signal; using medium` | 0 |
| T3 `Revisión de security: ¿…concatenar entrada… SQL?…` | `NO` | `NO.` + explicación de inyección SQL | `effort=high status=applied duration=8.89s reason=high-impact work signal detected` | 0 |

El runner clasificó las tres clases, pasó `--effort low|medium|high` nativo y
completó la tarea con el CLI real (AC-001, AC-003 para Claude Code/Anthropic).
**Resultado TEST-015: PASS.**

## Benchmark NFR-001 — policy frente a `medium` fijo

Baseline: `printf '%s' "<tarea>" | claude --model claude-sonnet-5-5 --effort medium -p`,
con las mismas tareas y el mismo modelo. Una ejecución por celda (n=1).

| Tarea | Clase | Policy: resultado / duración | Baseline medium: resultado / duración |
|-------|-------|------------------------------|---------------------------------------|
| T1 | low | correcto / 6,98 s | correcto / 7,30 s |
| T2 | medium | correcto / 10,92 s | correcto / 8,28 s |
| T3 | high | correcto / 8,89 s | correcto / 10,75 s |

Lectura: ambas configuraciones resolvieron 3/3. T2 aplica el mismo nivel en las
dos columnas, así que su diferencia de 2,6 s es ruido de red/servicio. Con n=1
no hay evidencia de mejora de duración ni de calidad, y no se declara ninguna
(PLAN-011 §3, NFR-001). La duración del baseline incluye el arranque del
shell; la de la policy la mide el runner.

## Firma real de rechazo de effort en Claude Code (AC-002 / BR-001)

| Prueba | rc | stderr | Efecto |
|--------|----|--------|--------|
| `claude --model claude-sonnet-5-5 --effort bogus -p` | 0 | `Warning: Unknown --effort value 'bogus' — ignoring it and using the default effort. Valid values: low, medium, high, xhigh, max.` | Tarea completada con effort por defecto |
| `claude --model claude-haiku-5-5 --effort high -p` | 0 | vacío | Aceptado sin warning |

Claude Code no rechaza con error un nivel desconocido: degrada a su valor por
defecto él mismo. Los tres niveles que emite la policy son válidos y se
aceptaron en los dos modelos probados, así que en estas combinaciones no se da
el caso de AC-002. Ver DISCOVERY-001 en `validation.md`.

## TEST-016 — Smoke Codex CLI

NOT_RUN. CLI disponible, pero el usuario no indicó modelo y no se infirió uno
leyendo la configuración personal.

## TEST-017 — Smoke OpenCode

BLOCKED por decisión del usuario del 2026-11-03. Nueva causa observada:
`opencode models` falla con
`ServiceUnavailableError: Location plugins did not finish activating`.

## Regresión

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests` → `Ran 72 tests … OK`.
- `PYTHONDONTWRITEBYTECODE=1 python3 src/check_harness_state.py` → `HARNESS STATE: PASS`.
