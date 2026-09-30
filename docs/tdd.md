# TDD en el SDD Harness

TDD es obligatorio para cambios nuevos de comportamiento que puedan probarse
automáticamente, incluidas correcciones de bugs reproducibles. La regla completa
está en `.spec/standards/testing.md` §21. Se aplica después de aprobar SPEC,
PLAN y TASKS; no autoriza escribir tests durante la planificación.

## Flujo por fase

1. En SPEC, define el comportamiento y criterios de aceptación verificables.
2. En PLAN, identifica los casos automatizables y el nivel/comando de prueba
   apropiado para el stack del proyecto. Documenta por qué un caso no aplica.
3. En TASKS, asigna casos TEST trazados a requisitos y AC, con la evidencia
   esperada. No se escribe aún código de prueba.
4. En `/implement`, por cada caso aplicable, ejecuta RED → GREEN → REFACTOR:
   - RED: escribe o ajusta el test, ejecútalo antes de cambiar código productivo
     y confirma que falla por el comportamiento faltante.
   - GREEN: implementa lo mínimo para hacerlo pasar y ejecuta pruebas relevantes.
   - REFACTOR: mejora el código solo si hace falta y verifica que sigue verde.
5. En `/validate`, comprueba la secuencia, causa y resultados en la evidencia.

Ejemplo conceptual: `AC-001` requiere rechazar un importe negativo. La prueba
`TEST-001` afirma ese rechazo y falla porque hoy se acepta el importe (RED).
Tras agregar la regla mínima, la misma prueba pasa (GREEN). El nombre del
comando dependerá del proyecto; no se impone un framework.

## Evidencia mínima

Guarda el detalle en `specs/<feature-id>/evidence/` y enlázalo desde TASKS y
VALIDATE. Por cada TEST registra requisito/AC, comando, resultado RED y causa,
comando y resultado GREEN, y comprobación tras refactor cuando exista. Basta
una salida breve y verificable; evita logs grandes o datos sensibles.

| TEST | Requisito / AC | RED antes de código | GREEN después | Refactor |
|------|----------------|---------------------|---------------|----------|
| TEST-001 | FR-001 / AC-001 | comando, FAIL por rechazo faltante | comando, PASS | PASS o no requerido |

Una falla de sintaxis, dependencia, configuración o infraestructura no es RED
válido. Si la prueba ya pasaba, revisa el caso y encuentra el comportamiento
faltante real; nunca fabriques un fallo. Si el entorno impide ejecutar una
prueba automatizable, registra BLOCK y mantén la tarea BLOCKED.

## Fuera de TDD

Documentación, criterios exclusivamente manuales y refactors sin comportamiento
nuevo pueden verificarse de otra forma. Registra el motivo, la comprobación
alternativa y su resultado. La preferencia por saltar TDD no es una excepción;
`/validate` exige evidencia suficiente antes de PASS. La política es
prospectiva: no reescribas pruebas o resultados de features ya validadas.
