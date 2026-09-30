# Comando: Plan

## Propósito

Transformar una especificación aprobada en un plan técnico
implementable, trazable y consistente con la arquitectura,
estándares y estado actual del repositorio.

Este comando genera:

specs/<feature-id>/plan.md

El comando NO implementa código.

El comando NO genera tareas de implementación.

---

# 1. Entrada

El comando recibe una SPEC existente.

Ejemplo:

/plan SPEC-001

o conceptualmente:

/plan specs/001-task-management/spec.md

La SPEC deberá encontrarse en estado:

APPROVED

Si la SPEC no está aprobada:

PLANNING STATUS: BLOCKED

No deberá generarse el plan.

---

# 2. Contexto obligatorio

Antes de generar el plan deberá consultarse:

1. `.spec/constitution.md`
2. `.spec/standards/architecture.md`
3. `.spec/standards/coding.md`
4. `.spec/standards/testing.md`
5. `.spec/standards/security.md`
6. `.spec/templates/plan.template.md`
7. la SPEC objetivo;
8. documentación técnica relevante;
9. ADR existentes relevantes;
10. código existente relacionado.

La planificación deberá basarse en el estado real del repositorio.

No deberá diseñarse el sistema suponiendo que el repositorio
está vacío.

---

# 3. Inspección del repositorio

Antes de proponer cambios técnicos deberá inspeccionarse
la estructura existente del proyecto.

Deberá identificarse cuando corresponda:

- lenguaje;
- runtime;
- framework;
- package manager;
- estructura de carpetas;
- módulos existentes;
- patrones arquitectónicos;
- base de datos;
- ORM o mecanismo de persistencia;
- APIs;
- sistema de configuración;
- autenticación;
- autorización;
- estrategia de testing;
- logging;
- observabilidad;
- CI/CD;
- infraestructura;
- convenciones existentes.

El objetivo es integrar la nueva funcionalidad con el sistema
existente en lugar de crear estructuras paralelas innecesarias.

## Regla de reutilización

Antes de proponer un nuevo:

- servicio;
- repository;
- módulo;
- helper;
- componente;
- middleware;
- abstracción;
- dependencia;

deberá verificarse si ya existe una capacidad equivalente
en el repositorio.

Preferir:

REUSE

antes de:

CREATE

cuando la reutilización sea coherente con la arquitectura
y no introduzca acoplamiento incorrecto.

---

# 4. Contexto técnico detectado

El plan deberá documentar el contexto técnico relevante encontrado.

Ejemplo:

Runtime:
Node.js

Framework:
Next.js

Language:
TypeScript

Database:
PostgreSQL

ORM:
Prisma

Testing:
Vitest

Package Manager:
Bun

Architecture:
Modular application

Relevant modules:

- src/modules/users
- src/modules/projects
- src/modules/tasks

Este contexto deberá derivarse del repositorio.

No deberá inventarse.

---

# 5. Mapa de requisitos

Antes de diseñar la solución deberá construirse un mapa
de los requisitos que necesitan implementación.

Ejemplo:

FR-001
Crear tareas

FR-002
Editar tareas

FR-003
Completar tareas

SEC-001
Solo usuarios autorizados pueden modificar tareas

NFR-001
La operación deberá mantener el comportamiento esperado
bajo las restricciones definidas.

Cada requisito MUST deberá tener una estrategia técnica
dentro del plan.

---

# 6. Diseño de la solución

El plan deberá proponer la solución técnica mínima necesaria
para satisfacer la SPEC aprobada.

El diseño deberá favorecer:

- simplicidad;
- coherencia con el sistema existente;
- reutilización;
- separación clara de responsabilidades;
- testabilidad;
- mantenibilidad;
- seguridad;
- trazabilidad.

No deberá agregarse infraestructura o abstracciones únicamente
por anticipar necesidades futuras no especificadas.

Evitar:

"We may need this someday."

Preferir:

"This is required by FR-003 because..."

---

# 7. Decisiones técnicas

Las decisiones relevantes deberán documentarse mediante:

DEC-[XXX]

Cada decisión deberá incluir:

- decisión;
- justificación;
- requisitos relacionados;
- alternativas consideradas;
- consecuencias;
- necesidad de ADR.

Ejemplo:

DEC-001

Decisión:

Reutilizar el TaskRepository existente.

Justificación:

El repositorio ya encapsula la persistencia de Task y puede
extenderse para satisfacer FR-002 sin crear una abstracción paralela.

Relacionado con:

FR-002

Alternativas:

1. Crear un nuevo repository.
2. Extender TaskRepository existente.

Decisión:

Extender el existente.

ADR:

NO

---

# 8. Evaluación de ADR

Una decisión deberá considerarse candidata a ADR cuando:

- modifica significativamente la arquitectura;
- introduce una tecnología importante;
- reemplaza una tecnología existente;
- cambia límites entre componentes;
- introduce un patrón arquitectónico relevante;
- modifica una estrategia de persistencia;
- afecta múltiples features;
- tiene consecuencias difíciles de revertir;
- representa un trade-off arquitectónico significativo.

Ejemplo:

Migrar de REST a GraphQL.

ADR: YES

Agregar un método a un repository existente.

ADR: NO

El plan deberá registrar:

ADR-[XXX]

y su ubicación esperada:

docs/decisions/ADR-[XXX]-<slug>.md

El ADR deberá documentarse antes de implementar la decisión
cuando ésta sea necesaria para continuar.

---

# 9. Diseño de datos

Cuando la SPEC implique persistencia deberá analizarse:

- entidades existentes;
- relaciones existentes;
- nuevos campos;
- nuevas entidades;
- constraints;
- índices cuando sean necesarios;
- integridad referencial;
- migraciones;
- compatibilidad con datos existentes.

El modelo físico deberá derivarse de las necesidades de la SPEC.

No deberán agregarse campos o relaciones sin justificación.

## Cambios destructivos

Si el diseño requiere:

- eliminar columnas;
- eliminar tablas;
- cambiar tipos incompatibles;
- eliminar datos;
- modificar relaciones de forma incompatible;

deberá marcarse:

DESTRUCTIVE CHANGE: YES

y documentarse una estrategia explícita de migración,
rollback o mitigación.

---

# 10. Diseño de contratos

Cuando corresponda deberán definirse:

- endpoints;
- eventos;
- comandos;
- interfaces;
- schemas;
- contratos entre módulos;
- integraciones externas.

Cada contrato deberá relacionarse con uno o más requisitos.

Ejemplo:

POST /tasks

Relacionado con:

FR-001

No deberán crearse endpoints o interfaces sin una necesidad
derivada de la SPEC o arquitectura existente.

---

# 11. Diseño de seguridad

El plan deberá evaluar:

Authentication

¿Quién realiza la operación?

Authorization

¿Está autorizado para realizarla?

Input Validation

¿Qué entradas deben validarse?

Sensitive Data

¿Existe información sensible?

Secrets

¿Se requieren credenciales o secretos?

Audit

¿La operación requiere trazabilidad?

Destructive Operations

¿Existe una operación destructiva?

Los controles deberán mapearse contra los requisitos SEC
cuando existan.

---

# 12. Estrategia de pruebas

Cada criterio de aceptación deberá tener una estrategia
de verificación.

Ejemplo:

AC-001
→ Integration Test

AC-002
→ Unit Test

AC-003
→ E2E Test

SEC-001 / AC-007
→ Authorization Integration Test

El plan deberá definir el tipo de prueba.

Los IDs concretos TEST-[XXX] podrán asignarse posteriormente
durante la generación de tareas.

Para cada cambio de comportamiento automatizable, el PLAN deberá identificar
casos derivados de requisitos y criterios de aceptación, nivel de prueba,
herramienta o comando previsto y viabilidad de ejecutar RED antes de modificar
código productivo. Cuando TDD no aplique, deberá registrar el motivo y la
verificación alternativa. La política está en `.spec/standards/testing.md`.

La planificación no autoriza escribir código de pruebas: ese trabajo comienza
en `/implement` tras aprobar SPEC, PLAN y TASKS.

---

# 13. Análisis de impacto

Antes de finalizar el plan deberá estimarse qué partes
del repositorio serán afectadas.

Clasificar como:

CREATE
MODIFY
REUSE
REMOVE

Ejemplo:

REUSE
src/modules/tasks/task.repository.ts

MODIFY
src/modules/tasks/task.service.ts

CREATE
src/modules/tasks/task.controller.ts

CREATE
tests/tasks/create-task.integration.test.ts

El listado puede ajustarse durante TASKS si aparecen detalles
menores, pero cambios estructurales deberán volver al PLAN.

---

# 14. Nuevas dependencias

Antes de introducir una dependencia externa deberá verificarse:

1. ¿Es realmente necesaria?
2. ¿Existe una solución ya disponible en el proyecto?
3. ¿Puede resolverse razonablemente sin una nueva dependencia?
4. ¿Es compatible con el stack?
5. ¿Introduce riesgos de seguridad?
6. ¿Introduce mantenimiento significativo?

Toda nueva dependencia deberá incluir una justificación.

No deberá instalarse durante `/plan`.

---

# 15. Aclaraciones técnicas

Si durante la planificación aparece una decisión que no puede
resolverse utilizando:

- SPEC;
- Constitución;
- Standards;
- arquitectura existente;
- ADR existentes;
- restricciones documentadas;

deberá utilizarse:

[NEEDS CLARIFICATION]

Formato:

Q-TECH-[XXX]

Estado:
[NEEDS CLARIFICATION]

Pregunta:
[Pregunta]

Impacto:
[Impacto]

Bloqueante:
YES | NO

Una aclaración técnica no deberá utilizarse para ocultar
una deficiencia funcional de la SPEC.

Si la pregunta realmente corresponde a comportamiento de negocio,
permisos, alcance o requisitos:

STOP

La pregunta deberá regresar a la SPEC.

---

# 16. Deficiencias descubiertas en la SPEC

Si durante `/plan` se descubre que la SPEC contiene:

- ambigüedad bloqueante;
- contradicción;
- requisito imposible de interpretar;
- comportamiento faltante;
- problema de seguridad funcional;

el proceso deberá detenerse.

Resultado:

SPEC REVISION REQUIRED

El agente deberá indicar:

- problema detectado;
- requisito afectado;
- motivo;
- aclaración necesaria.

No deberá corregirse silenciosamente desde el PLAN.

---

# 17. Análisis de riesgos

Los riesgos técnicos relevantes deberán documentarse como:

RISK-[XXX]

Cada riesgo deberá indicar:

- descripción;
- impacto;
- probabilidad;
- mitigación.

Clasificaciones:

LOW
MEDIUM
HIGH

No deberán registrarse riesgos triviales únicamente para llenar
la sección.

---

# 18. Self-check

Antes de finalizar `/plan` deberá verificarse:

- [ ] La SPEC está APPROVED.
- [ ] Se inspeccionó el repositorio.
- [ ] Se identificó el stack real.
- [ ] Se identificaron componentes reutilizables.
- [ ] Todos los requisitos MUST tienen cobertura técnica.
- [ ] Las decisiones relevantes tienen justificación.
- [ ] No existe overengineering evidente.
- [ ] El modelo de datos está definido cuando corresponde.
- [ ] Los contratos están definidos cuando corresponde.
- [ ] La seguridad fue considerada.
- [ ] Los criterios de aceptación tienen estrategia de pruebas.
- [ ] El impacto sobre el repositorio está identificado.
- [ ] Las nuevas dependencias están justificadas.
- [ ] Los cambios destructivos están identificados.
- [ ] Los riesgos relevantes están documentados.
- [ ] Los ADR necesarios están identificados.
- [ ] No existen contradicciones con la SPEC.
- [ ] No existen `[NEEDS CLARIFICATION]` bloqueantes.

---

# 19. Creación del artefacto

El comando deberá utilizar:

.spec/templates/plan.template.md

como estructura base.

El resultado deberá guardarse en:

specs/<feature-id>/plan.md

Ejemplo:

specs/001-task-management/
├── spec.md
└── plan.md

La plantilla original no deberá modificarse.

---

# 20. Estado resultante

`PLANNING STATUS` describe el resultado de la operación, no el estado del
documento. Un bloqueo no añade `BLOCKED` al ciclo del PLAN: un borrador
permanece `DRAFT`; una revisión de diseño aprobado deberá recuperar los
approval gates aplicables antes de continuar el trabajo dependiente.

Si existen aclaraciones técnicas bloqueantes:

PLAN STATUS:

DRAFT

RESULT:

NEEDS CLARIFICATION

---

Si se detecta un problema funcional en la SPEC:

PLANNING STATUS:

BLOCKED

RESULT:

SPEC REVISION REQUIRED

---

Si el plan está completo pero requiere revisión:

PLAN STATUS:

IN_REVIEW

RESULT:

READY FOR REVIEW

---

El plan solamente podrá pasar a:

APPROVED

mediante aprobación humana explícita.

Para features nuevas, registrar la decisión humana y la huella del contenido
autorizado de PLAN en `decisions.json` siguiendo
`docs/state-reconstruction.md`. Ejecutar el comprobador local antes de
generar TASKS; un fallo de procedencia o huella bloquea el gate.

---

# 21. Salida

Formato recomendado:

SDD TECHNICAL PLAN
────────────────────────────────

SPEC:
SPEC-001

PLAN:
PLAN-001

Path:
specs/001-task-management/plan.md

Requirements covered:
FR: 5/5
NFR: 1/1
SEC: 2/2

Technical decisions:
4

ADR required:
1

Repository impact:

CREATE: 3
MODIFY: 4
REUSE: 5
REMOVE: 0

Technical clarifications:
0 blocking
1 non-blocking

Risks:
2

Status:
READY FOR REVIEW

Next:
Human approval
────────────────────────────────

---

# 22. Acciones prohibidas

Durante `/plan` el agente NO deberá:

- implementar código;
- modificar código de aplicación;
- instalar dependencias;
- ejecutar migraciones;
- generar `tasks.md`;
- modificar requisitos silenciosamente;
- cambiar la SPEC sin revisión;
- introducir arquitectura no justificada;
- crear abstracciones especulativas;
- agregar funcionalidad no solicitada;
- ignorar estándares;
- ignorar ADR existentes;
- marcar el PLAN como APPROVED sin aprobación humana explícita.

El objetivo exclusivo es producir un diseño técnico
implementable y trazable.
