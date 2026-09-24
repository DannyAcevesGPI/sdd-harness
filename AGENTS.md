## SDD Harness — Agent Operating Instructions

Este repositorio utiliza un proceso de desarrollo:

Spec-Driven Development (SDD)

Todo agente que trabaje dentro del repositorio deberá operar
siguiendo el flujo, reglas, artefactos y gates definidos por
este Harness.

La regla fundamental es:

> No implementation without an approved specification.

Y para features gestionadas mediante el flujo completo:

> No implementation without an approved SPEC, PLAN and TASKS.

---

# 1. Source of Truth

Las instrucciones del repositorio se organizan mediante
la siguiente jerarquía:

1. Decisiones humanas explícitas y aprobadas.
2. `.spec/constitution.md`
3. `.spec/standards/`
4. SPEC de la feature.
5. PLAN de la feature.
6. TASKS de la feature.
7. Detalles de implementación.

Un artefacto de nivel inferior no deberá contradecir
silenciosamente uno superior.

Cuando exista conflicto deberá prevalecer la fuente
de mayor autoridad.

El conflicto deberá documentarse y resolverse antes
de continuar cuando afecte el trabajo actual.

---

# 2. Mandatory Bootstrap

Antes de realizar trabajo significativo dentro del repositorio,
el agente deberá leer:

`.spec/constitution.md`

Después deberá determinar:

1. qué solicita el usuario;
2. qué feature está involucrada;
3. en qué fase SDD se encuentra;
4. qué artefactos existen;
5. qué command corresponde;
6. qué standards aplican.

No deberá comenzar modificando código únicamente porque
la solicitud mencione una funcionalidad.

---

# 3. Repository Structure

La estructura principal del Harness es:

.spec/
├── constitution.md
├── standards/
├── templates/
└── commands/

specs/
└── <feature-id>/
    ├── spec.md
    ├── plan.md
    ├── tasks.md
    └── validation.md

docs/
├── architecture/
└── decisions/

src/

tests/

AGENTS.md
README.md

---

# 4. Harness Components

## Constitution

Ubicación:

`.spec/constitution.md`

Define las reglas fundamentales del proceso.

Debe considerarse obligatoria.

---

## Standards

Ubicación:

`.spec/standards/`

Incluyen:

- architecture.md
- coding.md
- testing.md
- security.md

Los standards deberán consultarse según la actividad realizada.

---

## Templates

Ubicación:

`.spec/templates/`

Incluyen:

- specification.template.md
- plan.template.md
- tasks.template.md
- validation.template.md

Las plantillas definen la estructura base de los artefactos SDD.

Las plantillas no deberán modificarse al crear una feature.

---

## Commands

Ubicación:

`.spec/commands/`

Incluyen:

- specify.md
- clarify.md
- plan.md
- tasks.md
- implement.md
- validate.md

Cada command define las reglas operativas de una fase del ciclo SDD.

---

# 5. SDD Lifecycle

El flujo principal es:

IDEA
  ↓
/specify
  ↓
SPEC
  ↓
/clarify
  ↓
SPEC APPROVED
  ↓
/plan
  ↓
PLAN APPROVED
  ↓
/tasks
  ↓
TASKS APPROVED
  ↓
/implement
  ↓
TASKS IN_PROGRESS
  ↓
IMPLEMENTATION
  ↓
TASKS COMPLETED
  ↓
/validate
  ↓
SPEC COMPLIANCE: PASS
  ↓
FEATURE STATUS: VALIDATED

No deberán omitirse gates obligatorios.

`TASK DONE`, `TASKS COMPLETED` y `FEATURE STATUS: VALIDATED`
representan estados distintos y no deberán tratarse como equivalentes.

---

# 6. Intent Routing

El agente deberá determinar el command correspondiente
según la intención del trabajo.

## Nueva funcionalidad o cambio de comportamiento

Utilizar:

`/specify`

Consultar:

`.spec/commands/specify.md`

---

## Ambigüedad o pregunta funcional

Utilizar:

`/clarify`

Consultar:

`.spec/commands/clarify.md`

---

## Diseño técnico

Utilizar:

`/plan`

Consultar:

`.spec/commands/plan.md`

---

## Descomposición del trabajo

Utilizar:

`/tasks`

Consultar:

`.spec/commands/tasks.md`

---

## Modificación de código

Utilizar:

`/implement`

Consultar:

`.spec/commands/implement.md`

---

## Verificación final

Utilizar:

`/validate`

Consultar:

`.spec/commands/validate.md`

---

# 7. Phase Detection

Antes de actuar sobre una feature existente deberá inspeccionarse
su directorio:

`specs/<feature-id>/`

Utilizar los artefactos y estados existentes para determinar
la fase actual.

Ejemplo:

Solo existe:

spec.md

y está:

DRAFT

La feature continúa en:

SPECIFICATION / CLARIFICATION

---

Si existe:

spec.md → APPROVED

pero no existe:

plan.md

La siguiente fase es:

PLAN

---

Si existe:

spec.md → APPROVED
plan.md → APPROVED

pero no existe:

tasks.md

La siguiente fase es:

TASKS

---

Si existe:

spec.md → APPROVED
plan.md → APPROVED
tasks.md → APPROVED

La feature puede avanzar a:

IMPLEMENTATION

---

Si:

tasks.md → COMPLETED

y:

todas las TASKS obligatorias → DONE

La feature puede avanzar a:

VALIDATION

El estado `DONE` de las TASKS individuales no sustituye
el estado `COMPLETED` del documento TASKS.

Si todas las TASKS obligatorias están `DONE` pero el documento
TASKS permanece `IN_PROGRESS`, deberá completarse y verificarse
el cierre del documento TASKS antes de avanzar a `/validate`.

---

Si:

validation.md

indica:

SPEC COMPLIANCE: PASS

y:

FEATURE STATUS: VALIDATED

la feature ha completado el flujo SDD.

Si una validación detecta un defecto exclusivamente de implementación
con TASKS `COMPLETED` y tareas `DONE`, deberá aplicarse la reapertura
definida en `.spec/commands/implement.md`, sección 17.1, antes de modificar
código. Después de corregir y cerrar TASKS deberá repetirse `/validate`.

---

# 8. Approval Gates

Los siguientes cambios requieren aprobación humana explícita:

SPEC:
IN_REVIEW → APPROVED

PLAN:
IN_REVIEW → APPROVED

TASKS:
IN_REVIEW → APPROVED

El agente no deberá autoaprobar estos artefactos.

La ausencia de preguntas o problemas no equivale
a aprobación humana.

---

# 9. Mutation Boundary

Antes de `/implement` el agente deberá tratar el código
de aplicación como:

READ-ONLY

Las fases:

/specify
/clarify
/plan
/tasks

pueden crear o modificar sus artefactos SDD correspondientes,
pero no deberán implementar la feature en:

src/
tests/
migrations/
application configuration

salvo que el propio artefacto del Harness requiera una
actualización explícitamente autorizada.

La modificación de implementación comienza en:

/implement

---

# 10. Traceability

Toda implementación deberá mantener la cadena:

Requirement
→ Acceptance Criterion
→ Plan
→ Task
→ Code
→ Test
→ Validation

El agente deberá poder responder:

¿Por qué existe este cambio?

mediante referencias a los artefactos superiores.

Código significativo sin una TASK justificante deberá
considerarse implementación no trazada.

Una TASK sin SPEC o PLAN justificante deberá considerarse
una tarea huérfana.

---

# 11. Requirement IDs

Utilizar los identificadores definidos por el Harness:

Functional Requirement:

FR-[XXX]

Non-Functional Requirement:

NFR-[XXX]

Security Requirement:

SEC-[XXX]

Business Rule:

BR-[XXX]

Acceptance Criterion:

AC-[XXX]

Assumption:

ASM-[XXX]

---

# 12. Planning IDs

Technical Decision:

DEC-[XXX]

Technical Risk:

RISK-[XXX]

Technical Clarification:

Q-TECH-[XXX]

Architecture Decision Record:

ADR-[XXX]

---

# 13. Execution IDs

Task:

TASK-[XXX]

Test:

TEST-[XXX]

Blocker:

BLOCK-[XXX]

Discovery:

DISCOVERY-[XXX]

Task Clarification:

Q-TASK-[XXX]

---

# 14. Validation IDs

Validation:

VALIDATION-[XXX]

Validation Finding:

FINDING-[XXX]

Traceability Gap:

GAP-[XXX]

Security Finding:

SEC-FINDING-[XXX]

Deviation:

DEV-[XXX]

---

# 15. Clarification Protocol

Cuando exista información insuficiente, ambigua o contradictoria
deberá utilizarse:

[NEEDS CLARIFICATION]

El agente no deberá convertir una suposición en una decisión
sin indicarlo.

Antes de preguntar deberá revisar si la respuesta existe
explícitamente en una fuente autorizada.

No deberán realizarse preguntas cuya respuesta ya esté definida
claramente por:

- la solicitud del usuario;
- Constitution;
- Standards;
- SPEC;
- PLAN;
- decisiones humanas previas relevantes;
- ADR aplicables.

Una respuesta existente solamente podrá utilizarse para resolver
una aclaración cuando sea:

- explícita;
- aplicable al contexto actual;
- no contradictoria con una fuente de mayor precedencia;
- todavía autoritativa para la decisión actual.

Las decisiones humanas previas no deberán reutilizarse
automáticamente únicamente porque existan.

Antes de reutilizar una decisión humana previa deberá verificarse que:

- corresponde al mismo comportamiento o regla relevante;
- su alcance aplica al contexto actual;
- no fue reemplazada por una decisión posterior;
- no contradice Constitution, Standards o una decisión humana
  posterior aplicable.

Si existe duda razonable sobre su aplicabilidad, vigencia o alcance
deberá mantenerse:

[NEEDS CLARIFICATION]

y solicitarse decisión humana cuando corresponda.

No deberá inferirse que una decisión histórica constituye
autorización para un comportamiento nuevo.

---

# 16. Clarification Ownership

La pregunta deberá resolverse en el nivel que posee la decisión.

## Functional

Comportamiento
Reglas de negocio
Permisos
Alcance
Actores

→ SPEC

---

## Technical

Arquitectura
Persistencia
Contratos
Integraciones
Estrategia técnica

→ PLAN

---

## Work Breakdown

División de tareas
Dependencias
Conflictos de ejecución

→ TASKS

---

## Implementation

Problema localizado de código que no modifica decisiones superiores

→ IMPLEMENTATION

No deberá solucionarse un problema modificando silenciosamente
un artefacto de menor nivel.

---

# 17. Escalation

Durante implementación o validación:

Si el problema pertenece a requisitos:

STOP
→ SPEC REVISION REQUIRED

Si pertenece al diseño técnico:

STOP
→ PLAN REVISION REQUIRED

Si pertenece a la descomposición del trabajo:

STOP
→ TASK REVISION REQUIRED

Si pertenece únicamente a la implementación:

resolver dentro de `/implement`.

Después de una revisión superior deberán reevaluarse
los artefactos dependientes.

---

# 18. Change Propagation

Los artefactos SDD forman una cadena de dependencias:

SPEC
  ↓
PLAN
  ↓
TASKS
  ↓
IMPLEMENTATION
  ↓
VALIDATION

Cuando cambia un artefacto superior deberá evaluarse
el impacto sobre todos los artefactos inferiores.

Ejemplo:

SPEC changes
    ↓
review PLAN
    ↓
review TASKS
    ↓
review IMPLEMENTATION
    ↓
repeat VALIDATION

No deberá asumirse que los artefactos inferiores continúan
siendo válidos automáticamente.

## Approval Recovery

Cuando un artefacto previamente `APPROVED` sea modificado,
su aprobación previa no deberá considerarse suficiente para
autorizar automáticamente el nuevo contenido.

Las actualizaciones de estados de ejecución y evidencia que no cambian
el trabajo autorizado no requieren una nueva aprobación; esto incluye
la reapertura para corregir defectos de implementación según `/implement`.

Antes de continuar con trabajo dependiente deberá:

1. identificarse el artefacto propietario del cambio;
2. actualizarse dicho artefacto;
3. evaluarse el impacto sobre los artefactos downstream;
4. actualizarse solamente los artefactos realmente afectados;
5. recuperarse el approval gate de todo artefacto previamente
   `APPROVED` cuyo contenido haya sido modificado;
6. reevaluarse evidencia y pruebas obtenidas previamente cuando
   el cambio pueda haberlas invalidado;
7. volver a comprobarse las precondiciones de la fase siguiente.

Si una SPEC aprobada es modificada:

- deberá recuperar aprobación humana;
- deberá evaluarse el impacto sobre PLAN;
- PLAN solamente deberá modificarse si resulta afectado;
- TASKS solamente deberá modificarse si resulta afectado.

Si un PLAN aprobado es modificado:

- deberá recuperar aprobación humana;
- deberá evaluarse el impacto sobre TASKS;
- TASKS solamente deberá modificarse si resulta afectado.

Si TASKS aprobado es modificado de forma que cambie el trabajo
autorizado:

- deberá recuperar aprobación humana antes de continuar
  la implementación afectada.

La modificación de un artefacto downstream no será obligatoria
cuando la evaluación determine que el cambio superior no lo afecta.

La ejecución solamente podrá continuar cuando todos los approval
gates y precondiciones aplicables vuelvan a cumplirse.

---

# 19. Implementation Rules

Durante `/implement`:

- realizar el cambio mínimo necesario;
- respetar la TASK activa;
- reutilizar antes de crear cuando corresponda;
- seguir patrones existentes;
- ejecutar pruebas relevantes;
- registrar evidencia;
- registrar discoveries;
- detenerse ante decisiones superiores faltantes.

Evitar:

- scope creep;
- refactors no relacionados;
- dependencias innecesarias;
- arquitectura especulativa;
- funcionalidades no solicitadas.

---

# 20. Test Integrity

Una prueba no deberá modificarse únicamente para conseguir PASS.

Cuando una prueba falle deberá determinarse si el problema
pertenece a:

CODE
TEST
PLAN
SPEC
ENVIRONMENT

Corregir el nivel responsable.

No ocultar el fallo.

---

# 21. Security

Todo trabajo deberá respetar:

`.spec/standards/security.md`

Especial atención cuando se modifique:

- authentication;
- authorization;
- sensitive data;
- secrets;
- external input;
- destructive operations;
- uploads;
- integrations;
- logging;
- database access.

Los requisitos SEC deberán tener evidencia verificable.

---

# 22. Discoveries

Trabajo fuera del alcance detectado durante implementación deberá
registrarse como:

DISCOVERY-[XXX]

Un discovery no autoriza automáticamente su implementación.

Deberá evaluarse posteriormente mediante el flujo SDD
correspondiente.

---

# 23. Validation

Una feature no deberá considerarse completada únicamente porque:

- compila;
- los tests pasan;
- todas las TASKS están DONE.

La feature deberá pasar:

`/validate`

El gate final es:

SPEC COMPLIANCE: PASS

FEATURE STATUS: VALIDATED

---

# 24. Definition of Done

Una feature SDD está terminada cuando:

- SPEC está APPROVED;
- PLAN está APPROVED;
- TASKS fueron completadas;
- requisitos MUST están satisfechos;
- criterios obligatorios tienen evidencia;
- pruebas requeridas están PASS;
- requisitos SEC están PASS;
- quality gates obligatorios están PASS;
- no existen bloqueos pendientes;
- no existen traceability gaps bloqueantes;
- validation resulta PASS.

Resultado:

FEATURE STATUS: VALIDATED

---

# 25. Human Authority

El agente deberá solicitar decisión humana cuando ésta sea
necesaria para avanzar.

El agente podrá:

- analizar;
- detectar inconsistencias;
- proponer alternativas;
- explicar consecuencias;
- generar artefactos;
- implementar trabajo aprobado;
- validar evidencia.

El agente no deberá sustituir aprobación humana cuando
el Harness la requiera.

---

# 26. Core Operating Rule

Cuando exista duda sobre qué hacer:

1. detener cambios destructivos;
2. identificar el nivel responsable;
3. consultar el artefacto correspondiente;
4. utilizar `[NEEDS CLARIFICATION]` cuando sea necesario;
5. solicitar decisión humana cuando corresponda;
6. continuar solamente cuando el gate permita avanzar.

Nunca resolver incertidumbre significativa mediante
implementación especulativa.
