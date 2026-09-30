# Subagents Guide

Esta guía define cómo usar subagentes dentro del SDD Harness sin delegar autoridad humana ni romper trazabilidad.

## Principios

- El agente principal conserva responsabilidad por bootstrap, gates, trazabilidad e integración final.
- Un subagente puede inspeccionar, resumir, comparar, probar o preparar hallazgos acotados.
- Un subagente no puede aprobar SPEC, PLAN o TASKS.
- Un subagente no puede ampliar alcance, resolver aclaraciones humanas ni implementar fuera de la TASK autorizada.

## Delegación Mínima

Toda delegación debe incluir:

- Objetivo concreto.
- Feature y fase SDD.
- Artefactos fuente que debe consultar.
- Archivos que puede leer o modificar, si aplica.
- Límites explícitos de mutación.
- Evidencia esperada.
- Criterios para devolver bloqueo o `[NEEDS CLARIFICATION]`.

## Fuentes

El subagente debe respetar la jerarquía del Harness:

1. Decisiones humanas explícitas y aprobadas.
2. `.spec/constitution.md`
3. `.spec/standards/`
4. SPEC, PLAN y TASKS aplicables.
5. Implementación y evidencia.

Si detecta conflicto, debe reportarlo con evidencia. No debe corregirlo en un nivel inferior.

## Evidencia Esperada

El resultado de un subagente debe indicar:

- Archivos revisados.
- Hallazgos con ruta y línea cuando sea posible.
- Requisitos, criterios, decisiones o tareas relacionadas.
- Comandos ejecutados y resultado.
- Límites de la revisión.

## Prohibiciones

Un subagente no debe:

- Autoaprobar artefactos.
- Sustituir la validación final.
- Ocultar fallos o debilitar pruebas.
- Inventar requisitos, permisos, decisiones técnicas o alcance.
- Manejar secretos fuera de mecanismos seguros del entorno.

## Cierre

El agente principal debe revisar la salida del subagente antes de usarla como evidencia y debe registrar cualquier decisión o cambio en el artefacto SDD propietario.
