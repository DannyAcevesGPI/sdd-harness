# Documentation Index

Este índice ayuda a decidir qué leer primero y qué abrir solo bajo demanda.

## Lectura obligatoria de bootstrap

- `AGENTS.md` — índice operativo para agentes.
- `.spec/constitution.md` — reglas no negociables.
- `handoff.md` — estado vivo del repositorio.
- [`CHANGELOG.md`](../CHANGELOG.md) — hitos y cambios relevantes.

## Lectura por fase

- `/specify`: `.spec/commands/specify.md`
- `/clarify`: `.spec/commands/clarify.md`
- `/plan`: `.spec/commands/plan.md`
- `/tasks`: `.spec/commands/tasks.md`
- `/implement`: `.spec/commands/implement.md`
- `/validate`: `.spec/commands/validate.md`

Templates:

- `.spec/templates/specification.template.md`
- `.spec/templates/plan.template.md`
- `.spec/templates/tasks.template.md`
- `.spec/templates/validation.template.md`

## Standards

Consultar solo cuando aplique al trabajo:

- `.spec/standards/architecture.md`
- `.spec/standards/coding.md`
- `.spec/standards/testing.md`
- `.spec/standards/security.md`

## Operación de agentes

- `docs/quickstart.md`
- `docs/adoption.md` — uso del Harness en proyectos nuevos.
- [`docs/tdd.md`](tdd.md) — ciclo TDD y evidencia por tarea.
- `docs/agents/subagents.md`
- `docs/agents/hooks.md`
- [`docs/state-reconstruction.md`](state-reconstruction.md) — registro durable y bootstrap sin chat.

## Evidencia y features

Las aprobaciones de SPEC-001 a SPEC-006 que dependen del chat se tratan como
legado no verificable, sin cambiar sus validaciones.

- `specs/001-audit-task-management/validation.md` — feature de prueba validada.
- `specs/001-audit-task-management/evidence/` — evidencia funcional y adversa.
- `specs/002-agent-operating-readiness/validation.md` — AGENTS compacto, subagentes y hooks.
- `specs/002-agent-operating-readiness/evidence/implementation.md`
- `specs/003-context-window-optimization/validation.md` — handoff vivo y contexto optimizado.
- `specs/003-context-window-optimization/evidence/implementation.md`
- `specs/004-harness-adoption-guide/validation.md` — guía de adopción validada.
- `specs/005-harness-changelog/validation.md` — changelog validado.
- `specs/006-tdd-workflow/validation.md` — TDD validado.
- `specs/007-chat-independent-state/validation.md` — estado sin chat validado.
- `specs/007-chat-independent-state/decisions.json` — registro de decisiones.

## Historia auditada

- `docs/audit-history.md` resume AUDIT-01 a AUDIT-10.
- Git commits relevantes:
  - `34740af8f8a3d0bf3c86a996adcded4c02fb4185` — baseline pre-release auditada.
  - `38a5edc` — cierre AUDIT-10 y promoción a 1.0.0 STABLE.

## Regla de contexto

No abras artefactos largos completos salvo que el command o un hallazgo lo exija.
Prefiere empezar por índices, estados y validaciones.
