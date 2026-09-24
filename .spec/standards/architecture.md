# Estándar de Arquitectura

**Versión:** 1.0.0  
**Estado:** Activo

## Propósito

Este documento define los estándares arquitectónicos que deberán
seguirse durante el diseño e implementación del software.

Su objetivo es mantener una arquitectura comprensible, modular,
mantenible y trazable respecto a las especificaciones.

---

# 1. La arquitectura debe derivarse de la especificación

Las decisiones arquitectónicas deberán responder a requisitos
documentados.

No deberán introducirse tecnologías, servicios, patrones o
infraestructura sin una justificación relacionada con:

- requisitos funcionales;
- requisitos no funcionales;
- restricciones;
- seguridad;
- rendimiento;
- escalabilidad;
- mantenibilidad;
- operación.

La arquitectura no deberá diseñarse únicamente alrededor de una
preferencia tecnológica.

---

# 2. Separación de responsabilidades

Los componentes deberán tener responsabilidades claramente definidas.

Se deberá evitar mezclar innecesariamente:

- presentación;
- lógica de negocio;
- acceso a datos;
- integraciones externas;
- infraestructura;
- configuración.

La separación concreta dependerá de las necesidades del proyecto
y deberá documentarse en el plan técnico.

---

# 3. Dependencias explícitas

Las dependencias entre componentes deberán ser visibles y
comprensibles.

Se evitarán:

- dependencias circulares;
- acoplamiento innecesario;
- acceso indirecto no documentado;
- dependencias globales difíciles de sustituir o probar.

Cuando sea relevante, las dependencias externas deberán abstraerse
mediante interfaces o mecanismos equivalentes.

---

# 4. Límites del sistema

Cada plan técnico deberá identificar, cuando corresponda:

- componentes internos;
- sistemas externos;
- bases de datos;
- APIs;
- servicios;
- usuarios o actores;
- procesos asíncronos;
- almacenamiento;
- límites de confianza.

Las interacciones importantes entre estos elementos deberán quedar
documentadas.

---

# 5. Modelado de dominio

La estructura del software deberá reflejar los conceptos importantes
del dominio cuando esto mejore su comprensión.

Los nombres utilizados en:

- código;
- modelos;
- APIs;
- eventos;
- documentación;

deberán utilizar terminología consistente con la especificación.

---

# 6. Contratos explícitos

Las interfaces entre componentes deberán tener contratos claros.

Dependiendo del proyecto, estos contratos podrán incluir:

- tipos;
- schemas;
- DTOs;
- interfaces;
- eventos;
- contratos HTTP;
- mensajes;
- estructuras de datos.

Los contratos deberán poder validarse cuando sea técnicamente
razonable.

---

# 7. Gestión de datos

Las decisiones relacionadas con persistencia deberán documentarse
cuando sean relevantes.

Esto incluye:

- modelo de datos;
- relaciones;
- restricciones;
- índices;
- migraciones;
- transacciones;
- consistencia;
- retención;
- eliminación.

Los cambios destructivos deberán identificarse explícitamente.

---

# 8. Integraciones externas

Toda integración externa deberá documentar como mínimo:

- propósito;
- sistema externo;
- datos enviados;
- datos recibidos;
- autenticación cuando aplique;
- manejo de errores;
- comportamiento ante indisponibilidad.

La lógica principal del sistema no deberá depender innecesariamente
de detalles específicos de un proveedor externo.

---

# 9. Manejo de errores

Los errores deberán manejarse explícitamente.

La arquitectura deberá distinguir cuando corresponda entre:

- errores de validación;
- errores de negocio;
- errores de infraestructura;
- errores de integraciones externas;
- errores inesperados.

Los errores no deberán ignorarse silenciosamente.

---

# 10. Observabilidad

Cuando la naturaleza del proyecto lo requiera, el plan técnico deberá
considerar mecanismos de observabilidad como:

- logs;
- métricas;
- trazas;
- auditoría;
- health checks.

La información registrada no deberá exponer datos sensibles
innecesariamente.

---

# 11. Configuración

La configuración dependiente del entorno deberá mantenerse separada
del código cuando sea posible.

Ejemplos:

- credenciales;
- URLs externas;
- puertos;
- feature flags;
- configuraciones de infraestructura.

Los secretos nunca deberán almacenarse directamente en el código
fuente.

---

# 12. Simplicidad

Se deberá elegir la arquitectura más simple que satisfaga los
requisitos actuales y las restricciones conocidas.

No deberán introducirse patrones, capas, servicios o infraestructura
basados únicamente en necesidades hipotéticas futuras.

La complejidad deberá justificarse.

---

# 13. Decisiones arquitectónicas importantes

Las decisiones arquitectónicas que tengan impacto significativo
deberán documentarse.

Estas decisiones podrán almacenarse en:

docs/decisions/

utilizando Architecture Decision Records (ADR).

Ejemplos:

ADR-001-eleccion-base-datos.md
ADR-002-autenticacion.md
ADR-003-arquitectura-eventos.md

---

# 14. Cambios arquitectónicos

Si durante la implementación se requiere modificar una decisión
arquitectónica definida en el plan:

1. detener la implementación afectada;
2. identificar la causa;
3. evaluar el impacto sobre los artefactos, implementación y evidencia
   dependientes;
4. actualizar el plan;
5. crear o actualizar un ADR cuando corresponda;
6. actualizar las tareas afectadas cuando corresponda;
7. obtener nuevamente las aprobaciones requeridas para los artefactos
   modificados;
8. comprobar que los gates aplicables vuelvan a cumplirse;
9. continuar la implementación afectada únicamente después de cumplir
   dichos gates.

Los cambios arquitectónicos significativos no deberán realizarse
silenciosamente.

Este procedimiento deberá respetar las reglas de ownership y propagación
de cambios definidas en el Artículo VIII de la Constitution.

---

# Checklist arquitectónico

Antes de aprobar un plan técnico deberá verificarse:

- [ ] La arquitectura responde a requisitos identificables.
- [ ] Las responsabilidades están claramente separadas.
- [ ] Las dependencias principales están identificadas.
- [ ] Los límites del sistema están definidos.
- [ ] Los contratos importantes están documentados.
- [ ] La estrategia de datos está definida cuando corresponde.
- [ ] Las integraciones externas están identificadas.
- [ ] Existe una estrategia de manejo de errores.
- [ ] Se consideró observabilidad cuando es necesaria.
- [ ] Los secretos están separados del código.
- [ ] La complejidad introducida está justificada.
- [ ] Las decisiones arquitectónicas importantes están documentadas.