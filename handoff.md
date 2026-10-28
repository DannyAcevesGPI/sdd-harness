# SDD Harness — Live Handoff

Fecha de actualización: 2026-10-28.

```json harness-state
{"schema_version": 1, "active": [{"id": "SPEC-011", "phase": "VALIDATE", "next": "/validate"}, {"id": "SPEC-012", "phase": "TASKS", "next": "approve TASKS"}], "validated": ["SPEC-001", "SPEC-002", "SPEC-003", "SPEC-004", "SPEC-005", "SPEC-006", "SPEC-007", "SPEC-008", "SPEC-009", "SPEC-010"]}
```

Este archivo es estado vivo. No contiene el historial completo de auditorías; ese
detalle se consulta bajo demanda en `docs/audit-history.md`, `specs/` y Git.

SPEC-011 tiene TASKS COMPLETED y validación BLOCKED: los contratos simulados y
la suite local pasan, pero faltan smokes reales por CLI/modelo y el benchmark
NFR-001. Detalle en `specs/011-task-based-model-effort/validation.md` y
`specs/011-task-based-model-effort/evidence/task-006-compatibility.md`.

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

Las aprobaciones de SPEC-001 a SPEC-006 cuya prueba depende del chat son
**legado no verificable**. Sus estados de validación se conservan; no se
inventan respaldos retroactivos. Protocolo nuevo: `docs/state-reconstruction.md`.

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

## SPEC-004 a SPEC-006 — Features posteriores

Todas tienen `SPEC COMPLIANCE: PASS` y `FEATURE STATUS: VALIDATED`:

- SPEC-004: `specs/004-harness-adoption-guide/validation.md`
- SPEC-005: `specs/005-harness-changelog/validation.md`
- SPEC-006: `specs/006-tdd-workflow/validation.md`

El detalle y la evidencia permanecen en sus carpetas `specs/`.

## SPEC-007 — Estado reconstruible sin chat

```text
SPEC COMPLIANCE: PASS
FEATURE STATUS: VALIDATED
```

- `specs/007-chat-independent-state/validation.md`
- `specs/007-chat-independent-state/decisions.json`
- `docs/state-reconstruction.md`

## SPEC-008 — Adopción portable del Harness

```text
SPEC COMPLIANCE: PASS
FEATURE STATUS: VALIDATED
```

- `specs/008-portable-harness-adoption/validation.md`
- `specs/008-portable-harness-adoption/evidence/implementation.md`
- `specs/008-portable-harness-adoption/evidence/ci.md` — primer CI remoto PASS.

## SPEC-009 — Concisión de `.spec`

```text
SPEC COMPLIANCE: PASS
FEATURE STATUS: VALIDATED
```

- `specs/009-spec-docs-concision/validation.md`
- `specs/009-spec-docs-concision/evidence/`

## SPEC-010 — Gates de validación y estados de tarea

```text
SPEC COMPLIANCE: PASS
FEATURE STATUS: VALIDATED
```

- `specs/010-validation-gates/validation.md`
- `specs/010-validation-gates/decisions.json`

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

## 5.1 Retomar aquí (sesión del 2026-10-28 → 2026-10-29)

Estado al cierre:

| Feature | SPEC | PLAN | TASKS | Validación |
|---------|------|------|-------|------------|
| SPEC-011 effort por tarea | APPROVED | APPROVED | COMPLETED | BLOCKED (FINDING-002: smokes reales y benchmark) |
| SPEC-012 orquestador de subagentes | APPROVED v0.3.0 (DECISION-005) | APPROVED v0.2.0 (DECISION-007) | IN_REVIEW v0.1.0, 12 TASK | — |

```text
Bloqueos conocidos: 1 (validación SPEC-011)
Próxima acción: aprobación humana de TASKS-012; luego /implement SPEC-012
```

Pasos para continuar:

1. Bootstrap (§2) y `python3 src/check_harness_state.py` → debe dar PASS.
2. Revisar `specs/012-subagent-orchestrator/tasks.md`. Solo con aprobación
   humana explícita: metadatos `APPROVED`, huella con `canonical_bytes`, evento
   `APPROVAL` en `specs/012-subagent-orchestrator/decisions.json` (siguiente ID:
   DECISION-008) y checker PASS.
3. `/implement SPEC-012`, primera oleada paralela con rutas disjuntas:
   TASK-001, TASK-002, TASK-003, TASK-004. Después TASK-005 → TASK-006 →
   TASK-007 → TASK-008 → TASK-009 → {TASK-010, TASK-011} → TASK-012. TDD
   obligatorio salvo TASK-001 y TASK-012 (justificado en TASKS).
4. Antes de TASK-012 (prerrequisitos del usuario):
   - Declarar `harness-models.json` en la raíz (niveles `economy`, `standard`,
     `advanced` por runtime; formato en PLAN-012 DEC-003).
   - Configurar permisos de edición headless en cada CLI sin flags de omisión
     de permisos (RISK-003).
5. SPEC-011 sigue pendiente de GAP-001/GAP-002; los smokes de TASK-012 de
   SPEC-012 ejercitan los mismos adaptadores y pueden aportar evidencia.

Decisiones vigentes que no deben reabrirse sin motivo:

- Meta NFR-001 de SPEC-012: ≥ 30 % menos tokens; `cache_read` cuenta y se
  reporta también el total sin cache (Q-001, Q-TECH-001).
- Catálogo de modelos declarado por el usuario; sin catálogo no se cambia de
  modelo (Q-002).
- Paralelo solo sin retrabajo; orquestador cubre `/implement` y `/validate`
  (Q-003, Q-004).

Repositorio y CI:

- Rama de trabajo: `v1` (sincronizada con `origin/v1`). Ramas de fase ya
  integradas en `v1`: `spec-012-subagent-orchestrator`,
  `plan-012-subagent-orchestrator`, `fix-011-ci-hermetic-test`,
  `tasks-012-subagent-orchestrator`; sus worktrees en `.claude/worktrees/`
  pueden eliminarse.
- GitHub Actions corre solo en push/PR a `master` y manualmente
  (`workflow_dispatch`); pushes a `v1` no la disparan. Último run verde:
  40781872859 (FINDING-004 de SPEC-011 resuelto, suite 72/72).

## 5.2 Contexto adicional

FINDING-001/002 de SPEC-010 quedaron resueltos; SPEC-009 sigue revalidada tras
DECISION-004.

El permiso de ledger y proyecciones por fase ya está incorporado a `AGENTS.md`
y commands. Verificar gates con `decisions.json` y
`python3 src/check_harness_state.py`.

Antes de iniciar una nueva modificación:

1. Identificar si es nueva SPEC, revisión de una feature existente o defecto de
   implementación.
2. Abrir solo los artefactos necesarios según `docs/index.md`.
3. Mantener evidencia fuera de este handoff.
