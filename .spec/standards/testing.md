# Estándar de Pruebas

**Versión:** 1.0.0  
**Estado:** Activo

## Propósito

Este documento define los estándares generales para diseñar,
implementar y ejecutar pruebas dentro del repositorio.

El objetivo de las pruebas no es únicamente detectar errores,
sino proporcionar evidencia verificable de que la implementación
cumple con los requisitos y criterios de aceptación definidos
en las especificaciones.

---

# 1. Las pruebas derivan de requisitos

Las pruebas deberán estar relacionadas con comportamientos,
requisitos, criterios de aceptación o riesgos identificados.

La relación esperada es:

Requisito
→ Criterio de aceptación
→ Implementación
→ Prueba
→ Evidencia

No deberán crearse pruebas únicamente para aumentar métricas
de cobertura.

---

# 2. Trazabilidad

Los requisitos críticos deberán poder relacionarse con una o más
pruebas.

Ejemplo:

FR-001 — El usuario puede iniciar sesión.

AC-001 — Credenciales válidas permiten acceso.
AC-002 — Credenciales inválidas son rechazadas.

Pruebas:

TEST-001 → AC-001
TEST-002 → AC-002

---

# 3. Tipos de pruebas

El proyecto podrá utilizar diferentes niveles de pruebas según
sus necesidades.

## Unitarias

Verifican unidades pequeñas de comportamiento de manera aislada.

Ejemplos:

- funciones;
- servicios;
- reglas de negocio;
- validadores;
- transformaciones.

## Integración

Verifican la interacción entre componentes.

Ejemplos:

- servicio + base de datos;
- API + servicio;
- repositorio + base de datos;
- integración con infraestructura.

## End-to-End

Verifican flujos completos desde la perspectiva del usuario
o consumidor del sistema.

Ejemplos:

Usuario
→ API
→ lógica
→ base de datos
→ respuesta

## Contract Tests

Cuando existan contratos entre sistemas o componentes, podrán
utilizarse pruebas específicas para verificar dichos contratos.

No todos los proyectos necesitan todos los tipos de pruebas.

El plan técnico deberá determinar cuáles son necesarios.

---

# 4. Casos positivos y negativos

Cuando corresponda, las pruebas deberán cubrir:

- comportamiento esperado;
- entradas inválidas;
- límites;
- errores esperados;
- permisos;
- estados no permitidos.

Ejemplo:

Para:

FR-005 — Crear una tarea.

No basta con probar:

✓ tarea válida → creada

También podrán ser relevantes:

✗ título vacío
✗ proyecto inexistente
✗ usuario sin permisos
✗ datos inválidos

La cobertura deberá derivarse del comportamiento especificado.

---

# 5. Pruebas deterministas

Las pruebas deberán producir resultados consistentes.

Se deberán evitar dependencias innecesarias de:

- tiempo real;
- servicios externos;
- datos externos cambiantes;
- orden de ejecución;
- estado global;
- aleatoriedad no controlada.

Cuando estos elementos sean necesarios deberán controlarse
o aislarse adecuadamente.

---

# 6. Independencia

Una prueba no deberá depender innecesariamente de la ejecución
previa de otra prueba.

Cada prueba deberá preparar el estado que necesita y limpiar
sus efectos cuando corresponda.

---

# 7. Datos de prueba

Los datos utilizados deberán ser:

- explícitos;
- comprensibles;
- mínimos;
- reproducibles.

No deberán utilizarse secretos ni datos personales reales
cuando no sean estrictamente necesarios.

Cuando una prueba requiera utilizar credenciales o secretos reales para
interactuar con un entorno o integración autorizados, estos deberán
suministrarse mediante los mecanismos seguros definidos para dicho
entorno.

La necesidad de utilizar un secreto no autoriza almacenarlo o
incorporarlo directamente en:

- código de pruebas;
- fixtures;
- archivos versionados;
- resultados de pruebas;
- logs;
- documentación.

El manejo de secretos deberá cumplir con el Estándar de Seguridad.

---

# 8. Pruebas de regresión

Cuando se corrija un defecto reproducible deberá considerarse
agregar una prueba que demuestre el comportamiento incorrecto
antes de la corrección.

El objetivo es evitar que el mismo defecto vuelva a introducirse.

Flujo recomendado:

Bug
 ↓
Prueba que reproduce el bug
 ↓
Prueba falla
 ↓
Corrección
 ↓
Prueba pasa
 ↓
Regression suite

---

# 9. Las pruebas no se modifican para ocultar errores

Si una prueba derivada correctamente de la especificación falla,
la implementación deberá considerarse incorrecta hasta demostrar
lo contrario.

Está prohibido:

- eliminar la prueba para conseguir éxito;
- deshabilitarla sin justificación;
- reducir sus assertions para permitir una implementación incorrecta;
- modificar datos esperados únicamente para hacer pasar el test.

Si se determina que la prueba contradice la especificación,
la discrepancia deberá documentarse y resolverse explícitamente.

---

# 10. Prohibido ignorar pruebas fallidas

Una tarea no podrá marcarse como completada cuando existan pruebas
relevantes fallidas.

Una prueba fallida deberá clasificarse como:

1. defecto de implementación;
2. defecto de prueba;
3. problema de infraestructura;
4. discrepancia con la especificación;
5. comportamiento aún no implementado.

La causa deberá resolverse o documentarse como bloqueante.

---

# 11. Tests skipped

Las pruebas marcadas como:

skip
disabled
pending
todo

no deberán considerarse evidencia de cumplimiento.

Si una prueba necesaria está deshabilitada, el requisito asociado
no podrá considerarse completamente validado.

---

# 12. Mocks y test doubles

Mocks, stubs, fakes y otras técnicas de aislamiento podrán utilizarse
cuando mejoren la calidad o velocidad de las pruebas.

No deberán utilizarse de forma que la prueba deje de representar
el comportamiento relevante.

Los límites externos son candidatos naturales para aislamiento.

Ejemplos:

- APIs externas;
- correo;
- pagos;
- almacenamiento externo;
- servicios de terceros.

---

# 13. Pruebas de integración reales

Cuando un requisito dependa de comportamiento específico de una
tecnología o integración, deberán considerarse pruebas de integración
contra una implementación suficientemente representativa.

Un mock exitoso no demuestra necesariamente que una integración
real funcione.

---

# 14. Cobertura

La cobertura de código podrá utilizarse como indicador auxiliar.

No deberá interpretarse automáticamente como evidencia de calidad.

Un proyecto con alta cobertura puede seguir teniendo requisitos
sin validar.

La prioridad será:

Cumplimiento de requisitos
> calidad de pruebas
> cobertura numérica

Los porcentajes mínimos, si fueran necesarios, deberán definirse
según las características del proyecto.

---

# 15. Nombres de pruebas

Los nombres deberán expresar claramente el comportamiento esperado.

Preferible:

rechaza_login_cuando_password_es_incorrecto

o:

shouldRejectLoginWhenPasswordIsInvalid

Evitar nombres genéricos como:

test1
testFunction
works
check

---

# 16. Evidencia de validación

La ejecución exitosa de pruebas deberá poder utilizarse como evidencia
durante la fase de validación.

La evidencia podrá incluir:

- nombre de la prueba;
- requisito relacionado;
- criterio de aceptación relacionado;
- resultado;
- comando ejecutado;
- fecha cuando sea relevante.

---

# 17. Matriz de trazabilidad

Cuando la complejidad de la funcionalidad lo justifique deberá poder
construirse una matriz similar a:

| Requisito | Criterio | Tarea | Prueba | Estado |
|-----------|----------|-------|--------|--------|
| FR-001 | AC-001 | TASK-001 | TEST-001 | PASS |
| FR-001 | AC-002 | TASK-002 | TEST-002 | PASS |
| FR-002 | AC-003 | TASK-003 | TEST-003 | FAIL |

Esta matriz permitirá identificar requisitos sin evidencia suficiente.

---

# 18. Estado de una prueba

Los resultados deberán clasificarse mediante estados explícitos.

Estados recomendados:

PASS
FAIL
BLOCKED
NOT_RUN

Cuando corresponda también podrá utilizarse:

NOT_APPLICABLE

Un estado desconocido no deberá interpretarse como PASS.

---

# 19. Validación manual

Algunos criterios pueden requerir validación manual.

Ejemplos:

- comportamiento visual;
- accesibilidad;
- experiencia de usuario;
- dispositivos físicos;
- procesos humanos.

La validación manual deberá documentar:

- qué se verificó;
- cómo se verificó;
- resultado;
- criterio de aceptación asociado.

La validación manual no deberá utilizarse como sustituto de una
prueba automatizable sin una razón válida.

---

# 20. Finalización

Una funcionalidad no podrá considerarse completamente validada
mientras exista un requisito obligatorio sin evidencia suficiente.

El hecho de que:

- compile;
- inicie;
- no produzca errores inmediatos;
- o pase algunas pruebas;

no implica por sí mismo cumplimiento de la especificación.

---

# Checklist de pruebas

Antes de considerar validada una funcionalidad deberá verificarse:

- [ ] Los requisitos críticos tienen pruebas o validación correspondiente.
- [ ] Los criterios de aceptación relevantes están cubiertos.
- [ ] Existen casos positivos y negativos cuando corresponde.
- [ ] Las pruebas son reproducibles.
- [ ] Las pruebas relevantes son independientes.
- [ ] No existen pruebas requeridas deshabilitadas.
- [ ] No existen pruebas relevantes fallidas.
- [ ] Las integraciones importantes fueron verificadas adecuadamente.
- [ ] Los bugs corregidos tienen pruebas de regresión cuando corresponde.
- [ ] La evidencia de validación puede relacionarse con los requisitos.