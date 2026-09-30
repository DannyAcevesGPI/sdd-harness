# Plan Técnico: Preparación operativa para agentes, subagentes y hooks

**ID:** PLAN-002
**SPEC relacionada:** SPEC-002
**Estado:** APPROVED
**Versión:** 0.1.0
**Fecha:** 2026-09-30

---

# 1. Precondiciones

Antes de generar este plan se verificó:

- [x] Existe una SPEC asociada: `specs/002-agent-operating-readiness/spec.md`.
- [x] La SPEC se encuentra en estado `APPROVED`.
- [x] No existen `[NEEDS CLARIFICATION]` bloqueantes.
- [x] Los requisitos MUST tienen criterios de aceptación.
- [x] El alcance está claramente definido.
- [x] Las restricciones relevantes están documentadas.

---

# 2. Resumen técnico

## 2.1 Objetivo

Preparar una actualización documental del Harness para que `AGENTS.md` sea un
índice operativo compacto de menos de 200 líneas y para que existan reglas
explícitas de uso de subagentes y hooks compatibles con SDD.

## 2.2 Enfoque

La implementación deberá reducir duplicación normativa en `AGENTS.md`, conservar
solo el bootstrap y reglas operativas mínimas, y remitir a Constitución,
standards, commands y artefactos SDD como fuentes autoritativas. La preparación
de subagentes y hooks se resolverá inicialmente como documentación operativa y
contratos de uso, sin crear automatización ejecutable ni dependencias externas.

---

# 3. Requisitos cubiertos

| Requisito | Tipo | Cobertura en el plan |
|-----------|------|----------------------|
| FR-001 | Funcional | `AGENTS.md` se compactará por debajo de 200 líneas. |
| FR-002 | Funcional | El bootstrap SDD y el mutation boundary permanecerán explícitos. |
| FR-003 | Funcional | Se documentarán límites de delegación a subagentes y responsabilidad del agente principal. |
| FR-004 | Funcional | Se documentarán hooks como apoyo verificable, no como autoridad ni validación final. |
| NFR-001 | No funcional | Se reducirá duplicación con fuentes superiores mediante referencias. |
| NFR-002 | No funcional | Se preservará compatibilidad con Harness 1.0.0 STABLE. |
| SEC-001 | Seguridad | Las reglas de hooks prohibirán secretos en código, logs, evidencia y documentación. |
| SEC-002 | Seguridad | Las reglas de subagentes impedirán transferir aprobaciones humanas. |
| BR-001 | Regla | `AGENTS.md` resumirá sin sustituir fuentes superiores. |
| BR-002 | Regla | La responsabilidad final permanecerá en el agente principal. |

Todo requisito MUST queda cubierto.

---

# 4. Contexto técnico existente

## Stack actual

- Lenguaje: Python para la feature de ejemplo existente; Markdown para Harness.
- Framework: Ninguno.
- Base de datos: Ninguna.
- Runtime: Python 3.12 para pruebas de la feature existente.
- Package manager: Ninguno configurado.
- Testing: `unittest` con `PYTHONPATH=src`.

## Componentes existentes relacionados

- `AGENTS.md`: instrucciones operativas actuales, 935 líneas.
- `.spec/constitution.md`: fuente normativa superior interna.
- `.spec/commands/`: procedimientos SDD por fase.
- `.spec/standards/`: arquitectura, código, testing y seguridad.
- `handoff.md`: estado de auditoría y baseline estable.
- `README.md`: documentación general del Harness.

## Restricciones técnicas existentes

- No hay herramienta de hooks configurada.
- No hay directorio de subagentes existente.
- No hay ADR existentes ni carpeta `docs/decisions/` materializada.
- La preparación no debe modificar `src/`, `tests/` ni la feature validada
  `001-audit-task-management`.

---

# 5. Decisiones técnicas

## DEC-001 — Convertir AGENTS.md en índice operativo compacto

**Decisión:**

Reescribir `AGENTS.md` como documento compacto de menos de 200 líneas que
mantenga el bootstrap obligatorio, ruteo por intención, gates, mutation boundary,
trazabilidad, delegación y hooks en forma resumida.

**Justificación:**

Satisface FR-001 y NFR-001 reduciendo duplicación, mientras FR-002 y BR-001 se
preservan mediante referencias explícitas a fuentes autoritativas.

**Requisitos relacionados:**

- FR-001
- FR-002
- NFR-001
- BR-001

**Alternativas consideradas:**

1. Mantener `AGENTS.md` completo y agregar apéndices.
2. Dividir `AGENTS.md` en muchos archivos sin índice compacto.
3. Reescribirlo como índice operativo compacto.

**Consecuencias:**

- Reduce carga de contexto para agentes.
- Requiere validar que no se pierdan reglas obligatorias.
- Las reglas completas deberán seguir leyéndose desde sus fuentes superiores.

**Requiere ADR:** NO

---

## DEC-002 — Documentar subagentes como protocolo de delegación

**Decisión:**

Crear una guía documental para subagentes que defina alcance, fuentes, límites,
evidencia esperada y prohibición de aprobación delegada.

**Justificación:**

Satisface FR-003, SEC-002 y BR-002 sin introducir una plataforma de ejecución ni
dependencias prematuras.

**Requisitos relacionados:**

- FR-003
- SEC-002
- BR-002

**Alternativas consideradas:**

1. No documentar subagentes hasta tener herramienta concreta.
2. Crear configuración ejecutable de subagentes ahora.
3. Crear protocolo documental independiente y referenciarlo desde `AGENTS.md`.

**Consecuencias:**

- Permite uso seguro de subagentes por convención del Harness.
- La implementación futura de herramientas podrá derivar de esta guía.

**Requiere ADR:** NO

---

## DEC-003 — Documentar hooks como contrato preparatorio

**Decisión:**

Crear una guía documental para hooks que defina categorías recomendadas,
controles de seguridad, límites de autoridad y evidencia esperada, sin crear
hooks ejecutables en esta feature.

**Justificación:**

Q-002 permanece no bloqueante, y esta decisión mantiene el alcance inicial en
instrucciones/documentación, suficiente para FR-004 y SEC-001 sin inventar una
herramienta específica.

**Requisitos relacionados:**

- FR-004
- SEC-001
- NFR-002

**Alternativas consideradas:**

1. Crear hooks reales de Git.
2. Crear configuración de una herramienta no especificada.
3. Documentar contrato preparatorio y postergar automatización.

**Consecuencias:**

- Evita automatización especulativa.
- Deja preparada una base verificable para tareas futuras.

**Requiere ADR:** NO

---

# 6. Arquitectura propuesta

## 6.1 Componentes involucrados

| Componente | Responsabilidad | Cambio |
|------------|-----------------|--------|
| `AGENTS.md` | Índice operativo compacto para agentes | MODIFY |
| `docs/agents/subagents.md` | Protocolo de delegación a subagentes | CREATE |
| `docs/agents/hooks.md` | Contrato preparatorio de hooks | CREATE |
| `.spec/constitution.md` | Fuente normativa superior | REUSE |
| `.spec/commands/` | Procedimientos por fase SDD | REUSE |
| `.spec/standards/` | Reglas de arquitectura, código, pruebas y seguridad | REUSE |
| `handoff.md` | Estado estable y límites auditados | REUSE |

## 6.2 Flujo principal

Agente inicia trabajo
  ↓
Lee `AGENTS.md` compacto
  ↓
Lee `.spec/constitution.md`
  ↓
Detecta feature, fase, artefactos, command y standards
  ↓
Si delega, usa `docs/agents/subagents.md`
  ↓
Si evalúa automatización, usa `docs/agents/hooks.md`
  ↓
Ejecuta el command SDD aplicable y registra evidencia

## 6.3 Dependencias entre componentes

`AGENTS.md`
  ↓
`.spec/constitution.md`
  ↓
`.spec/commands/` y `.spec/standards/`
  ↓
`docs/agents/subagents.md` / `docs/agents/hooks.md`

No se introducen dependencias circulares ni dependencias ejecutables.

---

# 7. Modelo de datos

No aplica. La feature no introduce persistencia, entidades de dominio, schemas,
migraciones ni datos almacenados.

## 7.4 Migraciones

**¿Requiere migración?:** NO

Cambios destructivos: NO

---

# 8. Interfaces y contratos

No hay API, endpoint ni contrato de aplicación.

Contratos documentales internos:

| Contrato | Propósito | Requisitos |
|----------|-----------|------------|
| Bootstrap de `AGENTS.md` | Obligar lectura y ruteo SDD mínimo | FR-002, BR-001 |
| Protocolo de subagentes | Definir delegación acotada y evidencia | FR-003, SEC-002, BR-002 |
| Contrato de hooks | Definir límites de automatización futura | FR-004, SEC-001 |

---

# 9. Validación de entradas

Entradas relevantes:

- Solicitudes humanas sobre cambios al Harness.
- Instrucciones delegadas a subagentes.
- Resultados o salidas de hooks futuros.

Validación:

- `AGENTS.md` deberá instruir revisar Constitución y artefactos antes de actuar.
- Las delegaciones deberán incluir alcance, fuentes y límites de mutación.
- Los hooks futuros deberán tratar entradas externas como no confiables y no
  exponer secretos.

---

# 10. Seguridad

## Requisitos relacionados

- SEC-001
- SEC-002

## Autenticación

No aplica autenticación de aplicación. La autoridad humana se registra en
artefactos SDD cuando corresponda.

## Autorización

Subagentes y hooks no podrán aprobar SPEC, PLAN o TASKS ni sustituir decisiones
humanas. El agente principal deberá verificar gates antes de ejecutar trabajo
dependiente.

## Datos sensibles

No se espera manejar datos sensibles. Las guías deberán prohibir incluir secretos,
tokens o credenciales en documentación, comandos, logs o evidencia.

## Secretos

No se requieren secretos. Si un hook futuro necesita credenciales, deberán
suministrarse por mecanismos seguros del entorno y quedar fuera del repositorio.

## Riesgos relevantes

| Riesgo | Mitigación |
|--------|------------|
| Hook registra secretos accidentalmente | Guía de hooks con prohibición explícita y revisión de seguridad. |
| Subagente omite gates | Protocolo de delegación mantiene responsabilidad en agente principal. |
| `AGENTS.md` compacto pierde reglas | Validación documental contra Constitución, commands y standards. |

---

# 11. Estrategia de pruebas

## Documentales

- Conteo de líneas de `AGENTS.md`.
- Revisión de presencia de bootstrap obligatorio.
- Revisión de referencias a fuentes autoritativas.
- Revisión de guías de subagentes y hooks.

## Seguridad

- Revisión textual para confirmar prohibición de secretos.
- Revisión textual para confirmar que subagentes/hooks no aprueban gates.

## Regresión

- Ejecutar la suite existente con `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src
  python3 -m unittest discover -s tests -v` para comprobar que la feature
  validada no fue afectada.

## 11.1 Mapeo inicial

| Criterio | Tipo de prueba previsto |
|----------|-------------------------|
| AC-001 | Documental / conteo |
| AC-002 | Documental / revisión de bootstrap |
| AC-003 | Documental / seguridad de delegación |
| AC-004 | Documental / seguridad de hooks |
| AC-005 | Documental / consistencia normativa |

Los IDs concretos `TEST-XXX` se asignarán durante Tasks.

---

# 12. Observabilidad

## Logs

No se agregan logs de aplicación.

## Métricas

- Líneas totales de `AGENTS.md`.
- Resultado de pruebas existentes.

## Auditoría

- Evidencia documental de revisión de consistencia.
- Evidencia de conteo de líneas.
- Evidencia de pruebas de regresión.

## Health checks

No aplica.

---

# 13. Impacto en el repositorio

## Archivos o módulos a crear

- `docs/agents/subagents.md`
- `docs/agents/hooks.md`

## Archivos o módulos a modificar

- `AGENTS.md`

## Elementos a reutilizar

- `.spec/constitution.md`
- `.spec/commands/`
- `.spec/standards/`
- `handoff.md`
- `README.md`
- `specs/002-agent-operating-readiness/spec.md`

## Elementos a eliminar

Ninguno.

---

# 14. Dependencias

## Nuevas dependencias

Ninguna.

---

# 15. Configuración

Variables o configuración requerida:

Ninguna.

---

# 16. Migración y compatibilidad

No hay cambios de API, schemas, base de datos, configuración ejecutable ni datos.

## Breaking changes

**¿Existen?:** NO

---

# 17. Manejo de errores

| Escenario | Comportamiento esperado |
|-----------|-------------------------|
| `AGENTS.md` queda en 200 líneas o más | No cerrar TASKS; corregir compactación antes de validar. |
| Se detecta contradicción con fuente superior | Detener implementación, corregir el artefacto propietario y recuperar gates si aplica. |
| Hook futuro requiere secreto | No documentar secreto; exigir mecanismo seguro externo al repositorio. |
| Subagente reporta conclusión sin evidencia | El agente principal no debe usarla como evidencia suficiente. |

---

# 18. Riesgos técnicos

## RISK-001 — Pérdida de reglas por compactación

**Descripción:**

Al reducir `AGENTS.md`, una regla obligatoria podría omitirse o formularse de
forma ambigua.

**Impacto:** HIGH

**Probabilidad:** MEDIUM

**Mitigación:**

Mantener `AGENTS.md` como índice con referencias explícitas y validar contra
Constitución, commands y standards.

---

## RISK-002 — Automatización especulativa de hooks

**Descripción:**

Crear hooks ejecutables sin herramienta o alcance aprobado podría introducir
dependencias, falsos PASS o fricción operativa.

**Impacto:** MEDIUM

**Probabilidad:** MEDIUM

**Mitigación:**

Limitar esta feature a guía documental y dejar hooks ejecutables para una SPEC o
PLAN futuro si se solicita.

---

# 19. Aclaraciones técnicas

No existen aclaraciones técnicas bloqueantes.

## Q-TECH-001 — Alcance técnico inicial de hooks

**Estado:** [CLARIFIED]

**Pregunta:**

¿Debe esta feature crear hooks ejecutables?

**Impacto:**

Afecta archivos a crear, dependencias y configuración.

**Bloqueante:** NO

**Respuesta:**

No. El alcance inicial será documental porque la SPEC no define herramienta ni
tipo de hook concreto, y Q-002 era no bloqueante.

---

# 20. ADR requeridos

Ninguno.

---

# 21. Orden de implementación

1. Reescribir `AGENTS.md` como índice operativo de menos de 200 líneas.
2. Crear guía de subagentes.
3. Crear guía de hooks.
4. Ejecutar verificaciones documentales y conteo de líneas.
5. Ejecutar regresión existente.
6. Registrar evidencia en TASKS y preparar validación.

---

# 22. Criterios para avanzar a Tasks

El plan podrá avanzar a `tasks.md` cuando:

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

Los agentes pueden preparar y revisar el PLAN, pero no podrán autoaprobarlo.

**Aprobado por:**

Usuario, mediante respuesta "Apruebo ese plan" en conversación del 2026-09-30.

**Fecha de aprobación:**

2026-09-30

No deberá generarse implementación a partir de un plan que no haya sido aprobado.
