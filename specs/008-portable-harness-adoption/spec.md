# Especificación: Adopción portable del Harness

**ID:** SPEC-008  
**Estado:** APPROVED  
**Versión:** 0.2.0  
**Fecha:** 2026-09-30

---

# 1. Resumen

## 1.1 Descripción

El Harness deberá poder adoptarse en un proyecto nuevo como un conjunto
coherente, verificable y de lectura inicial acotada. Sus reglas de registro,
guía de copia y comprobaciones deberán funcionar también en el primer ciclo
SDD de ese proyecto.

## 1.2 Problema

El estado sin chat ya funciona en este repo, pero la guía de adopción omite
archivos necesarios, el primer ledger contradice el límite de mutación de
`/specify`, no hay una prueba de adopción desde cero ni un control CI, y la
coherencia de `handoff.md`/índice depende de revisión manual. El README largo
mezcla entrada rápida y detalle que podría leerse solo bajo demanda.

## 1.3 Objetivo

Permitir que una persona o agente inicie un proyecto nuevo con el Harness,
ejecute su primera feature sin contradicciones de fase y detecte automáticamente
omisiones de registro o estado antes de integrar cambios.

---

# 2. Alcance

## 2.1 Incluido

- Resolver el permiso de creación/actualización del registro de decisiones en
  las fases SDD, sin abrir permisos de implementación prematuros.
- Definir el conjunto reusable completo y su adaptación al proyecto destino.
- Probar la adopción sobre un repo nuevo sin historia heredada.
- Ejecutar comprobaciones automáticas en CI y detectar resumen/índice obsoletos.
- Reducir la lectura inicial y separar guía breve de referencia extensa.

## 2.2 Fuera de alcance

- Autoaprobar SPEC, PLAN o TASKS, o sustituir `/validate` por CI.
- Copiar auditorías, validaciones o aprobaciones de este repo como estado del
  proyecto destino.
- Requerir un proveedor, stack de aplicación o servicio externo para el flujo
  SDD en sí; el PLAN decidirá el mecanismo de CI del repositorio actual.
- Introducir hooks ejecutables o subagentes obligatorios.
- Cambiar el comportamiento de la feature de prueba `src/audit_tasks.py`.

---

# 3. Actores

## ACT-001 — Responsable de proyecto nuevo

Selecciona la base reusable, adapta reglas locales, aprueba gates y comprueba
que el proyecto inicia sin arrastrar estado ajeno.

## ACT-002 — Agente de desarrollo

Sigue el bootstrap, crea artefactos permitidos por fase y reconstruye gates sin
leer conversaciones previas.

## ACT-003 — Integrador o revisor

Recibe resultados de checks automáticos y decide si el cambio puede continuar;
los checks no ejercen autoridad humana.

---

# 4. Requisitos funcionales

## FR-001 — Registro permitido por fase

**Descripción:** El flujo deberá permitir crear el registro vacío al iniciar
una feature y añadir decisiones/aprobaciones humanas en SPEC, PLAN o TASKS,
incluidas aclaraciones, sin contradecir límites de mutación. El permiso se
limitará al registro de decisiones y a proyecciones de estado/enlaces de
`handoff.md` e índice documental; no autorizará código, pruebas ni cambios de
contenido no operativos antes de `/implement`.

**Prioridad:** MUST  
**Origen:** Contradicción entre `AGENTS.md`, `/specify` y el protocolo de
reconstrucción.

## FR-002 — Paquete de adopción completo

**Descripción:** La guía deberá identificar todos los archivos y requisitos de
ejecución necesarios para que las instrucciones copiadas sean ejecutables en un
repo nuevo, así como qué archivos deben adaptarse y cuáles no deben copiarse
como estado propio. La comprobación de estado deberá funcionar en una primera
feature con ID bajo, sin clasificarla por error como legado de este repo.

**Prioridad:** MUST  
**Origen:** Guía de adopción desactualizada respecto de SPEC-007.

## FR-003 — Prueba de adopción desde cero

**Descripción:** Existirá una comprobación reproducible en un repo aislado sin
features históricas que verifique la instalación de la base, el primer SPEC en
`DRAFT`, el registro de un gate de ejemplo etiquetado como sintético, el
diagnóstico de una aprobación inválida y la reconstrucción de la siguiente
acción. No tratará una decisión sintética como aprobación humana real.

**Prioridad:** MUST  
**Origen:** Necesidad de verificar adopción antes de usar el Harness en otros
proyectos.

## FR-004 — Comprobación continua

**Descripción:** Los cambios del Harness en este repositorio deberán ejecutar
automáticamente las pruebas y la comprobación de estado en CI. Un fallo en un
gate verificable deberá producir un resultado fallido visible. CI no aprobará
artefactos ni declarará una feature `VALIDATED`.

**Prioridad:** MUST  
**Origen:** Evitar depender de ejecución manual para detectar regresiones.

## FR-005 — Consistencia del estado vivo

**Descripción:** Una comprobación repetible deberá detectar cuando
`handoff.md` o el índice anuncien una feature, fase, validación o siguiente
acción incompatible con los artefactos vigentes, y reportar la discrepancia
sin reescribir decisiones ni ocultar el origen del conflicto.

**Prioridad:** MUST  
**Origen:** El comprobador actual verifica ledgers/huellas, pero no el resumen
de arranque.

## FR-006 — Entrada documental breve

**Descripción:** La documentación de entrada para un proyecto nuevo deberá
mostrar una ruta corta hacia bootstrap, adopción y comandos SDD; el detalle
histórico y de referencia se consultará mediante enlaces, sin duplicarlo en el
README o handoff.

**Prioridad:** MUST  
**Origen:** Optimización de contexto solicitada por el usuario.

---

# 5. Requisitos no funcionales

## NFR-001 — Presupuesto de contexto

**Categoría:** Usabilidad / Mantenibilidad  
**Descripción:** El bootstrap obligatorio no incluirá leer el README completo
ni evidencias históricas. `AGENTS.md` y `handoff.md` mantendrán menos de 200
líneas cada uno; el README principal será un índice práctico de hasta 300
líneas, con referencia detallada enlazada bajo demanda.  
**Métrica o condición:** Conteo de líneas y recorrido de arranque documentado.

## NFR-002 — Portabilidad verificable

**Categoría:** Mantenibilidad  
**Descripción:** La base reusable no exigirá conservar nombres o estados de
features de este repo para operar correctamente; cualquier requisito del
runtime de herramientas deberá declararse al adoptarla.  
**Métrica o condición:** La prueba de adopción pasa con primera feature nueva y
sin las carpetas SPEC-001 a SPEC-007 originales.

---

# 6. Requisitos de seguridad

## SEC-001 — Adopción aislada y sin secretos

**Descripción:** La instalación y la prueba de adopción no deberán trasladar
secretos, credenciales ni evidencia sensible de este repo al proyecto destino;
la comprobación aislada no deberá escribir fuera del destino de prueba ni
interpretar datos sintéticos como autorización humana real.  
**Riesgo mitigado:** Fuga de datos y falsa procedencia de aprobaciones.

---

# 7. Reglas de negocio

## BR-001 — Autoridad humana intacta

El registro y CI solo verifican procedencia documental e integridad interna.
Ninguno crea una aprobación humana por sí mismo.

## BR-002 — Legado local, no portable

Las excepciones de procedencia de SPEC-001 a SPEC-006 pertenecen a este repo.
Un proyecto nuevo no heredará esas excepciones por coincidencia de ID.

---

# 8. Criterios de aceptación

## AC-001 — Primera SPEC sin contradicción

**Relacionado con:** FR-001, BR-001

**Given** un proyecto nuevo sin features, **when** un agente inicia `/specify` y
la SPEC queda `DRAFT`, **then** puede crear el registro vacío permitido por esa
fase y actualizar solo estado/enlaces del handoff e índice sin tocar
implementación; tras aprobación humana explícita puede registrar el gate y
avanzar sin infringir el límite de mutación.

## AC-002 — Base copiada funcional

**Relacionado con:** FR-002, NFR-002, BR-002

**Given** la guía de adopción, **when** se copia exactamente la base declarada a
un repo nuevo y se aplican sus adaptaciones obligatorias, **then** todas las
rutas/comandos de bootstrap existen, la primera feature se comprueba como nueva
y no se interpreta como legado local.

## AC-003 — Smoke test aislado

**Relacionado con:** FR-003, SEC-001

**Given** un destino temporal vacío, **when** se ejecuta la prueba de adopción,
**then** verifica caso válido y casos inválidos de registro/estado, termina sin
red ni secretos y deja evidencia de que los datos de aprobación son sintéticos.

## AC-004 — CI detecta falla

**Relacionado con:** FR-004, BR-001

**Given** un cambio con ledger ausente o huella inválida, **when** CI ejecuta
los checks, **then** el job falla y muestra la causa; un cambio válido ejecuta
tests y comprobador en PASS sin producir aprobaciones.

## AC-005 — Resumen/índice desactualizado

**Relacionado con:** FR-005

**Given** un `handoff.md` o índice incompatible con artefactos vigentes,
**when** se ejecuta el diagnóstico, **then** identifica archivo y diferencia,
sin afirmar PASS ni corregir el estado automáticamente.

## AC-006 — Lectura inicial acotada

**Relacionado con:** FR-006, NFR-001

**Given** una sesión nueva, **when** sigue el bootstrap, **then** encuentra la
acción autorizada sin leer el README completo o auditorías cerradas;
`AGENTS.md` y `handoff.md` tienen menos de 200 líneas y README no supera 300.

## AC-007 — Sin contaminación histórica

**Relacionado con:** FR-002, SEC-001, BR-002

**Given** un paquete para otro proyecto, **when** se inspecciona el destino,
**then** no contiene `specs/` históricos, `handoff.md` de este repo, secretos ni
evidencia de auditoría ajena como estado propio.

---

# 9. Casos límite y escenarios de error

## EDGE-001 — Aprobación ambigua o inexistente

El ledger podrá existir vacío durante DRAFT, pero no habilitará PLAN ni
implementación sin una decisión humana explícita y registro vigente.

## EDGE-002 — Mismo ID que una feature legada

Una nueva `001-*` en otro proyecto seguirá las reglas nuevas; la excepción
histórica de este repo no se aplicará por número solamente.

## EDGE-003 — Resumen manual atrasado

El diagnóstico fallará y señalará la discrepancia; no inferirá que el resumen
es fuente más fuerte que SPEC/PLAN/TASKS/validación.

## EDGE-004 — CI no disponible

La indisponibilidad del servicio CI se reportará como límite externo; no se
interpretará como PASS ni como aprobación.

---

# 10. Datos involucrados

## Base reusable

Lista de artefactos necesarios, adaptables y excluidos al adoptar el Harness.

## Estado y decisiones

Feature, fase, gate, resultado de validación, próximo paso y eventos de
decisión. Los registros históricos del repo fuente no son estado del destino.

---

# 11. Dependencias

- SPEC-007 y `docs/state-reconstruction.md` para el contrato vigente.
- `docs/adoption.md`, `docs/quickstart.md`, README, commands y templates.
- Constitución y standards del Harness.

---

# 12. Restricciones y transición

- Antes de aprobar v0.2.0 solo se modificó esta SPEC; la excepción anterior no
  se amplió ni se creó contenido nuevo fuera de ella sin autorización.
- **Excepción transitoria solicitada para la revisión 0.2.0:** Al aprobar
  SPEC-008, autorizar explícitamente crear/actualizar
  `specs/008-portable-harness-adoption/decisions.json` para registrar esa
  aprobación y decisiones relacionadas, y actualizar solo estado y enlaces de
  `handoff.md` y `docs/index.md` durante SPEC/PLAN/TASKS. Reglas afectadas:
  límite de mutación de `AGENTS.md` sección 5 y prohibición de editar fuera de
  SPEC en `.spec/commands/specify.md` sección 18. Justificación: el gate nuevo
  y la reconstrucción del estado serían imposibles de mantener coherentes con
  el proceso actual. No autoriza código, templates ni cambios sustantivos en
  otros documentos antes de sus fases aprobadas.
- La excepción dura solo hasta que esta feature corrija formalmente los límites
  de mutación; luego se aplicará el contrato permanente aprobado.

---

# 13. Suposiciones

Ninguna que cambie el comportamiento solicitado. El proveedor y formato
concreto de CI, así como la forma de empaquetar la base, se deciden en PLAN
según el repositorio real.

---

# 14. Preguntas abiertas

No hay aclaraciones funcionales bloqueantes conocidas.

---

# 15. Matriz inicial de trazabilidad

| Requisito | Criterios de aceptación | Prioridad |
|-----------|-------------------------|-----------|
| FR-001 | AC-001 | MUST |
| FR-002 | AC-002, AC-007 | MUST |
| FR-003 | AC-003 | MUST |
| FR-004 | AC-004 | MUST |
| FR-005 | AC-005 | MUST |
| FR-006 | AC-006 | MUST |
| NFR-001 | AC-006 | MUST |
| NFR-002 | AC-002 | MUST |
| SEC-001 | AC-003, AC-007 | MUST |
| BR-001 | AC-001, AC-004 | MUST |
| BR-002 | AC-002, AC-007 | MUST |

---

# 16. Criterios para avanzar a planificación

- [x] Problema, objetivo, alcance, actores y fuera de alcance definidos.
- [x] Cinco casos solicitados cubiertos por requisitos y AC verificables.
- [x] Seguridad, legado y casos límite considerados.
- [x] No hay aclaraciones bloqueantes ni arquitectura prematura.
- [x] Nueva aprobación humana explícita de SPEC-008 v0.2.0 y de la excepción
      transitoria ampliada de la sección 12.
- [x] Registro durable de la nueva decisión antes de generar PLAN.

---

# 17. Estado de aprobación

**Estado actual:** APPROVED  
**Aprobado por:** Usuario responsable del proyecto  
**Fecha de aprobación:** 2026-09-30  
**Decisión explícita y alcance:** "Listo aprobado" en respuesta a la solicitud
de aprobación de SPEC-008 v0.2.0 y de la excepción transitoria ampliada al
ledger, `handoff.md` y `docs/index.md` solo para estado y enlaces. Autoriza
preparar PLAN; no autoriza implementación.  
**Registro durable:** `decisions.json`, DECISION-001 (aprobación histórica),
DECISION-002 (sustitución), DECISION-003 (aprobación vigente).

**Historial:** El usuario aprobó explícitamente SPEC-008 v0.1.0 y una excepción
limitada a `decisions.json` el 2026-09-30 (DECISION-001). Esa aprobación no
cubre la ampliación de v0.2.0 a proyecciones de estado/enlaces. La huella de
DECISION-001 quedó desplazada por DECISION-002 al abrir la revisión 0.2.0.
No se compara como aprobación vigente. Solo DECISION-003 habilita PLAN.
