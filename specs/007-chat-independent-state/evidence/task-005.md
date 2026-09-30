# TASK-005 — Reconstruccion integrada

Cobertura: FR-001 a FR-006, NFR-001, NFR-002, SEC-001; AC-001 a AC-006;
TEST-005 y TEST-006.

## TEST-005 — Regresion y casos adversos

- `PYTHONPATH=src python3 -m unittest discover -s tests`: 25 tests, OK.
- `python3 src/check_harness_state.py`: `HARNESS STATE: PASS`.
- `python3 -m py_compile src/check_harness_state.py tests/test_check_harness_state.py`:
  PASS.
- `git diff --check`: PASS.
- `wc -l AGENTS.md handoff.md`: 171 y 144 lineas, respectivamente.
- Casos adversos: huella alterada, registro ausente/JSON invalido, ID duplicado,
  revocacion, conflicto, ruta fuera del repo, directorio symlink externo,
  estado desconocido y feature 001 nueva sin ledger.

## TEST-006 — Sesion sin chat

Recorrido solo con archivos: `AGENTS.md` -> Constitucion -> `handoff.md` ->
`docs/index.md` -> `specs/007-chat-independent-state/{spec,plan,tasks}.md` ->
`decisions.json` -> comprobador. Resultado: SPEC y PLAN aprobados, TASKS en
ejecucion, ninguna aclaracion bloqueante, evidencia localizada en `evidence/`,
siguiente accion `/validate` tras completar TASKS. SPEC-001 a SPEC-006 se
localizan como validadas con procedencia historica limitada.

## Seguridad, TDD y alcance

El ledger se inspecciono: no contiene secretos. TDD de TEST-001 a TEST-004 en
`task-001.md`; aqui se reejecutaron pruebas. TEST-006 es verificacion manual
reproducible. Al revisar TEST-003 se agrego la proteccion contra symlinks; al
probar adopcion se sustituyo el umbral numerico de legado por una lista exacta
de las seis carpetas historicas. Una carpeta vacia no se trata como feature.
Son correcciones locales del comprobador aprobado por DEC-002, sin dependencia
nueva, cambio de contrato ni requisito. `handoff.md` se actualizo para reflejar
el cierre, desviacion menor necesaria dentro de FR-003/FR-005.
