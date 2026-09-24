# TEST-012 — Ensayo aislado de reapertura

Resultado: PASS. Fecha: 2026-09-24.
Autorización: PLAN-001 §11.3 y TASKS-001 TASK-004 aprobados por el usuario.
Este reporte evalúa el procedimiento; el defecto inducido no es un hallazgo
normativo del Harness ni un defecto de la implementación principal.

## Secuencia y evidencia

| Paso | Evidencia | Resultado observado |
|---|---|---|
| Copia de trabajo funcional ya terminado | reopening-initial.md, reopening-baseline-source.txt | TASKS del fixture COMPLETED; documento real IN_PROGRESS |
| Verificación inicial en copia | reopening-baseline.txt | 11 tests PASS, exit 0 |
| Inyección de orden invertido | reopening-injected.diff | Solo cambia iteración de listado; conserva filtrado de propietario |
| Pruebas originales contra copia alterada | reopening-failed.txt | 11 tests, 4 fallos, exit 1; TEST-003 detecta AC-003 |
| Evaluación desfavorable | reopening-failed-state.md | FINDING-001 OPEN, evidencia previa invalidada, fixture FAIL |
| Reapertura y preflight | reopening-active.md | TASKS IN_PROGRESS; TASK-001 activa, dependientes TODO |
| Corrección sin modificar tests | reopening-repaired-1.txt | 11 tests PASS, exit 0 |
| Reevaluación de dependientes | reopening-dependents.md | TASK-002 revalidada; TASK-003 en ejecución |
| Segunda ejecución limpia | reopening-repaired-2.txt | 11 tests PASS, exit 0 |
| Cierre y revalidación del fixture | reopening-final.md | Tareas DONE, TASKS COMPLETED, conformidad del fixture PASS |

Los fallos afectaron TEST-001, TEST-003, TEST-005 y TEST-011 porque comparan
listados ordenados. Se reabrieron TASK-001 y las dependientes TASK-002/003;
no fue necesario cambiar sus objetivos ni obtener nuevas aprobaciones.
Se reutilizó explícitamente evidencia posterior a la corrección donde era válida,
sin inventar ejecuciones adicionales. Las dos ejecuciones reparadas son procesos
independientes y los tests conservaron el mismo hash en todo el ensayo.

## Integridad y límites

La comprobación SHA-256 de reopening-final.md confirma que código y pruebas
principales no cambiaron frente a evidence/hashes.txt. No se desactivaron controles
de seguridad, se alteraron criterios o se presentaron fallos como PASS de la aplicación.
Los estados del fixture están rotulados como simulación; las pruebas y sus fallos
son ejecuciones reales. La suite del proyecto no ejecuta automáticamente un motor
SDD: el Harness define commands conceptuales ejecutados por el agente.

El resultado prueba esta ruta de corrección localizada, no todos los posibles
cambios de SPEC/PLAN o entornos. La feature real aún debe cerrar sus TASKS y pasar
su propia validación. El histórico reproducible queda preservado en este directorio
sin depender de conservar la carpeta temporal.
