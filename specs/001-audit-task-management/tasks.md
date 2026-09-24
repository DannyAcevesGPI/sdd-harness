# Tareas: Gestión de tareas para AUDIT-08

**ID:** TASKS-001  
**SPEC relacionada:** SPEC-001 v0.1.0, APPROVED  
**PLAN relacionado:** PLAN-001 v0.1.0, APPROVED  
**Estado:** COMPLETED  
**Versión:** 0.1.0  
**Fecha:** 2026-09-24

# 1. Precondiciones

- [x] SPEC aprobada; Q-001 resuelta.
- [x] PLAN aprobado mediante «Apruebo ese plan» el 2026-09-24.
- [x] Todos los MUST tienen cobertura técnica.
- [x] Orden de implementación, contratos y alcance definidos.
- [x] Sin aclaraciones bloqueantes ni ADR pendientes.

# 2. Objetivo

Ejecutar PLAN-001 en cuatro tareas obligatorias, secuenciales y verificables.
Cada tarea incluye sus pruebas y evidencia; el ensayo aislado de auditoría
no sustituye la validación de la implementación principal.

Rutas abreviadas usadas en este documento:

- `FEATURE`: `specs/001-audit-task-management/`.
- `EVIDENCE`: `specs/001-audit-task-management/evidence/`.

En cada ejecución registrar fecha, comando exacto, código de salida, resultados,
archivos y hashes SHA-256 en `FEATURE/evidence.md` y archivos bajo `EVIDENCE`.
Las abreviaturas son documentales, no variables de entorno requeridas.

# 3. Estados de tarea

TODO → IN_PROGRESS → DONE; usar BLOCKED cuando exista un impedimento documentado.
Todas las tareas comienzan TODO. Ninguna se marca DONE sin cumplir su DoD.
La reapertura DONE → TODO sigue `/implement` §17.1 y conserva evidencia previa.
Los estados de la aplicación PENDING/COMPLETED no son los estados de estas TASKS.

# 4. Prioridades

P1 para las cuatro tareas. Todas son requeridas; prioridad no altera dependencias.

# 5. Identificadores y catálogo de pruebas

TASK-001 a TASK-004 y TEST-001 a TEST-012 son estables dentro de esta feature.
No se reutilizan ni renumeran después de ser referenciados.

| Test | Tipo | Comportamiento o comprobación | Criterios |
|---|---|---|---|
| TEST-001 | UNIT | Creación normalizada, duplicados, IDs distintos, propietario y estado | AC-001 |
| TEST-002 | UNIT | Títulos inválidos rechazados sin alterar listados existentes | AC-002 |
| TEST-003 | SECURITY | Listado propio, orden con actores intercalados e inclusión de completadas | AC-003 |
| TEST-004 | SECURITY | Listado vacío aunque otro actor tenga tareas | AC-004 |
| TEST-005 | UNIT | Completar dos veces sin cambiar otras tareas ni datos | AC-005 |
| TEST-006 | SECURITY | Identidad ausente/vacía/espacios/no textual en todas las operaciones | AC-006 |
| TEST-007 | SECURITY | Tarea ajena, inexistente o ID inválido: mismo error y ninguna mutación | AC-007; PLAN §§8/9/17 |
| TEST-008 | CONTRACT | Propietario derivado del actor y rechazo del argumento owner_id | AC-008 |
| TEST-009 | OTHER | Dos ejecuciones independientes de la suite con estado limpio | AC-009 |
| TEST-010 | UNIT | Registros inmutables, listado independiente y aislamiento entre instancias | AC-003, AC-008, AC-009; DEC-002 |
| TEST-011 | E2E | Flujo local crear → listar → completar → listar para dos actores | AC-001, AC-003, AC-005, AC-007, AC-008 |
| TEST-012 | OTHER | Ensayo aislado de fallo de orden, reapertura, corrección y revalidación | AC-003; PLAN §11.3 |

TEST-009 es un procedimiento de repetición, no un test que se autoinvoque.
TEST-012 verifica el procedimiento de auditoría con ejecuciones reales sobre una
copia; no es una prueba adicional de producción. Los demás IDs deberán aparecer
en nombres de métodos o docstrings de `tests/test_audit_tasks.py`.
Un TEST puede contener subcasos; registrar su alcance sin inflar conteos de tests.

# 6. Tareas

## TASK-001 — Crear y consultar tareas propias

**Estado:** DONE  
**Tipo:** FEATURE  
**Prioridad:** P1  
**Cambio sensible:** YES, identidad y aislamiento de listados.

### Objetivo

Construir el modelo inmutable y la base del servicio con creación y listado
por propietario. Implementar primero modelo/creación y después listado,
respetando el orden técnico del PLAN.

### Trazabilidad

**Requisitos:** FR-001, FR-002, SEC-001, SEC-002, BR-001, BR-002, BR-003.
**Criterios:** AC-001, AC-002, AC-003, AC-004, AC-006, AC-008.
**Decisiones:** DEC-001, DEC-002, DEC-003.
La parte de AC-003 sobre tareas completadas y la de AC-006 sobre finalización
quedan explícitamente pendientes de TASK-002; no declarar esos AC totalmente PASS aquí.

### Dependencias

**Depende de:** ninguna.

### Alcance permitido

**CREATE:** `src/audit_tasks.py`, `tests/test_audit_tasks.py`,
`FEATURE/evidence.md`, resultados `EVIDENCE/task-001-*`.
**REUSE:** biblioteca estándar; SPEC y PLAN en lectura.
**MODIFY:** únicamente estados/evidencia de esta tarea y checkpoint de auditoría.
**No modificar:** SPEC/PLAN aprobados, normas del Harness, configuración ajena.

### Implementación esperada

Task inmutable, estado por instancia, contador y diccionario ordenado;
`create_task` y `list_tasks` con validación de identidad en runtime, título
normalizado, propietario derivado y copia del listado. Aplicar contratos y
mensajes del PLAN. No añadir stubs de finalización ni APIs fuera del PLAN.

### Pruebas requeridas

TEST-001, TEST-002, TEST-004, TEST-008, TEST-010 y cobertura inicial de
TEST-003 (pendientes ordenadas) y TEST-006 (crear/listar).
Incluir entradas no textuales y casos con espacios; verificar identidad exacta
sin fusionar actores distintos, según DEC-003. Toda aserción usa la API pública.

### Validaciones y Definition of Done

- [x] Creación y listado implementados conforme al PLAN, sin filtraciones ni mutaciones indebidas.
- [x] Las pruebas requeridas dentro de este alcance pasan, sin skipped ni assertions debilitadas.
- [x] Sintaxis e indentación verificadas; tipos, formato y controles revisados.
- [x] Evidencia registrada con alcance parcial de AC-003/006 identificado.
- [x] Ningún bloqueo o cambio de alcance pendiente.

### Evidencia esperada

Salida de suite disponible en esta etapa, código de salida, hashes y relación
TEST → AC → requisitos. No se presume cumplimiento de la finalización todavía.


**Evidencia obtenida:** `evidence/task-001-tests.txt`: 8 tests PASS; sintaxis e
indentación PASS. AC-003/006 parcialmente cubiertos según alcance; sin bloqueos.

## TASK-002 — Completar tareas con autorización e idempotencia

**Estado:** DONE  
**Tipo:** SECURITY  
**Prioridad:** P1  
**Cambio sensible:** YES, autorización de modificación.

### Objetivo

Completar la API de la feature y cerrar la cobertura funcional y de seguridad
de AC-001 a AC-008, incluyendo ausencia de mutación ante errores.

### Trazabilidad

**Requisitos:** FR-002, FR-003, SEC-001, SEC-002, BR-002, BR-003.
**Criterios:** AC-003, AC-005, AC-006, AC-007, AC-008.
**Decisiones:** DEC-002, DEC-003.

### Dependencias

**Depende de:** TASK-001.

### Alcance permitido

**MODIFY:** `src/audit_tasks.py`, `tests/test_audit_tasks.py`,
`FEATURE/evidence.md` y estados/evidencia de esta tarea.
**CREATE:** resultados `EVIDENCE/task-002-*`.
**REUSE:** modelo y validación existentes.
**No modificar:** SPEC, PLAN, normas del Harness o contratos aprobados.

### Implementación esperada

`complete_task` valida primero identidad, después ID y propiedad. ID inválido,
inexistente o ajeno produce el mismo error público sin datos de la tarea.
Completar sustituye únicamente estado, conserva orden y es idempotente.
No modificar campos privados directamente desde pruebas.

### Pruebas requeridas

Añadir TEST-005 y TEST-007. Extender TEST-003 para incluir completadas y
TEST-006 para finalización; conservar y repetir las aserciones previas.
TEST-007 incluye bool, cero, negativos, cadenas y valores no hashables como IDs
inválidos, así como comparación de clase/mensaje y listados antes/después.
Comprobar precedencia de identidad inválida frente a otros datos inválidos.
Reejecutar TEST-001 a TEST-008 y TEST-010 como regresión.

### Validaciones y Definition of Done

- [x] API completa con errores fijos, autorización e idempotencia.
- [x] AC-001 a AC-008 tienen pruebas satisfactorias, incluidas sus ramas negativas.
- [x] Regresiones, sintaxis e indentación PASS; revisión de seguridad registrada.
- [x] Evidencia nueva conserva la de TASK-001 y documenta las extensiones de pruebas.
- [x] Sin bloqueos, mutaciones ajenas ni trabajo no autorizado.

### Evidencia esperada

Resultados y hashes de suite completa hasta esta etapa; matriz de subcasos
SEC-001/002 y registro de las verificaciones de no divulgación/no mutación.


**Evidencia obtenida:** `evidence/task-002-tests.txt`: 10 tests PASS y controles
PASS; AC-003/006 completados. Errores ajenos/inexistentes iguales; sin bloqueos.

## TASK-003 — Verificar flujo completo, repetibilidad y calidad de evidencia

**Estado:** DONE  
**Tipo:** TEST  
**Prioridad:** P1.

### Objetivo

Demostrar el flujo local completo y AC-009 con dos procesos independientes;
preparar evidencia suficiente para la validación posterior.

### Trazabilidad

**Requisitos:** NFR-001, FR-001, FR-002, FR-003, SEC-001, SEC-002.
**Criterios:** AC-001 a AC-009.
**Decisiones:** DEC-001, DEC-004; PLAN §§11.1/11.2 y riesgos RISK-001 a RISK-003.

### Dependencias

**Depende de:** TASK-002.

### Alcance permitido

**MODIFY:** `tests/test_audit_tasks.py`, `FEATURE/evidence.md`, estados/evidencia de TASKS.
**CREATE:** `EVIDENCE/run-1.txt`, `EVIDENCE/run-2.txt`, `EVIDENCE/quality.txt`,
`EVIDENCE/hashes.txt` y registros auxiliares de los controles indicados.
**REUSE:** servicio real y pruebas existentes.
**No modificar:** implementación para ocultar fallos; SPEC, PLAN o normas del Harness.
Un defecto de código vuelve a la tarea propietaria con reapertura documentada;
no se corrige ampliando silenciosamente el alcance de esta tarea.

### Implementación esperada y pruebas requeridas

Añadir TEST-011. Ejecutar TEST-009 mediante dos invocaciones independientes de:

`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest discover -s tests -v`

Cada ejecución debe cubrir TEST-001 a TEST-008, TEST-010 y TEST-011. Registrar
comandos, fecha, versión de Python, número de tests, códigos de salida y SHA-256
de código y pruebas. Ejecutar controles de sintaxis e indentación del PLAN.
No instalar paquetes ni crear configuración de formatter/linter inexistentes.

### Validaciones y Definition of Done

- [x] TEST-011 PASS con servicio real y actores sintéticos.
- [x] TEST-009 PASS: dos ejecuciones limpias satisfactorias con resultados preservados.
- [x] Evidencia para AC-001 a AC-009 enlazada a requisitos y código actuales.
- [x] Sin tests requeridos omitidos; sintaxis/indentación y revisión manual documentadas.
- [x] Herramientas automáticas ausentes identificadas como no configuradas, no como PASS.
- [x] Sin bloqueos; hashes listos para detectar alteraciones del ensayo posterior.

### Evidencia esperada

Resultados originales de ambos procesos; resumen de controles, seguridad,
trazabilidad y revisión de scope. No generar aún `validation.md` de la feature
ni marcar TASKS COMPLETED mientras TASK-004 esté pendiente.


**Evidencia obtenida:** `evidence/run-1.txt`, `run-2.txt`, `quality.txt` y
`hashes.txt`: 11 tests PASS en cada proceso, sin skips; AC-009 PASS.

## TASK-004 — Ejercitar reapertura y revalidación en copia aislada

**Estado:** DONE  
**Tipo:** TEST  
**Prioridad:** P1.

### Objetivo

Ejecutar el ensayo de PLAN §11.3 y comprobar con evidencia real que un defecto
de orden es detectado y corregido siguiendo `/implement` §17.1.

### Trazabilidad

**Requisitos:** FR-002, NFR-001.
**Criterios:** AC-003, AC-009.
**Decisiones:** DEC-004; PLAN §11.3 y RISK-004.
**Motivo de auditoría:** verificar operativamente la corrección AUDIT-FINDING-034;
este motivo no sustituye la relación con SPEC/PLAN.

### Dependencias

**Depende de:** TASK-003.

### Alcance permitido

**CREATE/MODIFY:** copia temporal propia bajo `/tmp` con prefijo `audit08-`,
registros `EVIDENCE/reopening-*` y `EVIDENCE/reopening.md`.
**MODIFY:** `FEATURE/evidence.md`, estados/evidencia de esta tarea y checkpoint de `handoff.md`.
**REUSE en lectura:** implementación principal, pruebas originales, SPEC/PLAN
y evidencia de TASK-001 a TASK-003.
**No modificar:** código o pruebas principales, artefactos ajenos, reglas del Harness.
No ejecutar limpieza destructiva de rutas ajenas ni usar secretos.

### Ejecución esperada y TEST-012

1. Copiar código y pruebas a la carpeta temporal y registrar sus hashes contra
   TASK-003. El fixture representa solamente el trabajo funcional TASK-001 a
   TASK-003 ya completado; TASK-004 es su orquestación y permanece IN_PROGRESS
   en el documento real. Rotular todo estado de documento simulado como fixture.
2. Conservar una instantánea del fixture correcto y de sus resultados. Registrar
   las aprobaciones reales de SPEC/PLAN/TASKS como referencias, sin inventar
   aprobaciones de documentos simulados o declarar completa la feature real.
3. Alterar únicamente el orden del listado en la copia, manteniendo filtrado de
   propietario y pruebas originales. Registrar diff y hashes. Ejecutar la suite
   y conservar la salida fallida real: AC-003 deberá detectar el orden incorrecto.
4. Registrar `FINDING-001` en el reporte del fixture, tipo IMPLEMENTATION y
   causa de inyección conocida. Este ID es local al fixture y no consume el
   namespace AUDIT-FINDING del Harness ni los findings de la validación principal.
5. Registrar invalidación de evidencia, TASKS del fixture COMPLETED → IN_PROGRESS
   y reapertura de TASK-001 DONE → TODO. Evaluar y reabrir las dependientes cuya
   evidencia quede invalidada; respetar su orden y registrar preflight.
6. Corregir el orden en la copia sin tocar assertions. Registrar IN_PROGRESS,
   ejecutar de nuevo pruebas/controles y volver a DONE con evidencia real.
   Cerrar el TASKS simulado y reevaluar su conformidad conservando el fallo previo.
7. Verificar por SHA-256 que código y pruebas principales permanecen idénticos
   a TASK-003. Si no coinciden, investigar y repetir las verificaciones afectadas
   antes de cerrar la tarea. No presentar el PASS del fixture como PASS de la feature.

El resultado esperado del test de auditoría incluye una ejecución de aplicación
FAIL seguida de PASS. El FAIL inducido permanece registrado, pero no representa
una prueba fallida de la implementación principal. TEST-012 solamente pasa si
el fallo esperado fue observado, corregido y trazado sin alterar los controles.
Si no se reproduce el fallo o aparece una brecha real del Harness, documentarla;
no fabricar evidencia ni aplicar una corrección normativa sin autorización.

### Validaciones y Definition of Done

- [x] TEST-012 ejecutado con fallo y corrección observados, no solo narrados.
- [x] Evidencia antes/después, hashes, transiciones y evaluación de dependientes disponibles.
- [x] Aprobaciones y estados del fixture claramente diferenciados de los reales.
- [x] Código/pruebas principales sin alteraciones; evidencia de TASK-003 todavía vigente.
- [x] Sin hallazgos bloqueantes de auditoría pendientes que impidan cerrar la tarea.

### Evidencia esperada

`EVIDENCE/reopening.md` con secuencia y decisiones, instantáneas de estados del
fixture, diff, comandos, salidas y hashes. Evidencia suficiente para reconstruir
el ejercicio aunque la carpeta temporal deje de existir.


**Evidencia obtenida:** `evidence/reopening.md` y sus registros: baseline PASS,
4 fallos inducidos reales, dos ejecuciones reparadas de 11 tests PASS;
hashes principales sin cambios, sin bloqueos de auditoría pendientes.

# 7. Tareas técnicas

TASK-003 y TASK-004 son TEST: justificadas por NFR-001/AC-009 y FR-002/AC-003,
DEC-004 y PLAN §11. No requieren FR artificiales. No hay infraestructura,
migraciones, dependencias externas ni ADR adicionales que descomponer.

# 8. Grafo de dependencias

TASK-001 → TASK-002 → TASK-003 → TASK-004.
Sin ciclos ni candidatos a paralelización. Existe FILE CONFLICT entre las
tareas que comparten `src/audit_tasks.py`, `tests/test_audit_tasks.py` y evidencia;
la ejecución secuencial evita modificaciones incompatibles.

# 9. Orden de ejecución

| Orden | Tarea | Depende de | Estado |
|---:|---|---|---|
| 1 | TASK-001 | Ninguna | DONE |
| 2 | TASK-002 | TASK-001 | DONE |
| 3 | TASK-003 | TASK-002 | DONE |
| 4 | TASK-004 | TASK-003 | DONE |

# 10. Bloqueos

No se identificaron bloqueos de requisitos, diseño o descomposición.
La aprobación pendiente de TASKS es un gate obligatorio, no un defecto.
Registrar cualquier impedimento como BLOCK-[XXX] y escalar al nivel propietario.

# 11. Descubrimientos fuera de alcance

Ninguno identificado. Registrar DISCOVERY-[XXX] si aparece trabajo adicional;
un discovery no autoriza implementarlo. Un defecto normativo del Harness se
registra separadamente desde AUDIT-FINDING-037 con evidencia antes de proponer cambios.

# 12. Matriz de trazabilidad

| Requisito/regla | Criterios | Decisiones | Tareas | Pruebas |
|---|---|---|---|---|
| FR-001 | AC-001, AC-002, AC-008 | DEC-001, DEC-002, DEC-003 | TASK-001, TASK-003 | TEST-001, TEST-002, TEST-008, TEST-011 |
| FR-002 | AC-003, AC-004 | DEC-002, DEC-003 | TASK-001, TASK-002, TASK-003, TASK-004 | TEST-003, TEST-004, TEST-011, TEST-012 |
| FR-003 | AC-005, AC-007 | DEC-002, DEC-003 | TASK-002, TASK-003 | TEST-005, TEST-007, TEST-011 |
| NFR-001 | AC-009 | DEC-001, DEC-004 | TASK-003, TASK-004 | TEST-009, TEST-010, TEST-012 |
| SEC-001 | AC-006, AC-008 | DEC-003 | TASK-001, TASK-002, TASK-003 | TEST-006, TEST-008 |
| SEC-002 | AC-003, AC-004, AC-007 | DEC-002, DEC-003 | TASK-001, TASK-002, TASK-003 | TEST-003, TEST-004, TEST-007, TEST-010 |
| BR-001 | AC-001, AC-002 | DEC-003 | TASK-001 | TEST-001, TEST-002 |
| BR-002 | AC-001, AC-005 | DEC-002 | TASK-001, TASK-002 | TEST-001, TEST-005 |
| BR-003 | AC-001, AC-005, AC-008 | DEC-002, DEC-003 | TASK-001, TASK-002 | TEST-001, TEST-005, TEST-008, TEST-010 |

# 13. Cambios durante implementación

Cambios funcionales regresan a SPEC; cambios de diseño, a PLAN; cambios al
trabajo autorizado, a TASKS. Evaluar impacto downstream y recuperar aprobación
del contenido modificado antes de continuar. No debilitar pruebas para conseguir PASS.
Actualizaciones de estados y evidencia sin cambiar trabajo autorizado no requieren
nueva aprobación, incluidas reaperturas según `/implement` §17.1.

# 14. Criterios para comenzar implementación

- [x] SPEC y PLAN APPROVED, requisitos/criterios cubiertos por tareas.
- [x] Objetivos, alcance, dependencias, pruebas, riesgos y DoD definidos.
- [x] No existen tareas huérfanas, ciclos o aclaraciones bloqueantes identificadas.
- [x] Conflictos de archivos resueltos mediante ejecución secuencial.
- [x] TASKS-001 aprobado explícitamente por el humano.

# 15. Estado del documento

**Estado actual:** COMPLETED. **Resultado:** READY FOR VALIDATION.
Estados: DRAFT → IN_REVIEW → APPROVED → IN_PROGRESS → COMPLETED.
**Aprobado por:** usuario humano. **Fecha de aprobación:** 2026-09-24.
**Evidencia:** «Apruebo la task», en respuesta a la solicitud de aprobar
TASKS-001 v0.1.0. Transiciones registradas: IN_REVIEW → APPROVED → IN_PROGRESS;
TASK-001 TODO → IN_PROGRESS tras preflight satisfactorio.

Después de aprobación, registrar APPROVED → IN_PROGRESS al iniciar TASK-001.
Cerrar IN_PROGRESS → COMPLETED únicamente cuando las cuatro tareas estén DONE,
sus evidencias disponibles y no haya trabajo obligatorio pendiente o bloqueado.
Después ejecutar `/validate` de la feature real y producir `FEATURE/validation.md`
según la plantilla del Harness. La validación final no se incluye como tarea
obligatoria previa a sí misma, para evitar una dependencia circular con COMPLETED.

Las cuatro tareas están DONE con evidencia y sin bloqueos pendientes.
Se registra TASKS IN_PROGRESS → COMPLETED el 2026-09-24 después de verificar
sus DoD. AUDIT-08 permanece IN_PROGRESS hasta la validación final; COMPLETED
no implica por sí mismo FEATURE VALIDATED.
