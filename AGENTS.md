## SDD Harness — Agent Operating Instructions

Este repositorio opera con Spec-Driven Development (SDD).

Reglas base:

- No implementation without an approved specification.
- Para features del flujo completo: no implementation without approved SPEC, PLAN and TASKS.
- La Constitución, standards y commands son fuentes autoritativas; este archivo es un índice operativo compacto.

---

# 1. Source Of Truth

Precedencia:

1. Decisiones humanas explícitas y aprobadas.
2. `.spec/constitution.md`
3. `.spec/standards/`
4. SPEC de la feature.
5. PLAN de la feature.
6. TASKS de la feature.
7. Implementación y evidencia.

Si hay conflicto relevante, detenerse, identificar el nivel dueño y resolverlo antes de continuar.

---

# 2. Mandatory Bootstrap

Antes de trabajo significativo:

1. Leer `.spec/constitution.md`.
2. Determinar solicitud, feature, fase SDD, artefactos existentes, command aplicable y standards relevantes.
3. Revisar `handoff.md` cuando el estado auditado del Harness sea relevante.
4. Tratar `src/`, `tests/`, migraciones y configuración de aplicación como read-only antes de `/implement`.

---

# 3. Commands

Usar el command que corresponda y leer su archivo completo:

- Nueva funcionalidad o cambio de comportamiento: `.spec/commands/specify.md`
- Ambigüedad funcional: `.spec/commands/clarify.md`
- Diseño técnico: `.spec/commands/plan.md`
- Descomposición de trabajo: `.spec/commands/tasks.md`
- Modificación autorizada: `.spec/commands/implement.md`
- Verificación final: `.spec/commands/validate.md`

Templates: `.spec/templates/`. No modificarlos al crear features.

---

# 4. Phase Gates

Estados principales:

- SPEC: `DRAFT → IN_REVIEW → APPROVED → SUPERSEDED`
- PLAN: `DRAFT → IN_REVIEW → APPROVED → SUPERSEDED`
- TASKS: `DRAFT → IN_REVIEW → APPROVED → IN_PROGRESS → COMPLETED`
- TASK: `TODO → IN_PROGRESS → BLOCKED/DONE`
- Validación final: `SPEC COMPLIANCE: PASS` y `FEATURE STATUS: VALIDATED`

Transiciones a `APPROVED` requieren aprobación humana explícita. No autoaprobar.

---

# 5. Mutation Boundary

Antes de `/implement`, solo modificar artefactos permitidos por la fase:

- `/specify` y `/clarify`: SPEC
- `/plan`: PLAN
- `/tasks`: TASKS
- `/implement`: cambios autorizados por SPEC/PLAN/TASKS
- `/validate`: reporte de validación

Cambios de estado/evidencia que no alteran trabajo autorizado no requieren nuevo approval gate.

---

# 6. Traceability

Mantener la cadena:

Requirement → Acceptance Criterion → Plan → Task → Code/Docs → Test/Evidence → Validation

Usar IDs del Harness:

- Requisitos: `FR-[XXX]`, `NFR-[XXX]`, `SEC-[XXX]`, `BR-[XXX]`
- Criterios: `AC-[XXX]`
- Plan: `DEC-[XXX]`, `RISK-[XXX]`, `Q-TECH-[XXX]`, `ADR-[XXX]`
- Ejecución: `TASK-[XXX]`, `TEST-[XXX]`, `BLOCK-[XXX]`, `DISCOVERY-[XXX]`, `Q-TASK-[XXX]`
- Validación: `VALIDATION-[XXX]`, `FINDING-[XXX]`, `SEC-FINDING-[XXX]`, `GAP-[XXX]`, `DEV-[XXX]`

No crear tareas huérfanas ni código/documentación significativa sin TASK justificante.

---

# 7. Clarification And Escalation

Usar `[NEEDS CLARIFICATION]` cuando falte una decisión que pueda cambiar alcance, comportamiento, seguridad, diseño o tareas.

Resolver en el nivel dueño:

- Functional: SPEC
- Technical: PLAN
- Work breakdown: TASKS
- Local implementation defect: IMPLEMENTATION

Si un artefacto aprobado cambia su contenido autorizado, recuperar su approval gate y reevaluar downstream.

---

# 8. Implementation Rules

Durante `/implement`:

- Ejecutar solo tareas aprobadas, en dependencia definida.
- Hacer el cambio mínimo necesario.
- Reutilizar patrones y archivos existentes.
- Evitar scope creep, refactors no relacionados, dependencias innecesarias y arquitectura especulativa.
- Ejecutar pruebas/verificaciones relevantes y registrar evidencia.
- No debilitar pruebas para conseguir PASS.
- Registrar discoveries fuera de alcance como `DISCOVERY-[XXX]`; no implementarlos automáticamente.

---

# 9. Security

Consultar `.spec/standards/security.md` cuando haya autenticación, autorización, datos sensibles, secretos, integraciones, uploads, logging, entrada externa, operaciones destructivas o acceso a datos.

Nunca almacenar ni imprimir secretos en código, pruebas, fixtures, documentación, logs o evidencia.

---

# 10. Subagents

Los subagentes son apoyo delegado, no autoridad del Harness.

Antes de delegar, el agente principal debe definir alcance, fuentes, límites de mutación y evidencia esperada. El agente principal conserva responsabilidad por bootstrap, trazabilidad, integración de hallazgos y gates.

Guía: `docs/agents/subagents.md`.

---

# 11. Hooks

Los hooks son apoyo verificable futuro. No sustituyen SPEC, PLAN, TASKS, validación, revisión de seguridad ni aprobación humana.

No crear hooks ejecutables ni dependencias sin SPEC/PLAN/TASKS que lo autoricen. Todo hook futuro debe ser determinista o declarar límites, proteger secretos y producir evidencia revisable.

Guía: `docs/agents/hooks.md`.

---

# 12. Definition Of Done

Una feature SDD termina solo cuando:

- SPEC y PLAN están `APPROVED`.
- TASKS está `COMPLETED` y tareas requeridas están `DONE`.
- Requisitos MUST, AC, SEC y quality gates tienen evidencia PASS.
- No hay bloqueos ni traceability gaps bloqueantes.
- `/validate` produce `SPEC COMPLIANCE: PASS` y `FEATURE STATUS: VALIDATED`.
