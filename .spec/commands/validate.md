# Comando: Validate

## Propósito

Validar que la implementación final de una feature cumple la
especificación aprobada y que existe evidencia suficiente para demostrar
dicho cumplimiento.

Este comando constituye el gate final del flujo SDD.

La validación no se limita a comprobar que:

-   el código compila;
-   las tareas están marcadas como DONE;
-   los tests pasan.

Debe comprobar trazabilidad completa:

Requirement → Acceptance Criterion → Plan → Task → Implementation → Test
→ Evidence

El resultado final deberá ser:

PASS

FAIL

o:

BLOCKED

------------------------------------------------------------------------

# 1. Entrada

El comando recibe una feature implementada.

Ejemplo:

/validate SPEC-001

o conceptualmente:

/validate specs/001-task-management/

La feature deberá contener como mínimo:

spec.md plan.md tasks.md

y una implementación asociada.

------------------------------------------------------------------------

# 2. Precondiciones

Antes de iniciar la validación deberá verificarse:

-   [ ] La SPEC existe.
-   [ ] La SPEC está APPROVED.
-   [ ] El PLAN existe.
-   [ ] El PLAN está APPROVED.
-   [ ] TASKS existe.
-   [ ] TASKS está COMPLETED.
-   [ ] Las TASKS obligatorias están DONE.
-   [ ] No existen bloqueos conocidos pendientes.
-   [ ] Existe implementación para validar.

Si estas condiciones no se cumplen:

VALIDATION STATUS:

BLOCKED

------------------------------------------------------------------------

# 3. Contexto obligatorio

Durante validación deberán consultarse:

1.  `.spec/constitution.md`
2.  `.spec/standards/architecture.md`
3.  `.spec/standards/coding.md`
4.  `.spec/standards/testing.md`
5.  `.spec/standards/security.md`
6.  SPEC aprobada;
7.  PLAN aprobado;
8.  TASKS;
9.  ADR relacionados;
10. implementación final;
11. pruebas;
12. evidencia producida durante implementación.

La SPEC constituye la fuente principal para determinar el comportamiento
esperado.

Si un requisito obligatorio no puede trazarse hasta evidencia
verificable deberá marcarse:

TRACEABILITY GAP

La feature no podrá obtener PASS mientras exista un TRACEABILITY GAP
obligatorio.

## Regla normativa de validación

`.spec/templates/validation.template.md` define la estructura y los
gates obligatorios del artefacto de validación.

El comando `/validate` deberá completar y respetar todos los gates,
estados, findings, resultados y reglas aplicables definidos por dicha
plantilla.

Una regla obligatoria definida por la plantilla no podrá omitirse
únicamente porque no se encuentre repetida explícitamente en este
comando.

Si existiera una contradicción entre este comando y la plantilla, deberá
aplicarse la jerarquía de fuentes definida por el Harness y registrarse
la inconsistencia en lugar de resolverla silenciosamente.

------------------------------------------------------------------------

# 4. Requirement Coverage

Deberán revisarse individualmente:

FR-\[XXX\] NFR-\[XXX\] SEC-\[XXX\]

Cada requisito deberá recibir uno de los siguientes estados:

PASS FAIL BLOCKED NOT_APPLICABLE

`NOT_APPLICABLE` solamente podrá utilizarse con justificación explícita.

Los requisitos MUST deberán encontrarse en PASS para que la validación
final pueda resultar PASS.

------------------------------------------------------------------------

# 5. Acceptance Criteria Validation

Cada criterio de aceptación deberá verificarse contra la implementación
real.

Ejemplo:

AC-001

Given: usuario autenticado

When: crea una tarea válida

Then: la tarea queda disponible dentro del proyecto

Evidence:

TEST-004

Result:

PASS

Un criterio de aceptación no deberá marcarse PASS únicamente porque
exista código relacionado.

Debe existir evidencia suficiente de que el comportamiento esperado fue
verificado.

------------------------------------------------------------------------

# 6. Validación de pruebas

Deberán revisarse las pruebas requeridas por:

-   SPEC;
-   PLAN;
-   TASKS;
-   testing standard.

Para cada prueba registrar:

TEST-\[XXX\]

Type: UNIT \| INTEGRATION \| CONTRACT \| E2E \| SECURITY \| OTHER

Related:

FR-\[XXX\] AC-\[XXX\] SEC-\[XXX\]

Result:

PASS \| FAIL \| BLOCKED \| NOT_RUN

Una prueba requerida en:

FAIL BLOCKED NOT_RUN

no constituye evidencia de cumplimiento.

------------------------------------------------------------------------

# 7. Calidad de evidencia

La validación deberá comprobar que las pruebas realmente verifican el
comportamiento requerido.

Deberá detectar cuando sea razonablemente posible:

-   assertions insuficientes;
-   tests vacíos;
-   tests deshabilitados;
-   tests ignorados;
-   mocks que eliminan el comportamiento relevante;
-   tests que verifican implementación pero no comportamiento;
-   criterios de aceptación sin prueba;
-   pruebas que ya no corresponden con la SPEC.

PASS técnico no implica automáticamente PASS funcional.

------------------------------------------------------------------------

# 8. Quality Gates

Deberán ejecutarse o verificarse los controles disponibles y relevantes
del proyecto.

Cuando existan:

FORMAT LINT TYPE CHECK UNIT TESTS INTEGRATION TESTS CONTRACT TESTS E2E
TESTS SECURITY CHECKS BUILD

Cada gate deberá registrar:

PASS FAIL BLOCKED NOT_APPLICABLE

------------------------------------------------------------------------

# 9. Security Validation

Los requisitos de seguridad deberán validarse explícitamente.

Revisar cuando corresponda:

-   autenticación;
-   autorización;
-   ownership;
-   validación de input;
-   exposición de datos;
-   secretos;
-   operaciones destructivas;
-   uploads;
-   integraciones externas;
-   logs;
-   mensajes de error;
-   acceso a datos.

Cada SEC-\[XXX\] deberá tener evidencia verificable.

Una feature con un requisito de seguridad obligatorio en FAIL no podrá
obtener validación final PASS.

## Security Findings

Los hallazgos de seguridad deberán registrarse mediante:

SEC-FINDING-\[XXX\]

Estados permitidos:

OPEN MITIGATED ACCEPTED NOT_APPLICABLE

### OPEN

El hallazgo permanece sin resolver.

### MITIGATED

Existe una mitigación implementada y evidencia verificable de su
efectividad.

MITIGATED requiere evidencia.

### ACCEPTED

El riesgo fue aceptado mediante la autoridad correspondiente.

ACCEPTED no significa:

COMPLIANT

y no constituye automáticamente evidencia para:

PASS

### NOT_APPLICABLE

El hallazgo no aplica al alcance validado y deberá existir justificación
explícita.

Si la resolución o aceptación de un hallazgo implica modificar
requisitos, alcance o diseño técnico, deberá volver al artefacto
propietario correspondiente y recuperar los approval gates aplicables
antes de continuar.

------------------------------------------------------------------------

# 10. Scope Validation

La validación deberá comparar la implementación final contra el alcance
aprobado.

Revisar:

-   archivos creados;
-   archivos modificados;
-   archivos eliminados;
-   dependencias agregadas;
-   migraciones;
-   configuración;
-   contratos;
-   comportamiento nuevo.

Si existe trabajo no autorizado deberá clasificarse.

Clasificaciones:

AUTHORIZED MINOR DEVIATION UNAUTHORIZED CHANGE

## AUTHORIZED

El cambio está respaldado por SPEC, PLAN o TASKS.

## MINOR DEVIATION

Cambio menor necesario para implementar correctamente una tarea y
documentado en evidencia.

## UNAUTHORIZED CHANGE

Cambio significativo sin trazabilidad o aprobación.

Un UNAUTHORIZED CHANGE significativo deberá impedir PASS hasta que:

-   sea eliminado;

o:

-   sea incorporado correctamente al flujo SDD.

------------------------------------------------------------------------

# 11. Scope Creep Check

Deberá buscarse trabajo introducido fuera del alcance aprobado.

Ejemplos:

-   features adicionales;
-   refactors no relacionados;
-   endpoints no solicitados;
-   dependencias innecesarias;
-   cambios arquitectónicos;
-   comportamiento no especificado.

Cuando se detecte:

SCOPE CREEP DETECTED

y deberá registrarse el elemento afectado.

------------------------------------------------------------------------

# 12. Architecture Validation

La implementación deberá compararse contra:

-   PLAN;
-   architecture standard;
-   ADR aplicables.

Verificar:

-   límites de componentes;
-   responsabilidades;
-   dependencias;
-   contratos;
-   modelo de datos;
-   integraciones;
-   decisiones arquitectónicas.

Si la implementación contradice una decisión aprobada:

ARCHITECTURE DEVIATION

La desviación deberá resolverse o documentarse mediante el proceso
correspondiente antes de obtener PASS.

------------------------------------------------------------------------

# 13. Regression Validation

Deberán verificarse pruebas existentes relevantes para asegurar que la
feature no haya roto comportamiento previamente válido.

Una regresión conocida sin resolver deberá producir:

FAIL

salvo que el comportamiento anterior haya sido explícitamente
reemplazado mediante una SPEC aprobada.

------------------------------------------------------------------------

# 14. Task Validation

Cada TASK marcada como DONE deberá verificarse contra su Definition of
Done.

Revisar:

-   objetivo;
-   archivos;
-   tests;
-   requisitos;
-   criterios de aceptación;
-   quality checks;
-   evidencia.

Si una TASK está marcada DONE pero carece de evidencia suficiente:

TASK VALIDATION:

FAIL

------------------------------------------------------------------------

# 15. Discoveries

Los elementos DISCOVERY-\[XXX\] deberán revisarse.

Cada discovery deberá clasificarse como:

NON_BLOCKING BLOCKING

Un discovery será BLOCKING cuando revele que:

-   un requisito no se cumple;
-   existe un riesgo de seguridad obligatorio;
-   existe una regresión;
-   existe una contradicción;
-   la implementación no puede considerarse válida.

Los discoveries no bloqueantes podrán trasladarse a trabajo futuro.

------------------------------------------------------------------------

# 16. Matriz final de trazabilidad

La validación deberá producir una matriz final.

  ------------------------------------------------------------------------------------
  Requirement   Acceptance   Plan      Task       Implementation   Test       Result
  ------------- ------------ --------- ---------- ---------------- ---------- --------
  FR-001        AC-001       DEC-001   TASK-002   task.service     TEST-001   PASS

  FR-002        AC-002       DEC-002   TASK-003   task.service     TEST-002   PASS

  SEC-001       AC-005       DEC-004   TASK-005   authorization    TEST-006   PASS
  ------------------------------------------------------------------------------------

Toda fila obligatoria deberá terminar en:

PASS

------------------------------------------------------------------------

# 17. Missing Traceability

Deberá detectarse cualquiera de los siguientes casos:

Requirement without Acceptance Criterion

Acceptance Criterion without Task

Task without Requirement or Plan justification

Implementation without Task

Required behavior without Test or equivalent evidence

Test without relevant behavior

Cuando corresponda deberá registrarse:

TRACEABILITY GAP

------------------------------------------------------------------------

# 18. Resultado final

La validación solamente podrá resultar:

PASS

cuando:

-   todos los requisitos MUST estén PASS;
-   todos los criterios de aceptación obligatorios estén PASS;
-   todas las pruebas requeridas estén PASS;
-   todos los quality gates obligatorios estén PASS;
-   todos los requisitos SEC obligatorios estén PASS;
-   no existan regresiones conocidas sin resolver;
-   no existan traceability gaps bloqueantes;
-   no existan cambios no autorizados significativos;
-   no existan desviaciones arquitectónicas bloqueantes;
-   no permanezca OPEN ningún finding bloqueante;
-   ninguna TASK requerida permanezca incompleta;
-   TASKS esté COMPLETED;
-   la evidencia sea suficiente para demostrar cumplimiento.

## FAIL

Utilizar cuando existe evidencia suficiente para demostrar que la
implementación no cumple un requisito obligatorio.

Ejemplos:

-   test falla;
-   criterio de aceptación no satisfecho;
-   requisito de seguridad incumplido;
-   regresión confirmada;
-   implementación contradictoria con la SPEC.

## BLOCKED

Utilizar cuando no es posible determinar cumplimiento debido a:

-   entorno no disponible;
-   dependencia externa inaccesible;
-   prueba requerida no ejecutable;
-   evidencia faltante;
-   decisión pendiente.

BLOCKED no deberá tratarse como PASS.

------------------------------------------------------------------------

# 19. Manejo de fallos

Cuando la validación resulte FAIL deberá determinarse el nivel
responsable.

## Implementation defect

Volver a:

/implement

Antes de modificar código, aplicar el procedimiento de reapertura de la
sección 17.1 de `/implement`: vincular el finding, reabrir TASKS y las
tareas afectadas, conservar la evidencia anterior y comprobar nuevamente
las precondiciones. Tras la corrección, cerrar TASKS y repetir `/validate`.

------------------------------------------------------------------------

## Task decomposition defect

Volver a:

/tasks

------------------------------------------------------------------------

## Technical design defect

Volver a:

/plan

------------------------------------------------------------------------

## Requirement defect

Volver a:

/specify o /clarify

según corresponda.

------------------------------------------------------------------------

# 20. Artefacto de validación

El comando deberá utilizar:

.spec/templates/validation.template.md

como estructura base.

La plantilla original no deberá modificarse durante la validación.

El resultado deberá almacenarse en:

specs/`<feature-id>`{=html}/validation.md

Ejemplo:

specs/001-task-management/ ├── spec.md ├── plan.md ├── tasks.md └──
validation.md

El reporte deberá contener:

-   feature validada;
-   versión de SPEC;
-   versión de PLAN;
-   fecha;
-   requirement coverage;
-   acceptance criteria;
-   tests;
-   security validation;
-   quality gates;
-   scope validation;
-   traceability matrix;
-   findings;
-   resultado final.

------------------------------------------------------------------------

# 21. Salida

Formato recomendado:

SDD VALIDATION REPORT ────────────────────────────────

SPEC: SPEC-001

PLAN: PLAN-001

TASKS: TASKS-001

Requirements:

FR: 5 / 5 PASS

NFR: 2 / 2 PASS

SEC: 2 / 2 PASS

Acceptance Criteria: 9 / 9 PASS

Tests:

Unit: 12 PASS

Integration: 8 PASS

E2E: 3 PASS

Security: 4 PASS

Quality Gates:

Format: PASS Lint: PASS Types: PASS Build: PASS

Traceability Gaps: 0

Regressions: 0

Unauthorized Changes: 0

Blocking Findings: 0

────────────────────────────────

SPEC COMPLIANCE:

PASS

FEATURE STATUS:

VALIDATED ────────────────────────────────

SDD VALIDATION REPORT ────────────────────────────────

Requirements: 8 / 9 PASS

Failed:

SEC-002 AC-008 TEST-014

Finding:

Authorization check can be bypassed.

SPEC COMPLIANCE:

FAIL

FEATURE STATUS:

NOT VALIDATED

Required Action:

Return to /implement ────────────────────────────────

------------------------------------------------------------------------

# 22. Self-check

Antes de finalizar `/validate` verificar:

-   [ ] Todos los requisitos MUST fueron revisados.
-   [ ] Todos los criterios obligatorios fueron revisados.
-   [ ] La trazabilidad fue reconstruida.
-   [ ] Las pruebas requeridas fueron verificadas.
-   [ ] La calidad de la evidencia fue revisada.
-   [ ] Los quality gates relevantes fueron verificados.
-   [ ] Los requisitos de seguridad fueron verificados.
-   [ ] Se revisaron regresiones.
-   [ ] Se revisó scope creep.
-   [ ] Se revisaron desviaciones arquitectónicas.
-   [ ] Se revisaron TASKS marcadas DONE.
-   [ ] Se revisaron discoveries.
-   [ ] Se identificaron traceability gaps.
-   [ ] Todo FAIL tiene una causa documentada.
-   [ ] Todo BLOCKED tiene una causa documentada.
-   [ ] PASS solamente fue utilizado con evidencia suficiente.

------------------------------------------------------------------------

# 23. Acciones prohibidas

Durante `/validate` el agente NO deberá:

-   marcar PASS sin evidencia;
-   ignorar pruebas fallidas;
-   tratar BLOCKED como PASS;
-   ignorar requisitos MUST;
-   ignorar requisitos SEC;
-   modificar criterios para hacer coincidir la implementación;
-   eliminar evidencia desfavorable;
-   ocultar regresiones;
-   ignorar cambios no autorizados;
-   modificar silenciosamente la SPEC;
-   modificar silenciosamente el PLAN;
-   redefinir el comportamiento esperado;
-   declarar VALIDATED una feature que no cumple el gate.

El objetivo es determinar objetivamente si la implementación cumple la
especificación aprobada.
