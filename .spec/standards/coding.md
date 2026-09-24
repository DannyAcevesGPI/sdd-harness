# Estándar de Código

**Versión:** 1.0.0  
**Estado:** Activo

## Propósito

Este documento define los estándares generales que deberán seguirse
durante la implementación y modificación del código fuente.

Su objetivo es producir código comprensible, mantenible, verificable
y trazable respecto a las especificaciones del sistema.

---

# 1. El código implementa trabajo trazable

Todo código nuevo deberá responder a trabajo definido y trazable dentro
del proceso SDD.

Esto puede originarse en:

- un requisito;
- un criterio de aceptación;
- una corrección documentada;
- o una necesidad técnica definida en el plan.

Toda modificación de implementación deberá ejecutarse mediante una tarea
autorizada.

Las correcciones documentadas y necesidades técnicas no sustituyen la
trazabilidad requerida por el Harness.

Cuando el trabajo sea técnico, la tarea deberá mantener relación con el
PLAN y con los requisitos o criterios que dicho trabajo soporta.

No deberá inventarse un requisito funcional únicamente para justificar
un detalle técnico.

No deberá agregarse funcionalidad no solicitada durante la
implementación.

Si durante el desarrollo se identifica una funcionalidad adicional
necesaria, deberá seguirse el proceso de cambio definido por la
Constitution antes de implementarla.

---

# 2. Alcance mínimo

Cada cambio deberá limitarse al alcance de la tarea actual.

Durante una tarea no deberán realizarse modificaciones no relacionadas,
como:

- refactors innecesarios;
- cambios cosméticos extensos;
- nuevas funcionalidades;
- cambios arquitectónicos no aprobados;
- actualizaciones de dependencias sin justificación.

Si se detecta una mejora fuera del alcance, deberá registrarse
separadamente.

---

# 3. Código simple y comprensible

Se deberá favorecer código:

- explícito;
- legible;
- predecible;
- fácil de probar;
- fácil de modificar.

Se evitará introducir abstracciones antes de que exista una necesidad
concreta.

La complejidad deberá justificarse por los requisitos o por una
necesidad técnica documentada.

---

# 4. Responsabilidad única

Funciones, clases, módulos y componentes deberán tener una
responsabilidad claramente identificable.

Se deberán evitar unidades que mezclen múltiples responsabilidades
sin una razón documentada.

Cuando una unidad crezca significativamente, deberá evaluarse su
división.

---

# 5. Nombres descriptivos

Los nombres deberán expresar intención.

Se deberán utilizar nombres que representen conceptos del dominio o
responsabilidades técnicas reconocibles.

Evitar nombres ambiguos como:

data
temp
thing
stuff
manager
helper

cuando exista una alternativa más específica.

Ejemplo:

Incorrecto:

processData()

Preferible:

calculateInvoiceTotal()

---

# 6. Funciones pequeñas y enfocadas

Las funciones deberán realizar una tarea claramente identificable.

Una función deberá dividirse cuando:

- tenga múltiples responsabilidades;
- contenga demasiadas ramas de decisión;
- resulte difícil de probar;
- requiera una explicación extensa para comprenderla.

No se establece un límite arbitrario de líneas.

La claridad tiene prioridad sobre una métrica rígida.

---

# 7. Evitar duplicación significativa

La duplicación que represente la misma regla de negocio deberá
reducirse cuando sea razonable.

No deberá introducirse una abstracción únicamente porque dos fragmentos
de código sean visualmente similares.

Primero deberá determinarse si representan realmente el mismo concepto.

---

# 8. Manejo explícito de errores

Los errores esperados deberán manejarse explícitamente.

No deberán:

- ignorarse silenciosamente;
- convertirse automáticamente en éxito;
- ocultarse sin registro cuando sean relevantes;
- exponerse detalles internos innecesarios al usuario.

Los mensajes de error deberán aportar contexto suficiente para
diagnosticar el problema.

---

# 9. Validación en límites del sistema

Los datos provenientes de fuentes externas deberán considerarse
no confiables hasta ser validados.

Esto incluye:

- solicitudes HTTP;
- formularios;
- archivos;
- variables de entorno;
- APIs externas;
- eventos;
- mensajes;
- entradas de usuario.

La validación deberá realizarse lo más cerca posible del límite
de entrada correspondiente.

---

# 10. Tipos y contratos

Cuando el lenguaje lo permita, deberán utilizarse tipos para hacer
explícitos los contratos del sistema.

Se evitará desactivar o evadir el sistema de tipos sin una
justificación técnica.

Los contratos importantes deberán expresar claramente:

- entradas;
- salidas;
- estados válidos;
- errores esperados.

---

# 11. Estado mutable

El estado mutable deberá mantenerse controlado y localizado.

Se evitarán variables globales mutables y efectos secundarios
innecesarios.

Los cambios de estado importantes deberán ocurrir en lugares
claramente identificables.

---

# 12. Comentarios

Los comentarios deberán explicar principalmente:

- por qué existe una decisión;
- restricciones no evidentes;
- comportamientos inesperados;
- decisiones temporales relevantes.

No deberán utilizarse para describir literalmente lo que el código
ya expresa claramente.

Incorrecto:

// Incrementa contador en uno
counter += 1

Preferible:

// El proveedor comienza la numeración en 1, no en 0.
providerIndex = internalIndex + 1

---

# 13. Código muerto

No deberá mantenerse código:

- comentado;
- inaccesible;
- obsoleto;
- duplicado sin uso;
- creado "por si acaso".

El control de versiones deberá utilizarse para recuperar
implementaciones anteriores cuando sea necesario.

---

# 14. Dependencias

Una dependencia nueva deberá tener una razón técnica clara.

Antes de agregar una dependencia deberá evaluarse:

- si el problema puede resolverse razonablemente sin ella;
- su mantenimiento;
- su impacto;
- su seguridad;
- su compatibilidad con el proyecto.

No deberán agregarse librerías únicamente para resolver operaciones
triviales.

---

# 15. Configuración y secretos

Los secretos nunca deberán almacenarse directamente en el código.

Ejemplos:

- passwords;
- API keys;
- tokens;
- private keys;
- credenciales de bases de datos.

Los valores dependientes del entorno deberán utilizar mecanismos
de configuración apropiados para el stack.

---

# 16. Cambios de base de datos

Los cambios al esquema de datos deberán realizarse mediante mecanismos
reproducibles cuando la tecnología utilizada lo permita.

Ejemplos:

- migrations;
- schema migrations;
- versioned scripts.

Los cambios destructivos deberán identificarse explícitamente
antes de ejecutarse.

---

# 17. Compatibilidad

Los cambios que puedan romper contratos existentes deberán
identificarse antes de su implementación.

Esto incluye cambios en:

- APIs;
- schemas;
- eventos;
- formatos de archivos;
- interfaces públicas;
- modelos persistidos.

Cuando corresponda deberá definirse una estrategia de migración.

---

# 18. Formato automático

Cuando el ecosistema utilizado disponga de herramientas estándar para:

- formatting;
- linting;
- análisis estático;

deberán configurarse y ejecutarse de manera consistente.

Las reglas específicas deberán definirse durante la configuración
técnica del proyecto.

---

# 19. Código generado por agentes

El código generado por un agente deberá cumplir exactamente los mismos
estándares que el código escrito manualmente.

Un agente no deberá:

- inventar requisitos;
- modificar alcance silenciosamente;
- ignorar errores existentes;
- desactivar pruebas para conseguir un resultado exitoso;
- eliminar validaciones para hacer pasar una prueba;
- introducir dependencias sin justificación;
- cambiar contratos sin documentarlo.

---

# 20. Prohibido adaptar pruebas para ocultar errores

Cuando una implementación no cumpla una prueba derivada de un requisito,
la solución predeterminada deberá ser corregir la implementación.

No deberá modificarse o eliminarse una prueba únicamente para hacer
que una implementación incorrecta sea aceptada.

Si la prueba resulta incorrecta respecto a la especificación:

1. deberá identificarse la discrepancia;
2. deberá revisarse la especificación;
3. deberá corregirse la prueba cuando corresponda;
4. deberá documentarse el cambio.

---

# 21. Refactoring

Un refactor deberá preservar el comportamiento observable del sistema,
salvo que exista una especificación que indique lo contrario.

Los refactors significativos deberán realizarse separadamente cuando
esto facilite su revisión.

Después de un refactor deberán ejecutarse las pruebas relevantes.

---

# 22. TODO y deuda técnica

Los marcadores como:

TODO
FIXME
HACK

no deberán utilizarse como sustituto de una implementación requerida
por la especificación.

Cuando se utilicen deberán incluir contexto suficiente para entender
por qué existen.

La deuda técnica relevante deberá documentarse como trabajo pendiente
en lugar de permanecer oculta en el código.

---

# Checklist de implementación

Antes de considerar una tarea de código completada deberá verificarse:

- [ ] El cambio corresponde a una tarea definida.
- [ ] La tarea mantiene trazabilidad con el PLAN y con los requisitos
      o criterios que soporta.
- [ ] No se agregó funcionalidad fuera del alcance.
- [ ] El código tiene responsabilidades claras.
- [ ] Los nombres expresan intención.
- [ ] Las entradas externas se validan.
- [ ] Los errores relevantes se manejan explícitamente.
- [ ] No existen secretos en el código.
- [ ] No se agregó código muerto.
- [ ] Las dependencias nuevas están justificadas.
- [ ] Los contratos afectados fueron respetados.
- [ ] Las pruebas relevantes son satisfactorias.
- [ ] Formatting, linting y análisis estático son satisfactorios
      cuando estén configurados.