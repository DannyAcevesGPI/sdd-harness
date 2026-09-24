# Estándar de Seguridad

**Versión:** 1.0.0  
**Estado:** Activo

## Propósito

Este documento define los principios mínimos de seguridad que deberán
considerarse durante la especificación, planificación, implementación
y validación del software.

La seguridad deberá formar parte del diseño del sistema y no tratarse
únicamente como una revisión posterior a la implementación.

---

# 1. Seguridad desde la especificación

Los requisitos relacionados con seguridad deberán identificarse
durante la especificación cuando sean relevantes.

Esto puede incluir:

- autenticación;
- autorización;
- protección de datos;
- privacidad;
- auditoría;
- integridad;
- disponibilidad;
- gestión de sesiones;
- restricciones de acceso;
- cumplimiento normativo.

Los requisitos de seguridad relevantes deberán ser explícitos
y verificables.

---

# 2. Entradas no confiables

Toda información proveniente de fuera del límite de confianza del
sistema deberá considerarse no confiable hasta ser validada.

Esto incluye:

- solicitudes HTTP;
- formularios;
- archivos;
- parámetros;
- headers;
- cookies;
- eventos;
- mensajes;
- APIs externas;
- webhooks;
- variables provenientes del cliente.

Las entradas deberán validarse antes de utilizarse en operaciones
sensibles.

---

# 3. Autenticación

Cuando un sistema requiera identificar usuarios o servicios,
el mecanismo de autenticación deberá definirse explícitamente
en el plan técnico.

No deberán implementarse mecanismos de autenticación improvisados
cuando existan soluciones estándar y suficientemente seguras.

Las credenciales nunca deberán almacenarse en texto plano.

---

# 4. Autorización

Autenticación y autorización deberán tratarse como conceptos
independientes.

Autenticación responde:

¿Quién eres?

Autorización responde:

¿Qué puedes hacer?

Toda operación protegida deberá verificar los permisos necesarios
en un límite confiable del sistema.

No deberá confiarse únicamente en restricciones implementadas
en la interfaz de usuario.

---

# 5. Principio de mínimo privilegio

Usuarios, servicios y componentes deberán recibir únicamente
los permisos necesarios para realizar sus funciones.

Se evitarán permisos globales o administrativos cuando no sean
necesarios.

---

# 6. Secretos

Los secretos no deberán almacenarse directamente en:

- código fuente;
- archivos versionados;
- pruebas;
- documentación;
- logs;
- mensajes de error.

Ejemplos de secretos:

- passwords;
- API keys;
- access tokens;
- refresh tokens;
- private keys;
- credenciales de bases de datos.

Los secretos deberán administrarse mediante mecanismos apropiados
para el entorno utilizado.

La prohibición de almacenar o insertar secretos directamente no impide
que una aplicación o prueba autorizada los utilice cuando sean
necesarios.

En esos casos, deberán suministrarse mediante mecanismos seguros del
entorno y evitar su exposición en código, archivos versionados, logs,
resultados de pruebas o documentación.

---

# 7. Datos sensibles

Los datos sensibles deberán identificarse cuando existan.

Su tratamiento deberá considerar:

- acceso;
- almacenamiento;
- transmisión;
- logs;
- backups;
- retención;
- eliminación.

El sistema deberá evitar almacenar información sensible que no sea
necesaria para cumplir sus requisitos.

---

# 8. Protección de datos en tránsito

Cuando exista comunicación a través de redes no confiables,
deberán utilizarse mecanismos apropiados para proteger la información
durante su transmisión.

Las decisiones concretas dependerán de la arquitectura y deberán
documentarse en el plan técnico cuando sean relevantes.

---

# 9. Protección de datos almacenados

Cuando la sensibilidad de los datos lo requiera, deberá evaluarse
la necesidad de protección adicional durante su almacenamiento.

La estrategia deberá definirse según:

- sensibilidad;
- amenazas;
- requisitos legales;
- infraestructura;
- impacto potencial.

---

# 10. Manejo seguro de errores

Los errores mostrados a consumidores externos no deberán revelar
innecesariamente:

- stack traces;
- credenciales;
- secretos;
- consultas internas;
- rutas internas;
- configuración;
- información sensible.

Los detalles necesarios para diagnóstico deberán registrarse
de forma segura cuando corresponda.

---

# 11. Logging seguro

Los logs deberán evitar registrar información sensible
innecesariamente.

Se deberá prestar especial atención a:

- passwords;
- tokens;
- cookies de sesión;
- headers de autorización;
- documentos sensibles;
- datos personales.

Cuando sea necesario registrar identificadores sensibles,
deberá evaluarse su anonimización o enmascaramiento.

---

# 12. Dependencias

Las dependencias externas forman parte de la superficie de riesgo
del sistema.

Antes de introducir una dependencia deberá evaluarse:

- necesidad;
- mantenimiento;
- procedencia;
- vulnerabilidades conocidas;
- impacto;
- permisos requeridos.

Las dependencias deberán mantenerse actualizadas según el nivel
de riesgo y necesidades del proyecto.

---

# 13. Configuración segura

Los valores predeterminados deberán favorecer configuraciones seguras
cuando sea razonable.

Las configuraciones sensibles deberán revisarse para cada entorno.

Se deberá evitar que configuraciones destinadas a desarrollo
se utilicen accidentalmente en producción.

---

# 14. Operaciones destructivas

Las operaciones destructivas o irreversibles deberán requerir
controles adecuados.

Ejemplos:

- eliminar información;
- sobrescribir datos;
- cerrar cuentas;
- revocar accesos;
- ejecutar migraciones destructivas.

Cuando el riesgo lo justifique deberán existir mecanismos adicionales
como confirmación, autorización o auditoría.

---

# 15. Integraciones externas

Las integraciones externas deberán considerarse límites de confianza.

El sistema deberá:

- validar respuestas cuando corresponda;
- manejar indisponibilidad;
- manejar respuestas inesperadas;
- limitar permisos;
- proteger credenciales;
- verificar autenticidad cuando sea aplicable.

---

# 16. Archivos

Cuando el sistema permita subir archivos deberá evaluarse:

- tipo de archivo;
- tamaño;
- nombre;
- extensión;
- contenido;
- almacenamiento;
- permisos;
- acceso posterior.

El nombre o extensión proporcionados por el usuario no deberán
considerarse evidencia suficiente del tipo real de contenido.

---

# 17. Base de datos

El acceso a datos deberá utilizar mecanismos que reduzcan riesgos
de inyección y modificaciones no autorizadas.

Cuando la tecnología lo permita deberán utilizarse:

- consultas parametrizadas;
- ORMs seguros;
- validación;
- restricciones de base de datos;
- permisos mínimos.

---

# 18. Seguridad del cliente

Las validaciones realizadas en el cliente deberán considerarse
una mejora de experiencia y no un límite de seguridad.

Las reglas críticas deberán verificarse nuevamente en un entorno
confiable.

Ejemplo:

Frontend:

"Este botón sólo aparece para administradores."

Esto NO demuestra que:

API:

"Este endpoint sólo puede ejecutarlo un administrador."

La API deberá realizar su propia autorización.

---

# 19. Fallo seguro

Cuando exista incertidumbre sobre permisos o estado de seguridad,
el comportamiento predeterminado deberá favorecer la opción segura.

Ejemplo:

Permiso desconocido
→ acceso denegado

y no:

Permiso desconocido
→ acceso permitido

---

# 20. Seguridad y agentes

Los agentes que implementen código no deberán:

- desactivar controles de seguridad para facilitar una implementación;
- insertar secretos reales;
- reducir validaciones sin justificación;
- otorgar permisos adicionales innecesarios;
- desactivar autenticación o autorización para hacer pasar pruebas;
- ignorar vulnerabilidades detectadas relevantes para la tarea.

Cuando una implementación requiera comprometer un control de seguridad,
el agente deberá detenerse y solicitar una decisión explícita.

---

# 21. Cambios sensibles

Los cambios relacionados con:

- autenticación;
- autorización;
- criptografía;
- secretos;
- permisos;
- sesiones;
- datos sensibles;
- operaciones destructivas;

deberán identificarse como cambios sensibles durante el plan
y las tareas.

Estos cambios podrán requerir validaciones adicionales.

---

# 22. Seguridad verificable

Los controles de seguridad relevantes deberán tener evidencia
de validación.

## Ejemplo ilustrativo

El siguiente ejemplo muestra cómo mantener trazabilidad entre un
requisito de seguridad, su criterio de aceptación y su prueba.

No representa un requisito real del proyecto.

SEC-001

Los usuarios no autenticados no podrán acceder a recursos privados.

AC-004

Una solicitud sin autenticación recibe una respuesta de acceso denegado.

TEST-004

Verifica acceso sin autenticación.

Resultado:

PASS


---

# 23. Revisión de seguridad

Antes de considerar completada una funcionalidad con impacto
de seguridad deberá verificarse:

- autenticación;
- autorización;
- validación de entradas;
- exposición de información;
- secretos;
- manejo de errores;
- logs;
- dependencias;
- operaciones sensibles.

La profundidad de la revisión deberá ser proporcional al riesgo.

---

# 24. Hallazgos de seguridad

Un hallazgo relevante deberá clasificarse y documentarse.

Estados recomendados:

OPEN
MITIGATED
ACCEPTED
NOT_APPLICABLE

Un riesgo no deberá considerarse resuelto únicamente porque
no produzca errores funcionales.

La aceptación explícita de un riesgo deberá quedar documentada
cuando corresponda.

El estado de un hallazgo no deberá interpretarse por sí mismo como
evidencia de cumplimiento.

`ACCEPTED` indica que el riesgo fue aceptado explícitamente, pero no
equivale automáticamente a que un requisito de seguridad esté satisfecho
ni autoriza por sí mismo un resultado de validación `PASS`.

La aceptación deberá documentar, cuando corresponda:

- responsable de la decisión;
- justificación;
- alcance;
- efecto sobre cualquier bloqueo existente.

Cuando aceptar un riesgo implique una excepción a una regla superior,
un cambio de requisito o un cambio de alcance, deberá seguirse la
autoridad y propagación de cambios definidas por la Constitution.

Un hallazgo `MITIGATED` deberá contar con evidencia suficiente para
determinar si la mitigación resolvió el riesgo o bloqueo correspondiente.

---

# Checklist de seguridad

Antes de validar una funcionalidad deberá verificarse, cuando aplique:

- [ ] Las entradas externas están validadas.
- [ ] La autenticación está correctamente aplicada.
- [ ] La autorización se verifica en límites confiables.
- [ ] Se aplica mínimo privilegio.
- [ ] No existen secretos en código o documentación versionada.
- [ ] Los datos sensibles están identificados.
- [ ] Los logs no contienen secretos ni exponen información sensible
      innecesariamente o sin protección adecuada.
- [ ] Los errores externos no revelan información interna innecesaria.
- [ ] Las operaciones destructivas tienen controles apropiados.
- [ ] Las integraciones externas se consideran límites no confiables.
- [ ] Las dependencias introducidas fueron evaluadas.
- [ ] Los controles de seguridad relevantes tienen evidencia.
- [ ] No existen hallazgos bloqueantes sin resolver.
