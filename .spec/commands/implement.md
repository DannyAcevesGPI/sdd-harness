# Comando: Implement

## Propósito

Ejecutar las tareas aprobadas de una feature de forma controlada,
trazable y verificable.

Este es el primer comando del flujo SDD autorizado para modificar el
código fuente del repositorio.

El comando deberá implementar exclusivamente trabajo autorizado por:

SPEC → PLAN → TASKS

La implementación no deberá introducir silenciosamente nuevos
requisitos, decisiones arquitectónicas o cambios fuera de alcance.

------------------------------------------------------------------------

# 1. Entrada

El comando puede recibir:

-   una TASK específica;
-   un conjunto de TASKS;
-   todas las tareas pendientes de una feature.

Ejemplos conceptuales:

/implement TASK-003

/implement TASK-003 TASK-004

/implement SPEC-001

Cuando se solicite implementar una feature completa deberán respetarse
las dependencias definidas en `tasks.md`.

------------------------------------------------------------------------

# 2. Precondiciones

Antes de modificar código deberá verificarse:

-   [ ] La SPEC existe.
-   [ ] La SPEC está `APPROVED`.
-   [ ] El PLAN existe.
-   [ ] El PLAN está `APPROVED`.
-   [ ] TASKS existe.
-   [ ] TASKS está `APPROVED` o `IN_PROGRESS`.
-   [ ] La tarea objetivo existe.
-   [ ] La tarea está en estado `TODO` o `IN_PROGRESS`.
-   [ ] Sus dependencias obligatorias están satisfechas.
-   [ ] No existen `[NEEDS CLARIFICATION]` bloqueantes.
-   [ ] No existe un bloqueo conocido que impida la tarea.

Si alguna precondición obligatoria no se cumple:

IMPLEMENTATION STATUS:

BLOCKED

No deberá modificarse código.

------------------------------------------------------------------------

# 3. Contexto obligatorio

Antes de implementar deberá consultarse:

1.  `.spec/constitution.md`
2.  `.spec/standards/architecture.md`
3.  `.spec/standards/coding.md`
4.  `.spec/standards/testing.md`
5.  `.spec/standards/security.md`
6.  la SPEC asociada;
7.  el PLAN asociado;
8.  TASKS;
9.  la tarea objetivo;
10. ADR relevantes;
11. código relacionado;
12. pruebas existentes relacionadas.

El agente deberá comprender el contexto real del código antes de
modificarlo.

------------------------------------------------------------------------

# 4. Preflight

Antes de comenzar una TASK deberá realizarse un preflight.

Verificar:

## Task

-   ID válido;
-   objetivo;
-   tipo;
-   estado;
-   prioridad.

## Traceability

-   requisitos relacionados;
-   criterios de aceptación;
-   decisiones técnicas relacionadas;
-   pruebas requeridas.

## Dependencies

-   TASKS requeridas completadas.

## Scope

-   archivos previstos;
-   módulos afectados;
-   elementos reutilizables.

## Repository State

-   los archivos esperados existen cuando corresponde;
-   la estructura coincide razonablemente con el PLAN;
-   no existen cambios inesperados que invaliden la tarea.

## Blocking Conditions

-   no existen aclaraciones bloqueantes;
-   no existen conflictos conocidos;
-   no existe una revisión superior pendiente.

------------------------------------------------------------------------

# 5. Inicio de tarea

Una vez superado el preflight:

## Estado del documento TASKS

Si el documento TASKS se encuentra en `APPROVED` y comienza la primera
tarea requerida de la feature:

TASKS STATUS:

APPROVED → IN_PROGRESS

Esta transición deberá registrarse antes o junto con el inicio de la
primera tarea cuando el mecanismo utilizado lo permita.

El inicio de tareas posteriores no deberá volver a modificar el estado
del documento mientras permanezca `IN_PROGRESS`.

## Estado de la TASK

TASK STATUS:

TODO → IN_PROGRESS

El cambio de estado deberá registrarse antes de realizar la
implementación cuando el mecanismo utilizado lo permita.

------------------------------------------------------------------------

# 6. Implementación

El agente deberá realizar el cambio mínimo necesario para cumplir el
objetivo de la TASK.

La implementación deberá respetar:

-   SPEC;
-   PLAN;
-   TASKS;
-   Constitution;
-   Standards;
-   ADR aplicables;
-   patrones existentes del repositorio.

No deberá ampliarse el alcance únicamente porque exista una oportunidad
de mejora.

## Regla de mínimo cambio

Preferir:

el cambio más pequeño que satisface correctamente los requisitos
aprobados.

Evitar:

-   refactors no relacionados;
-   renombrados innecesarios;
-   cambios cosméticos masivos;
-   nuevas abstracciones especulativas;
-   nuevas dependencias innecesarias;
-   funcionalidades "por si acaso";
-   modificaciones fuera de la TASK.

------------------------------------------------------------------------

# 7. Control de alcance

Antes de modificar un archivo deberá comprobarse si está dentro del
alcance previsto de la TASK.

Clasificaciones:

CREATE MODIFY REUSE REMOVE

Si durante implementación es necesario modificar un archivo no previsto
deberá evaluarse el motivo.

## Cambio menor no previsto

Puede realizarse cuando:

-   es estrictamente necesario para completar la TASK;
-   no cambia arquitectura;
-   no cambia requisitos;
-   no cambia contratos importantes;
-   no introduce una dependencia nueva;
-   permanece dentro del objetivo aprobado.

El cambio deberá registrarse en la evidencia.

------------------------------------------------------------------------

## Cambio estructural no previsto

Si requiere:

-   nueva arquitectura;
-   nueva dependencia importante;
-   nuevo módulo significativo;
-   cambio de contrato;
-   cambio de persistencia no planificado;
-   cambio de requisito;

deberá detenerse la implementación.

Resultado:

PLAN REVISION REQUIRED

o:

SPEC REVISION REQUIRED

------------------------------------------------------------------------

# 8. Pruebas durante implementación

Para cambios de comportamiento automatizable, TDD es obligatorio:

1.  RED: implementar o ajustar el caso aprobado y ejecutarlo antes del cambio
    productivo. Confirmar que falla por el comportamiento faltante o incorrecto.
2.  GREEN: aplicar el cambio mínimo y repetir hasta que el caso pase; ejecutar
    las pruebas relevantes.
3.  REFACTOR: mejorar el código solo cuando sea necesario y mantener las
    pruebas en verde.

Registrar TEST, requisito/AC, comando, resultado y causa del RED, comando y
resultado GREEN, y resultado posterior al refactor cuando exista. La prueba
que ya pasaba antes del cambio no demuestra RED; revisar el caso sin fabricar
un fallo. Fallas de sintaxis, configuración, dependencias o infraestructura
no son RED válido. Si el entorno impide ejecutar una prueba automatizable,
registrar BLOCK y dejar la TASK en BLOCKED hasta resolverlo.

Documentación, validación exclusivamente manual y refactors sin comportamiento
nuevo requieren motivo y verificación alternativa. Una preferencia por omitir
TDD no justifica una excepción. Seguir `.spec/standards/testing.md` y guardar
el detalle en `specs/<feature-id>/evidence/`.

------------------------------------------------------------------------

# 9. Manejo de pruebas fallidas

Cuando una prueba falle deberá determinarse la causa.

Posibles causas:

A. Implementación incorrecta. B. Test incorrecto. C. SPEC incorrecta o
incompleta. D. PLAN incorrecto. E. Problema externo o de entorno.

## A --- Implementación incorrecta

Corregir la implementación.

NO modificar el test para ocultar el fallo.

------------------------------------------------------------------------

## B --- Test incorrecto

Si el test contradice claramente la SPEC o el comportamiento aprobado:

corregir el test;

documentar el motivo.

------------------------------------------------------------------------

## C --- Problema en SPEC

STOP

Resultado:

SPEC REVISION REQUIRED

No adaptar silenciosamente la implementación.

------------------------------------------------------------------------

## D --- Problema en PLAN

STOP

Resultado:

PLAN REVISION REQUIRED

------------------------------------------------------------------------

## E --- Problema externo

Registrar:

BLOCK-\[XXX\]

y cambiar la TASK a:

BLOCKED

cuando impida continuar.

------------------------------------------------------------------------

# 10. Integridad de pruebas

El agente NO deberá hacer que una prueba pase mediante:

-   eliminar la prueba;
-   saltarla sin justificación;
-   debilitar una aserción correcta;
-   reemplazar datos reales por mocks irrelevantes;
-   capturar silenciosamente errores;
-   hardcodear valores exclusivamente para satisfacer el test;
-   modificar el comportamiento esperado sin actualizar la SPEC.

Una prueba en PASS solamente constituye evidencia cuando realmente
verifica el comportamiento requerido.

------------------------------------------------------------------------

# 11. Quality checks

Después de implementar una TASK deberán ejecutarse los controles
relevantes disponibles en el proyecto.

Cuando existan:

-   formatter;
-   linter;
-   type checker;
-   unit tests;
-   integration tests;
-   contract tests;
-   security checks;
-   build.

No todos los proyectos tendrán todos los controles.

Deberán ejecutarse los relevantes para el cambio realizado.

------------------------------------------------------------------------

# 12. Regresión

Además de las pruebas nuevas deberán ejecutarse pruebas existentes
relevantes para detectar regresiones.

Si una prueba previamente válida falla como consecuencia del cambio:

la TASK no podrá marcarse como DONE hasta comprender y resolver el
impacto.

No deberá ignorarse una regresión únicamente porque la nueva
funcionalidad funciona.

------------------------------------------------------------------------

# 13. Security check

Cuando la TASK afecte:

-   autenticación;
-   autorización;
-   datos sensibles;
-   secretos;
-   uploads;
-   operaciones destructivas;
-   integraciones externas;
-   queries;
-   inputs externos;

deberán revisarse los controles definidos en:

.spec/standards/security.md

Los requisitos SEC asociados deberán tener evidencia.

------------------------------------------------------------------------

# 14. Descubrimientos

Durante implementación pueden descubrirse:

-   deuda técnica;
-   bugs no relacionados;
-   mejoras;
-   oportunidades de refactor;
-   problemas arquitectónicos;
-   necesidades futuras.

Cuando estén fuera del alcance de la TASK deberán registrarse como:

DISCOVERY-\[XXX\]

No deberán implementarse automáticamente.

------------------------------------------------------------------------

# 15. Aclaraciones durante implementación

Si aparece una ambigüedad que impida implementar correctamente:

\[NEEDS CLARIFICATION\]

Registrar:

BLOCK-\[XXX\]

**Task:** TASK-\[XXX\]

**Estado:** \[NEEDS CLARIFICATION\]

**Pregunta:**

\[Pregunta.\]

**Impacto:**

\[Impacto.\]

**Bloqueante:** YES

**Origen probable:**

SPEC \| PLAN \| TASK \| EXTERNAL

La TASK deberá cambiar a:

BLOCKED

No deberá continuar con una suposición que pueda cambiar el
comportamiento esperado.

------------------------------------------------------------------------

# 16. Escalamiento

Cuando aparezca un problema deberá escalarse al artefacto que posee la
decisión.

## Problema funcional

Ejemplos:

-   comportamiento;
-   permisos;
-   alcance;
-   reglas de negocio.

Volver a:

SPEC

Resultado:

SPEC REVISION REQUIRED

------------------------------------------------------------------------

## Problema arquitectónico o técnico

Ejemplos:

-   componente incorrecto;
-   contrato incorrecto;
-   modelo de datos incorrecto;
-   dependencia técnica faltante.

Volver a:

PLAN

Resultado:

PLAN REVISION REQUIRED

------------------------------------------------------------------------

## Problema de descomposición

Ejemplos:

-   TASK demasiado grande;
-   dependencia incorrecta;
-   conflicto de archivos.

Volver a:

TASKS

Resultado:

TASK REVISION REQUIRED

------------------------------------------------------------------------

## Problema exclusivamente de implementación

Corregir dentro de la TASK.

------------------------------------------------------------------------

# 17. Reanudación después de revisión

Cuando la implementación se haya detenido debido a:

SPEC REVISION REQUIRED

PLAN REVISION REQUIRED

o:

TASK REVISION REQUIRED

la implementación NO deberá reanudarse automáticamente.

Antes de continuar deberá verificarse:

1.  que el artefacto propietario de la decisión fue actualizado;
2.  que se evaluó el impacto sobre los artefactos downstream;
3.  que solamente los artefactos realmente afectados fueron
    actualizados;
4.  que todo artefacto previamente `APPROVED` cuyo contenido autorizado
    haya cambiado recuperó su approval gate correspondiente; las
    actualizaciones de estado y evidencia que no cambian el trabajo
    autorizado no requieren una nueva aprobación;
5.  que TASKS fue actualizado cuando el cambio afecte descomposición,
    dependencias, alcance o pruebas;
6.  que se revisó si evidencia obtenida previamente quedó invalidada;
7.  que se revisó si pruebas previamente ejecutadas deben repetirse;
8.  que las precondiciones de `/implement` vuelven a cumplirse;
9.  que el preflight de la TASK afectada vuelve a resultar válido.

Si una SPEC aprobada fue modificada:

-   deberá recuperar aprobación humana;
-   deberá evaluarse impacto sobre PLAN;
-   PLAN solamente deberá modificarse si resulta afectado;
-   TASKS solamente deberá modificarse si resulta afectado.

Si un PLAN aprobado fue modificado:

-   deberá recuperar aprobación humana;
-   deberá evaluarse impacto sobre TASKS;
-   TASKS solamente deberá modificarse si resulta afectado.

Si TASKS aprobado fue modificado de forma que cambie el trabajo
autorizado:

-   deberá recuperar aprobación humana antes de continuar la
    implementación afectada.

La implementación solamente podrá reanudarse cuando todos los approval
gates y precondiciones aplicables vuelvan a cumplirse.

------------------------------------------------------------------------

# 17.1 Reapertura después de validación

Si `/validate` detecta un defecto exclusivamente de implementación en
trabajo ya cerrado, deberá prepararse su reapertura antes de aplicar las
precondiciones de la sección 2 y antes de modificar código:

1.  Registrar el `FINDING-[XXX]` o `SEC-FINDING-[XXX]` de validación y
    vincularlo con las TASKS afectadas.
2.  Verificar que la corrección permanece dentro de SPEC, PLAN y trabajo
    autorizado. Si requiere cambiar requisitos, diseño o descomposición,
    seguir las secciones 16 y 17 y recuperar los approval gates aplicables.
3.  Conservar el resultado desfavorable de validación y la evidencia previa;
    identificar qué evidencia dejó de demostrar cumplimiento.
4.  Reabrir el documento TASKS de `COMPLETED` a `IN_PROGRESS` y las tareas
    afectadas de `DONE` a `TODO`, registrando motivo y finding. Evaluar las
    tareas dependientes y reabrirlas solamente si su finalización o
    evidencia resultó invalidada.
5.  Comprobar nuevamente las precondiciones y el preflight. El finding que
    motiva la corrección es trabajo pendiente a resolver, no un impedimento
    para iniciar esa misma corrección; cualquier bloqueo independiente
    continúa impidiendo la ejecución. Las dependencias obligatorias
    deberán estar satisfechas antes de iniciar cada tarea.
6.  Pasar cada tarea a `IN_PROGRESS`, corregir el defecto y repetir las
    pruebas, controles y verificaciones de regresión afectados.
7.  Registrar nueva evidencia, cumplir de nuevo el DoD de cada tarea y
    cerrar TASKS según la sección 23 antes de repetir `/validate`.

La reapertura y el registro de evidencia no requieren una nueva aprobación
cuando no cambian el trabajo autorizado. No convierten por sí mismos la
validación anterior en PASS: la feature permanece sin validar hasta que
una nueva ejecución de `/validate` satisfaga el gate final.

------------------------------------------------------------------------

# 18. Evidencia de implementación

Cada TASK deberá producir evidencia suficiente para demostrar qué se
hizo y qué se verificó.

Registrar:

## Files

Archivos creados:

-   \[archivo\]

Archivos modificados:

-   \[archivo\]

Archivos eliminados:

-   \[archivo\]

## Tests

Ejecutados:

-   TEST-\[XXX\]

Resultado:

PASS \| FAIL \| BLOCKED

## TDD

Para comportamiento automatizable: enlazar evidencia RED y GREEN por TEST,
incluida la causa del fallo y el orden respecto al cambio productivo; anotar
refactor y nueva ejecución cuando exista. Si no aplica: registrar motivo y
verificación alternativa. Un impedimento de entorno queda BLOCKED.

## Quality checks

-   Lint: PASS
-   Types: PASS
-   Build: PASS

cuando correspondan.

## Requirements

Requisitos cubiertos:

-   FR-\[XXX\]
-   SEC-\[XXX\]

## Acceptance Criteria

-   AC-\[XXX\] → PASS

## Discoveries

-   DISCOVERY-\[XXX\]

## Deviations

\[Cambios menores respecto al alcance previsto y justificación.\]

------------------------------------------------------------------------

# 19. Definition of Done de TASK

Una TASK podrá cambiar a:

DONE

solamente cuando:

-   [ ] El objetivo fue implementado.
-   [ ] La SPEC fue respetada.
-   [ ] El PLAN fue respetado.
-   [ ] El alcance de la TASK fue respetado.
-   [ ] Los criterios de aceptación relacionados tienen evidencia.
-   [ ] Las pruebas requeridas están en PASS.
-   [ ] La evidencia TDD RED/GREEN aplicable es válida, o existe motivo y
        verificación alternativa para un caso fuera de TDD.
-   [ ] Las pruebas de regresión relevantes están en PASS.
-   [ ] Los quality checks relevantes están en PASS.
-   [ ] Los requisitos de seguridad relacionados están cubiertos.
-   [ ] No existen bloqueos pendientes.
-   [ ] La evidencia fue registrada.

------------------------------------------------------------------------

# 20. Ejecución de múltiples tareas

Cuando se implementen múltiples TASKS deberán respetarse las
dependencias definidas en `tasks.md`.

Ejemplo:

TASK-001 │ ├───────┐ ▼ ▼ TASK-002 TASK-003 │ │ └───┬───┘ ▼ TASK-004

Una TASK no deberá comenzar si una dependencia obligatoria permanece:

TODO IN_PROGRESS BLOCKED

------------------------------------------------------------------------

# 21. Paralelización

Las tareas marcadas como paralelizables podrán ejecutarse
concurrentemente únicamente cuando:

-   no exista dependencia entre ellas;
-   no exista conflicto de archivos;
-   no compartan una decisión bloqueante;
-   la herramienta de ejecución soporte aislamiento seguro.

La ejecución paralela no deberá comprometer:

-   trazabilidad;
-   consistencia;
-   revisión;
-   evidencia.

La ejecución secuencial seguirá siendo válida.

------------------------------------------------------------------------

# 22. Control de versiones

Cuando el repositorio utilice Git, los cambios deberán mantenerse
pequeños y revisables.

Se recomienda que los commits puedan relacionarse con TASKS.

Ejemplo:

feat(tasks): implement task creation \[TASK-003\]

No es obligatorio realizar un commit por cada TASK si el flujo del
proyecto define otra estrategia.

No deberán realizarse commits automáticamente salvo que el entorno o el
usuario lo autorice explícitamente.

------------------------------------------------------------------------

# 23. Finalización de implementación

Cuando todas las TASKS requeridas estén:

DONE

deberá comprobarse:

-   ninguna TASK requerida permanece TODO;
-   ninguna TASK requerida permanece IN_PROGRESS;
-   ninguna TASK requerida permanece BLOCKED;
-   todos los requisitos MUST que requieren implementación tienen
    cobertura;
-   todos los criterios de aceptación obligatorios tienen evidencia;
-   todas las TASKS requeridas cumplen su Definition of Done;
-   la evidencia requerida fue registrada.

Cuando estas condiciones se cumplan:

TASKS STATUS:

IN_PROGRESS → COMPLETED

Después:

IMPLEMENTATION STATUS:

COMPLETED

NEXT:

/validate

IMPLEMENTATION COMPLETED

NO significa:

SPEC COMPLIANT

La conformidad final solamente podrá determinarse mediante:

/validate

------------------------------------------------------------------------

# 24. Self-check

Antes de finalizar `/implement` verificar:

-   [ ] Se implementaron únicamente TASKS aprobadas.
-   [ ] Se respetaron dependencias.
-   [ ] No se introdujo scope creep.
-   [ ] Los cambios fuera de alcance fueron registrados.
-   [ ] Las pruebas requeridas fueron ejecutadas.
-   [ ] Las regresiones relevantes fueron verificadas.
-   [ ] Los quality checks relevantes fueron ejecutados.
-   [ ] Los requisitos SEC fueron considerados.
-   [ ] No se modificaron tests para ocultar errores.
-   [ ] Los descubrimientos fueron registrados.
-   [ ] Los bloqueos fueron registrados.
-   [ ] Cada TASK DONE tiene evidencia.
-   [ ] No existen cambios arquitectónicos silenciosos.
-   [ ] No existen cambios funcionales silenciosos.

------------------------------------------------------------------------

# 25. Salida

Formato recomendado:

SDD IMPLEMENTATION ────────────────────────────────

SPEC: SPEC-001

PLAN: PLAN-001

TASKS: TASKS-001

Implemented:

TASK-001 DONE TASK-002 DONE TASK-003 DONE TASK-004 BLOCKED

Progress: 3 / 4

Files:

Created: 3 Modified: 6 Removed: 0

Tests:

PASS: 12 FAIL: 0 BLOCKED: 2

Quality:

Lint: PASS Types: PASS Build: PASS

Discoveries: 1

Blocking issues: 1

Status: BLOCKED

Next: Resolve BLOCK-001 ────────────────────────────────

SDD IMPLEMENTATION ────────────────────────────────

Tasks: 8 / 8 DONE

Tests: 24 PASS 0 FAIL

Quality: PASS

Blocking issues: 0

Implementation: COMPLETED

Next: /validate ────────────────────────────────

------------------------------------------------------------------------

# 26. Acciones prohibidas

Durante `/implement` el agente NO deberá:

-   implementar requisitos inexistentes;
-   modificar la SPEC silenciosamente;
-   modificar el PLAN silenciosamente;
-   modificar TASKS silenciosamente;
-   cambiar arquitectura sin revisión;
-   agregar dependencias importantes no aprobadas;
-   realizar refactors no relacionados;
-   eliminar tests para conseguir PASS;
-   debilitar tests válidos;
-   ignorar pruebas fallidas;
-   ignorar regresiones;
-   ignorar controles de seguridad;
-   inventar decisiones ante ambigüedad;
-   marcar una TASK como DONE sin evidencia;
-   marcar la feature como validada.

El objetivo es ejecutar fielmente el trabajo aprobado y producir
evidencia verificable.
