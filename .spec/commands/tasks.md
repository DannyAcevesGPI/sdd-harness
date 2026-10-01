# Comando: Tasks

## Propósito

Transformar un PLAN aprobado en un conjunto ordenado, trazable y
verificable de tareas de implementación.

Este comando genera:

specs/`<feature-id>`{=html}/tasks.md

Cada tarea deberá representar una unidad de trabajo suficientemente
pequeña para ser implementada, revisada y validada de forma
independiente cuando sea razonable.

El comando NO implementa código.

------------------------------------------------------------------------

# 1. Entrada

El comando recibe un PLAN existente.

Ejemplo:

/tasks PLAN-001

o conceptualmente:

/tasks specs/001-task-management/plan.md

La SPEC relacionada deberá encontrarse en:

APPROVED

El PLAN relacionado deberá encontrarse en:

APPROVED

Si alguna de estas condiciones no se cumple:

TASK GENERATION STATUS: BLOCKED

No deberán generarse tareas de implementación.

------------------------------------------------------------------------

# 2. Contexto obligatorio

Antes de generar tareas deberá consultarse:

1.  `.spec/constitution.md`
2.  `.spec/standards/architecture.md`
3.  `.spec/standards/coding.md`
4.  `.spec/standards/testing.md`
5.  `.spec/standards/security.md`
6.  `.spec/templates/tasks.template.md`
7.  la SPEC relacionada;
8.  el PLAN aprobado;
9.  ADR relevantes;
10. código existente relacionado cuando sea necesario para determinar
    correctamente el alcance de las tareas.

Las tareas deberán derivarse del PLAN.

No deberán introducir nuevas decisiones arquitectónicas sin actualizar
primero el PLAN.

------------------------------------------------------------------------

# 3. Análisis del PLAN

Antes de generar tareas deberá identificarse:

-   requisitos cubiertos;
-   criterios de aceptación;
-   decisiones técnicas;
-   componentes afectados;
-   archivos previstos;
-   cambios de datos;
-   migraciones;
-   contratos;
-   controles de seguridad;
-   pruebas requeridas;
-   configuración;
-   dependencias externas;
-   ADR;
-   riesgos;
-   orden de implementación.

El objetivo es transformar cada parte implementable del PLAN en trabajo
explícito.

------------------------------------------------------------------------

# 4. Tamaño de tarea

Cada tarea deberá representar un cambio cohesivo y revisable.

Una tarea es demasiado grande cuando:

-   contiene múltiples objetivos independientes;
-   afecta múltiples áreas no relacionadas;
-   mezcla cambios arquitectónicos con funcionalidad;
-   resulta difícil determinar cuándo está terminada;
-   requiere una cantidad excesiva de archivos sin justificación;
-   no puede validarse claramente.

Una tarea es demasiado pequeña cuando:

-   no produce un resultado significativo por sí misma;
-   representa únicamente una operación trivial;
-   divide artificialmente un cambio cohesivo.

Preferir tareas que puedan describirse mediante:

Un objetivo + Un alcance + Una evidencia

------------------------------------------------------------------------

# 5. Identificadores

Cada tarea deberá recibir un identificador único:

TASK-001 TASK-002 TASK-003

Los identificadores:

-   deberán ser únicos dentro de la feature;
-   no deberán reutilizarse;
-   no deberán renumerarse después de ser referenciados.

Si una tarea se elimina después de haber sido utilizada:

TASK-004 --- CANCELLED

El identificador permanecerá reservado.

`CANCELLED` es una anotación histórica del identificador retirado, no un
estado de tarea activa. Deberán registrarse el motivo y la revisión que
autoriza el retiro, recuperando los approval gates aplicables cuando
cambie trabajo aprobado. El retiro no permite omitir trabajo requerido
por SPEC o PLAN; si afecta ese trabajo, deberá revisarse primero el
artefacto propietario. La tarea retirada no pertenece al conjunto activo
de tareas requeridas y su evidencia anterior deberá conservarse.

------------------------------------------------------------------------

# 6. Tipos de tarea

Cuando sea útil, las tareas podrán clasificarse como:

FEATURE TECHNICAL TEST MIGRATION SECURITY CONFIGURATION DOCUMENTATION
REFACTOR

## FEATURE

Implementa comportamiento requerido por la SPEC.

## TECHNICAL

Implementa infraestructura técnica necesaria para otras tareas.

## TEST

Agrega o amplía evidencia automatizada.

## MIGRATION

Modifica estructuras o datos persistentes.

## SECURITY

Implementa controles de seguridad específicos.

## CONFIGURATION

Modifica configuración requerida.

## DOCUMENTATION

Actualiza documentación necesaria.

## REFACTOR

Modifica estructura interna sin cambiar comportamiento observable.

Toda tarea deberá tener una justificación trazable, independientemente
de su tipo.

------------------------------------------------------------------------

# 7. Trazabilidad

Cada tarea deberá indicar por qué existe.

Toda tarea deberá mantener trazabilidad hacia una fuente autorizada de
SPEC o PLAN.

Una tarea podrá relacionarse con:

-   FR-\[XXX\]
-   NFR-\[XXX\]
-   SEC-\[XXX\]
-   AC-\[XXX\]
-   DEC-\[XXX\]
-   ADR-\[XXX\]

También podrá relacionarse adicionalmente con:

-   TASK-\[XXX\]

Una relación con otra TASK puede expresar dependencia, secuencia o
soporte entre unidades de trabajo, pero una relación únicamente con otra
TASK no constituye justificación suficiente.

Las tareas TECHNICAL, MIGRATION, CONFIGURATION, TEST, SECURITY,
DOCUMENTATION o REFACTOR no deberán recibir requisitos funcionales
artificiales únicamente para justificar su existencia.

Cuando no exista relación funcional directa, la justificación deberá
alcanzar una fuente técnica autorizada del PLAN, por ejemplo:

-   DEC-\[XXX\];
-   ADR-\[XXX\];
-   NFR-\[XXX\];
-   SEC-\[XXX\];
-   infraestructura explícitamente requerida por el PLAN;
-   necesidad técnica documentada por el PLAN.

En todos los casos deberá referenciarse al menos un requisito o criterio
de aceptación real que la tarea soporte, directamente o mediante una
cadena explícita del PLAN. Una referencia únicamente a DEC, ADR o
infraestructura no sustituye esta obligación del Artículo IV de la
Constitution. No deberán inventarse requisitos funcionales para cumplirla.

Ejemplo:

TASK-004 --- Validar ownership de Task

Tipo:

SECURITY

Relacionado con:

FR-003 SEC-001 AC-006 DEC-004

Una tarea sin origen trazable deberá considerarse:

ORPHAN TASK

Las tareas huérfanas deberán:

1.  justificarse correctamente;
2.  relacionarse con un artefacto válido;

o:

3.  eliminarse.

No deberán avanzar a implementación.

------------------------------------------------------------------------

# 8. Dependencias

Cada tarea deberá declarar sus dependencias.

Ejemplo:

TASK-001

Depends on: None

TASK-002

Depends on: TASK-001

TASK-003

Depends on: TASK-001

TASK-004

Depends on: TASK-002 TASK-003

Una dependencia significa que la tarea dependiente no puede completarse
correctamente antes de que la dependencia esté lista.

No deberán existir dependencias circulares.

Ejemplo inválido:

TASK-001 → TASK-002

TASK-002 → TASK-003

TASK-003 → TASK-001

Resultado:

DEPENDENCY CYCLE DETECTED

TASK GENERATION STATUS:

BLOCKED

------------------------------------------------------------------------

# 9. Paralelización

Después de construir el grafo de dependencias deberá identificarse qué
tareas pueden ejecutarse en paralelo.

Una tarea podrá considerarse candidata a ejecución paralela cuando:

-   no depende de la otra tarea;
-   no modifica los mismos archivos de forma conflictiva;
-   no depende del resultado intermedio de la otra;
-   no requiere una decisión pendiente compartida.

Ejemplo:

        TASK-001
            │
       ┌────┴────┐
       ▼         ▼

TASK-002 TASK-003 │ │ └────┬────┘ ▼ TASK-004

TASK-002 y TASK-003 pueden ser paralelizables.

La posibilidad de paralelización deberá considerarse una propiedad del
grafo de trabajo, no una obligación.

La corrección y trazabilidad tienen prioridad sobre la velocidad.

------------------------------------------------------------------------

# 10. Alcance de archivos

Cada tarea deberá identificar, cuando sea posible:

CREATE MODIFY REUSE REMOVE

Ejemplo:

TASK-003

CREATE:

src/tasks/task.service.ts

MODIFY:

src/tasks/task.module.ts

REUSE:

src/auth/current-user.ts

REMOVE:

None

Durante implementación, una tarea no deberá modificar archivos fuera de
su alcance previsto salvo que:

1.  el cambio sea necesario para completar correctamente la tarea;
2.  sea coherente con el PLAN;
3.  se documente el motivo.

Si el cambio implica una modificación estructural no prevista:

STOP

PLAN REVISION REQUIRED

------------------------------------------------------------------------

# 11. Conflictos potenciales

Si dos tareas potencialmente paralelas modifican el mismo archivo deberá
marcarse:

FILE CONFLICT

Ejemplo:

TASK-003 MODIFY: src/tasks/task.service.ts

TASK-004 MODIFY: src/tasks/task.service.ts

Resultado:

TASK-003 ↔ TASK-004

Potential file conflict.

Estas tareas deberán:

-   ejecutarse secuencialmente;

o:

-   redefinir su alcance;

cuando sea necesario para evitar cambios incompatibles.

------------------------------------------------------------------------

# 12. Pruebas

Las pruebas no deberán tratarse como trabajo opcional posterior.

Cada criterio de aceptación deberá tener evidencia prevista.

Cuando corresponda deberán generarse tareas o subtareas para:

-   unit tests;
-   integration tests;
-   contract tests;
-   end-to-end tests;
-   security tests;
-   regression tests.

Los tests deberán relacionarse mediante:

TEST-\[XXX\]

Cuando una prueba forme parte natural de una tarea de implementación,
podrá incluirse dentro de la misma tarea.

No es obligatorio crear una tarea separada para cada test.

Ejemplo:

TASK-003 Implementar creación de Task

Incluye:

TEST-004 Task se crea con datos válidos.

TEST-005 Task rechaza datos inválidos.

Para tareas con comportamiento automatizable, TASKS deberá identificar los
casos TEST derivados del PLAN, su relación con requisitos y AC, y exigir en
su Definition of Done evidencia de RED válido antes del cambio productivo y
GREEN después. El ciclo se ejecuta en `/implement`, no durante `/tasks`.

Para trabajo fuera del ámbito TDD, la tarea deberá registrar el motivo y la
verificación alternativa. Una prueba automatizable bloqueada por entorno no
es una excepción: la tarea permanecerá BLOCKED. Véase
`.spec/standards/testing.md`.

------------------------------------------------------------------------

# 13. Definition of Done

Cada tarea deberá incluir condiciones verificables de finalización.

Como mínimo:

-   implementación completada;
-   requisitos asociados satisfechos;
-   pruebas requeridas implementadas;
-   pruebas relevantes en PASS;
-   estándares respetados;
-   alcance respetado;
-   evidencia disponible.

Una tarea no podrá marcarse DONE únicamente porque "el código fue
escrito".

------------------------------------------------------------------------

# 14. Aclaraciones durante generación de tareas

Si durante `/tasks` aparece una ambigüedad deberá determinarse su
origen.

Si corresponde a:

SPEC

Resultado:

SPEC REVISION REQUIRED

Si corresponde a:

PLAN

Resultado:

PLAN REVISION REQUIRED

Si corresponde únicamente a cómo dividir trabajo:

Q-TASK-\[XXX\] \[NEEDS CLARIFICATION\]

No deberá inventarse una decisión que cambie la SPEC o PLAN.

------------------------------------------------------------------------

# 15. Coverage check

Antes de finalizar deberá verificarse que todo elemento implementable
del PLAN tenga cobertura.

Ejemplo:

PLAN

DEC-001 → TASK-001 DEC-002 → TASK-002 SEC-001 → TASK-004 AC-001 →
TASK-003 AC-002 → TASK-005

Si existe un elemento obligatorio sin tarea:

UNCOVERED PLAN ITEM

El documento no podrá considerarse completo.

------------------------------------------------------------------------

# 16. Orphan check

Toda tarea deberá poder justificarse mediante SPEC o PLAN.

Una relación únicamente con otra TASK no evita que una tarea sea
considerada ORPHAN TASK si no puede reconstruirse su justificación hasta
una fuente autorizada de SPEC o PLAN.

Ejemplo:

TASK-009 Agregar Redis

No existe:

FR NFR SEC DEC ADR dependencia técnica

que justifique Redis.

Resultado:

ORPHAN TASK

La tarea deberá eliminarse o justificarse mediante una revisión del
PLAN.

------------------------------------------------------------------------

# 17. Orden de ejecución

Después de generar las tareas deberá construirse un orden de ejecución
respetando dependencias.

Ejemplo:

PHASE 1 --- Foundation

TASK-001 TASK-002

PHASE 2 --- Core behavior

TASK-003 TASK-004

PHASE 3 --- Interfaces

TASK-005

PHASE 4 --- Verification

TASK-006

Las fases sirven para mejorar legibilidad.

Las dependencias TASK → TASK constituyen la fuente real de orden de
ejecución.

------------------------------------------------------------------------

# 18. Creación del artefacto

El comando deberá utilizar:

.spec/templates/tasks.template.md

como estructura base.

El resultado deberá guardarse en:

specs/`<feature-id>`{=html}/tasks.md

Ejemplo:

specs/001-task-management/ ├── spec.md ├── plan.md └── tasks.md

La plantilla original no deberá modificarse.

------------------------------------------------------------------------

# 19. Self-check

Antes de finalizar `/tasks` verificar:

-   [ ] SPEC está APPROVED.
-   [ ] PLAN está APPROVED.
-   [ ] Cada tarea tiene un objetivo claro.
-   [ ] Cada tarea tiene trazabilidad.
-   [ ] No existen tareas huérfanas.
-   [ ] Todo elemento obligatorio del PLAN tiene cobertura.
-   [ ] Todos los requisitos MUST tienen cobertura.
-   [ ] Las dependencias están definidas.
-   [ ] No existen dependencias circulares.
-   [ ] El alcance de archivos está identificado cuando es posible.
-   [ ] Los conflictos potenciales están identificados.
-   [ ] Las pruebas requeridas están contempladas.
-   [ ] Cada tarea tiene Definition of Done.
-   [ ] Las tareas son suficientemente pequeñas y cohesivas.
-   [ ] No se introdujeron nuevas decisiones arquitectónicas.
-   [ ] No existen `[NEEDS CLARIFICATION]` bloqueantes.

------------------------------------------------------------------------

# 20. Estado resultante

`TASK GENERATION STATUS` describe el resultado de la operación, no el
estado del documento. Un bloqueo no añade `BLOCKED` al ciclo de TASKS:
un borrador permanece `DRAFT`; una revisión de trabajo aprobado deberá
recuperar los approval gates aplicables antes de continuar su ejecución.

Si existe una deficiencia funcional:

TASK GENERATION STATUS:

BLOCKED

RESULT:

SPEC REVISION REQUIRED

------------------------------------------------------------------------

Si existe una deficiencia técnica:

TASK GENERATION STATUS:

BLOCKED

RESULT:

PLAN REVISION REQUIRED

------------------------------------------------------------------------

Si existen aclaraciones bloqueantes:

TASKS STATUS:

DRAFT

RESULT:

NEEDS CLARIFICATION

------------------------------------------------------------------------

Si las tareas están completas:

TASKS STATUS:

IN_REVIEW

RESULT:

READY FOR REVIEW

------------------------------------------------------------------------

Las tareas solamente podrán pasar a:

APPROVED

mediante aprobación humana explícita.

Para features nuevas, registrar la aprobación de TASKS con su alcance y
huella normalizada en `decisions.json` y ejecutar el comprobador de
`docs/state-reconstruction.md` antes de `/implement`. Las transiciones de
estado y checklists operativos permitidos no cambian el contenido autorizado;
un cambio de objetivos, dependencias, pruebas o alcance sí recupera el gate.
Durante `/tasks`, se permite modificar ese ledger y solo estado/enlaces de
`handoff.md` y `docs/index.md`; no código ni pruebas antes de `/implement`.

------------------------------------------------------------------------

# 21. Salida

Formato recomendado:

SDD TASK BREAKDOWN ────────────────────────────────

SPEC: SPEC-001

PLAN: PLAN-001

TASKS: TASKS-001

Path: specs/001-task-management/tasks.md

Tasks: 8

By type:

FEATURE: 3 TECHNICAL: 1 MIGRATION: 1 SECURITY: 1 TEST: 2

Dependencies: 7

Parallel candidates: 2

File conflicts: 1

Coverage: FR: 5/5 NFR: 1/1 SEC: 2/2 AC: 8/8

Orphan tasks: 0

Blocking clarifications: 0

Status: READY FOR REVIEW

Next: Human approval ────────────────────────────────

------------------------------------------------------------------------

# 22. Acciones prohibidas

Durante `/tasks` el agente NO deberá:

-   implementar código;
-   modificar código de aplicación;
-   instalar dependencias;
-   ejecutar migraciones;
-   modificar la SPEC silenciosamente;
-   modificar el PLAN silenciosamente;
-   introducir arquitectura nueva no aprobada;
-   agregar funcionalidad no solicitada;
-   crear tareas sin justificación;
-   ignorar dependencias;
-   ignorar conflictos conocidos;
-   marcar TASKS como APPROVED sin aprobación humana explícita.

El objetivo exclusivo es transformar el PLAN aprobado en unidades de
trabajo implementables, trazables y verificables.
