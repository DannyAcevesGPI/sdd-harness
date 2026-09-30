# TASK-003 — Guia y bootstrap

Cobertura: FR-003, FR-005, NFR-001, NFR-002, SEC-001; AC-002, AC-006.

Se creo `docs/state-reconstruction.md` y se actualizaron `AGENTS.md` y
`docs/quickstart.md`. El flujo parte de archivos del repo, usa `git status`,
ledger y comprobador, y abre evidencia solo bajo demanda.

Verificacion alternativa (documentacion, sin TDD): rutas y comandos revisados;
`wc -l AGENTS.md` da 171 lineas (<200). La guia distingue procedencia
documental de autenticacion humana y no contiene secretos.
