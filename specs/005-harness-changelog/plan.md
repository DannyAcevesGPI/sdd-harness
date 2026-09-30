# Plan Técnico: Historial de cambios del Harness

**ID:** PLAN-005
**SPEC relacionada:** SPEC-005
**Estado:** APPROVED
**Versión:** 0.1.0
**Fecha:** 2026-09-30

---

# 1. Precondiciones

- [x] Existe `spec.md` y está `APPROVED` por el usuario.
- [x] No hay aclaraciones bloqueantes.
- [x] Los requisitos MUST tienen criterios de aceptación.
- [x] Alcance y restricciones definidos.

---

# 2. Resumen técnico

## 2.1 Objetivo

Crear un historial corto, verificable y fácil de encontrar.

## 2.2 Enfoque

Crear `CHANGELOG.md` en la raíz con hitos respaldados por Git y evidencia SDD.
Agregar enlaces breves desde `README.md` y `docs/index.md`. No se introduce
código, automatización ni dependencias.

---

# 3. Requisitos cubiertos

| Requisito | Tipo | Cobertura |
|-----------|------|-----------|
| FR-001 | Funcional | Entradas cronológicas con referencias verificables. |
| FR-002 | Funcional | Enlaces en README e índice documental. |
| FR-003 | Funcional | Pauta breve para futuras entradas. |
| NFR-001 | No funcional | Texto breve; metadatos sustentados por Git o validaciones. |

BR-001 se cumple al tratar Git y las validaciones como respaldo, no como texto
que deba duplicarse.

---

# 4. Contexto técnico existente

- Documentación: Markdown en raíz y `docs/`.
- Índices: `README.md` y `docs/index.md`.
- Estado vivo: `handoff.md`.
- Evidencia: `specs/<feature-id>/validation.md` y `evidence/`.
- Historia Git disponible: `34740af`, `38a5edc`, `73e41e6`, `8515abd`.
- Versión comprobada: 1.0.0 STABLE en el cierre de AUDIT-10.
- Pruebas de aplicación: Python `unittest`; el cambio documental requiere
  comprobación de enlaces, orden y afirmaciones.

No hay base de datos, API, configuración ni runtime nuevo involucrado.

---

# 5. Decisiones técnicas

## DEC-001 — Documento dedicado en la raíz

**Decisión:** Crear `CHANGELOG.md` con entradas de más reciente a más antigua,
referencias relativas a evidencia SDD y commits identificados por hash corto.

**Justificación:** Cumple FR-001 y NFR-001 con el patrón documental actual.

**Requisitos relacionados:** FR-001, NFR-001.

**Alternativas consideradas:** Colocar el historial en README o `handoff.md`.

**Consecuencias:** El historial queda separado del estado vivo y del índice.

**Requiere ADR:** NO.

## DEC-002 — Enlaces de entrada

**Decisión:** Añadir referencias cortas al changelog en `README.md` y
`docs/index.md`; no copiar entradas en estos archivos.

**Justificación:** Cumple FR-002 sin duplicar contenido.

**Requisitos relacionados:** FR-002, NFR-001.

**Alternativas consideradas:** Enlazar solo desde el README.

**Consecuencias:** Ambos puntos de entrada permiten descubrir el historial.

**Requiere ADR:** NO.

## DEC-003 — Pauta de mantenimiento dentro del changelog

**Decisión:** Incluir una nota corta para futuras entradas: describir cambios
observables, enlazar la evidencia, usar versión solo si existe respaldo y
mantener orden descendente.

**Justificación:** Satisface FR-003 sin agregar un documento de proceso.

**Requisitos relacionados:** FR-003, NFR-001.

**Alternativas consideradas:** Documento separado de convenciones.

**Consecuencias:** Una única referencia para lectura y actualización.

**Requiere ADR:** NO.

---

# 6. Arquitectura propuesta

| Componente | Responsabilidad | Cambio |
|------------|-----------------|--------|
| `CHANGELOG.md` | Historial y pauta | CREATE |
| `README.md` | Entrada general | MODIFY |
| `docs/index.md` | Índice documental | MODIFY |
| `handoff.md` | Estado vivo | REUSE |
| `specs/` y Git | Evidencia histórica | REUSE |

Flujo: punto de entrada → changelog → evidencia dedicada o commit.

---

# 7. Modelo de datos

No aplica. No hay persistencia ni migraciones.

# 8. Interfaces y contratos

No aplica. Las rutas Markdown relativas constituyen los enlaces a verificar.

# 9. Validación de entradas

Antes de redactar cada entrada, contrastar fecha, hash, estado y versión con
Git o la validación correspondiente. Comprobar que las rutas relativas existen.

# 10. Seguridad

No hay autenticación ni autorización nuevas. Revisar que el texto no exponga
secretos ni datos sensibles. No hay operaciones destructivas.

# 11. Estrategia de pruebas

| Criterio | Verificación prevista |
|----------|-----------------------|
| AC-001 | Revisión documental del orden y respaldo en Git/SDD. |
| AC-002 | Comprobación de enlaces relativos desde README e índice. |
| AC-003 | Revisión de pauta de actualización y ausencia de duplicación extensa. |

`git diff --check` verificará formato básico. No se agregan tests automatizados
para contenido Markdown estático; la regresión Python solo se ejecutará si una
necesidad concreta lo justifica.

# 12. Observabilidad

No aplica. La evidencia de verificación se guardará bajo la feature.

# 13. Impacto en el repositorio

- CREATE: `CHANGELOG.md` y evidencia de SPEC-005.
- MODIFY: `README.md`, `docs/index.md`.
- REUSE: Git, validaciones existentes, `handoff.md` como estado vivo.
- REMOVE: Ninguno.

# 14. Dependencias

Ninguna nueva.

# 15. Configuración

Ninguna.

# 16. Migración y compatibilidad

No hay cambios de API, esquema, datos ni configuración. Breaking changes: NO.

# 17. Manejo de errores

Si un hito no puede verificarse, omitir el dato incierto y registrar solo lo
respaldado. Si una ruta enlazada no existe, corregirla antes de validar.

# 18. Riesgos técnicos

## RISK-001 — Atribución histórica incorrecta

**Impacto:** MEDIUM
**Probabilidad:** LOW
**Mitigación:** Contrastar cada entrada con commits y validaciones; evitar
versiones o fechas inferidas.

# 19. Aclaraciones técnicas

Ninguna bloqueante.

# 20. ADR requeridos

Ninguno.

# 21. Orden de implementación

1. Redactar changelog con evidencia comprobada.
2. Enlazarlo desde README e índice.
3. Verificar enlaces, contenido y formato; registrar evidencia.
4. Validar contra la SPEC.

# 22. Criterios para avanzar a Tasks

- [x] SPEC aprobada y requisitos MUST cubiertos.
- [x] Componentes, seguridad, verificación e impacto identificados.
- [x] Sin dependencias, migraciones, ADR ni dudas bloqueantes.
- [x] Aprobación humana explícita del PLAN.

# 23. Estado del plan

**Estado actual:** APPROVED
**Aprobado por:** usuario en esta conversación
**Fecha de aprobación:** 2026-09-30
