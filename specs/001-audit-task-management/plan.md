# Plan Técnico: Gestión de tareas para AUDIT-08

**ID:** PLAN-001  
**SPEC relacionada:** SPEC-001 v0.1.0  
**Estado:** APPROVED  
**Versión:** 0.1.0  
**Fecha:** 2026-09-24

# 1. Precondiciones

- [x] SPEC-001 existe y está APPROVED por confirmación humana registrada en Q-001.
- [x] No quedan aclaraciones funcionales bloqueantes.
- [x] Todos los MUST tienen criterios de aceptación.
- [x] Alcance y restricciones están definidos.
- [x] Se inspeccionaron repositorio, standards y entorno local.

# 2. Resumen técnico

## 2.1 Objetivo

Implementar una biblioteca local mínima que permita ejecutar los nueve AC
de SPEC-001 y producir evidencia real para AUDIT-08.

## 2.2 Enfoque

Un servicio Python con estado por instancia, tres operaciones públicas y
datos de salida inmutables. Pruebas con `unittest` y biblioteca estándar.
No requiere servidor, base de datos, instalación de paquetes ni red.
Las decisiones siguientes fueron aprobadas por el usuario para este ejercicio.

# 3. Requisitos cubiertos

| Requisito | Cobertura técnica | Decisiones |
|---|---|---|
| FR-001 | Validar título, asignar ID y propietario, almacenar tarea pendiente | DEC-001, DEC-002, DEC-003 |
| FR-002 | Filtrar por identidad y conservar orden de inserción | DEC-002, DEC-003 |
| FR-003 | Validar propiedad y completar de forma idempotente | DEC-002, DEC-003 |
| NFR-001 | Ejecución local sin dependencias externas; dos ejecuciones limpias | DEC-001, DEC-004 |
| SEC-001 | Identidad válida obligatoria; creación sin argumento propietario | DEC-003 |
| SEC-002 | Filtrado y verificación de propiedad; error común sin datos ajenos | DEC-002, DEC-003 |
| BR-001 | Normalización mediante strip, rechazo de no texto/vacío, duplicados válidos | DEC-003 |
| BR-002 | PENDING/COMPLETED y finalización idempotente | DEC-002 |
| BR-003 | Propietario asignado desde identidad y no modificable | DEC-002, DEC-003 |

# 4. Contexto técnico existente

Inspección realizada el 2026-09-24 mediante listado de archivos, búsqueda en
`src/`, `tests/`, `docs/` y consulta del runtime:

- El repositorio contiene el Harness y SPEC-001; no hay aplicación existente.
- `src/`, `tests/` y `docs/` no contienen archivos; no hay ADR previos.
- No hay framework, ORM, API, configuración de paquetes o CI/CD establecido.
- `python3 --version`: Python 3.12.3, disponible en el entorno.
- No se encontraron ejecutables ni módulos de ruff, black, mypy o pytest.
- `.gitignore` está vacío. Los artefactos actuales aún no están versionados
  mediante commits; se usará working tree y hashes como referencia de evidencia.

No existe componente de aplicación reutilizable. Se reutilizan los standards,
templates, commands y herramientas de la biblioteca estándar. El stack propuesto
aplica al espécimen y no prescribe el stack de futuros proyectos del Harness.

# 5. Decisiones técnicas

## DEC-001 — Python y biblioteca estándar

**Decisión:** Python 3.12, sin dependencias externas; `unittest` para pruebas.
**Justificación:** satisface NFR-001 con el runtime local comprobado y permite
implementar FR-001 a FR-003 sin bootstrap de infraestructura.
**Alternativas:** framework web o herramientas externas de pruebas; no aportan
capacidad requerida por la SPEC y ampliarían instalación y superficie de fallo.
**Consecuencias:** biblioteca local, sin interfaz de red ni distribución como paquete.
**Requisitos:** FR-001, FR-002, FR-003, NFR-001. **Requiere ADR:** NO.

## DEC-002 — Estado encapsulado por instancia

**Decisión:** `TaskService` mantiene un diccionario privado ordenado por inserción
y un contador de ID por instancia. `Task` es una dataclass inmutable; completar
sustituye el registro conservando ID, título, propietario y posición.
**Justificación:** no hay persistencia entre ejecuciones ni concurrencia requerida.
**Alternativas:** base de datos o capa repository separada; innecesarias para la muestra.
**Consecuencias:** cada nueva instancia comienza vacía; listados y objetos devueltos
no permiten modificar el estado interno mediante la interfaz pública.
**Requisitos:** FR-001, FR-002, FR-003, SEC-002, BR-002, BR-003.
**Requiere ADR:** NO.

## DEC-003 — Límite confiable e identidad explícita

**Decisión:** cada operación recibe `actor_id` como argumento keyword-only desde
el llamador confiable del ejercicio. No existe argumento `owner_id` en creación.
Validar identidad antes de procesar título o buscar tareas. Toda autorización se
realiza dentro del servicio; no se delega en las pruebas como único control.
**Justificación:** SEC-001/002 y AC-008 requieren separar identidad de datos de creación.
**Alternativas:** proveedor de autenticación o actor tomado de un payload arbitrario;
el primero está fuera de alcance y el segundo permitiría suplantación en ese límite.
**Consecuencias:** código local hostil con acceso al proceso no está aislado; estas
pruebas no demuestran autenticación de producción. La identidad se compara exactamente
como fue proporcionada; strip solo detecta identidad vacía, no fusiona identificadores.
**Requisitos:** SEC-001, SEC-002, FR-001, FR-002, FR-003, BR-001, BR-003.
**Cambio sensible:** YES, autorización y validación de entradas.
**Requiere ADR:** NO.

## DEC-004 — Evidencia reproducible y separada por ejecución

**Decisión:** pruebas observables vía API pública, estado nuevo por caso y dos
ejecuciones de la suite en procesos independientes. Guardar comandos, resultados,
fecha y hashes del código/pruebas en evidencia de la feature.
**Justificación:** NFR-001/AC-009 y la cadena de trazabilidad del Harness.
**Alternativas:** evidencia verbal o mocks del propio servicio; no demuestran los AC.
**Consecuencias:** ningún PASS se registra hasta ejecutar y examinar su resultado.
**Requisitos:** NFR-001; soporta FR-001 a FR-003 y SEC-001/002.
**Requiere ADR:** NO.

# 6. Arquitectura propuesta

## 6.1 Componentes

| Componente | Responsabilidad | Cambio |
|---|---|---|
| `src/audit_tasks.py` | Modelo, servicio, validación y errores públicos | CREATE |
| `tests/test_audit_tasks.py` | Casos funcionales, seguridad y flujo completo local | CREATE |
| Evidencia de la feature | Trazabilidad, comandos, resultados y hashes | CREATE |
| `unittest`, `dataclasses` | Pruebas y representación inmutable | REUSE |

## 6.2 Flujo

Llamador confiable con identidad → operación pública → validación de identidad
→ validación de entrada/autorización → estado en memoria → resultado inmutable.

## 6.3 Dependencias

Pruebas → módulo de aplicación → biblioteca estándar. Sin dependencias circulares,
estado global mutable, integraciones externas ni procesos asíncronos.

# 7. Modelo de datos

| Campo de Task | Tipo | Regla |
|---|---|---|
| id | int | Positivo, incremental y único por instancia |
| title | str | strip aplicado; no vacío |
| owner_id | str | Identidad validada del actor de creación, inmutable |
| status | str | PENDING o COMPLETED |

Relación conceptual: un actor posee cero o más tareas. No existe tabla de usuarios.
No se usa reloj para ordenar: el diccionario conserva el orden de creación.
El contador avanza solo tras validar la creación. El listado devuelve una nueva
lista de registros inmutables, no la colección interna.
**Migración:** NO. **Cambio destructivo:** NO.

# 8. Interfaces y contratos

API Python pública propuesta; las firmas describen contratos, no implementación:

| Operación | Entrada | Salida | Requisitos |
|---|---|---|---|
| `TaskService()` | Ninguna | Servicio vacío | NFR-001 |
| `create_task(*, actor_id, title)` | Identidad confiable y título | Task recién creada | FR-001, SEC-001, BR-001/003 |
| `list_tasks(*, actor_id)` | Identidad confiable | list[Task] propia ordenada | FR-002, SEC-001/002 |
| `complete_task(*, actor_id, task_id)` | Identidad confiable e ID | Task en COMPLETED | FR-003, SEC-001/002, BR-002 |

Se agregarán anotaciones de tipos sin reemplazar validación en runtime. La ausencia
de identidad se representa con `None`; omitir un argumento requerido es un error
de llamada Python y no modifica el estado. Un argumento `owner_id` extra se rechaza
por la firma de creación, sin mutación.

Errores públicos: `IdentityRequiredError`, `InvalidTitleError` y
`TaskUnavailableError`, derivados de `ValueError`, con mensajes fijos definidos
en §17. No incorporan valores de entrada ni datos de otras tareas.

# 9. Validación de entradas

- Identidad: str y `strip()` no vacío; no modificar su valor para compararla.
- Título: str y `strip()` no vacío; guardar el valor recortado.
- ID de tarea: int positivo, excluyendo bool; valores inválidos se tratan como
  tarea no disponible, igual que identificadores inexistentes.
- Orden: identidad primero; en creación, título después; en finalización,
  formato del ID, búsqueda y propiedad antes de cualquier mutación.
- Todas las comprobaciones aplican en el servicio, sin depender de una UI.

# 10. Seguridad

SEC-001 se verifica en las tres operaciones. SEC-002 se aplica al filtrar listados
y al comprobar propietario antes de completar. El error de tarea ajena y el de
tarea inexistente comparten clase y mensaje. No se afirma indistinguibilidad temporal.

Solo se usan datos sintéticos, sin secretos, archivos subidos, consultas SQL,
operaciones destructivas ni salida de red. No hay logs de aplicación. Los registros
devueltos son inmutables para evitar mutaciones indirectas por el contrato público.
La identidad proviene del entorno de prueba confiable, no de un mecanismo de login.

# 11. Estrategia de pruebas

## 11.1 Mapeo inicial

| Criterio | Tipo previsto | Verificación |
|---|---|---|
| AC-001 | UNIT | Creación, strip, duplicados, IDs distintos y estado inicial |
| AC-002 | UNIT | Entradas inválidas y ausencia de mutaciones |
| AC-003 | SECURITY | Listado propio ordenado con tareas intercaladas y completadas |
| AC-004 | SECURITY | Actor vacío frente a tareas de otro actor |
| AC-005 | UNIT | Finalización repetida, estado y propiedad preservados |
| AC-006 | SECURITY | Matriz de identidades inválidas por cada operación |
| AC-007 | SECURITY | Error común para tarea ajena/inexistente y estado intacto |
| AC-008 | SECURITY / CONTRACT | Propietario derivado, argumento owner_id rechazado |
| AC-009 | OTHER | Dos procesos de pruebas limpios con resultados registrados |

Además se verificará un flujo completo crear → listar → completar → listar
usando el servicio real, y que modificar una lista devuelta no modifica el servicio.
Los IDs TEST se asignarán en TASKS. No hay pruebas de navegador ni integraciones
externas que justificar; el flujo completo local es el E2E de esta biblioteca.

## 11.2 Comandos y quality gates previstos

Desde la raíz, ejecutar dos veces en procesos independientes:

`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest discover -s tests -v`

Registrar número de pruebas, subcasos relevantes, códigos de salida y resultados
sin tests requeridos omitidos. Una instancia nueva por caso evita contaminación.
Verificar sintaxis y consistencia de indentación con herramientas estándar de
Python (`compile` sin escribir bytecode y `tabnanny`). Revisar nombres, tipos,
formato y controles de seguridad mediante inspección trazada a los standards.

El repositorio no tiene formatter, linter ni type checker configurados: no se
inventará un PASS automático para esos controles. Se documentará la revisión
manual y la ausencia de esas herramientas; no se instalarán dependencias para
este espécimen. No hay build de distribución ni migraciones aplicables.

## 11.3 Ensayo controlado del retorno desde validación

Para comprobar el proceso corregido en AUDIT-FINDING-034, TASKS deberá separar
un ensayo de auditoría de la evidencia final de la implementación:

1. Partir de una ejecución correcta y conservar sus artefactos y hashes.
2. En una copia temporal aislada y explícitamente identificada como fixture de
   auditoría, representar TASKS completadas y aplicar un defecto controlado de
   orden de listado (FR-002/AC-003). No desactivar controles de autorización.
3. Ejecutar pruebas originales sin debilitar assertions; registrar el fallo real
   y la invalidez de la evidencia anterior para esa copia. No fingir que las
   pruebas pasaron con el código alterado ni atribuir el defecto al Harness.
4. Registrar el finding de validación de la copia y ejercitar `/implement` §17.1:
   reapertura, preflight, corrección de orden y nuevas pruebas/evidencia.
5. Cerrar las tareas de la copia y repetir su validación. Guardar un registro
   diferenciado del ensayo; solo validar la feature principal contra su código
   y evidencia reales. No copiar aprobaciones ficticias ni cambiar alcance.

La aprobación de PLAN y TASKS deberá cubrir este ensayo. Los artefactos de la
copia son una simulación rotulada; no autorizan trabajo adicional ni reemplazan
los gates reales de la feature. Los detalles de ejecución se concretarán en TASKS.

# 12. Observabilidad

Salida de `unittest` y registros de evidencia por ejecución. Registrar comandos,
fecha, entorno, archivos y hashes; solamente datos sintéticos. Métricas de servicio,
health checks y logging productivo no aplican a esta biblioteca local.

# 13. Impacto en el repositorio

**CREATE durante implementación:** `src/audit_tasks.py`, `tests/test_audit_tasks.py`,
`specs/001-audit-task-management/evidence.md` y archivos de resultados bajo
`specs/001-audit-task-management/evidence/`.
**CREATE en su fase SDD:** `tasks.md` y `validation.md` en el directorio de la feature.
**MODIFY:** estados y evidencia de TASKS; checkpoint de `handoff.md` como registro
de auditoría. No se modifica la SPEC aprobada para acomodar la implementación.
**REUSE:** Harness y biblioteca estándar. **REMOVE:** ninguno.
El ensayo usa una carpeta temporal propia; no altera archivos ajenos ni añade
defectos deliberados a la implementación principal.

# 14. Dependencias

Ninguna dependencia externa nueva. Python 3.12 disponible es el prerrequisito;
`unittest` y `dataclasses` forman parte de su biblioteca estándar.

# 15. Configuración

`PYTHONPATH=src` para importar el módulo en pruebas y
`PYTHONDONTWRITEBYTECODE=1` para evitar cachés durante la ejecución.
No son secretos. No se requiere `.env`, configuración de aplicación ni package manager.

# 16. Migración y compatibilidad

No hay datos existentes, contratos anteriores o esquema persistente.
**Breaking changes:** NO. **Migraciones/rollback de datos:** NOT_APPLICABLE.
La biblioteca se añade exclusivamente para el espécimen de auditoría.

# 17. Manejo de errores

| Condición | Excepción | Mensaje fijo |
|---|---|---|
| Identidad inválida | IdentityRequiredError | Valid actor identity required |
| Título inválido con identidad válida | InvalidTitleError | Valid title required |
| ID inválido, inexistente o tarea ajena | TaskUnavailableError | Task unavailable |
| Argumento omitido o extra | TypeError de la firma Python | No se fija texto dependiente del runtime |

Errores de entrada y autorización no alteran estado. No se capturan excepciones
inesperadas para convertirlas en éxito; quedan visibles para diagnóstico local.

# 18. Riesgos técnicos

| ID | Riesgo | Impacto | Probabilidad | Mitigación |
|---|---|---|---|---|
| RISK-001 | Confundir identidad sintética con autenticación real | HIGH | MEDIUM | Límite confiable explícito y alcance de evidencia restringido |
| RISK-002 | Mutación del estado por referencias devueltas | MEDIUM | MEDIUM | Registros inmutables y colecciones nuevas; prueba observable |
| RISK-003 | Contaminación entre casos o uso de evidencia obsoleta | HIGH | MEDIUM | Estado por instancia, procesos independientes y hashes |
| RISK-004 | Confundir el defecto inyectado con un defecto real del Harness | MEDIUM | MEDIUM | Copia aislada y registros separados del ensayo |

# 19. Aclaraciones técnicas

No se identificaron decisiones técnicas bloqueantes pendientes de información.
Las decisiones de este PLAN fueron aprobadas sin modificaciones técnicas. Si una
revisión posterior cambia alcance funcional, se volverá a SPEC antes de continuar.

# 20. ADR requeridos

Ninguno. Las decisiones son locales, reversibles y limitadas al espécimen,
sin arquitectura productiva o transversal. Se documentan en DEC-001 a DEC-004.

# 21. Orden de implementación

1. Modelo, errores y creación validada con pruebas.
2. Listado, finalización y controles de propietario con pruebas.
3. Flujo completo, revisión de controles, dos ejecuciones limpias y evidencia.
4. Ensayo aislado de retorno desde validación y registro de resultados.
5. Cierre de TASKS y `/validate` de la feature principal.

Esta secuencia orienta la descomposición; no constituye TASKS aprobado.

# 22. Criterios para avanzar a Tasks

- [x] SPEC aprobada y cobertura de FR, NFR, SEC y BR identificada.
- [x] Repositorio y runtime inspeccionados; reutilización evaluada.
- [x] Componentes, datos, contratos, seguridad y errores definidos.
- [x] Los nueve AC tienen estrategia de evidencia.
- [x] Impacto, dependencias, riesgos y aplicabilidad de ADR documentados.
- [x] No hay aclaraciones técnicas bloqueantes identificadas.
- [x] PLAN aprobado explícitamente por el humano.

# 23. Estado del plan

**Estado actual:** APPROVED. **Resultado:** READY FOR TASKS.
Estados permitidos: DRAFT → IN_REVIEW → APPROVED → SUPERSEDED.
**Aprobado por:** usuario humano. **Fecha de aprobación:** 2026-09-24.
**Evidencia:** «Apruebo ese plan», en respuesta a la solicitud de aprobación
de PLAN-001 v0.1.0 para avanzar a `/tasks`. Se registra IN_REVIEW → APPROVED;
no se cambian decisiones, contratos ni estrategia del contenido presentado.

Siguiente fase autorizada: `/tasks`. La implementación aún requiere aprobación
humana del documento TASKS resultante.
