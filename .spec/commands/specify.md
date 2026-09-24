# Comando: Specify

## Propósito

Transformar una petición, idea o necesidad expresada por el usuario
en una especificación estructurada siguiendo los principios de
Spec-Driven Development definidos por este repositorio.

Este comando genera el artefacto:

specs/<feature-id>/spec.md

El comando NO implementa código.

---

# 1. Entradas

El comando recibe una descripción proporcionada por el usuario.

Ejemplo:

/specify

Los usuarios necesitan crear, editar y completar tareas
dentro de un proyecto.

La entrada puede ser:

- una idea;
- una funcionalidad;
- un problema;
- una mejora;
- un cambio de comportamiento;
- una necesidad de negocio;
- una corrección que implique comportamiento nuevo.

---

# 2. Contexto obligatorio

Antes de generar la especificación deberá consultarse:

1. `.spec/constitution.md`
2. `.spec/standards/architecture.md`
3. `.spec/standards/coding.md`
4. `.spec/standards/testing.md`
5. `.spec/standards/security.md`
6. `.spec/templates/specification.template.md`

Cuando exista documentación relevante del proyecto también deberá
considerarse.

La Constitución tiene precedencia sobre cualquier instrucción
de nivel inferior.

---

# 3. Regla principal

El comando deberá describir:

QUÉ necesita el sistema

y:

POR QUÉ lo necesita.

No deberá diseñar prematuramente:

- arquitectura;
- base de datos física;
- endpoints concretos;
- estructura de carpetas;
- clases;
- frameworks;
- librerías;
- implementación;
- algoritmos;

salvo que alguno de estos elementos sea una restricción explícita
proporcionada por el usuario o por el proyecto.

---

# 4. Identificación de la SPEC

Cada especificación deberá recibir:

SPEC-[XXX]

y una carpeta:

specs/<feature-id>/

Ejemplo:

SPEC-001

specs/001-task-management/
    spec.md

El identificador deberá ser único dentro del repositorio.

Los identificadores existentes no deberán reutilizarse.

---

# 5. Nombre de la feature

El nombre de carpeta deberá:

- utilizar minúsculas;
- utilizar guiones;
- ser descriptivo;
- evitar nombres excesivamente largos.

Ejemplo:

Correcto:

001-user-authentication
002-task-management
003-password-recovery

Evitar:

001-feature
002-new-stuff
003-changes

---

# 6. Análisis de la petición

Antes de escribir la SPEC deberá identificarse:

## Problema

¿Qué problema intenta resolver el usuario?

## Objetivo

¿Qué resultado espera obtener?

## Actores

¿Quién interactúa con esta funcionalidad?

## Comportamientos

¿Qué debe poder hacer el sistema?

## Restricciones

¿Qué límites ya fueron proporcionados?

## Seguridad

¿Existen implicaciones de:

- autenticación;
- autorización;
- datos sensibles;
- permisos;
- operaciones destructivas?

## Casos límite

¿Qué escenarios importantes podrían cambiar el comportamiento?

Este análisis deberá utilizarse para construir la SPEC.

No deberá utilizarse para inventar requisitos.

---

# 7. Detección de ambigüedad

Durante la generación deberán detectarse:

- requisitos incompletos;
- comportamientos ambiguos;
- reglas contradictorias;
- permisos desconocidos;
- resultados no definidos;
- límites desconocidos;
- decisiones de negocio faltantes.

Cuando una ambigüedad pueda cambiar significativamente
el comportamiento esperado deberá utilizarse:

[NEEDS CLARIFICATION]

El agente no deberá seleccionar silenciosamente una opción.

---

# 8. Cuándo NO utilizar NEEDS CLARIFICATION

No deberá generarse una aclaración cuando la respuesta pueda
determinarse claramente mediante:

1. la petición explícita del usuario;
2. la Constitución;
3. los estándares;
4. una especificación relacionada aprobada;
5. una regla de negocio ya documentada;
6. una restricción existente del proyecto.

Tampoco deberán solicitarse aclaraciones por detalles que puedan
resolverse posteriormente durante la planificación técnica sin
afectar el comportamiento esperado.

El objetivo es detectar ambigüedad relevante, no convertir cada
detalle en una pregunta.


---

# 9. Clasificación de aclaraciones

Toda aclaración deberá clasificarse como:

Bloqueante: YES

o:

Bloqueante: NO

## Bloqueante

Utilizar cuando la respuesta pueda modificar:

- comportamiento;
- alcance;
- permisos;
- reglas de negocio;
- seguridad;
- datos importantes;
- criterios de aceptación.

Una aclaración bloqueante impide que la SPEC avance a `APPROVED`.

## No bloqueante

Utilizar cuando la respuesta pendiente no impida definir
correctamente el comportamiento principal.

Las aclaraciones no bloqueantes deberán permanecer documentadas.

---

# 10. Generación de requisitos

Los requisitos deberán clasificarse cuando corresponda como:

FR-[XXX]
Functional Requirement

NFR-[XXX]
Non-Functional Requirement

SEC-[XXX]
Security Requirement

BR-[XXX]
Business Rule

Los requisitos deberán ser:

- explícitos;
- verificables;
- independientes cuando sea razonable;
- comprensibles;
- trazables.

Evitar requisitos vagos.

Incorrecto:

FR-001
El sistema deberá ser fácil de usar.

Preferible:

NFR-001
El flujo principal de creación de tareas deberá poder completarse
sin abandonar la vista del proyecto.

---

# 11. Generación de criterios de aceptación

Los requisitos MUST deberán contar con criterios de aceptación
suficientes para demostrar su comportamiento.

Los criterios utilizarán:

AC-[XXX]

Formato recomendado:

Given
When
Then

Ejemplo:

AC-001

Relacionado con: FR-001

Given
un usuario autenticado con acceso al proyecto

When
crea una tarea con datos válidos

Then
la tarea queda disponible dentro del proyecto.

---

# 12. Priorización

Los requisitos deberán clasificarse mediante:

MUST
SHOULD
COULD

MUST:

Necesario para considerar cumplida la funcionalidad.

SHOULD:

Importante, pero puede omitirse únicamente con justificación
documentada.

COULD:

Opcional y no bloquea el cumplimiento principal de la SPEC.

El agente no deberá utilizar prioridad para eliminar silenciosamente
parte del alcance solicitado por el usuario.

---

# 13. Suposiciones

Cuando sea necesario utilizar una suposición no bloqueante deberá
registrarse mediante:

ASM-[XXX]

Las suposiciones deberán ser explícitas.

Una suposición que pueda cambiar significativamente el comportamiento
no deberá utilizarse para evitar una aclaración.

En ese caso deberá utilizarse:

[NEEDS CLARIFICATION]

---

# 14. Creación del artefacto

Una vez analizada la petición deberá:

1. determinar el siguiente ID disponible;
2. crear la carpeta de la feature;
3. utilizar:

.spec/templates/specification.template.md

como estructura base;
4. completar las secciones aplicables;
5. registrar aclaraciones;
6. generar la matriz inicial de trazabilidad;
7. guardar:

specs/<feature-id>/spec.md

La plantilla original no deberá modificarse durante este proceso.

---

# 15. Self-check

Antes de finalizar `/specify`, verificar:

- [ ] Existe un problema claramente definido.
- [ ] Existe un objetivo.
- [ ] El alcance está definido.
- [ ] El fuera de alcance está definido.
- [ ] Los actores relevantes están identificados.
- [ ] Los FR son verificables.
- [ ] Los requisitos MUST tienen criterios de aceptación.
- [ ] Los SEC relevantes fueron considerados.
- [ ] Los principales edge cases fueron considerados.
- [ ] Las suposiciones están visibles.
- [ ] Las ambigüedades relevantes están marcadas.
- [ ] No se inventaron decisiones técnicas.
- [ ] No se agregó funcionalidad no solicitada.
- [ ] La matriz de trazabilidad es consistente.

---

# 16. Estado resultante

Si existen aclaraciones bloqueantes:

SPEC STATUS:

DRAFT

RESULT:

NEEDS CLARIFICATION

No deberá avanzarse a PLAN.

---

Si no existen aclaraciones bloqueantes pero todavía requiere
revisión humana:

SPEC STATUS:

IN_REVIEW

RESULT:

READY FOR REVIEW

---

La SPEC solamente podrá pasar a:

APPROVED

cuando exista aprobación humana explícita.

---

# 17. Salida del comando

Al finalizar deberá reportarse:

- SPEC creada;
- ruta;
- requisitos detectados;
- criterios de aceptación;
- aclaraciones;
- estado.

Formato recomendado:

SDD SPECIFICATION
────────────────────────────────

SPEC:
SPEC-001

Feature:
Task Management

Path:
specs/001-task-management/spec.md

Requirements:
FR: 5
NFR: 1
SEC: 2

Acceptance Criteria:
8

Clarifications:
2 blocking
1 non-blocking

Status:
NEEDS CLARIFICATION

Next:
Run /clarify
────────────────────────────────

---

# 18. Acciones prohibidas

Durante `/specify` el agente NO deberá:

- escribir código de aplicación;
- instalar dependencias;
- crear migraciones;
- modificar infraestructura;
- crear endpoints;
- seleccionar tecnologías sin necesidad;
- generar `plan.md`;
- generar `tasks.md`;
- modificar archivos fuera de la SPEC;
- resolver silenciosamente decisiones de negocio;
- marcar la SPEC como APPROVED por cuenta propia.

El objetivo exclusivo de este comando es producir
una especificación correcta y revisable.