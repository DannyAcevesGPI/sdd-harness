# SDD Harness Quickstart

Lectura mínima para iniciar una sesión sin llenar la ventana de contexto.

## 1. Leer primero

1. `AGENTS.md`
2. `.spec/constitution.md`
3. `handoff.md`

Con eso debes saber:

- estado actual del Harness;
- si hay findings abiertos;
- qué feature o fase aplica;
- qué command SDD debes leer completo.

## 2. Elegir command

- Nueva funcionalidad o cambio de comportamiento: `.spec/commands/specify.md`
- Aclaración funcional: `.spec/commands/clarify.md`
- Diseño técnico: `.spec/commands/plan.md`
- Tareas: `.spec/commands/tasks.md`
- Implementación: `.spec/commands/implement.md`
- Validación final: `.spec/commands/validate.md`

Lee solo el command aplicable y los standards relevantes.

## 3. Antes de modificar

Verifica:

- SPEC aprobada para implementar comportamiento.
- PLAN aprobado para decisiones técnicas.
- TASKS aprobadas para modificar artefactos de implementación.
- No hay `[NEEDS CLARIFICATION]` bloqueante.
- La tarea activa permite tocar los archivos objetivo.

## 4. Dónde buscar detalle

- Índice documental: `docs/index.md`
- Historia auditada compacta: `docs/audit-history.md`
- Subagentes: `docs/agents/subagents.md`
- Hooks: `docs/agents/hooks.md`
- Feature de prueba validada: `specs/001-audit-task-management/`
- Optimización operativa validada: `specs/002-agent-operating-readiness/`
- Optimización de contexto: `specs/003-context-window-optimization/`

## 5. Evidencia

En nuevas features, registra evidencia en la carpeta de la feature:

```text
specs/<feature-id>/evidence/
```

`handoff.md` solo debe resumir estado vivo y enlazar evidencia.
