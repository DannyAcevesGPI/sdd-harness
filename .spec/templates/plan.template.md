# Plan Técnico: [Nombre de la funcionalidad]

**ID:** PLAN-[XXX]  
**SPEC relacionada:** SPEC-[XXX]  
**Estado:** DRAFT  
**Versión:** 0.1.0  
**Fecha:** [YYYY-MM-DD]

---

# 1. Precondiciones

Antes de generar este plan deberá verificarse:

- [ ] Existe una SPEC asociada.
- [ ] La SPEC se encuentra en estado `APPROVED`.
- [ ] No existen `[NEEDS CLARIFICATION]` bloqueantes.
- [ ] Los requisitos MUST tienen criterios de aceptación.
- [ ] El alcance está claramente definido.
- [ ] Las restricciones relevantes están documentadas.

Si alguna precondición obligatoria no se cumple:

**PLANNING STATUS: BLOCKED**

Este resultado corresponde a la operación de planificación, no al estado
del documento PLAN. `BLOCKED` no es un estado de su ciclo de vida.

No deberá continuarse con decisiones técnicas que dependan
de información faltante.

---

# 2. Resumen técnico

## 2.1 Objetivo

[Describir brevemente qué se construirá desde una perspectiva técnica.]

## 2.2 Enfoque

[Describir la estrategia general de implementación.]

Ejemplo:

La funcionalidad se implementará mediante un módulo de autenticación
que expondrá operaciones a través de la API existente y utilizará
la capa de persistencia actual.

---

# 3. Requisitos cubiertos

Este plan deberá indicar explícitamente qué requisitos implementará.

| Requisito | Tipo | Cobertura en el plan |
|-----------|------|----------------------|
| FR-001 | Funcional | [Descripción] |
| FR-002 | Funcional | [Descripción] |
| NFR-001 | No funcional | [Descripción] |
| SEC-001 | Seguridad | [Descripción] |

Todo requisito MUST deberá estar cubierto.

---

# 4. Contexto técnico existente

Describir únicamente elementos relevantes del sistema actual.

## Stack actual

- Lenguaje: [valor]
- Framework: [valor]
- Base de datos: [valor]
- Runtime: [valor]
- Package manager: [valor]
- Testing: [valor]

## Componentes existentes relacionados

- [Componente]
- [Componente]

## Restricciones técnicas existentes

- [Restricción]
- [Restricción]

No deberán inventarse tecnologías que no existan o que no hayan
sido aprobadas.

---

# 5. Decisiones técnicas

## DEC-001 — [Nombre de la decisión]

**Decisión:**

[Decisión técnica.]

**Justificación:**

[Por qué esta decisión satisface los requisitos.]

**Requisitos relacionados:**

- FR-[XXX]
- NFR-[XXX]
- SEC-[XXX]

**Alternativas consideradas:**

1. [Alternativa]
2. [Alternativa]

**Consecuencias:**

- [Consecuencia positiva o negativa]
- [Trade-off]

**Requiere ADR:** [YES | NO]

Cuando `Requiere ADR` sea `YES`, deberá crearse o actualizarse
el Architecture Decision Record correspondiente.

---

# 6. Arquitectura propuesta

## 6.1 Componentes involucrados

| Componente | Responsabilidad | Cambio |
|------------|-----------------|--------|
| [Componente] | [Responsabilidad] | CREATE |
| [Componente] | [Responsabilidad] | MODIFY |
| [Componente] | [Responsabilidad] | REUSE |

Estados recomendados:

CREATE
MODIFY
REUSE
REMOVE

---

## 6.2 Flujo principal

Describir el flujo técnico principal.

Ejemplo:

Cliente
  ↓
API
  ↓
Validación
  ↓
Servicio de aplicación
  ↓
Reglas de negocio
  ↓
Repositorio
  ↓
Base de datos
  ↓
Respuesta

El flujo deberá adaptarse a la arquitectura real del proyecto.

---

## 6.3 Dependencias entre componentes

Documentar las dependencias relevantes.

Ejemplo:

TaskController
    ↓
TaskService
    ↓
TaskRepository
    ↓
Database

Se deberán evitar dependencias circulares.

---

# 7. Modelo de datos

Esta sección aplica cuando la funcionalidad requiere persistencia
o modificación de datos.

## 7.1 Entidades afectadas

### [Entidad]

Campos:

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| id | [tipo] | YES | Identificador |
| [campo] | [tipo] | YES/NO | [Descripción] |

---

## 7.2 Relaciones

[Describir relaciones relevantes.]

Ejemplo:

User
  1
  │
  N
Task

---

## 7.3 Restricciones

- [Unique]
- [Foreign key]
- [Not null]
- [Regla]

---

## 7.4 Migraciones

**¿Requiere migración?:** [YES | NO]

Si YES:

[Describir el cambio requerido.]

Cambios destructivos:

[YES | NO]

Si existe un cambio destructivo deberá documentarse una estrategia
de migración o mitigación.

---

# 8. Interfaces y contratos

Esta sección aplica cuando existen interfaces públicas o internas
relevantes.

## API / Endpoint

### [METHOD] /[path]

**Propósito:**

[Descripción.]

**Requisito relacionado:**

FR-[XXX]

### Entrada

[Schema conceptual.]

### Salida exitosa

[Resultado esperado.]

### Errores esperados

| Condición | Resultado |
|-----------|-----------|
| [Condición] | [Resultado] |
| [Condición] | [Resultado] |

---

# 9. Validación de entradas

Documentar:

- qué datos requieren validación;
- dónde se validarán;
- reglas relevantes;
- comportamiento ante datos inválidos.

Ejemplo:

Entrada HTTP
    ↓
Schema Validation
    ↓
Application

---

# 10. Seguridad

## Requisitos relacionados

- SEC-[XXX]

## Autenticación

[Cómo se aplica, si corresponde.]

## Autorización

[Cómo se verifican permisos.]

## Datos sensibles

[Qué datos requieren protección.]

## Secretos

[Cómo se gestionarán.]

## Riesgos relevantes

| Riesgo | Mitigación |
|--------|------------|
| [Riesgo] | [Control] |

Los controles deberán respetar:

.spec/standards/security.md

---

# 11. Estrategia de pruebas

Las pruebas deberán derivarse de los criterios de aceptación
y riesgos relevantes.

## Unitarias

- [Comportamiento]
- [Comportamiento]

## Integración

- [Integración]
- [Integración]

## End-to-End

- [Flujo]

## Seguridad

- [Control]

---

## 11.1 Mapeo inicial

| Criterio | Tipo de prueba previsto |
|----------|-------------------------|
| AC-001 | Unit |
| AC-002 | Integration |
| AC-003 | E2E |
| AC-004 | Security |

Los IDs concretos `TEST-XXX` podrán asignarse durante
la implementación o preparación de tareas.

## 11.2 Estrategia TDD

| Criterio | Comportamiento automatizable | Caso previsto y comando/nivel | Motivo y verificación alternativa si no aplica |
|----------|-------------------------------|-------------------------------|--------------------------------------------------|
| AC-001 | YES/NO | [Caso y comando previstos; sin ejecutar aún] | [Motivo y alternativa, si NO] |

Para comportamiento automatizable, TDD es obligatorio según
`.spec/standards/testing.md`. Preparar casos aquí no autoriza modificar código
de pruebas antes de `/implement` ni sustituye el gate de TASKS.

---

# 12. Observabilidad

Cuando corresponda:

## Logs

- [Evento relevante]

## Métricas

- [Métrica]

## Auditoría

- [Acción que requiere auditoría]

## Health checks

- [Verificación]

No deberán registrarse secretos ni información sensible
innecesariamente.

---

# 13. Impacto en el repositorio

## Archivos o módulos a crear

- [ruta o módulo]

## Archivos o módulos a modificar

- [ruta o módulo]

## Elementos a reutilizar

- [ruta, componente o servicio]

## Elementos a eliminar

- [elemento]

El listado podrá precisarse durante TASKS. Un ajuste menor de archivos
no previstos podrá documentarse en la evidencia sin modificar el PLAN
solamente si satisface todas las condiciones de la sección 7 de
`/implement`: es estrictamente necesario para la tarea, permanece dentro
del objetivo aprobado y no cambia arquitectura, requisitos, contratos
importantes ni introduce dependencias nuevas.

Si modifica el alcance o diseño aprobado, deberá detenerse el trabajo
afectado, revisarse el artefacto propietario y recuperarse los approval
gates aplicables antes de continuar.

---

# 14. Dependencias

## Nuevas dependencias

| Dependencia | Propósito | Justificación |
|-------------|-----------|---------------|
| [nombre] | [uso] | [razón] |

Si no se requieren:

Ninguna.

Las dependencias deberán cumplir con los estándares definidos
en `coding.md` y `security.md`.

---

# 15. Configuración

Variables o configuración requerida:

| Variable | Propósito | Secreto |
|----------|-----------|---------|
| [VARIABLE] | [Uso] | YES/NO |

Los valores secretos nunca deberán almacenarse en el repositorio.

---

# 16. Migración y compatibilidad

Evaluar:

- compatibilidad hacia atrás;
- cambios de API;
- cambios de schemas;
- cambios de base de datos;
- cambios de configuración;
- impacto sobre datos existentes.

## Breaking changes

**¿Existen?:** [YES | NO]

Si YES:

[Describir impacto y estrategia.]

---

# 17. Manejo de errores

| Escenario | Comportamiento esperado |
|-----------|-------------------------|
| [Error] | [Respuesta] |
| [Error] | [Respuesta] |

Los errores deberán seguir los estándares definidos en:

.spec/standards/coding.md
.spec/standards/security.md

---

# 18. Riesgos técnicos

## RISK-001 — [Nombre]

**Descripción:**

[Riesgo.]

**Impacto:** [LOW | MEDIUM | HIGH]

**Probabilidad:** [LOW | MEDIUM | HIGH]

**Mitigación:**

[Acción.]

---

# 19. Aclaraciones técnicas

Si durante la planificación aparece una decisión que no puede
resolverse utilizando la SPEC, Constitution o Standards:

[NEEDS CLARIFICATION]

## Q-TECH-001 — [Pregunta]

**Estado:** [NEEDS CLARIFICATION]

**Pregunta:**

[Pregunta.]

**Impacto:**

[Qué parte del plan depende de la respuesta.]

**Bloqueante:** [YES | NO]

**Respuesta:**

[PENDIENTE]

Las aclaraciones técnicas bloqueantes deberán resolverse antes
de generar las tareas afectadas.

---

# 20. ADR requeridos

| ADR | Decisión | Estado |
|-----|----------|--------|
| ADR-[XXX] | [Decisión] | PENDING |

Si no se requieren:

Ninguno.

---

# 21. Orden de implementación

Definir dependencias técnicas entre bloques de trabajo.

Ejemplo:

1. Modelo de datos
2. Migración
3. Repository
4. Service
5. API
6. Tests de integración
7. Validación

Este orden servirá como entrada para generar `tasks.md`.

No deberá confundirse esta sección con las tareas concretas.

---

# 22. Criterios para avanzar a Tasks

El plan podrá avanzar a `tasks.md` cuando:

- [ ] La SPEC asociada está `APPROVED`.
- [ ] Todos los requisitos MUST tienen cobertura técnica.
- [ ] La arquitectura necesaria está definida.
- [ ] Los componentes afectados están identificados.
- [ ] El modelo de datos está definido cuando corresponde.
- [ ] Los contratos están definidos cuando corresponde.
- [ ] La estrategia de seguridad está definida.
- [ ] La estrategia de pruebas está definida.
- [ ] Los cambios de repositorio están identificados.
- [ ] Las dependencias nuevas están justificadas.
- [ ] Los breaking changes están identificados.
- [ ] Los riesgos técnicos relevantes están documentados.
- [ ] Los ADR necesarios están identificados.
- [ ] No existen `[NEEDS CLARIFICATION]` bloqueantes.

---

# 23. Estado del plan

Estados permitidos:

DRAFT
→ IN_REVIEW
→ APPROVED
→ SUPERSEDED

**Estado actual:**

DRAFT

## Aprobación

La transición a `APPROVED` requiere aprobación humana explícita.

Los agentes pueden preparar y revisar el PLAN, pero no podrán
autoaprobarlo.

**Aprobado por:**

[PENDIENTE]

**Fecha de aprobación:**

[PENDIENTE]

**Decisión explícita y alcance:**

[PENDIENTE; registrar el contenido de la decisión humana]

**Registro durable:**

Registrar el evento de aprobación y su huella en
`specs/<feature-id>/decisions.json` y comprobarlo antes de generar TASKS.

No deberá generarse implementación a partir de un plan
que no haya sido aprobado.
