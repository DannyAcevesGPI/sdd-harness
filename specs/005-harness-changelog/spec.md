# Especificación: Historial de cambios del Harness

**ID:** SPEC-005
**Estado:** APPROVED
**Versión:** 0.1.0
**Fecha:** 2026-09-30

---

# 1. Resumen

## 1.1 Descripción

Incorporar un historial de cambios dedicado y fácil de encontrar.

## 1.2 Problema

El repositorio registra cambios en Git y en evidencia SDD, pero no ofrece una
vista breve y cronológica de los hitos para lectores del Harness.

## 1.3 Objetivo

Permitir consultar los cambios relevantes y su evidencia sin convertir
`handoff.md` en un historial extenso.

---

# 2. Alcance

## 2.1 Incluido

- Agregar `CHANGELOG.md` en la raíz del repositorio.
- Registrar hitos relevantes respaldados por Git o por artefactos SDD.
- Establecer una pauta breve para registrar futuros cambios.
- Enlazar el historial desde los puntos de entrada documentales.

## 2.2 Fuera de alcance

- Documentar o reorganizar la estructura de carpetas existente.
- Cambiar las reglas SDD de la Constitución.
- Modificar código de aplicación, pruebas o dependencias.
- Trasladar el historial auditado completo al changelog.

---

# 3. Actores

## ACT-001 — Mantenedor del Harness

Necesita identificar hitos y consultar la evidencia correspondiente.

## ACT-002 — Persona que adopta el Harness

Necesita conocer los cambios relevantes sin leer todo el historial de Git.

---

# 4. Requisitos funcionales

## FR-001 — Historial consultable

**Descripción:** El repositorio deberá incluir un historial dedicado de cambios
relevantes, ordenados del más reciente al más antiguo y con referencias a su
evidencia cuando exista.

**Prioridad:** MUST
**Origen:** Solicitud humana de agregar un "changeload", interpretado como
`CHANGELOG.md`.

## FR-002 — Navegación

**Descripción:** El historial deberá poder encontrarse desde el README y el
índice documental existente.

**Prioridad:** MUST
**Origen:** Necesidad de consulta rápida en el repositorio.

## FR-003 — Pauta para entradas futuras

**Descripción:** El historial deberá indicar cómo registrar cambios futuros sin
repetir evidencia extensa ni inventar versiones.

**Prioridad:** MUST
**Origen:** Necesidad de mantener el historial útil tras esta entrega.

---

# 5. Requisitos no funcionales

## NFR-001 — Brevedad y veracidad

**Categoría:** Mantenibilidad
**Descripción:** Cada entrada deberá ser breve, verificable y vinculada a un
commit o artefacto SDD cuando corresponda.
**Métrica o condición:** No se asignarán fechas, versiones ni estados que la
evidencia disponible no confirme.

---

# 6. Requisitos de seguridad

No se identifican controles nuevos. Aplican las reglas existentes para evitar
secretos y datos sensibles en documentación.

---

# 7. Reglas de negocio

## BR-001 — Fuente de verdad histórica

**Regla:** Git y las validaciones SDD respaldan los hitos; el changelog es un
resumen consultable.
**Ejemplo:** Un hito puede enlazar un `validation.md` o identificar un commit.

---

# 8. Criterios de aceptación

## AC-001 — Consultar hitos

**Relacionado con:** FR-001, NFR-001

### Given

Un lector abre el repositorio.

### When

Consulta `CHANGELOG.md`.

### Then

Ve hitos relevantes en orden descendente, con referencias verificables y sin
afirmaciones de versión o fecha sin respaldo.

## AC-002 — Encontrar el historial

**Relacionado con:** FR-002

### Given

Un lector inicia desde README o `docs/index.md`.

### When

Busca el historial de cambios.

### Then

Encuentra un enlace funcional a `CHANGELOG.md`.

## AC-003 — Registrar cambios futuros

**Relacionado con:** FR-003

### Given

Se completa una nueva feature del Harness.

### When

Un mantenedor consulta la pauta del changelog.

### Then

Sabe cómo resumir el cambio y enlazar su evidencia sin copiarla íntegra ni
sobrecargar `handoff.md`.

---

# 9. Casos límite y escenarios de error

## EDGE-001 — Hito sin versión verificable

**Condición:** Existe un cambio conocido sin etiqueta de versión.
**Comportamiento esperado:** Se registra con el hito o commit verificable, sin
inventar versión.

## EDGE-002 — Evidencia extensa

**Condición:** Un cambio tiene auditorías o registros largos.
**Comportamiento esperado:** Se enlaza la evidencia dedicada sin copiarla al
changelog ni a `handoff.md`.

---

# 10. Datos involucrados

Texto Markdown, referencias a commits, archivos SDD y rutas relativas. No hay
datos de usuario ni persistencia nueva.

---

# 11. Dependencias

- README y `docs/index.md` existentes.
- Historial Git y validaciones SDD para respaldar las entradas.

---

# 12. Restricciones

- Respetar la precedencia y los gates de `.spec/constitution.md`.
- Mantener `handoff.md` como estado vivo.
- No alterar artefactos SDD ya aprobados para crear el historial.

---

# 13. Suposiciones

## ASM-001

"Changeload" se refiere al nombre convencional `CHANGELOG.md`.

---

# 14. Preguntas abiertas y necesidades de aclaración

Ninguna bloqueante. El usuario aclaró que la estructura de carpetas ya existe
y debe omitirse de esta feature (2026-09-30).

---

# 15. Matriz inicial de trazabilidad

| Requisito | Criterios de aceptación | Prioridad |
|-----------|-------------------------|-----------|
| FR-001 | AC-001 | MUST |
| FR-002 | AC-002 | MUST |
| FR-003 | AC-003 | MUST |
| NFR-001 | AC-001 | MUST |

---

# 16. Criterios para avanzar a planificación

- [x] Problema, objetivo, actores y alcance definidos.
- [x] Requisitos y criterios trazables.
- [x] Casos límite y restricciones documentados.
- [x] No hay aclaraciones bloqueantes.
- [x] Aprobación humana explícita de la SPEC.

---

# 17. Estado de aprobación

**Estado actual:** APPROVED
**Resultado:** APPROVED
**Aprobado por:** usuario en esta conversación
**Fecha de aprobación:** 2026-09-30
