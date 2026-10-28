# Compatibilidad de CLIs — TASK-006

**Fecha:** 2026-10-27  
**Trazabilidad:** FR-003, NFR-002 → AC-001, AC-002, AC-003 → TEST-015 a TEST-017

## Matriz observada

| CLI | Versión/opciones observadas | Combinación real modelo/proveedor | Estado smoke | Motivo/evidencia |
|-----|-----------------------------|-----------------------------------|--------------|------------------|
| Claude Code | `2.1.312`; `claude --help` expone `--effort` | No confirmada sin leer configuración personal | NOT_RUN | No se hizo solicitud de modelo porque la combinación seleccionada no estaba declarada en la tarea y el consumo/cuota real no estaba confirmado. El contrato del adaptador se verifica con fake CLI en TEST-005..011. |
| Codex CLI | `0.162.1`; `codex exec --help` expone override `-c/--config` | No confirmada sin leer configuración personal | NOT_RUN | No se hizo solicitud de modelo por el mismo límite de configuración/consumo. El contrato de argumentos y fallback se verifica con fake CLI en TEST-005..011. |
| OpenCode | Versión/opciones locales no disponibles | No confirmada | BLOCKED | `opencode --version` y `opencode run --help` requieren escribir el log bajo `/home/dannyac/.local/share/opencode/`; la escritura fue rechazada por el sandbox y la solicitud de escalación fue cancelada. No se modificó configuración ni se evitó el límite. El contrato usa la forma de variantes documentada oficialmente y fake CLI. |

## Pruebas y limitaciones

- TEST-015: NOT_RUN — versión y opción disponibles; falta smoke con combinación configurada y consumo autorizado.
- TEST-016: NOT_RUN — versión y opción disponibles; falta smoke con combinación configurada y consumo autorizado.
- TEST-017: BLOCKED — no se pudo ejecutar siquiera la inspección local de OpenCode por el límite de escritura descrito.
- No se instalaron ni actualizaron CLIs, no se consultaron ni alteraron credenciales/configuraciones y no se guardaron prompts o datos de entorno.
- La evidencia de contratos simulados está en `evidence/task-003.md` y `evidence/task-004.md`. La inspección de versión/opciones no equivale a integración real con un modelo/proveedor.

## Referencias oficiales de CLI

- [Claude Code CLI](https://code.claude.com/docs/en/cli-reference)
- [Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
- [OpenCode models and variants](https://dev.opencode.ai/v2/docs/models/)

## Estado

TEST-015 y TEST-016 quedan NOT_RUN con causa concreta; TEST-017 queda BLOCKED por el entorno. No se afirma PASS para smoke real ni compatibilidad de combinación modelo/proveedor no ejecutada.
