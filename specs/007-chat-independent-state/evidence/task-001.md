# TASK-001 — Comprobador de estado

Cobertura: FR-001, FR-002, FR-004, NFR-002, BR-001, BR-002;
AC-001, AC-003, AC-004; TEST-001 a TEST-004.

## RED

- `python3 -m unittest discover -s tests -p test_check_harness_state.py`:
  7 errores por `NotImplementedError` en `audit_repository` después de definir
  la interfaz mínima. Fallo causado por comportamiento ausente, no por entorno.
- Tras GREEN inicial, las pruebas de revocación y sustitución fallaron (2 FAIL):
  la aprobación revocada seguía vigente y se comparaba una huella reemplazada.
- La prueba de campo sustantivo `Estado` falló (1 FAIL): la normalización lo
  ocultaba fuera de metadata operativa.

El primer intento previo a la interfaz produjo `ModuleNotFoundError`; no se
cuenta como RED válido.

## GREEN

- `python3 -m unittest discover -s tests -p test_check_harness_state.py`:
  11 tests, OK.
- `PYTHONPATH=src python3 -m unittest discover -s tests`:
  22 tests, OK.
- `python3 -m py_compile src/check_harness_state.py tests/test_check_harness_state.py`:
  PASS.

El comprobador es de solo lectura; distingue legado, valida eventos/rutas,
revocaciones y huellas de contenido autorizado. No se añadieron dependencias.
