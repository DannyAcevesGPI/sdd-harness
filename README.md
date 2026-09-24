# SDD Harness

Harness base para desarrollar software utilizando **Spec-Driven Development (SDD)**.

El objetivo del proyecto es establecer un proceso estructurado y trazable para transformar una necesidad en software validado mediante:

```text
Idea
  ↓
Specification
  ↓
Clarification
  ↓
Technical Plan
  ↓
Tasks
  ↓
Implementation
  ↓
Validation
```

La regla fundamental del Harness es:

> No implementation without an approved specification.

Para features que recorren el flujo completo:

> No implementation without an approved SPEC, PLAN and TASKS.

---

# 1. ¿Qué es Spec-Driven Development?

Spec-Driven Development es un enfoque donde la implementación parte de una especificación explícita y verificable.

En lugar de comenzar directamente modificando código:

```text
Idea
  ↓
Code
```

el Harness utiliza:

```text
Idea
  ↓
SPEC
  ↓
PLAN
  ↓
TASKS
  ↓
CODE
  ↓
VALIDATION
```

Cada etapa produce información que permite justificar y verificar la siguiente.

El objetivo no es generar más documentación por sí misma.

El objetivo es reducir:

* ambigüedad;
* decisiones implícitas;
* cambios fuera de alcance;
* implementación especulativa;
* pérdida de contexto;
* falta de trazabilidad;
* diferencias entre lo solicitado y lo implementado.

---

# 2. Objetivos del Harness

Este Harness busca proporcionar un proceso reutilizable para:

* especificar funcionalidades antes de implementarlas;
* detectar ambigüedades;
* separar decisiones funcionales y técnicas;
* diseñar soluciones basadas en requisitos reales;
* dividir el trabajo en unidades pequeñas y verificables;
* mantener trazabilidad entre requisitos y código;
* integrar pruebas desde la planificación;
* considerar seguridad durante todo el ciclo;
* controlar cambios de alcance;
* producir evidencia de implementación;
* validar la implementación contra la especificación original;
* permitir colaboración controlada entre humanos y agentes de IA.

---

# 3. Principio de trazabilidad

El Harness mantiene la siguiente cadena:

```text
Requirement
    ↓
Acceptance Criterion
    ↓
Technical Plan
    ↓
Task
    ↓
Implementation
    ↓
Test
    ↓
Validation
```

Esto permite responder preguntas como:

```text
¿Por qué existe este código?
```

siguiendo:

```text
Code
 ↓
Task
 ↓
Plan
 ↓
Requirement
```

Y también:

```text
¿Cómo sabemos que FR-001 fue implementado?
```

siguiendo:

```text
FR-001
 ↓
AC-001
 ↓
DEC-001
 ↓
TASK-003
 ↓
Code
 ↓
TEST-004
 ↓
PASS
```

---

# 4. Estructura del repositorio

```text
.
├── .spec/
│   ├── constitution.md
│   │
│   ├── standards/
│   │   ├── architecture.md
│   │   ├── coding.md
│   │   ├── testing.md
│   │   └── security.md
│   │
│   ├── templates/
│   │   ├── specification.template.md
│   │   ├── plan.template.md
│   │   ├── tasks.template.md
│   │   └── validation.template.md
│   │
│   └── commands/
│       ├── specify.md
│       ├── clarify.md
│       ├── plan.md
│       ├── tasks.md
│       ├── implement.md
│       └── validate.md
│
├── specs/
│
├── docs/
│   ├── architecture/
│   └── decisions/
│
├── src/
├── tests/
│
├── AGENTS.md
├── README.md
└── .gitignore
```

---

# 5. Componentes del Harness

## Constitution

Archivo:

```text
.spec/constitution.md
```

Define las reglas fundamentales del proceso SDD.

Tiene precedencia sobre los demás artefactos internos del Harness, después de las decisiones humanas explícitas y aprobadas.

---

## Standards

Directorio:

```text
.spec/standards/
```

Contiene los estándares generales del repositorio.

### Architecture

```text
.spec/standards/architecture.md
```

Define principios para decisiones arquitectónicas, componentes, dependencias, contratos, datos e integraciones.

### Coding

```text
.spec/standards/coding.md
```

Define principios de implementación, mantenibilidad, errores, dependencias, configuración y calidad de código.

### Testing

```text
.spec/standards/testing.md
```

Define cómo las pruebas se relacionan con requisitos, criterios de aceptación y evidencia.

### Security

```text
.spec/standards/security.md
```

Define los principios mínimos de seguridad aplicables durante especificación, planificación, implementación y validación.

---

# 6. Templates

Los templates definen la estructura de los artefactos producidos durante el proceso.

```text
.spec/templates/
```

Incluye:

```text
specification.template.md
plan.template.md
tasks.template.md
validation.template.md
```

Los templates funcionan como estructuras base.

No representan una feature concreta y no deberán modificarse para almacenar información específica de una feature.

---

# 7. Commands

Los commands describen cómo ejecutar cada fase del proceso.

```text
.spec/commands/
```

Actualmente existen:

| Command      | Propósito                                 |
| ------------ | ----------------------------------------- |
| `/specify`   | Crear una especificación                  |
| `/clarify`   | Resolver ambigüedades funcionales         |
| `/plan`      | Diseñar la solución técnica               |
| `/tasks`     | Descomponer el plan en trabajo ejecutable |
| `/implement` | Implementar tareas aprobadas              |
| `/validate`  | Validar la implementación contra la SPEC  |

Estos comandos representan operaciones conceptuales del Harness.

La versión inicial del proyecto no requiere necesariamente un CLI que implemente literalmente estos comandos.

---

# 8. Flujo SDD

El flujo completo es:

```text
                    IDEA
                     │
                     ▼
                  /specify
                     │
                     ▼
                    SPEC
                     │
                     ▼
                  /clarify
                     │
                     ▼
              SPEC APPROVED
                     │
                     ▼
                   /plan
                     │
                     ▼
              PLAN APPROVED
                     │
                     ▼
                   /tasks
                     │
                     ▼
             TASKS APPROVED
                     │
                     ▼
                /implement
                     │
                     ▼
            TASKS IN_PROGRESS
                     │
                     ▼
               IMPLEMENTATION
                     │
                     ▼
             TASKS COMPLETED
                     │
                     ▼
                 /validate
                     │
              ┌──────┴──────┐
              ▼             ▼
             PASS       FAIL / BLOCKED
              │             │
              ▼             ▼
 SPEC COMPLIANCE: PASS    Correction
              │             │
              ▼             ▼
 FEATURE STATUS:       Repeat affected
    VALIDATED               stages
```

Los estados:

```text
TASK DONE
TASKS COMPLETED
FEATURE STATUS: VALIDATED
```

representan conceptos distintos y no deberán tratarse como equivalentes.

`TASK DONE` representa la finalización de una tarea individual.

`TASKS COMPLETED` representa que el documento TASKS cumple las condiciones necesarias para cerrar la ejecución planificada.

`FEATURE STATUS: VALIDATED` solamente se alcanza después de una validación final satisfactoria.

---

# 9. Estados principales

## Specification

```text
DRAFT
  ↓
IN_REVIEW
  ↓
APPROVED
  ↓
SUPERSEDED
```

## Plan

```text
DRAFT
  ↓
IN_REVIEW
  ↓
APPROVED
  ↓
SUPERSEDED
```

## Tasks document

```text
DRAFT
  ↓
IN_REVIEW
  ↓
APPROVED
  ↓
IN_PROGRESS
  ↓
COMPLETED
```

## Individual Task

```text
TODO
  ↓
IN_PROGRESS
  ├──→ BLOCKED
  │
  └──→ DONE
```

Cuando la validación detecte un defecto exclusivamente de implementación,
el procedimiento de `/implement`, sección 17.1, permite reabrir TASKS
`COMPLETED → IN_PROGRESS` y las tareas afectadas `DONE → TODO`. Conserva
la evidencia anterior y exige repetir las verificaciones afectadas,
cerrar nuevamente TASKS y ejecutar `/validate`.

`PLANNING STATUS: BLOCKED` y `TASK GENERATION STATUS: BLOCKED` describen
operaciones bloqueadas, no estados adicionales de PLAN o TASKS.
`CANCELLED` es una anotación histórica de un identificador de tarea
retirado mediante la revisión correspondiente, no un estado de tarea activa.

## Validation

Resultado:

```text
PASS
FAIL
BLOCKED
```

Cuando la validación final resulta:

```text
SPEC COMPLIANCE: PASS
```

la feature puede alcanzar:

```text
FEATURE STATUS: VALIDATED
```

---

# 10. Human Approval Gates

El Harness mantiene autoridad humana sobre decisiones relevantes.

Requieren aprobación humana explícita:

```text
SPEC
IN_REVIEW → APPROVED

PLAN
IN_REVIEW → APPROVED

TASKS
IN_REVIEW → APPROVED
```

Un agente no deberá interpretar la ausencia de comentarios como aprobación.

---

# 11. Mutation Boundary

Las primeras fases trabajan principalmente sobre artefactos SDD:

```text
/specify
/clarify
/plan
/tasks
```

Estas fases no implementan la feature.

La modificación del código de aplicación comienza en:

```text
/implement
```

Conceptualmente:

```text
SPECIFICATION / DESIGN
──────────────────────────────

/specify
/clarify
/plan
/tasks

══════════════════════════════
      MUTATION BOUNDARY
══════════════════════════════

IMPLEMENTATION
──────────────────────────────

/implement
    ↓
src/
tests/
migrations/
configuration
```

---

# 12. Quick Start

## Paso 1 — Crear o utilizar un repositorio con el Harness

La estructura mínima deberá contener:

```text
.spec/
specs/
docs/
src/
tests/
AGENTS.md
README.md
```

---

## Paso 2 — Describir una feature

Ejemplo conceptual:

```text
/specify

Quiero permitir que los usuarios creen y administren tareas.
```

El resultado esperado será una nueva carpeta:

```text
specs/001-task-management/
```

con:

```text
spec.md
```

basado en:

```text
.spec/templates/specification.template.md
```

---

## Paso 3 — Resolver ambigüedades

Si la SPEC contiene:

```text
[NEEDS CLARIFICATION]
```

utilizar:

```text
/clarify
```

Las respuestas deberán incorporarse a la SPEC.

Una respuesta no se considera integrada únicamente por existir dentro de la sección de preguntas.

---

## Paso 4 — Aprobar la SPEC

Cuando la especificación esté completa:

```text
DRAFT
 ↓
IN_REVIEW
 ↓
APPROVED
```

La aprobación deberá ser explícita.

---

## Paso 5 — Crear el plan técnico

Ejecutar conceptualmente:

```text
/plan
```

El resultado será:

```text
specs/001-task-management/plan.md
```

El plan deberá derivarse de:

* SPEC aprobada;
* estado real del repositorio;
* standards;
* arquitectura existente;
* decisiones previas aplicables.

---

## Paso 6 — Aprobar el PLAN

```text
DRAFT
 ↓
IN_REVIEW
 ↓
APPROVED
```

---

## Paso 7 — Generar TASKS

Ejecutar:

```text
/tasks
```

Resultado:

```text
specs/001-task-management/tasks.md
```

Cada tarea deberá tener trazabilidad y criterios claros de finalización.

---

## Paso 8 — Aprobar TASKS

```text
DRAFT
 ↓
IN_REVIEW
 ↓
APPROVED
```

Solamente después de este gate comienza la implementación.

---

## Paso 9 — Implementar

Ejemplo:

```text
/implement TASK-001
```

La implementación deberá:

* respetar el alcance de la tarea;
* seguir SPEC y PLAN;
* implementar pruebas;
* ejecutar checks relevantes;
* producir evidencia;
* registrar blockers y discoveries.

---

## Paso 10 — Validar

Cuando:

```text
tasks.md → COMPLETED
```

y:

```text
todas las TASKS obligatorias → DONE
```

podrá ejecutarse conceptualmente:

```text
/validate SPEC-001
```

El estado `DONE` de las tareas individuales no sustituye el estado `COMPLETED` del documento TASKS.

Si todas las TASKS obligatorias están `DONE` pero el documento TASKS permanece `IN_PROGRESS`, deberá completarse y verificarse el cierre del documento TASKS antes de avanzar a `/validate`.

Se generará:

```text
specs/001-task-management/validation.md
```

utilizando:

```text
.spec/templates/validation.template.md
```

El resultado final podrá ser:

```text
PASS
FAIL
BLOCKED
```

Una feature solamente podrá alcanzar:

```text
FEATURE STATUS: VALIDATED
```

cuando la validación final determine:

```text
SPEC COMPLIANCE: PASS
```

---

# 13. Estructura de una feature

Una feature completa tendrá aproximadamente:

```text
specs/
└── 001-task-management/
    ├── spec.md
    ├── plan.md
    ├── tasks.md
    └── validation.md
```

Cada archivo responde una pregunta diferente:

```text
spec.md
¿Qué debemos construir y por qué?

plan.md
¿Cómo lo construiremos?

tasks.md
¿Qué trabajo concreto debemos ejecutar?

validation.md
¿Cómo demostramos que realmente cumplimos la SPEC?
```

---

# 14. Clarifications

Cuando exista una ambigüedad relevante deberá utilizarse:

```text
[NEEDS CLARIFICATION]
```

Ejemplo:

```text
Q-001

Estado:
[NEEDS CLARIFICATION]

Pregunta:
¿Puede un administrador modificar tareas pertenecientes
a otros usuarios?

Bloqueante:
YES
```

No deberá inventarse una respuesta para continuar.

Una vez resuelta:

```text
[NEEDS CLARIFICATION]
        ↓
[CLARIFIED]
```

La decisión deberá propagarse a los requisitos y criterios afectados.

---

# 15. Escalamiento

Los problemas deberán corregirse en el nivel que posee la decisión.

```text
Problema funcional
        ↓
       SPEC

Problema técnico
        ↓
       PLAN

Problema de descomposición
        ↓
      TASKS

Problema de implementación
        ↓
   IMPLEMENTATION
```

Esto evita resolver problemas de diseño mediante cambios improvisados en código.

---

# 16. Change Propagation

Los artefactos dependen entre sí:

```text
SPEC
 ↓
PLAN
 ↓
TASKS
 ↓
IMPLEMENTATION
 ↓
VALIDATION
```

Si cambia un artefacto superior, deberá evaluarse el impacto sobre todos los artefactos inferiores.

Ejemplo:

```text
SPEC v1.0
   ↓
PLAN v1.0
   ↓
TASKS
   ↓
IMPLEMENTATION
```

Si cambia la SPEC:

```text
SPEC v1.1
   ↓
Review PLAN
   ↓
Review TASKS
   ↓
Review IMPLEMENTATION
   ↓
Repeat VALIDATION
```

Un artefacto inferior no deberá considerarse automáticamente válido después de un cambio superior.

La revisión de un artefacto downstream no implica que éste deba modificarse obligatoriamente.

Solamente deberán modificarse los artefactos realmente afectados por el cambio.

## Approval Recovery

Cuando un artefacto previamente `APPROVED` sea modificado, su aprobación previa no deberá considerarse suficiente para autorizar automáticamente el nuevo contenido.

Las actualizaciones de estados de ejecución y evidencia que no cambian
el trabajo autorizado no requieren una nueva aprobación, incluida la
reapertura para corregir defectos de implementación según `/implement`.

Antes de continuar con trabajo dependiente deberá:

1. identificarse el artefacto propietario del cambio;
2. actualizarse dicho artefacto;
3. evaluarse el impacto sobre los artefactos downstream;
4. actualizarse solamente los artefactos realmente afectados;
5. recuperarse el approval gate de todo artefacto previamente `APPROVED` cuyo contenido haya sido modificado;
6. reevaluarse evidencia y pruebas obtenidas previamente cuando el cambio pueda haberlas invalidado;
7. volver a comprobarse las precondiciones de la fase siguiente.

Si una SPEC aprobada es modificada:

* deberá recuperar aprobación humana;
* deberá evaluarse el impacto sobre PLAN;
* PLAN solamente deberá modificarse si resulta afectado;
* TASKS solamente deberá modificarse si resulta afectado.

Si un PLAN aprobado es modificado:

* deberá recuperar aprobación humana;
* deberá evaluarse el impacto sobre TASKS;
* TASKS solamente deberá modificarse si resulta afectado.

Si TASKS aprobado es modificado de forma que cambie el trabajo autorizado:

* deberá recuperar aprobación humana antes de continuar la implementación afectada.

La modificación de un artefacto downstream no será obligatoria cuando la evaluación determine que el cambio superior no lo afecta.

La ejecución solamente podrá continuar cuando todos los approval gates y precondiciones aplicables vuelvan a cumplirse.

---

# 17. Architecture Decision Records

Las decisiones arquitectónicas significativas podrán documentarse en:

```text
docs/decisions/
```

Ejemplo:

```text
docs/decisions/
└── ADR-001-authentication-strategy.md
```

No toda decisión técnica requiere un ADR.

Los ADR deberán reservarse para decisiones con impacto arquitectónico significativo, trade-offs relevantes o consecuencias difíciles de revertir.

---

# 18. Documentación de arquitectura

La documentación arquitectónica transversal podrá almacenarse en:

```text
docs/architecture/
```

Este directorio puede utilizarse para describir aspectos que exceden una única feature, como:

* visión general del sistema;
* límites principales;
* componentes;
* flujos;
* integraciones;
* diagramas;
* decisiones estructurales vigentes.

---

# 19. Convenciones de identificadores

El Harness utiliza identificadores estables para mantener trazabilidad.

## Requirements

```text
FR-001
NFR-001
SEC-001
BR-001
```

## Acceptance

```text
AC-001
```

Todos los Acceptance Criteria utilizan el namespace:

```text
AC-[XXX]
```

incluidos los criterios relacionados con requisitos de seguridad.

La trazabilidad de seguridad deberá expresarse mediante la cadena:

```text
SEC-[XXX]
   ↓
AC-[XXX]
   ↓
TEST-[XXX]
   ↓
Evidence
   ↓
Validation
```

Ejemplo:

```text
SEC-001
   ↓
AC-004
   ↓
TEST-004
   ↓
Security Evidence
   ↓
Validation
```

No deberá crearse un namespace independiente como:

```text
AC-SEC-[XXX]
TEST-SEC-[XXX]
```

salvo que una versión futura del Harness lo defina explícitamente.

## Assumptions and Clarifications

```text
ASM-001
Q-001
Q-TECH-001
Q-TASK-001
```

## Planning

```text
DEC-001
RISK-001
ADR-001
```

## Execution

```text
TASK-001
TEST-001
BLOCK-001
DISCOVERY-001
```

## Validation

```text
VALIDATION-001
FINDING-001
GAP-001
DEV-001
SEC-FINDING-001
```

Los identificadores referenciados no deberán reutilizarse para representar elementos diferentes.

---

# 20. Seguridad

La seguridad forma parte de todo el ciclo:

```text
SPEC
 ↓
Security Requirements

PLAN
 ↓
Security Design

TASKS
 ↓
Security Work

IMPLEMENTATION
 ↓
Security Controls

TESTS
 ↓
Security Evidence

VALIDATION
 ↓
Security Compliance
```

El estándar correspondiente se encuentra en:

```text
.spec/standards/security.md
```

---

# 21. Agentes de IA

Los agentes que trabajen dentro del repositorio deberán comenzar consultando:

```text
AGENTS.md
```

Este archivo define:

* cómo detectar la fase actual;
* cómo seleccionar el command correcto;
* qué artefactos consultar;
* cuándo puede modificarse código;
* cómo manejar clarifications;
* cómo escalar problemas;
* cómo preservar trazabilidad.

Las instrucciones detalladas continúan en:

```text
.spec/
```

---

# 22. Filosofía de diseño

El Harness busca favorecer:

```text
Explicit > Implicit

Small changes > Large speculative changes

Traceable decisions > Hidden decisions

Evidence > Assumptions

Reuse > Unnecessary creation

Simple architecture > Premature complexity

Human approval > Agent self-approval
```

El Harness no prescribe automáticamente:

* lenguaje;
* framework;
* base de datos;
* arquitectura específica;
* proveedor cloud;
* librerías;
* estrategia de deployment.

Estas decisiones deberán derivarse del contexto real de cada proyecto.

---

# 23. Qué NO es este Harness

Este proyecto no pretende ser:

* un framework de aplicación;
* una arquitectura obligatoria;
* un generador automático de código;
* un reemplazo de revisión humana;
* una metodología que obliga a documentar todo;
* una excusa para introducir burocracia innecesaria.

El nivel de detalle deberá ser proporcional al impacto y riesgo del cambio.

---

# 24. Estado del proyecto

Versión del Harness:

```text
1.0.0
```

Estado:

```text
STABLE
```

La versión se declara estable después de completar:

1. revisión integral del Harness;
2. corrección de inconsistencias;
3. ejecución de una feature de prueba end-to-end;
4. evaluación de los resultados;
5. ajustes derivados del ejercicio.

---

# 25. Baseline auditada

AUDIT-01 a AUDIT-10 completados: PASS. Sin hallazgos abiertos.
El cierre y la autorización humana constan en `handoff.md`, sección 44.

Baseline candidata posterior al ejercicio, conservada inicialmente como PRE-RELEASE:
`34740af8f8a3d0bf3c86a996adcded4c02fb4185`.

Secuencia realmente ejecutada y autorizada:

```text
Harness Documentation
        ↓
Integral Review
        ↓
Consistency Check
        ↓
Test Feature
        ↓
End-to-End SDD Cycle
        ↓
Lessons Learned
        ↓
Harness Adjustments
        ↓
Post-audit Baseline Commit
        ↓
Baseline Verification
        ↓
Version:
1.0.0

Status:
STABLE
```

STABLE se refiere al Harness procedimental auditado, no a una aplicación
productiva ni a un motor CLI automatizado. La muestra validada usa identidades
sintéticas y estado en memoria; no demuestra autenticación productiva ni todas
las rutas posibles de revisión de SPEC/PLAN.

La promoción se registra en un segundo commit local. No implica tag, push ni
publicación remota; estas operaciones requieren autorización separada.
