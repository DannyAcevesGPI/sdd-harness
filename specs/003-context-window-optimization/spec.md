# Especificación: Optimización de handoff y ventana de contexto

**ID:** SPEC-003
**Estado:** APPROVED
**Versión:** 0.1.0
**Fecha:** 2026-09-30

---

# 1. Resumen

## 1.1 Descripción

Esta feature compacta `handoff.md` y define recomendaciones de trabajo para
reducir carga en la ventana de contexto sin perder estado, trazabilidad ni
evidencia validada.

## 1.2 Problema

`handoff.md` contiene 2406 líneas e incrusta auditorías históricas ya cerradas.
Esto ocupa contexto útil en cada bootstrap y duplica información cuyo estado
actual ya está resumido por validaciones, artefactos SDD y baseline estable.

## 1.3 Objetivo

Convertir `handoff.md` en un handoff operativo limpio y breve que indique estado
actual, decisiones vigentes, rutas a evidencia histórica y próximos criterios de
trabajo. Además, documentar qué otros artefactos o hábitos conviene pulir para
trabajar con menor carga de contexto.

---

# 2. Alcance

## 2.1 Incluido

Esta especificación incluye:

- Compactar `handoff.md` eliminando el cuerpo detallado de AUDIT-01 a AUDIT-10.
- Mover el detalle histórico largo que siga siendo útil desde `handoff.md` hacia
  documentación bajo `docs/`.
- Crear `docs/quickstart.md` como guía breve de entrada para humanos y agentes.
- Crear o actualizar un índice documental claro para saber qué leer primero y
  qué consultar solo bajo demanda.
- Preservar el estado final auditado: Harness `1.0.0 STABLE`, audits PASS,
  findings resueltos y siguiente ID disponible.
- Incluir referencia a artefactos donde vive la evidencia completa.
- Incorporar el estado validado de SPEC-002 como contexto operativo reciente.
- Establecer que futuras features registren evidencia en archivos dedicados y
  que el handoff solo enlace al estado vigente.

## 2.2 Fuera de alcance

Esta especificación NO incluye:

- Cambiar Constitución, standards, commands o templates.
- Modificar código de aplicación o pruebas.
- Reescribir README completo.
- Borrar evidencia histórica de `specs/` o commits.
- Cambiar reglas SDD ya validadas.

Los elementos fuera de alcance no deberán implementarse como parte de esta
especificación.

---

# 3. Actores

## ACT-001 — Agente principal

**Descripción:**

Agente que inicia una nueva sesión y necesita comprender rápido el estado del
repositorio.

**Responsabilidades o necesidades:**

- Cargar solo el contexto operativo vigente.
- Saber dónde consultar evidencia histórica si aparece una duda.
- Evitar repetir auditorías cerradas sin evidencia nueva.

## ACT-002 — Mantenedor humano

**Descripción:**

Persona que decide el nivel de compactación y aprueba cambios del Harness.

**Responsabilidades o necesidades:**

- Mantener recuperabilidad y trazabilidad.
- Reducir ruido de contexto para trabajo cotidiano.

---

# 4. Requisitos funcionales

## FR-001 — Compactar handoff operativo

**Descripción:**

El sistema deberá reemplazar `handoff.md` por un resumen operativo breve que no
incluya el cuerpo detallado de auditorías ya cerradas.

**Prioridad:** MUST

**Origen:**

Solicitud humana: actualizar `handoff.md` y dejarlo limpio, sin incluir audits
ya pasados.

---

## FR-002 — Preservar estado y trazabilidad

**Descripción:**

El handoff compacto deberá preservar estado vigente, resultados finales,
identificadores relevantes y rutas a evidencia histórica suficiente.

**Prioridad:** MUST

**Origen:**

Constitución, handoff actual y necesidad de no perder trazabilidad.

---

## FR-003 — Incorporar estado operativo reciente

**Descripción:**

El handoff compacto deberá reflejar que SPEC-002 fue validada y que `AGENTS.md`
quedó compacto con guías de subagentes y hooks.

**Prioridad:** MUST

**Origen:**

Trabajo validado de SPEC-002.

---

## FR-004 — Crear quickstart e índice de lectura

**Descripción:**

El sistema deberá crear una guía `docs/quickstart.md` y un índice documental que
indiquen qué leer primero y qué consultar solo cuando aplique.

**Prioridad:** MUST

**Origen:**

Decisión humana del 2026-09-30 sobre optimización de contexto.

---

## FR-005 — Separar evidencia de handoff

**Descripción:**

El sistema deberá establecer que futuras features registren evidencia en archivos
dedicados y que `handoff.md` solamente enlace al estado vigente.

**Prioridad:** MUST

**Origen:**

Decisión humana del 2026-09-30 sobre evidencia dedicada y handoff vivo.

---

# 5. Requisitos no funcionales

## NFR-001 — Brevedad verificable

**Categoría:** Mantenibilidad

**Descripción:**

`handoff.md` deberá quedar suficientemente corto para bootstrap operativo.

**Métrica o condición:**

`handoff.md` deberá quedar por debajo de 200 líneas.

---

## NFR-002 — No pérdida de evidencia

**Categoría:** Recuperabilidad

**Descripción:**

La compactación no deberá eliminar evidencia histórica recuperable en otros
artefactos o en Git.

**Métrica o condición:**

El handoff compacto deberá apuntar a `specs/001-*`, `specs/002-*`, README,
commits baseline y validaciones relevantes.

---

# 6. Requisitos de seguridad

## SEC-001 — No exposición de secretos

**Descripción:**

La compactación y recomendaciones no deberán introducir secretos, tokens,
credenciales ni instrucciones para exponerlos.

**Riesgo mitigado:**

Exposición accidental de información sensible en documentación operativa.

---

# 7. Reglas de negocio

## BR-001 — Handoff resume, no revalida

**Regla:**

`handoff.md` puede resumir estado actual y rutas de evidencia, pero no debe
presentarse como una revalidación nueva de audits históricos.

**Ejemplo:**

Puede decir "AUDIT-01 a AUDIT-10: PASS; ver evidencia histórica en Git y specs",
pero no debe repetir todo el cuerpo de cada AUDIT.

---

## BR-002 — Evidencia histórica permanece consultable

**Regla:**

La eliminación de detalle del handoff no autoriza borrar evidencia en artefactos
validados o historial Git.

**Ejemplo:**

El handoff puede apuntar a `specs/001-audit-task-management/validation.md` en vez
de duplicar su contenido.

---

# 8. Criterios de aceptación

## AC-001 — Handoff corto

**Relacionado con:** FR-001, NFR-001

### Given

Existe un `handoff.md` actualizado.

### When

Se cuenta su longitud.

### Then

El archivo tiene menos de 200 líneas y no contiene cuerpos detallados de
AUDIT-01 a AUDIT-10.

---

## AC-002 — Estado vigente preservado

**Relacionado con:** FR-002

### Given

Un agente lee el handoff compacto.

### When

Busca el estado actual del Harness.

### Then

Encuentra `1.0.0 STABLE`, audits PASS, open findings 0, next finding ID y rutas
de evidencia.

---

## AC-003 — SPEC-002 visible

**Relacionado con:** FR-003

### Given

Un agente lee el handoff compacto.

### When

Busca cambios operativos recientes.

### Then

Encuentra que SPEC-002 está `VALIDATED`, `AGENTS.md` tiene menos de 200 líneas y
existen guías de subagentes/hooks.

---

## AC-004 — Quickstart e índice

**Relacionado con:** FR-004

### Given

Un humano o agente inicia trabajo en el repositorio.

### When

Lee la documentación optimizada.

### Then

Encuentra `docs/quickstart.md` y un índice que distinguen lectura obligatoria,
lectura bajo demanda y rutas de evidencia.

---

## AC-006 — Evidencia fuera del handoff

**Relacionado con:** FR-005

### Given

Una feature futura produce evidencia.

### When

Se actualiza el estado operativo.

### Then

La evidencia vive en archivos dedicados de la feature o documentación
correspondiente, y `handoff.md` solo enlaza o resume el estado vigente.

---

## AC-005 — Seguridad y trazabilidad

**Relacionado con:** SEC-001, BR-001, BR-002

### Given

Se valida el cambio documental.

### When

Se revisa el handoff compacto.

### Then

No hay secretos, no hay pérdida de rutas a evidencia y no se fabrican nuevos PASS.

---

# 9. Casos límite y escenarios de error

## EDGE-001 — Duda sobre auditoría histórica

**Condición:**

Un agente necesita detalle de un AUDIT específico.

**Comportamiento esperado:**

Debe consultar evidencia histórica referenciada en specs, README, commits o Git,
no depender de contenido incrustado en `handoff.md`.

---

## EDGE-002 — Recomendación que implica cambio normativo

**Condición:**

Una optimización propuesta requiere cambiar Constitución, commands o standards.

**Comportamiento esperado:**

Debe abrirse flujo SDD propio antes de implementarla.

---

# 10. Datos involucrados

## Handoff operativo

Información requerida:

- Estado actual del Harness.
- Features validadas relevantes.
- Rutas de evidencia.
- Próximas reglas de trabajo.
- Recomendaciones de optimización.

Reglas relevantes:

- No revalidar históricamente.
- No borrar evidencia.
- No exponer secretos.

---

# 11. Dependencias

La funcionalidad depende de:

- `handoff.md`
- `docs/`
- `docs/quickstart.md`
- `README.md`
- `AGENTS.md`
- `specs/001-audit-task-management/validation.md`
- `specs/002-agent-operating-readiness/validation.md`
- Git history local.

---

# 12. Restricciones

Restricciones conocidas:

- No modificar código de aplicación.
- No modificar pruebas.
- No borrar evidencia histórica.
- No cambiar normas SDD sin aprobación específica.

---

# 13. Suposiciones

## ASM-001

El detalle completo de auditorías cerradas no necesita estar en el handoff activo
si permanece recuperable por evidencia y Git.

## ASM-002

El umbral de 200 líneas es apropiado para handoff operativo, igual que para
`AGENTS.md`.

---

# 14. Preguntas abiertas y necesidades de aclaración

No existen aclaraciones bloqueantes.

---

# 15. Matriz inicial de trazabilidad

| Requisito | Criterios de aceptación | Prioridad |
|-----------|-------------------------|-----------|
| FR-001 | AC-001 | MUST |
| FR-002 | AC-002, AC-005 | MUST |
| FR-003 | AC-003 | MUST |
| FR-004 | AC-004 | MUST |
| FR-005 | AC-006 | MUST |
| NFR-001 | AC-001 | MUST |
| NFR-002 | AC-002, AC-005 | MUST |
| SEC-001 | AC-005 | MUST |
| BR-001 | AC-005 | MUST |
| BR-002 | AC-005, AC-006 | MUST |

---

# 16. Criterios para avanzar a planificación

La especificación podrá avanzar a `plan.md` solamente cuando:

- [x] El problema está claramente definido.
- [x] El alcance está definido.
- [x] Los elementos fuera de alcance están definidos.
- [x] Los actores relevantes están identificados.
- [x] Los requisitos funcionales están identificados.
- [x] Los requisitos MUST tienen criterios de aceptación.
- [x] Los requisitos de seguridad relevantes están identificados.
- [x] Las reglas de negocio relevantes están documentadas.
- [x] Los principales casos límite están considerados.
- [x] Las restricciones conocidas están documentadas.
- [x] Las suposiciones importantes están documentadas.
- [x] No existen elementos `[NEEDS CLARIFICATION]` marcados como bloqueantes.
- [x] Las aclaraciones resueltas fueron incorporadas a los requisitos correspondientes.
- [x] Las decisiones obtenidas durante la aclaración quedaron documentadas.
- [x] Los requisitos son verificables.
- [x] No se han introducido decisiones técnicas innecesarias.

---

# 17. Estado de aprobación

**Estado actual:**

APPROVED

Estados permitidos:

DRAFT
→ IN_REVIEW
→ APPROVED
→ SUPERSEDED

## Aprobación

La transición a `APPROVED` requiere aprobación humana explícita.

Los agentes pueden preparar y revisar la SPEC, pero no podrán autoaprobarla.

**Aprobado por:**

Usuario, mediante respuesta "Aprobada" en conversación del 2026-09-30.

**Fecha de aprobación:**

2026-09-30

La implementación no podrá comenzar mientras la especificación no se encuentre
en estado:

APPROVED
