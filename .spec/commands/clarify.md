# Comando: Clarify

## Propósito

Resolver ambigüedades, decisiones pendientes y elementos marcados como
`[NEEDS CLARIFICATION]` dentro de una especificación.

Este comando actúa como un gate entre:

SPECIFICATION → PLAN

Su responsabilidad es obtener decisiones explícitas cuando la
información disponible no sea suficiente.

El comando NO implementa código.

El comando NO genera el plan técnico.

------------------------------------------------------------------------

# 1. Entradas

El comando recibe una SPEC existente.

Ejemplo:

/clarify SPEC-001

o conceptualmente:

/clarify specs/001-task-management/spec.md

La SPEC deberá existir antes de ejecutar este proceso.

------------------------------------------------------------------------

# 2. Contexto obligatorio

Antes de realizar aclaraciones deberá consultarse:

1.  `.spec/constitution.md`
2.  `.spec/templates/specification.template.md`
3.  la SPEC objetivo;
4.  documentación relacionada cuando sea relevante;
5.  especificaciones aprobadas relacionadas cuando existan.

Cuando una aclaración involucre estándares del proyecto también podrán
consultarse:

-   `.spec/standards/architecture.md`
-   `.spec/standards/coding.md`
-   `.spec/standards/testing.md`
-   `.spec/standards/security.md`

La Constitución mantiene precedencia sobre cualquier instrucción de
nivel inferior.

------------------------------------------------------------------------

# 3. Localización de aclaraciones existentes

El comando deberá buscar elementos marcados como:

\[NEEDS CLARIFICATION\]

Dentro de la SPEC.

Por cada elemento deberá identificar:

-   ID;
-   pregunta;
-   contexto;
-   impacto;
-   requisitos afectados;
-   criterios de aceptación afectados;
-   si es bloqueante;
-   estado actual.

Ejemplo:

Q-001 Estado: \[NEEDS CLARIFICATION\] Bloqueante: YES

Q-002 Estado: \[NEEDS CLARIFICATION\] Bloqueante: NO

------------------------------------------------------------------------

# 4. Segunda revisión de ambigüedad

Además de localizar aclaraciones existentes, el comando deberá revisar
la SPEC buscando ambigüedades que hayan pasado inadvertidas.

Deberá revisar especialmente:

-   permisos;
-   actores;
-   ownership;
-   estados;
-   transiciones;
-   operaciones destructivas;
-   comportamiento ante errores;
-   límites;
-   reglas de negocio;
-   datos requeridos;
-   casos límite;
-   comportamientos contradictorios;
-   criterios de aceptación insuficientes.

Si se detecta una nueva ambigüedad relevante deberá crearse una nueva
entrada:

Q-\[XXX\]

con estado:

\[NEEDS CLARIFICATION\]

No deberá inventarse una respuesta.

------------------------------------------------------------------------

# 5. Resolución mediante contexto existente

Antes de preguntar al humano, el comando deberá intentar determinar si
la aclaración ya puede resolverse utilizando información explícita.

Orden recomendado:

1.  SPEC actual.
2.  Constitución.
3.  Estándares.
4.  Requisitos relacionados.
5.  Reglas de negocio existentes.
6.  Especificaciones aprobadas relacionadas.
7.  Restricciones documentadas.
8.  Decisiones humanas previamente registradas.

### Condiciones para resolver mediante contexto existente

Una aclaración solamente podrá resolverse sin una nueva intervención
humana cuando la respuesta encontrada sea:

1.  explícita;
2.  aplicable al contexto actual de la SPEC;
3.  no contradictoria con información de mayor precedencia;
4.  todavía autoritativa para la decisión actual.

Una decisión humana previamente registrada no deberá reutilizarse
automáticamente únicamente porque exista.

Antes de utilizarla deberá verificarse que:

-   corresponde al mismo comportamiento o regla relevante;
-   su alcance aplica a la SPEC actual;
-   no fue reemplazada por una decisión posterior;
-   no contradice la Constitución, Standards o una decisión humana
    posterior aplicable.

Si existe duda razonable sobre su aplicabilidad o vigencia:

\[NEEDS CLARIFICATION\]

La decisión deberá volver al humano.

No deberá inferirse que una decisión histórica constituye autorización
para un comportamiento nuevo.

Si existe una respuesta explícita, aplicable, vigente y no
contradictoria:

-   utilizarla;
-   registrar su origen;
-   actualizar la SPEC;
-   marcar la aclaración como `[CLARIFIED]`.

No deberá utilizarse una inferencia especulativa como si fuera
información explícita.

------------------------------------------------------------------------

# 6. Priorización de aclaraciones

Las aclaraciones deberán procesarse en este orden:

1.  Bloqueantes de alcance.
2.  Bloqueantes de reglas de negocio.
3.  Bloqueantes de seguridad y permisos.
4.  Bloqueantes de comportamiento.
5.  Bloqueantes de datos.
6.  No bloqueantes.
7.  Preferencias menores.

Las preguntas relacionadas deberán agruparse cuando sea posible.

No deberán presentarse múltiples preguntas redundantes.

------------------------------------------------------------------------

# 7. Presentación de aclaraciones

Cada pregunta deberá ser:

-   concreta;
-   neutral;
-   breve;
-   relacionada con una decisión real;
-   acompañada del contexto necesario.

Formato recomendado:

Q-001 --- \[Título\]

Pregunta: \[Pregunta concreta\]

Contexto: \[Por qué necesitamos saberlo.\]

Impacto: \[Qué comportamiento depende de la respuesta.\]

Bloqueante: YES \| NO

Opciones conocidas:

A. \[Opción\] B. \[Opción\] C. \[Opción\] D. Otra: \[respuesta libre\]

------------------------------------------------------------------------

# 8. Opciones de respuesta

Cuando existan alternativas claramente identificables deberán
presentarse como opciones.

Las opciones deberán:

-   ser neutrales;
-   representar alternativas reales;
-   evitar inducir una respuesta;
-   incluir una opción abierta cuando sea necesario.

No deberá seleccionarse automáticamente una opción por considerarla
"mejor".

El humano mantiene autoridad sobre decisiones funcionales y de negocio.

------------------------------------------------------------------------

# 9. Aclaraciones derivadas

Una respuesta podrá revelar nuevas ambigüedades.

Ejemplo:

Q-001:

¿Los administradores pueden eliminar proyectos?

Respuesta:

Sí.

Esto puede generar:

Q-002:

¿Qué ocurre con las tareas pertenecientes al proyecto eliminado?

En ese caso deberá registrarse una nueva aclaración.

El proceso continuará hasta que no existan ambigüedades bloqueantes
relevantes.

------------------------------------------------------------------------

# 10. Registro de resolución

Cuando el humano responda una aclaración deberá registrarse:

**Estado:** \[CLARIFIED\]

**Respuesta:**

\[Respuesta proporcionada.\]

**Resuelto por:**

Human

**Fecha de resolución:**

\[YYYY-MM-DD\]

**Artefactos afectados:**

-   FR-\[XXX\]
-   AC-\[XXX\]
-   BR-\[XXX\]
-   SEC-\[XXX\]

------------------------------------------------------------------------

# 11. Propagación de la decisión

Resolver una pregunta NO es suficiente.

La respuesta deberá incorporarse en las secciones correspondientes de la
SPEC.

Ejemplo:

Q-001:

¿Los usuarios pueden eliminar tareas de otros usuarios?

Respuesta:

No.

No deberá quedar únicamente:

Q-001 → \[CLARIFIED\]

También deberá actualizarse el requisito correspondiente.

Ejemplo:

FR-004

El sistema solamente permitirá que un usuario elimine tareas que le
pertenecen.

Y deberá existir un criterio verificable.

Ejemplo:

AC-007

Given un usuario autenticado

And una tarea perteneciente a otro usuario

When intenta eliminarla

Then el sistema rechaza la operación.

------------------------------------------------------------------------

# 12. Análisis de impacto

Después de cada aclaración resuelta deberá verificarse si la respuesta
afecta:

-   otros requisitos;
-   criterios de aceptación;
-   reglas de negocio;
-   seguridad;
-   edge cases;
-   alcance;
-   fuera de alcance;
-   suposiciones.

Si existe impacto deberá actualizarse la SPEC de forma consistente.

No deberán mantenerse requisitos contradictorios.

------------------------------------------------------------------------

# 13. Conversión de suposiciones

Si durante `/clarify` se determina que una suposición afecta
significativamente el comportamiento, deberá convertirse en una
aclaración.

Ejemplo:

ASM-002

Se asume que todos los usuarios pueden ver todos los proyectos.

Si esta suposición afecta autorización:

ASM-002 ↓ Q-005 \[NEEDS CLARIFICATION\]

Una suposición no deberá utilizarse para ocultar una decisión de negocio
pendiente.

------------------------------------------------------------------------

# 14. Contradicciones

Si una respuesta humana contradice un requisito existente, el comando
deberá señalar el conflicto.

Ejemplo:

FR-003: Los proyectos no pueden eliminarse.

Respuesta Q-004: Los administradores pueden eliminar proyectos.

Resultado:

CONFLICT DETECTED

El conflicto deberá resolverse antes de continuar.

No deberá modificarse silenciosamente uno de los requisitos para ocultar
la contradicción.

------------------------------------------------------------------------

# 15. Self-check

Antes de finalizar el proceso deberá verificarse:

-   [ ] Todas las aclaraciones existentes fueron revisadas.
-   [ ] Se realizó una segunda revisión de ambigüedad.
-   [ ] Las respuestas fueron registradas.
-   [ ] Las decisiones fueron propagadas a los requisitos afectados.
-   [ ] Los criterios de aceptación fueron actualizados.
-   [ ] Las reglas de negocio fueron actualizadas cuando corresponde.
-   [ ] Las implicaciones de seguridad fueron revisadas.
-   [ ] No existen contradicciones conocidas.
-   [ ] No se inventaron respuestas.
-   [ ] No se introdujeron decisiones técnicas innecesarias.
-   [ ] La matriz de trazabilidad continúa siendo consistente.

------------------------------------------------------------------------

# 16. Gate de salida

Si existen aclaraciones bloqueantes:

RESULT:

NEEDS CLARIFICATION

SPEC STATUS:

DRAFT

NEXT:

Continuar `/clarify`

------------------------------------------------------------------------

Si existe una contradicción sin resolver:

RESULT:

CONFLICT DETECTED

SPEC STATUS:

DRAFT

NEXT:

Resolver conflicto

------------------------------------------------------------------------

Si no existen aclaraciones bloqueantes:

RESULT:

READY FOR REVIEW

SPEC STATUS:

IN_REVIEW

NEXT:

Human review

------------------------------------------------------------------------

# 17. Aprobación

Cuando el humano apruebe explícitamente la SPEC:

SPEC STATUS:

APPROVED

A partir de ese momento podrá iniciarse la fase:

PLAN

mediante:

/plan

Si posteriormente cambia un requisito aprobado deberá actualizarse la
SPEC y reevaluarse el impacto sobre PLAN, TASKS, implementación y
validación.

Las respuestas humanas que afectan requisitos o gates nuevos deberán quedar
registradas con su resultado y alcance en `decisions.json`, además de reflejarse
en la SPEC. La referencia al chat no sustituye el contenido de la decisión;
seguir `docs/state-reconstruction.md`. Si cambió contenido autorizado, obtener
de nuevo las aprobaciones afectadas y comprobar su huella antes de continuar.

------------------------------------------------------------------------

# 18. Salida

Formato recomendado:

SDD CLARIFICATION ────────────────────────────────

SPEC: SPEC-001

Clarifications reviewed: 4

Resolved: 3

Remaining: 1

Blocking: 0

Non-blocking: 1

Conflicts: 0

Requirements updated: FR-002 FR-004

Acceptance criteria updated: AC-003 AC-007

Status: READY FOR REVIEW

Next: Human approval ────────────────────────────────

------------------------------------------------------------------------

# 19. Acciones prohibidas

Durante `/clarify` el agente NO deberá:

-   implementar código;
-   generar `plan.md`;
-   generar `tasks.md`;
-   instalar dependencias;
-   crear migraciones;
-   cambiar arquitectura;
-   seleccionar silenciosamente respuestas;
-   convertir preferencias técnicas en requisitos;
-   ignorar contradicciones;
-   marcar una SPEC como `APPROVED` sin aprobación humana explícita.

El objetivo exclusivo es eliminar ambigüedad y mantener la
especificación consistente.
