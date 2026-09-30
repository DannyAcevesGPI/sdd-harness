# Tareas: Estado reconstruible sin chat

**ID:** TASKS-007  
**SPEC relacionada:** SPEC-007  
**PLAN relacionado:** PLAN-007  
**Estado:** COMPLETED  
**Versión:** 0.1.0  
**Fecha:** 2026-09-30

---

# 1. Precondiciones

- [x] SPEC-007 y PLAN-007 v0.2.0 están `APPROVED`.
- [x] No hay aclaraciones bloqueantes.
- [x] Todos los requisitos MUST tienen estrategia técnica y AC.
- [x] Orden general y alcance de archivos identificados.

# 2. Objetivo y estados

Dividir el registro durable, su comprobación y el bootstrap sin chat en cambios
revisables. Todas las tareas inician `TODO`; podrán pasar a `IN_PROGRESS`,
`BLOCKED` o `DONE` según la Constitución y `/implement`. `DONE` exige evidencia,
no solo archivos escritos.

# 3. Tareas

## TASK-001 — Contrato y comprobador de aprobaciones

**Tipo:** FEATURE / TEST  
**Estado:** DONE  
**Prioridad:** P0  
**Depende de:** Ninguna

**Objetivo:** Implementar un comprobador de solo lectura que valide eventos,
huellas normalizadas y gates de features nuevas, y que falle cerrado ante
formatos ambiguos o registros ausentes.

**Trazabilidad:** FR-001, FR-002, FR-004, NFR-002, BR-001, BR-002;
AC-001, AC-003, AC-004; DEC-001, DEC-002.

**Alcance:** CREATE `src/check_harness_state.py`,
`tests/test_check_harness_state.py`; REUSE `src/`, `tests/`, biblioteca estándar.
No modificar features históricas ni crear hooks.

**TEST-001:** Un evento completo enlaza artefacto, actor, decisión, fecha,
alcance y huella; gate válido.  
**TEST-002:** Cambio de estado/checklist permitido mantiene huella; cambio de
requisito, tarea, dependencia o criterio la invalida.  
**TEST-003:** Registro ausente, JSON inválido, ID duplicado, ruta fuera del repo,
evento contradictorio o formato desconocido producen error explícito.  
**TEST-004:** El comprobador distingue legado no verificable de gate nuevo sin
registro y nunca interpreta un commit/estado como aprobación.

**TDD:** Obligatorio. Ejecutar cada caso en RED antes del código productivo,
después GREEN con `python3 -m unittest discover -s tests`; guardar comandos,
fallos esperados y resultados en `evidence/`.

**Definition of Done:** TEST-001 a TEST-004 pasan, el script no muta archivos,
la normalización tiene lista cerrada de campos permitidos, las rutas se
restringen al repo y la evidencia RED/GREEN está enlazada.

## TASK-002 — Gates y templates con registro obligatorio

**Tipo:** DOCUMENTATION  
**Estado:** DONE  
**Prioridad:** P0  
**Depende de:** TASK-001

**Objetivo:** Exigir que decisiones y aprobaciones nuevas se registren antes de
avanzar de fase, y que una discrepancia de huella o procedencia detenga el gate.

**Trazabilidad:** FR-001, FR-002, FR-004, BR-001, BR-002; AC-001, AC-003,
AC-004; DEC-001, DEC-002.

**Alcance:** MODIFY `.spec/constitution.md`, `.spec/commands/specify.md`,
`.spec/commands/clarify.md`, `.spec/commands/plan.md`,
`.spec/commands/tasks.md`, `.spec/commands/implement.md`,
`.spec/commands/validate.md`, `.spec/templates/specification.template.md`,
`.spec/templates/plan.template.md`, `.spec/templates/tasks.template.md`.
REUSE el ciclo SDD y sus IDs. No cambiar autoridad humana ni autoaprobar.

**TDD:** No aplica: instrucciones y templates, sin comportamiento ejecutable.
**Verificación alternativa:** Revisión cruzada de gates por fase y ejecución
manual de un caso válido y otro con huella inválida usando el comprobador.

**Definition of Done:** Cada fase indica cuándo registrar/consultar decisiones,
qué campos son obligatorios, cómo detener un gate inconsistente y qué campos
operativos pueden cambiar sin nueva aprobación; no hay contradicción con SPEC
ni Constitución y la revisión queda en `evidence/`.

## TASK-003 — Guía de reconstrucción y entrada compacta

**Tipo:** DOCUMENTATION  
**Estado:** DONE  
**Prioridad:** P1  
**Depende de:** TASK-001, TASK-002

**Objetivo:** Documentar el protocolo de captura, cálculo de huella y bootstrap
desde una sesión vacía, manteniendo `AGENTS.md` como índice compacto.

**Trazabilidad:** FR-003, FR-005, NFR-001, NFR-002, SEC-001; AC-002, AC-006;
DEC-001, DEC-003.

**Alcance:** CREATE `docs/state-reconstruction.md`; MODIFY `AGENTS.md`,
`docs/quickstart.md`. REUSE `handoff.md`, `docs/index.md` como entradas.

**TDD:** No aplica a documentación. **Verificación alternativa:** Seguir la
guía sin chat desde la raíz del repo, comprobar que todos los comandos/rutas
existen, revisar que no haya secretos y que `AGENTS.md` mantenga menos de 200
líneas.

**Definition of Done:** El procedimiento distingue decisión humana de registro,
explica limitaciones de identidad/huellas y ofrece un bootstrap reproducible
sin cargar auditorías; evidencia de revisión disponible.

## TASK-004 — Estado vivo, índice y transición de legado

**Tipo:** DOCUMENTATION  
**Estado:** DONE  
**Prioridad:** P1  
**Depende de:** TASK-002, TASK-003

**Objetivo:** Hacer visibles feature/fase/bloqueos/siguiente acción, enlazar
features validadas y marcar honestamente la procedencia histórica.

**Trazabilidad:** FR-003, FR-005, FR-006, SEC-001; AC-002, AC-004, AC-005,
AC-006; DEC-003.

**Alcance:** CREATE `specs/007-chat-independent-state/decisions.json`;
MODIFY `handoff.md`, `docs/index.md`. REUSE validaciones SPEC-001 a SPEC-006.
No modificar aprobaciones ni validaciones históricas.

**TDD:** No aplica a estado/índices documentales. **Verificación alternativa:**
Comparar índice y handoff con directorios/validaciones reales; comprobar que
SPEC-001 a SPEC-006 se presentan como legado no verificable cuando corresponda
y que el registro de SPEC-007 usa decisiones textuales reales, sin inventar
evidencia retrospectiva.

**Definition of Done:** Todas las features se localizan desde el índice,
`handoff.md` conserva menos de 200 líneas y enlaza detalle; el registro de
SPEC-007 refleja las aprobaciones recibidas y no contiene secretos.

## TASK-005 — Reconstrucción y validación integrada

**Tipo:** TEST / DOCUMENTATION  
**Estado:** DONE  
**Prioridad:** P0  
**Depende de:** TASK-001, TASK-002, TASK-003, TASK-004

**Objetivo:** Ejecutar el flujo completo desde archivos del repo y dejar
evidencia suficiente para `/validate`.

**Trazabilidad:** FR-001 a FR-006, NFR-001, NFR-002, SEC-001;
AC-001 a AC-006; DEC-001 a DEC-003.

**Alcance:** CREATE/MODIFY solo `specs/007-chat-independent-state/evidence/`;
MODIFY `CHANGELOG.md` únicamente si lo exige el proceso vigente. REUSE script,
guía, SPEC/PLAN/TASKS e índices. No declarar feature `VALIDATED` aquí.

**TEST-005:** Suite completa y comprobador local en PASS sobre el estado real;
casos adversos siguen detectándose.  
**TEST-006:** Reconstrucción simulada sin chat identifica feature activa, fase,
aprobaciones, bloqueos, siguiente acción y evidencia.

**TDD:** No aplica como ciclo nuevo: reejecuta TEST-001 a TEST-004 ya cubiertos
por TDD. TEST-006 es revisión manual reproducible; guardar checklist y rutas.

**Definition of Done:** Suite y comprobador pasan, checklist sin chat tiene
resultado verificable, evidencia enlazada, no hay bloqueos ni hallazgos de
seguridad pendientes. La validación final sigue siendo `/validate`.

# 4. Grafo y orden

```text
TASK-001 -> TASK-002 -> TASK-003 -> TASK-004 -> TASK-005
```

TASK-003 también depende de TASK-001; TASK-004 de TASK-002. No hay ciclos ni
tareas paralelas previstas. Los archivos compartidos se modifican en secuencia.

| Orden | Tarea | Estado |
|------:|-------|--------|
| 1 | TASK-001 | DONE |
| 2 | TASK-002 | DONE |
| 3 | TASK-003 | DONE |
| 4 | TASK-004 | DONE |
| 5 | TASK-005 | DONE |

# 5. Bloqueos y discoveries

Ninguno conocido. Cualquier decisión funcional nueva vuelve a SPEC; un cambio
de diseño vuelve a PLAN. Los discoveries fuera de alcance se registran sin
implementarlos automáticamente.

# 6. Matriz de trazabilidad

| Tarea | Requisitos principales | AC | Decisión | Pruebas |
|-------|------------------------|----|----------|---------|
| TASK-001 | FR-001, FR-002, FR-004, NFR-002, BR-001, BR-002 | AC-001, AC-003, AC-004 | DEC-001, DEC-002 | TEST-001 a TEST-004 |
| TASK-002 | FR-001, FR-002, FR-004, BR-001, BR-002 | AC-001, AC-003, AC-004 | DEC-001, DEC-002 | Revisión manual |
| TASK-003 | FR-003, FR-005, NFR-001, NFR-002, SEC-001 | AC-002, AC-006 | DEC-001, DEC-003 | Checklist |
| TASK-004 | FR-003, FR-005, FR-006, SEC-001 | AC-002, AC-004, AC-005, AC-006 | DEC-003 | Revisión documental |
| TASK-005 | FR-001 a FR-006, NFR-001, NFR-002, SEC-001 | AC-001 a AC-006 | DEC-001 a DEC-003 | TEST-005, TEST-006 |

Cobertura: FR 6/6, NFR 2/2, SEC 1/1, AC 6/6, DEC 3/3. Tareas huérfanas: 0.

# 7. Criterios para comenzar implementación

- [x] SPEC y PLAN aprobados; requisitos, pruebas y dependencias cubiertos.
- [x] Alcance por tarea identificado; sin ciclos ni bloqueos conocidos.
- [x] TASKS-007 aprobadas explícitamente por el usuario.

# 8. Estado del documento

**Estado actual:** COMPLETED  
**Aprobado por:** Usuario responsable del proyecto  
**Fecha de aprobación:** 2026-09-30  
**Decisión explícita:** "aprobado" en respuesta a la solicitud de aprobación
de TASKS-007 para comenzar la implementación.  
**Alcance aprobado:** TASKS-007 versión 0.1.0, TASK-001 a TASK-005.

La implementación comenzará respetando dependencias y evidencias por tarea.
