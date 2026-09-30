# Changelog

Cambios relevantes del SDD Harness. Git y las validaciones SDD conservan el
detalle; este archivo resume hitos para consulta rápida.

## 2026-09-30

- Guía para adoptar el Harness en proyectos nuevos, con separación entre base
  reusable y evidencia local. [SPEC-004](specs/004-harness-adoption-guide/validation.md);
  commit `8515abd`.
- Instrucciones de agentes compactas, guías de subagentes y hooks, y handoff
  reducido a estado vivo con índice y quickstart.
  [SPEC-002](specs/002-agent-operating-readiness/validation.md),
  [SPEC-003](specs/003-context-window-optimization/validation.md);
  commit `73e41e6`.

## 2026-09-24

- Promoción del Harness procedimental a **1.0.0 STABLE** tras AUDIT-10.
  [Historial auditado](docs/audit-history.md); commit `38a5edc`.
- Registro de la baseline auditada, incluyendo Constitución, standards,
  commands, templates y la feature de prueba.
  [Validación de SPEC-001](specs/001-audit-task-management/validation.md);
  commit `34740af`.

## Mantenimiento

Al completar un cambio relevante, añade una entrada arriba, bajo su fecha
verificada. Resume el resultado observable y enlaza su validación o commit;
usa una versión solo si existe evidencia de su publicación. Mantén el detalle
de pruebas y auditorías en `specs/<feature-id>/evidence/` o documentos dedicados,
y el `handoff.md` como estado vivo.
