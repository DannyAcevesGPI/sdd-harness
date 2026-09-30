# TASK-004 — Estado vivo y legado

Cobertura: FR-003, FR-005, FR-006, SEC-001; AC-002, AC-004, AC-005,
AC-006.

`docs/index.md` y `handoff.md` enlazan ahora SPEC-001 a SPEC-006 validadas y
SPEC-007 activa. El legado se declara no verificable cuando la procedencia de
la aprobación depende del chat; no se modificaron validaciones históricas.

`decisions.json` conserva Q-001 y las decisiones humanas de SPEC-007. La
aprobación de PLAN v0.1.0 es antecedente, no gate vigente; v0.2.0 es la vigente.
`python3 src/check_harness_state.py` produjo `HARNESS STATE: PASS`.

Verificación alternativa (estado documental, sin TDD): comparación con
`specs/004` a `specs/006` y sus validaciones, inspección de enlaces y registro,
revisión de ausencia de secretos. No se fabricaron aprobaciones antiguas.
