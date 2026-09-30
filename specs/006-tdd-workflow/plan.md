# Plan Técnico: TDD en el flujo SDD

**ID:** PLAN-006
**SPEC relacionada:** SPEC-006
**Estado:** APPROVED
**Versión:** 0.1.0
**Fecha:** 2026-09-30

---

# 1. Precondiciones

- [x] SPEC-006 existe y está APPROVED por el usuario.
- [x] Q-001 está [CLARIFIED]; no hay aclaraciones bloqueantes.
- [x] Todos los requisitos MUST tienen criterios de aceptación.
- [x] Alcance, restricciones y excepciones están definidos.

# 2. Resumen técnico

## 2.1 Objetivo

Hacer exigible TDD para cambios de comportamiento automatizable en futuras
features, conservando el flujo SDD y su evidencia por tarea.

## 2.2 Enfoque

Extender los documentos de proceso existentes y crear una guía operativa corta.
La política se expresa una vez en el estándar de testing; commands y templates
la aplican en cada fase mediante enlaces y campos mínimos.

# 3. Requisitos cubiertos

| Requisito | Cobertura técnica |
|-----------|-------------------|
| FR-001 | Regla obligatoria y ámbito en testing standard; referencia en AGENTS. |
| FR-002 | PLAN y TASKS preparan casos trazables sin modificar código antes de /implement. |
| FR-003 | /implement exige RED → GREEN → REFACTOR para comportamiento automatizable. |
| FR-004 | /implement registra evidencia; /validate y templates comprueban RED, GREEN o excepción. |
| FR-005 | Guía stack agnostic enlazada desde adopción e índice. |
| NFR-001 | AGENTS bajo 200 líneas; handoff sin historial nuevo. |
| BR-001, BR-002 | Gates SDD preservados; excepciones acotadas y bloqueos por entorno. |

# 4. Contexto técnico existente

- Harness documental: `.spec/constitution.md`, cuatro standards, seis commands
  y cuatro templates.
- `.spec/commands/implement.md` §8 dice que TDD no es obligatorio; este texto
  deberá sustituirse por la nueva regla aprobada.
- PLAN ya define estrategia de pruebas; TASKS ya asigna TEST IDs; VALIDATE ya
  revisa evidencia, pero ninguno exige demostrar RED antes de código.
- `AGENTS.md` tiene menos de 200 líneas y sirve como índice compacto.
- `docs/adoption.md` y `docs/index.md` son puntos de entrada; `handoff.md` es
  estado vivo.
- El repositorio contiene un espécimen Python con `unittest`; no hay motor
  automático de gates ni framework TDD propio.

# 5. Decisiones técnicas

## DEC-001 — Regla autoritativa en testing standard

**Decisión:** Añadir una sección TDD a `.spec/standards/testing.md` que defina
ámbito, RED válido, GREEN, refactor, bloqueos y excepciones.

**Justificación:** FR-001 y BR-002 requieren una fuente común aplicable a
proyectos de distintos stacks.

**Requisitos relacionados:** FR-001, FR-003, FR-004, BR-002.

**Alternativas consideradas:** Poner toda la norma en AGENTS o repetirla en
cada command.

**Consecuencias:** Los commands podrán enlazar la regla y precisar su fase.

**Requiere ADR:** NO.

## DEC-002 — Integración por fases

**Decisión:** Ajustar `/plan` para declarar casos y viabilidad TDD; `/tasks`
para ligar pruebas a tareas; `/implement` para exigir y registrar RED/GREEN;
`/validate` para comprobar evidencia y bloquear PASS injustificado.

**Justificación:** FR-002 a FR-004 y BR-001 requieren orden temporal explícito.

**Requisitos relacionados:** FR-002, FR-003, FR-004, BR-001.

**Alternativas consideradas:** Una guía aislada sin cambios en commands.

**Consecuencias:** Los gates siguen siendo SDD; TDD ocurre dentro de
`/implement`.

**Requiere ADR:** NO.

## DEC-003 — Templates mínimos y evidencia local

**Decisión:** Agregar campos cortos a los templates de PLAN, TASKS y VALIDATE:
aplicabilidad TDD, casos previstos, referencia RED/GREEN y razón/verificación
alternativa cuando no aplica. La evidencia detallada queda bajo
`specs/<feature-id>/evidence/`.

**Justificación:** El agente debe producir artefactos verificables sin
sobrecargar cada documento.

**Requisitos relacionados:** FR-002, FR-004, NFR-001.

**Alternativas consideradas:** Copiar logs completos en PLAN, TASKS y VALIDATE.

**Consecuencias:** El validador accede a evidencia concreta por enlace.

**Requiere ADR:** NO.

## DEC-004 — Guía de adopción breve

**Decisión:** Crear `docs/tdd.md`, enlazarla desde `docs/adoption.md` y
`docs/index.md`, y añadir una línea en `AGENTS.md` que apunte al estándar.

**Justificación:** FR-005 y NFR-001 requieren descubrimiento rápido con contexto
acotado.

**Requisitos relacionados:** FR-001, FR-005, NFR-001.

**Alternativas consideradas:** Extender AGENTS o el README con un tutorial.

**Consecuencias:** La guía se lee bajo demanda.

**Requiere ADR:** NO.

# 6. Arquitectura propuesta

| Componente | Responsabilidad | Cambio |
|------------|-----------------|--------|
| `.spec/standards/testing.md` | Política TDD | MODIFY |
| `.spec/commands/plan.md` | Estrategia TDD por criterio | MODIFY |
| `.spec/commands/tasks.md` | Casos y secuencia por tarea | MODIFY |
| `.spec/commands/implement.md` | Ciclo RED/GREEN y evidencia | MODIFY |
| `.spec/commands/validate.md` | Gate de evidencia TDD | MODIFY |
| `.spec/templates/plan.template.md` | Campo de estrategia | MODIFY |
| `.spec/templates/tasks.template.md` | Campo y DoD TDD | MODIFY |
| `.spec/templates/validation.template.md` | Campo de verificación | MODIFY |
| `docs/tdd.md` | Ejemplo operativo y excepciones | CREATE |
| `docs/adoption.md`, `docs/index.md`, `AGENTS.md` | Navegación breve | MODIFY |
| `.spec/constitution.md`, `handoff.md` | Autoridad SDD y estado vivo | REUSE |

Flujo: SPEC aprobada → PLAN define casos → TASKS los asigna → `/implement`
registra RED antes del cambio productivo, luego GREEN y refactor si procede →
`/validate` verifica evidencia o excepción válida.

# 7. Modelo de datos

No aplica. No hay persistencia, migración ni cambios destructivos.

# 8. Interfaces y contratos

No hay API. El contrato documental será: cada tarea aplicable enlaza prueba,
resultado RED atribuible al comportamiento faltante y GREEN; cuando no aplica,
se registra motivo y verificación alternativa. Los resultados se conservan en
la evidencia de la feature.

# 9. Validación de entradas

No hay entradas de aplicación. Las rutas y referencias de evidencia deben
apuntar a archivos existentes y no contener secretos.

# 10. Seguridad

No se introducen credenciales ni controles nuevos. Los ejemplos y la evidencia
no deben imprimir secretos o datos personales reales. Las fallas por entorno
quedan BLOCKED y no se presentan como RED válido.

# 11. Estrategia de pruebas

| Criterio | Verificación prevista |
|----------|-----------------------|
| AC-001 | Revisión de consistencia entre estándar, commands y AGENTS. |
| AC-002 | Ejercicio documental de trazabilidad PLAN → TASKS → /implement y gate previo. |
| AC-003 | Ejercicio con comportamiento automatizable que distinga falla esperada de error de entorno y compruebe GREEN. |
| AC-004 | Ejercicio de excepción válida y caso de entorno bloqueado en /validate. |
| AC-005 | Enlaces, guía stack agnostic y conteo de líneas de AGENTS. |

Las verificaciones de esta feature son documentales; no se modifica el
espécimen Python. Ejecutar regresión del Harness si una regla o template afecta
la interpretación de evidencia de SPEC-001.

# 12. Observabilidad

No aplica. La evidencia se registrará en `specs/006-tdd-workflow/evidence/`.

# 13. Impacto en el repositorio

- CREATE: `docs/tdd.md`, evidencia y validación de SPEC-006.
- MODIFY: estándar de testing, cuatro commands, tres templates, AGENTS,
  adopción e índice.
- REUSE: Constitución, handoff y feature representativa.
- REMOVE: ninguno.

# 14. Dependencias

Ninguna dependencia de software nueva.

# 15. Configuración

Ninguna variable o configuración nueva.

# 16. Migración y compatibilidad

Política prospectiva para features nuevas; evidencia histórica no se reescribe.
No hay cambios de API, datos o configuración. El cambio de proceso obliga TDD
en futuras implementaciones aplicables, conforme a SPEC-006 aprobada.

# 17. Manejo de errores

- RED por falla de test/infraestructura no esperada: identificar causa y no
  registrar como RED válido.
- Test ya GREEN antes del cambio: revisar caso, sin fabricar un fallo.
- Entorno indisponible: TASK BLOCKED; no usar excepción para declarar PASS.
- Trabajo no automatizable: documentar motivo y verificación alternativa.

# 18. Riesgos técnicos

## RISK-001 — Inconsistencia entre documentos

**Impacto:** MEDIUM. **Probabilidad:** MEDIUM.
**Mitigación:** Buscar afirmaciones opuestas a TDD y revisar commands,
templates y guía en una sola verificación de consistencia.

## RISK-002 — Evidencia RED artificial

**Impacto:** HIGH. **Probabilidad:** LOW.
**Mitigación:** Exigir causa de fallo vinculada al comportamiento faltante;
rechazar fallas de entorno y no inventar logs históricos.

# 19. Aclaraciones técnicas

Ninguna bloqueante.

# 20. ADR requeridos

Ninguno: cambia el proceso documentado, no la arquitectura del software.

# 21. Orden de implementación

1. Política TDD en testing standard y guía operativa.
2. Integración de commands por fase.
3. Campos mínimos en templates.
4. Enlaces desde adopción, índice y AGENTS.
5. Verificación transversal, evidencia y validación final.

# 22. Criterios para avanzar a Tasks

- [x] SPEC aprobada y requisitos MUST cubiertos.
- [x] Componentes, pruebas, seguridad, riesgos e impacto identificados.
- [x] No hay dependencias, ADR ni aclaraciones bloqueantes.
- [x] Aprobación humana explícita del PLAN.

# 23. Estado del plan

**Estado actual:** APPROVED
**Aprobado por:** usuario en esta conversación
**Fecha de aprobación:** 2026-09-30
