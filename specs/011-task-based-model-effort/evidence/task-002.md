# Evidencia TASK-002 — Política determinista

**Estado:** PASS
**Fecha:** 2026-10-27
**Requisitos/AC:** FR-001, NFR-001, BR-001, AC-001

## TDD

- RED válido: con la interfaz mínima que devolvía siempre `medium`,
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_effort_policy.py' -v`
  ejecutó seis pruebas y falló en `low` y `high` (tres fallos de aserción).
- GREEN: tras agregar las reglas deterministas, el mismo comando ejecutó seis
  pruebas y terminó `OK`.
- La primera ejecución, antes de crear el módulo de interfaz, falló en import.
  Se descarta como RED porque no llegó a probar conducta.

## Resultado

`src/effort_policy.py` selecciona low para señales mecánicas, high ante
señales de impacto aunque haya una señal low, y medium para casos rutinarios,
vacíos o ambiguos. Cada respuesta incluye una razón breve sin copiar el texto
completo de la tarea.
