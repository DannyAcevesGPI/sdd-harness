# TASK-002 — Gates y templates

Cobertura: FR-001, FR-002, FR-004, BR-001, BR-002;
AC-001, AC-003, AC-004.

Se revisaron Constitución, seis commands y tres templates. Cada gate nuevo
requiere decisión humana explícita y registro durable antes de avanzar; una
huella inconsistente bloquea el gate. La captura no autoaprueba artefactos.

Verificación alternativa (sin TDD: documentación, no comportamiento
automatizable): búsqueda de `decisions.json`, `check_harness_state` y la guía en
los artefactos modificados; casos válidos e inválidos cubiertos por TEST-001 a
TEST-004 de TASK-001. No se cambiaron requisitos ni estados históricos.
