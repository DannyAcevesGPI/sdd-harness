# Constitución del SDD Harness

**Versión:** 1.0.0  
**Estado:** Activa

## Propósito

Esta constitución define los principios no negociables que gobiernan
el desarrollo de software dentro de este repositorio.

Toda especificación, plan, tarea, implementación y validación debe
cumplir con estos principios.

---

## Artículo I — Especificación antes de implementación

Ninguna funcionalidad podrá implementarse sin una especificación
explícita.

Toda funcionalidad deberá comenzar con una especificación ubicada en:

specs/<feature-id>/spec.md

La especificación deberá describir:

- El problema que se busca resolver.
- Los requisitos funcionales.
- Los requisitos no funcionales cuando correspondan.
- Los requisitos de seguridad cuando correspondan.
- Los criterios de aceptación.
- Las restricciones.
- Las suposiciones relevantes.

Los detalles de implementación no deberán introducirse en la
especificación salvo que formen parte de una restricción explícita.

---

## Artículo II — Los requisitos deben ser verificables

Todo requisito aplicable, incluyendo requisitos funcionales,
no funcionales y de seguridad, deberá ser:

- Explícito.
- Identificable de forma única.
- Verificable.
- Trazable.

Los requisitos funcionales utilizarán identificadores como:

FR-001
FR-002
FR-003

Las convenciones específicas para otros tipos de requisitos deberán
definirse en los templates y standards correspondientes.

Los criterios de aceptación utilizarán identificadores como:

AC-001
AC-002
AC-003

Los requisitos ambiguos deberán aclararse antes de comenzar
la implementación.

---

## Artículo III — Planificación antes de implementación

Una especificación aprobada deberá convertirse en un plan técnico
antes de comenzar la implementación.

Toda funcionalidad deberá contener como mínimo:

spec.md
plan.md
tasks.md

Antes de comenzar la implementación:

- La especificación deberá estar aprobada.
- El plan técnico deberá estar aprobado.
- El documento de tareas deberá estar aprobado.

La especificación define QUÉ debe lograr el sistema.

El plan define CÓMO se implementará.

Las tareas definen QUÉ trabajo concreto deberá ejecutarse para
implementar el plan.

Estas responsabilidades deberán mantenerse separadas.

La aprobación de SPEC, PLAN y TASKS deberá ser explícita y corresponder
a la autoridad humana definida por esta constitución.

---

## Artículo IV — Trazabilidad de tareas

Toda tarea de implementación deberá hacer referencia al menos a un
requisito o criterio de aceptación.

Ejemplo:

TASK-004
Implementa: FR-002
Valida: AC-003

No se permiten tareas de implementación sin relación con una
especificación.

---

## Artículo V — Trazabilidad completa

La implementación deberá poder rastrearse mediante la siguiente cadena:

Requisito
→ Criterio de aceptación
→ Plan
→ Tarea
→ Código
→ Prueba
→ Validación

Un requisito no se considerará completado hasta que pueda identificarse
su implementación y su validación.

---

## Artículo VI — La validación es obligatoria

Una funcionalidad no se considera terminada únicamente porque el
código haya sido escrito o porque sus tareas estén `DONE`.

La validación final deberá comprobar como mínimo que:

1. Las tareas requeridas estén terminadas.
2. Las pruebas correspondientes sean satisfactorias.
3. Los criterios de aceptación hayan sido validados.
4. No existan problemas bloqueantes sin resolver.
5. La implementación corresponda con la especificación aprobada.
6. La trazabilidad requerida pueda demostrarse mediante evidencia.

Los resultados de la validación deberán quedar documentados.

Una funcionalidad solamente podrá alcanzar:

`FEATURE STATUS: VALIDATED`

cuando la validación final produzca:

`SPEC COMPLIANCE: PASS`

---

## Artículo VII — Las pruebas forman parte del proceso

Las pruebas deberán verificar comportamientos observables definidos
por los requisitos y criterios de aceptación.

Las pruebas no deberán existir únicamente para aumentar métricas
de cobertura.

Todo requisito crítico deberá contar con una prueba automatizada
o una validación explícitamente documentada.

---


## Artículo VIII — Los cambios deberán resolverse en su nivel responsable

Cuando durante el proceso se descubra que una decisión existente es
incorrecta, incompleta, contradictoria o inviable:

1. Detener el trabajo afectado.
2. Documentar el conflicto.
3. Identificar el nivel responsable de la decisión.
4. Actualizar el artefacto correspondiente.
5. Evaluar el impacto sobre los artefactos y trabajo dependientes.
6. Actualizar únicamente los elementos afectados.
7. Obtener nuevamente las aprobaciones que correspondan.
8. Reanudar el trabajo afectado únicamente cuando los gates aplicables
   vuelvan a cumplirse.

El nivel responsable deberá determinarse según la naturaleza del cambio:

- Un cambio funcional o de comportamiento deberá resolverse en la SPEC.
- Un cambio técnico o arquitectónico deberá resolverse en el PLAN.
- Un cambio de descomposición o ejecución del trabajo deberá resolverse
  en TASKS.
- Un defecto localizado de implementación podrá resolverse durante
  IMPLEMENTATION cuando no altere decisiones superiores.

Los cambios deberán propagarse hacia los elementos dependientes:

SPEC
→ PLAN
→ TASKS
→ IMPLEMENTATION
→ VALIDATION

Modificar un artefacto superior no implica que todos los artefactos
inferiores deban modificarse automáticamente.

Su impacto deberá evaluarse y documentarse.

La implementación y evidencia existentes deberán revisarse cuando un
cambio pueda afectar su validez.

Si una funcionalidad previamente validada resulta afectada por un cambio,
la validación correspondiente deberá repetirse antes de volver a
considerarla `VALIDATED`.

La implementación no deberá modificar silenciosamente decisiones
definidas por artefactos superiores.

---

## Artículo IX — Cumplimiento de estándares

Todas las decisiones técnicas deberán cumplir con los estándares
definidos en:

.spec/standards/

Incluyendo:

- architecture.md
- coding.md
- testing.md
- security.md

Los planes de una funcionalidad podrán introducir restricciones
adicionales, pero no deberán ignorar silenciosamente los estándares
del repositorio.

---

## Artículo X — Explícito sobre implícito

Las suposiciones importantes deberán documentarse.

Los desarrolladores y agentes no deberán inventar:

- Reglas de negocio.
- Requisitos.
- Permisos.
- Relaciones de datos.
- Integraciones externas.

cuando estos elementos no hayan sido definidos.

La incertidumbre deberá generar una aclaración antes de implementar.

---

## Artículo XI — Cambios pequeños y revisables

La implementación deberá dividirse en tareas pequeñas y revisables.

Cada tarea deberá contar con:

- Un objetivo claro.
- Trazabilidad hacia los requisitos.
- Criterios explícitos de finalización.
- Un alcance limitado.

Las tareas excesivamente grandes deberán dividirse antes de comenzar
su implementación.

---

## Artículo XII — Autoridad humana

El desarrollador o responsable humano del proyecto tendrá la autoridad
final sobre:

- La aprobación de especificaciones.
- La aprobación de planes técnicos.
- La aprobación de documentos de tareas.
- Cambios de requisitos.
- Excepciones arquitectónicas.
- Cambios de alcance.
- Ambigüedades sin resolver.

Los agentes podrán analizar, proponer, implementar trabajo autorizado
y producir evidencia, pero no podrán autoaprobar SPEC, PLAN o TASKS.

La aprobación deberá ser explícita.

Para decisiones y aprobaciones nuevas, el resultado humano, su alcance y el
artefacto afectado deberán quedar registrados en el repositorio antes de
continuar a la fase dependiente. El chat puede transmitir la decisión, pero no
ser su único registro recuperable. El registro no sustituye a la persona ni
constituye por sí mismo una aprobación.

La ausencia de comentarios, objeciones o cambios solicitados no deberá
interpretarse como aprobación.

Una tarea individual podrá alcanzar el estado `DONE` mediante evidencia
objetiva de cumplimiento, sin requerir una aprobación humana adicional,
salvo que el proyecto establezca explícitamente lo contrario.

Los agentes no deberán redefinir silenciosamente el comportamiento
esperado del sistema.
---

# Definición de terminado (Definition of Done)

Una funcionalidad podrá considerarse terminada únicamente cuando alcance:

`FEATURE STATUS: VALIDATED`

Para alcanzar este estado deberá cumplirse:

- [ ] Existe una especificación aprobada.
- [ ] Los requisitos están identificados y son verificables.
- [ ] Los criterios de aceptación están definidos.
- [ ] Las ambigüedades bloqueantes fueron resueltas.
- [ ] Existe un plan técnico aprobado.
- [ ] Existe un documento de tareas aprobado.
- [ ] Las tareas requeridas están `DONE`.
- [ ] El documento TASKS está `COMPLETED`.
- [ ] Las tareas mantienen trazabilidad hacia requisitos y criterios aplicables.
- [ ] La implementación requerida está completa.
- [ ] Las pruebas correspondientes son satisfactorias.
- [ ] Los criterios de aceptación fueron validados.
- [ ] No existen inconsistencias o bloqueos que impidan la validación.
- [ ] Los resultados de validación están documentados.
- [ ] El resultado final de validación es `PASS`.
- [ ] `SPEC COMPLIANCE` es `PASS`.

Los estados deberán distinguirse según el objeto al que pertenecen:

- Una tarea individual puede alcanzar `DONE`.
- El documento TASKS puede alcanzar `COMPLETED`.
- Una funcionalidad alcanza `VALIDATED` únicamente después de una
  validación final satisfactoria.

---

# Precedencia

Cuando existan instrucciones contradictorias, se aplicará el siguiente
orden de precedencia:

1. Decisiones humanas explícitas y aprobadas.
2. Esta constitución.
3. Estándares del repositorio.
4. Especificación de la funcionalidad.
5. Plan técnico.
6. Tareas.
7. Detalles de implementación.

La aprobación ordinaria de un artefacto no deberá interpretarse como
aprobación implícita de una contradicción con un nivel superior.

Cuando se requiera una excepción a una regla superior, la decisión
humana deberá ser explícita e identificar, cuando corresponda:

- La regla o decisión afectada.
- El alcance de la excepción.
- La justificación.
- Los artefactos afectados.

Un nivel inferior no podrá modificar, ignorar o contradecir
silenciosamente las reglas establecidas por un nivel superior.

Cuando una contradicción no pueda resolverse mediante la precedencia
existente, deberá detenerse el trabajo afectado hasta obtener una
decisión explícita.
