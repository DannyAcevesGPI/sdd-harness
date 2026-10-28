# ADR-001: Adaptadores de runtime para reasoning effort

**Estado:** Aceptado
**Fecha:** 2026-10-27
**Feature:** SPEC-011 / PLAN-011

## Contexto

SPEC-011 requiere seleccionar effort por tarea en Claude Code, Codex y
OpenCode, con varios proveedores de modelos. El repositorio ofrece guías y
utilidades locales, pero no administra sesiones de esos agentes. Los runtimes
representan effort con controles y variantes diferentes, y algunos modelos no
exponen un control equivalente.

## Decisión

Mantener una política común `low` / `medium` / `high` en el Harness y
despachar cada tarea mediante una invocación local del CLI elegido. Cada
adaptador traduce la clase al control nativo de esa invocación. Si el runtime
rechaza explícitamente el nivel como no soportado, se hace un único reintento
sin override; el Harness no modifica configuración persistente ni gestiona
credenciales.

La clasificación es determinista y local para evitar una solicitud extra al
modelo antes de cada tarea. La salida por defecto ante señales desconocidas o
contradictorias es `medium`.

## Alternativas consideradas

1. **Solo instrucciones o skill compartida.** No garantiza que cada runtime
   aplique una opción nativa de effort a la ejecución que inicia la tarea.
2. **Modificar archivos globales de configuración.** Introduce cambios
   persistentes fuera del proyecto y permisos innecesarios.
3. **Una integración por runtime sin política común.** Duplica reglas y puede
   producir selecciones distintas para la misma tarea.

## Consecuencias

- Para recibir selección automática, la tarea debe iniciarse mediante el
  ejecutor del Harness.
- El uso directo de un CLI queda disponible con sus valores configurados.
- Las clases comunes requieren traducción por runtime/modelo; no son niveles
  idénticos entre proveedores.
- La detección de un nivel no soportado debe ser específica por runtime; los
  errores desconocidos no deben activar reintentos.
- La clasificación por reglas puede equivocarse; `medium` es el fallback y
  la razón de selección debe quedar visible para revisión.

## Trazabilidad

- Requisitos: FR-001, FR-002, FR-003, NFR-001, NFR-002.
- Criterios: AC-001, AC-002, AC-003.
- Decisiones: DEC-001, DEC-002, DEC-003, DEC-004 de PLAN-011.
