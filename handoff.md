# SDD Harness — Live Handoff

Fecha de actualización: 2026-09-30.

Este archivo es estado vivo. No contiene el historial completo de auditorías; ese
detalle se consulta bajo demanda en `docs/audit-history.md`, `specs/` y Git.

---

# 1. Estado actual

```text
Harness: 1.0.0 STABLE
AUDIT-01 through AUDIT-10: PASS
Open audit findings: 0
Next audit finding ID: AUDIT-FINDING-038
```

Baseline auditada:

- `34740af8f8a3d0bf3c86a996adcded4c02fb4185`
- `38a5edc`

No repetir auditorías cerradas salvo que exista evidencia nueva y concreta de
que un artefacto aprobado debe revisarse.

---

# 2. Bootstrap recomendado

Leer en este orden:

1. `AGENTS.md`
2. `.spec/constitution.md`
3. Este `handoff.md`
4. Command aplicable en `.spec/commands/`
5. Standards relevantes en `.spec/standards/`

Quickstart: `docs/quickstart.md`

Índice documental: `docs/index.md`

---

# 3. Features validadas

## SPEC-001 — Audit task management

```text
Path: specs/001-audit-task-management/
SPEC COMPLIANCE: PASS
FEATURE STATUS: VALIDATED
```

Evidencia:

- `specs/001-audit-task-management/validation.md`
- `specs/001-audit-task-management/evidence/`

## SPEC-002 — Agent operating readiness

```text
Path: specs/002-agent-operating-readiness/
SPEC COMPLIANCE: PASS
FEATURE STATUS: VALIDATED
AGENTS.md: 166 lines
```

Evidencia:

- `specs/002-agent-operating-readiness/validation.md`
- `specs/002-agent-operating-readiness/evidence/implementation.md`
- `docs/agents/subagents.md`
- `docs/agents/hooks.md`

## SPEC-003 — Context window optimization

```text
Path: specs/003-context-window-optimization/
SPEC COMPLIANCE: PASS
FEATURE STATUS: VALIDATED
handoff.md: live state under 200 lines
```

Evidencia:

- `specs/003-context-window-optimization/validation.md`
- `specs/003-context-window-optimization/evidence/implementation.md`
- `docs/quickstart.md`
- `docs/index.md`
- `docs/audit-history.md`

---

# 4. Reglas operativas vigentes

- No implementation without an approved specification.
- Para flujo completo: no implementation without approved SPEC, PLAN and TASKS.
- Handoff solo resume estado vivo y enlaza evidencia.
- Evidencia nueva debe vivir en `specs/<feature-id>/evidence/` o artefactos
  dedicados.
- Cambios en Constitución, standards, commands, templates o comportamiento del
  Harness requieren flujo SDD propio.
- No almacenar secretos en documentación, tests, logs ni evidencia.

---

# 5. Próximo trabajo

No hay bloqueos conocidos.

Antes de iniciar una nueva modificación:

1. Identificar si es nueva SPEC, revisión de una feature existente o defecto de
   implementación.
2. Abrir solo los artefactos necesarios según `docs/index.md`.
3. Mantener evidencia fuera de este handoff.
