# Plan Técnico: Optimización de handoff y ventana de contexto

**ID:** PLAN-003
**SPEC relacionada:** SPEC-003
**Estado:** APPROVED
**Versión:** 0.1.0
**Fecha:** 2026-09-30

---

# 1. Precondiciones

- [x] Existe una SPEC asociada.
- [x] La SPEC se encuentra en estado `APPROVED`.
- [x] No existen `[NEEDS CLARIFICATION]` bloqueantes.
- [x] Los requisitos MUST tienen criterios de aceptación.
- [x] El alcance está claramente definido.
- [x] Las restricciones relevantes están documentadas.

---

# 2. Resumen técnico

## 2.1 Objetivo

Reorganizar documentación operativa para reducir carga de contexto: `handoff.md`
será estado vivo breve, el detalle largo pasará a `docs/`, y habrá quickstart e
índice de lectura.

## 2.2 Enfoque

Implementar una reorganización Markdown sin cambiar normas SDD ni código de
aplicación. El handoff conservará solo estado vigente y enlaces. La evidencia y
detalle histórico quedarán en archivos dedicados de `docs/` y `specs/`.

---

# 3. Requisitos cubiertos

| Requisito | Tipo | Cobertura en el plan |
|-----------|------|----------------------|
| FR-001 | Funcional | Reescribir `handoff.md` como estado vivo menor a 200 líneas. |
| FR-002 | Funcional | Mantener estado final, next IDs y rutas a evidencia. |
| FR-003 | Funcional | Incluir SPEC-002 `VALIDATED`, `AGENTS.md` compacto y guías. |
| FR-004 | Funcional | Crear `docs/quickstart.md` e índice documental. |
| FR-005 | Funcional | Documentar evidencia dedicada y handoff como enlace/resumen. |
| NFR-001 | No funcional | Verificar línea total de `handoff.md`. |
| NFR-002 | No funcional | Mover o enlazar detalle histórico sin borrar evidencia. |
| SEC-001 | Seguridad | Revisar que no se introduzcan secretos. |
| BR-001 | Regla | Handoff resume estado, no revalida históricamente. |
| BR-002 | Regla | Evidencia histórica permanece consultable. |

---

# 4. Contexto técnico existente

## Stack actual

- Lenguaje: Markdown para Harness; Python solo para la feature de ejemplo.
- Framework: Ninguno.
- Base de datos: Ninguna.
- Runtime: Python 3.12 para regresión existente.
- Package manager: Ninguno.
- Testing: `unittest` y verificaciones documentales.

## Componentes existentes relacionados

- `handoff.md`: 2406 líneas, mezcla estado vivo e historial de auditoría.
- `README.md`: 1280 líneas, documentación general extensa.
- `AGENTS.md`: 166 líneas, índice operativo validado en SPEC-002.
- `docs/agents/`: guías de subagentes y hooks.
- `specs/001-audit-task-management/`: evidencia de feature auditada.
- `specs/002-agent-operating-readiness/`: evidencia de compactación operativa.

## Restricciones técnicas existentes

- No modificar `src/` ni `tests/`.
- No borrar evidencia histórica.
- No cambiar normas SDD.
- No introducir dependencias.

---

# 5. Decisiones técnicas

## DEC-001 — Handoff como estado vivo

**Decisión:**

Reescribir `handoff.md` como documento breve de estado vigente con enlaces a
evidencia, no como historial completo.

**Justificación:**

Cumple FR-001, FR-002, NFR-001 y BR-001 reduciendo contexto sin fabricar nuevos
PASS.

**Requisitos relacionados:**

- FR-001
- FR-002
- NFR-001
- BR-001

**Alternativas consideradas:**

1. Mantener handoff completo.
2. Borrar historial sin mover/enlazar evidencia.
3. Convertir handoff en estado vivo y mover/enlazar detalle.

**Consecuencias:**

- Bootstrap más ligero.
- El detalle histórico se consulta bajo demanda.

**Requiere ADR:** NO

---

## DEC-002 — Detalle largo bajo docs

**Decisión:**

Crear documentación bajo `docs/` para contexto histórico, quickstart e índice,
manteniendo handoff mínimo.

**Justificación:**

Cumple FR-004, FR-005, NFR-002 y BR-002 separando estado vivo de evidencia
histórica.

**Requisitos relacionados:**

- FR-004
- FR-005
- NFR-002
- BR-002

**Alternativas consideradas:**

1. Dejar detalle largo en README.
2. Crear múltiples documentos sin índice.
3. Crear quickstart, índice y archivo histórico enlazado.

**Consecuencias:**

- Mejora navegación y reduce lecturas innecesarias.
- Requiere validar que rutas principales existan.

**Requiere ADR:** NO

---

# 6. Arquitectura propuesta

## 6.1 Componentes involucrados

| Componente | Responsabilidad | Cambio |
|------------|-----------------|--------|
| `handoff.md` | Estado vivo actual | MODIFY |
| `docs/quickstart.md` | Entrada breve para humanos/agentes | CREATE |
| `docs/index.md` | Índice de lectura y rutas de evidencia | CREATE |
| `docs/audit-history.md` | Resumen histórico compacto de audits ya cerrados | CREATE |
| `specs/003-context-window-optimization/` | Artefactos SDD y evidencia | CREATE/MODIFY |
| `README.md` | Documentación general existente | REUSE |
| `AGENTS.md` | Índice operativo validado | REUSE |

## 6.2 Flujo principal

Nuevo agente o humano
  ↓
Lee `AGENTS.md`
  ↓
Lee `handoff.md` para estado vivo
  ↓
Usa `docs/quickstart.md` y `docs/index.md`
  ↓
Consulta evidencia histórica solo si aplica

## 6.3 Dependencias entre componentes

`handoff.md` enlaza a `docs/index.md`, `docs/quickstart.md`, specs validadas y
evidencia. `docs/index.md` enlaza a rutas largas.

---

# 7. Modelo de datos

No aplica. No hay persistencia ni migraciones.

---

# 8. Interfaces y contratos

Contratos documentales:

| Contrato | Propósito | Requisitos |
|----------|-----------|------------|
| Handoff vivo | Estado vigente y enlaces | FR-001, FR-002, FR-003 |
| Quickstart | Lectura mínima inicial | FR-004 |
| Índice documental | Qué leer primero y bajo demanda | FR-004, FR-005 |
| Audit history compacto | Referencia histórica sin cargar todo el contexto | NFR-002, BR-002 |

---

# 9. Validación de entradas

Entradas: documentación existente, estado validado de specs y Git. Se validará
mediante rutas existentes, conteo de líneas, búsqueda textual y regresión.

---

# 10. Seguridad

## Requisitos relacionados

- SEC-001

## Autenticación

No aplica.

## Autorización

No aplica fuera de approval gates SDD ya usados.

## Datos sensibles

No se espera manejar datos sensibles.

## Secretos

No se deben introducir secretos; ejecutar revisión textual de patrones.

## Riesgos relevantes

| Riesgo | Mitigación |
|--------|------------|
| Mover detalle elimina rutas útiles | Crear `docs/index.md` y validar enlaces/rutas clave. |
| Handoff compacto omite estado vigente | TEST documental contra AC-002/AC-003. |
| Documento nuevo introduce secretos por copia | Revisión textual de patrones sensibles. |

---

# 11. Estrategia de pruebas

## Documentales

- Conteo de líneas de `handoff.md`.
- Revisión de ausencia de cuerpos detallados de AUDIT-01 a AUDIT-10.
- Revisión de presencia de estado vigente y SPEC-002.
- Revisión de quickstart, índice y evidencia dedicada.

## Seguridad

- Búsqueda de patrones sensibles en archivos creados/modificados.

## Regresión

- Ejecutar `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest discover -s tests -v`.

## 11.1 Mapeo inicial

| Criterio | Tipo de prueba previsto |
|----------|-------------------------|
| AC-001 | Documental / conteo |
| AC-002 | Documental / revisión de estado |
| AC-003 | Documental / revisión de SPEC-002 |
| AC-004 | Documental / navegación |
| AC-005 | Seguridad / trazabilidad |
| AC-006 | Documental / evidencia dedicada |

---

# 12. Observabilidad

## Métricas

- Líneas de `handoff.md`.
- Archivos de documentación creados.
- Resultado de regresión.

## Auditoría

- Evidencia en `specs/003-context-window-optimization/evidence/`.

---

# 13. Impacto en el repositorio

## Archivos o módulos a crear

- `docs/quickstart.md`
- `docs/index.md`
- `docs/audit-history.md`
- `specs/003-context-window-optimization/evidence/implementation.md`

## Archivos o módulos a modificar

- `handoff.md`
- `specs/003-context-window-optimization/spec.md`
- `specs/003-context-window-optimization/tasks.md` cuando exista
- `specs/003-context-window-optimization/validation.md` durante validación

## Elementos a reutilizar

- `README.md`
- `AGENTS.md`
- `docs/agents/hooks.md`
- `docs/agents/subagents.md`
- `specs/001-audit-task-management/`
- `specs/002-agent-operating-readiness/`

## Elementos a eliminar

Ninguno.

---

# 14. Dependencias

Ninguna dependencia nueva.

---

# 15. Configuración

No se requiere configuración.

---

# 16. Migración y compatibilidad

No hay migración de datos ni breaking changes de aplicación.

## Breaking changes

**¿Existen?:** NO

---

# 17. Manejo de errores

| Escenario | Comportamiento esperado |
|-----------|-------------------------|
| `handoff.md` queda en 200 líneas o más | Corregir antes de cerrar TASKS. |
| Se pierde ruta de evidencia obligatoria | Corregir handoff/índice antes de validar. |
| Regresión de tests existentes | Investigar y corregir antes de PASS. |
| Se detecta secreto | Removerlo y repetir revisión. |

---

# 18. Riesgos técnicos

## RISK-001 — Pérdida de contexto histórico útil

**Descripción:**

Al compactar `handoff.md`, puede omitirse información necesaria para futuras
auditorías.

**Impacto:** MEDIUM

**Probabilidad:** MEDIUM

**Mitigación:**

Crear `docs/audit-history.md` y enlaces a specs/validaciones/evidencia.

---

## RISK-002 — Duplicación entre README y docs

**Descripción:**

Crear docs nuevos puede duplicar partes del README.

**Impacto:** LOW

**Probabilidad:** MEDIUM

**Mitigación:**

Mantener docs nuevos como índices operativos y dejar README como documentación
general.

---

# 19. Aclaraciones técnicas

No existen aclaraciones técnicas bloqueantes.

---

# 20. ADR requeridos

Ninguno.

---

# 21. Orden de implementación

1. Crear docs de quickstart, índice e historia compacta.
2. Reescribir `handoff.md` como estado vivo.
3. Registrar evidencia dedicada de SPEC-003.
4. Ejecutar verificaciones documentales y regresión.
5. Validar la feature.

---

# 22. Criterios para avanzar a Tasks

- [x] La SPEC asociada está `APPROVED`.
- [x] Todos los requisitos MUST tienen cobertura técnica.
- [x] La arquitectura necesaria está definida.
- [x] Los componentes afectados están identificados.
- [x] El modelo de datos está definido cuando corresponde.
- [x] Los contratos están definidos cuando corresponde.
- [x] La estrategia de seguridad está definida.
- [x] La estrategia de pruebas está definida.
- [x] Los cambios de repositorio están identificados.
- [x] Las dependencias nuevas están justificadas.
- [x] Los breaking changes están identificados.
- [x] Los riesgos técnicos relevantes están documentados.
- [x] Los ADR necesarios están identificados.
- [x] No existen `[NEEDS CLARIFICATION]` bloqueantes.

---

# 23. Estado del plan

Estados permitidos:

DRAFT
→ IN_REVIEW
→ APPROVED
→ SUPERSEDED

**Estado actual:**

APPROVED

## Aprobación

La transición a `APPROVED` requiere aprobación humana explícita.

**Aprobado por:**

Usuario, mediante respuesta "Aprobado" en conversación del 2026-09-30.

**Fecha de aprobación:**

2026-09-30
