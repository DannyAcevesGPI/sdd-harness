# Selección de reasoning effort por tarea

Esta guía define la política portable usada por `src/run_task.py`. El ejecutor
clasifica una tarea antes de iniciar el CLI y traduce la clase a la opción
nativa del agente y modelo seleccionados.

## Clases

| Clase común | Cuándo usarla | Propósito |
|-------------|---------------|-----------|
| `low` | Consulta, revisión o cambio pequeño y acotado; trabajo mecánico con resultado fácil de verificar | Reducir latencia y uso de razonamiento cuando el riesgo es bajo |
| `medium` | Tarea habitual con varios pasos, cambios localizados o decisiones moderadas | Equilibrar rapidez y calidad; también es el valor de respaldo de la política |
| `high` | Seguridad, arquitectura, migraciones, depuración compleja, varios componentes o impacto alto | Dedicar más razonamiento cuando un error tiene mayor costo |

La clasificación es local y determinista. Una señal de alto impacto prevalece
sobre señales de tarea sencilla. Si las señales se contradicen o no permiten
decidir, se usa `medium`. La clase describe la tarea; no cambia de modelo.

## Traducción por runtime

Los nombres del Harness son clases comunes, no garantizan equivalencia exacta
entre fabricantes. Cada adaptador usa el control disponible en el CLI/modelo:

- Claude Code: `--effort` para una invocación.
- Codex CLI: `model_reasoning_effort` como override de la invocación.
- OpenCode: variante del modelo, cuando el catálogo/configuración de ese
  modelo la expone.

El usuario configura autenticación, modelo, proveedor y permisos en su CLI.
El Harness no cambia configuración global, no solicita claves y no amplía
permisos.

## Nivel no disponible

Si el runtime indica explícitamente que no admite el nivel solicitado, el
ejecutor reintenta una sola vez sin override. La tarea usa entonces la
configuración predeterminada del runtime/modelo y el resultado lo indica.
Errores de autenticación, permisos, red, timeout, modelo inexistente u otros
errores no se reintentan como fallback.

## Límite de ejecución

La selección ocurre antes de iniciar cada tarea mediante el ejecutor del
Harness. Usar directamente el CLI o cambiar una solicitud ya iniciada conserva
el comportamiento propio del runtime y no aplica automáticamente esta
política.

## Referencias de controles nativos

- [Referencia del CLI de Claude Code](https://code.claude.com/docs/en/cli-reference)
- [Referencia de configuración de Codex](https://learn.chatgpt.com/docs/config-file/config-reference)
- [Modelos y variantes de OpenCode](https://dev.opencode.ai/v2/docs/models/)
