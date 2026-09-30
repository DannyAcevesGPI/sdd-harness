# Plan Técnico: Guía de adopción del Harness para nuevos proyectos

**ID:** PLAN-004
**SPEC relacionada:** SPEC-004
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

Crear documentación de adopción para usar el Harness en otros proyectos sin
copiar estado, evidencia o historial local de este repositorio.

## 2.2 Enfoque

Crear una guía dedicada bajo `docs/` y enlazarla de forma breve desde `README.md`
y `docs/index.md`. No se introducen scripts, instaladores ni dependencias.

---

# 3. Requisitos cubiertos

| Requisito | Tipo | Cobertura en el plan |
|-----------|------|----------------------|
| FR-001 | Funcional | Crear guía dedicada de adopción. |
| FR-002 | Funcional | Agregar referencia breve desde README. |
| FR-003 | Funcional | Documentar qué copiar y qué no copiar. |
| FR-004 | Funcional | Documentar primera feature desde cero. |
| NFR-001 | No funcional | Mantener guía bajo 250 líneas y escaneable. |
| NFR-002 | No funcional | Hacer la guía stack agnostic. |
| SEC-001 | Seguridad | Advertir sobre secretos y evidencia sensible. |
| BR-001 | Regla | Explicar que Harness es proceso, no stack. |
| BR-002 | Regla | Exigir handoff/evidencia propios por proyecto. |

---

# 4. Contexto técnico existente

## Stack actual

- Lenguaje: Markdown para documentación; Python para regresión existente.
- Framework: Ninguno.
- Base de datos: Ninguna.
- Runtime: Python 3.12 para pruebas existentes.
- Package manager: Ninguno.
- Testing: `unittest` y revisión documental.

## Componentes existentes relacionados

- `README.md`: documentación general.
- `docs/index.md`: índice documental.
- `docs/quickstart.md`: inicio rápido local.
- `AGENTS.md`: índice operativo compacto.
- `.spec/`: Harness reusable.
- `handoff.md`: estado vivo local que no debe copiarse como estado propio.

## Restricciones técnicas existentes

- No modificar código de aplicación.
- No cambiar reglas SDD.
- No crear instalador automático.

---

# 5. Decisiones técnicas

## DEC-001 — Guía dedicada bajo docs

**Decisión:**

Crear `docs/adoption.md` como guía principal de adopción.

**Justificación:**

Cumple FR-001 y NFR-001 sin inflar el README.

**Requisitos relacionados:**

- FR-001
- NFR-001

**Alternativas consideradas:**

1. Poner toda la guía en README.
2. Crear solo una nota breve sin pasos.
3. Crear guía dedicada y enlazarla.

**Consecuencias:**

- README se mantiene liviano.
- La guía puede crecer moderadamente sin cargar bootstrap.

**Requiere ADR:** NO

---

## DEC-002 — README e índice como entradas

**Decisión:**

Agregar enlaces breves a `docs/adoption.md` desde `README.md` y `docs/index.md`.

**Justificación:**

Cumple FR-002 y facilita descubrimiento sin duplicar contenido.

**Requisitos relacionados:**

- FR-002
- FR-003
- FR-004

**Alternativas consideradas:**

1. Enlazar solo desde docs.
2. Enlazar solo desde README.
3. Enlazar desde ambos con texto breve.

**Consecuencias:**

- Dos puntos naturales de entrada.
- Menor riesgo de documentación perdida.

**Requiere ADR:** NO

---

# 6. Arquitectura propuesta

## 6.1 Componentes involucrados

| Componente | Responsabilidad | Cambio |
|------------|-----------------|--------|
| `docs/adoption.md` | Guía reusable para nuevos proyectos | CREATE |
| `README.md` | Punto de descubrimiento público | MODIFY |
| `docs/index.md` | Índice operativo | MODIFY |
| `specs/004-harness-adoption-guide/` | Artefactos y evidencia SDD | CREATE/MODIFY |

## 6.2 Flujo principal

Usuario quiere adoptar Harness
  ↓
Lee README o docs index
  ↓
Abre `docs/adoption.md`
  ↓
Copia base del Harness
  ↓
Inicializa handoff/specs/evidence propios
  ↓
Ejecuta primera feature con flujo SDD

## 6.3 Dependencias entre componentes

`README.md` y `docs/index.md` enlazan a `docs/adoption.md`.

---

# 7. Modelo de datos

No aplica.

---

# 8. Interfaces y contratos

Contrato documental:

| Contrato | Propósito | Requisitos |
|----------|-----------|------------|
| Guía de adopción | Pasos para usar Harness en otro proyecto | FR-001, FR-003, FR-004 |
| Enlace README | Descubrimiento público | FR-002 |
| Enlace docs index | Descubrimiento operativo | FR-002 |

---

# 9. Validación de entradas

Entradas: documentación existente y reglas SDD actuales. Se validará mediante
revisión textual, conteo de líneas, rutas y regresión.

---

# 10. Seguridad

## Requisitos relacionados

- SEC-001

## Secretos

La guía deberá advertir que no se copien secretos, tokens, credenciales, logs
sensibles ni evidencia privada entre proyectos.

## Riesgos relevantes

| Riesgo | Mitigación |
|--------|------------|
| Usuario copia estado local como propio | Sección explícita de qué no copiar. |
| Usuario copia secretos/evidencia sensible | Advertencia SEC-001 y revisión textual. |
| Guía parece imponer stack | Sección stack agnostic. |

---

# 11. Estrategia de pruebas

## Documentales

- Verificar que `docs/adoption.md` existe y cubre pasos de adopción.
- Verificar que README enlaza la guía.
- Verificar que `docs/index.md` enlaza la guía.
- Verificar separación template/evidencia local.
- Verificar flujo de primera feature.
- Verificar portabilidad stack agnostic.

## Seguridad

- Revisión textual de secretos/patrones sensibles.

## Regresión

- Ejecutar `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest discover -s tests -v`.

## 11.1 Mapeo inicial

| Criterio | Tipo de prueba previsto |
|----------|-------------------------|
| AC-001 | Documental |
| AC-002 | Documental |
| AC-003 | Seguridad / documental |
| AC-004 | Documental |
| AC-005 | Documental |

---

# 12. Observabilidad

## Métricas

- Líneas de `docs/adoption.md`.
- Resultado de regresión.

## Auditoría

- Evidencia en `specs/004-harness-adoption-guide/evidence/`.

---

# 13. Impacto en el repositorio

## Archivos o módulos a crear

- `docs/adoption.md`
- `specs/004-harness-adoption-guide/evidence/implementation.md`

## Archivos o módulos a modificar

- `README.md`
- `docs/index.md`
- `specs/004-harness-adoption-guide/tasks.md` cuando exista
- `specs/004-harness-adoption-guide/validation.md` durante validación

## Elementos a reutilizar

- `.spec/`
- `AGENTS.md`
- `handoff.md`
- `docs/quickstart.md`
- `docs/index.md`

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

No hay migración ni breaking changes de aplicación.

## Breaking changes

**¿Existen?:** NO

---

# 17. Manejo de errores

| Escenario | Comportamiento esperado |
|-----------|-------------------------|
| Guía supera 250 líneas | Compactar antes de cerrar TASKS. |
| README duplica demasiado contenido | Reducir a enlace breve. |
| Se detecta secreto | Remover y repetir revisión. |
| Regresión falla | Investigar antes de validar. |

---

# 18. Riesgos técnicos

## RISK-001 — Guía demasiado específica del repo actual

**Impacto:** MEDIUM

**Probabilidad:** MEDIUM

**Mitigación:**

Separar base reusable de estado/evidencia local.

## RISK-002 — README vuelve a crecer demasiado

**Impacto:** LOW

**Probabilidad:** MEDIUM

**Mitigación:**

Agregar solo una sección breve con enlace.

---

# 19. Aclaraciones técnicas

No existen aclaraciones técnicas bloqueantes.

---

# 20. ADR requeridos

Ninguno.

---

# 21. Orden de implementación

1. Crear `docs/adoption.md`.
2. Enlazar desde `README.md` y `docs/index.md`.
3. Registrar evidencia dedicada.
4. Ejecutar verificaciones documentales, seguridad y regresión.
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
