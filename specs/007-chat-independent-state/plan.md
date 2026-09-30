# Plan Técnico: Estado reconstruible sin chat

**ID:** PLAN-007  
**SPEC relacionada:** SPEC-007  
**Estado:** APPROVED  
**Versión:** 0.2.0  
**Fecha:** 2026-09-30

---

# 1. Precondiciones

- [x] SPEC-007 está `APPROVED` y no tiene aclaraciones bloqueantes.
- [x] Requisitos MUST y criterios de aceptación están definidos.
- [x] El alcance y la política de legado están documentados.

# 2. Resumen técnico

Documentar un contrato de registro de decisiones/aprobaciones por feature,
actualizar las instrucciones de cada fase para mantenerlo y agregar una
comprobación local que detecte registros ausentes, contenido aprobado cambiado
y referencias de estado inconsistentes. El estado vivo seguirá siendo un índice
compacto que enlaza artefactos y evidencia.

# 3. Requisitos cubiertos

| Requisito | Cobertura en el plan |
|-----------|----------------------|
| FR-001 | Registro por feature con actor, fecha, decisión, alcance y huella del artefacto |
| FR-002 | Eventos explícitos de decisión, sustitución y revocación |
| FR-003 | Bootstrap desde índice/handoff y artefactos de feature |
| FR-004 | Comprobador local de vínculos, huellas y estados |
| FR-005 | Handoff breve; detalle en registros y evidencia dedicados |
| FR-006 | Etiqueta de legado no verificable para SPEC-001 a SPEC-006 |
| NFR-001 | Lectura bajo demanda desde índices |
| NFR-002 | Contrato documentado y comprobación repetible |
| SEC-001 | Campos mínimos, revisión de secretos y ausencia de tokens |
| BR-001 | Registro posterior a decisión humana explícita |
| BR-002 | Commit/estado no equivalen a aprobación |

# 4. Contexto técnico existente

- Repositorio documental SDD con `AGENTS.md`, `handoff.md`, `.spec/` y `specs/`.
- No hay aplicación web, base de datos, package manager ni framework.
- Runtime y pruebas disponibles: Python 3, `unittest` en `tests/`.
- `docs/index.md` y `docs/quickstart.md` sirven de entrada; hoy enumeran solo
  SPEC-001 a SPEC-003. `handoff.md` tampoco refleja SPEC-004 a SPEC-006.
- Las aprobaciones están en secciones de SPEC/PLAN/TASKS; algunas indican solo
  "usuario en esta conversación". No existe ledger ni comprobador de gates.
- No se detectaron ADR previos relevantes.

# 5. Decisiones técnicas

## DEC-001 — Registro estructurado por feature

**Decisión:** Usar `specs/<feature-id>/decisions.json` con eventos de aprobación,
aclaración decisoria, sustitución o revocación. Cada evento tendrá ID estable,
tipo, actor humano, fecha, decisión textual, artefacto afectado, alcance y
referencia a la versión aprobada. Para aprobaciones nuevas, esa referencia será
una huella SHA-256 del contenido autorizado normalizado. La normalización solo
ignorará campos operativos definidos de antemano: estados de documento/tarea,
marcas de checklists de ejecución y metadata de aprobación. Todo otro cambio,
incluidos títulos, alcance, dependencias y criterios, alterará la huella. El
JSON queda separado para evitar auto-referencia. La guía y las pruebas fijarán
el algoritmo exacto y sus casos adversos antes de usarlo en un gate.

**Justificación:** JSON admite validación estructurada con la biblioteca estándar
y mantiene el registro fuera del artefacto aprobado. Relacionado con FR-001,
FR-002, NFR-002 y BR-001.

**Alternativas:** Markdown libre (difícil de verificar); servicio externo
(innecesario).  
**Consecuencias:** Hay un archivo adicional por feature activa; la huella
detecta cambios de contenido autorizado, pero no autentica criptográficamente
a una persona. Los campos operativos permitidos requieren una lista cerrada.  
**Requiere ADR:** NO.

## DEC-002 — Comprobador local de estado

**Decisión:** Crear un script Python de solo lectura que revise features nuevas,
eventos, huellas y referencias desde la raíz del repo; reporte `PASS` o fallos
con rutas y códigos claros. El script no autoaprueba ni reescribe artefactos.

**Justificación:** FR-003/FR-004 requieren detectar omisiones y cambios de forma
repetible. Se reutiliza Python/unittest existente.  
**Alternativas:** Checklist puramente manual (no exige ni detecta omisiones);
hook obligatorio (no solicitado y dependería del entorno).  
**Consecuencias:** Los agentes deben ejecutar el comando en los gates; sigue
siendo necesaria revisión humana.  
**Requiere ADR:** NO.

## DEC-003 — Índice compacto y política prospectiva

**Decisión:** `handoff.md` mostrará feature/fase/bloqueos/siguiente paso y enlaces;
`docs/index.md` localizará todas las features. Una guía dedicada definirá cómo
registrar y reconstruir estado. SPEC-001 a SPEC-006 conservarán sus estados,
pero las aprobaciones cuya única prueba sea el chat se rotularán como legado no
verificable; no se calcularán huellas retroactivas como si fueran aprobaciones.

**Justificación:** FR-005/FR-006 y decisión Q-001.  
**Alternativas:** Copiar todo a handoff (aumenta contexto); reaprobar legado
(rechazado por usuario).  
**Consecuencias:** La comprobación distingue legado de registros completos
posteriores.  
**Requiere ADR:** NO.

# 6. Arquitectura propuesta

| Componente | Responsabilidad | Cambio |
|------------|-----------------|--------|
| `specs/<id>/decisions.json` | Eventos durables de la feature | CREATE |
| `src/check_harness_state.py` | Diagnóstico local de registros/gates | CREATE |
| `tests/test_check_harness_state.py` | Casos positivos y negativos | CREATE |
| `docs/state-reconstruction.md` | Contrato y bootstrap sin chat | CREATE |
| `.spec/commands/`, `.spec/templates/` | Instrucciones de captura y consulta | MODIFY |
| `AGENTS.md`, `docs/quickstart.md` | Punto de entrada al registro | MODIFY |
| `handoff.md`, `docs/index.md` | Estado vivo e índice completos | MODIFY |
| `.spec/constitution.md` | Aclarar persistencia de decisiones humanas | MODIFY |

Flujo: decisión humana explícita -> registro enlazado al artefacto ->
actualización de estado -> comprobación local -> siguiente fase. En bootstrap:
AGENTS/constitución -> handoff/índice -> artefacto/registro -> comprobador ->
acción autorizada. La precedencia constitucional no cambia.

# 7. Modelo de datos

No hay base de datos ni migración. El JSON por feature almacena una lista de
eventos con `id`, `kind`, `actor`, `date`, `decision`, `scope`, `artifact`,
`artifact_sha256`, `supersedes` (opcional) y `source` (referencia descriptiva,
sin depender de que el chat esté accesible). Una aprobación nueva exige todos
los campos salvo `supersedes`. Una aclaración sin artefacto versionado usa
campos aplicables y no se interpreta como gate. Los eventos no se borran:
revocaciones y sustituciones se agregan como eventos nuevos.

La huella se calcula sobre el contenido autorizado normalizado del artefacto.
La normalización conservará orden, texto y estructura; solo reemplazará por un
valor fijo los campos operativos conocidos por tipo de documento. En TASKS,
los cambios de estado `TODO`/`IN_PROGRESS`/`DONE`, estado general y marcas de
checklists no cambiarán la huella; un cambio de trabajo autorizado sí. La
evidencia nueva vivirá en archivos dedicados, no en bloques libres de TASKS.
Si el parser encuentra un formato ambiguo o un campo operativo desconocido,
fallará cerrado. El registro contiene el texto y alcance de la aprobación
humana; el comprobador recalcula la huella sin consultar el chat.
`artifact_sha256` no se aplica al legado no verificable.

**¿Requiere migración?:** NO.  
**Cambio destructivo:** NO.

# 8. Interfaces y contratos

- Entrada: `python3 src/check_harness_state.py` desde la raíz del repo.
- Salida: resumen legible con resultado, ruta/código por discrepancia y código
  de salida distinto de cero ante un gate nuevo sin registro válido.
- `decisions.json`: contrato versionado y ejemplos en la guía; referencias de
  artefacto relativas a la raíz del repo. Sin API externa.
- La guía documentará el procedimiento de captura humana, cálculo de huella,
  actualización de estado y lectura en sesión nueva.

# 9. Validación de entradas

El comprobador validará JSON, campos obligatorios, tipos, IDs únicos, rutas
dentro del repo, huellas de 64 hexadecimales y relación entre evento y estado.
Una ruta ausente, fuera de raíz o con contenido cambiado será error explícito.
No ejecutará contenido de registros ni seguirá enlaces externos.

# 10. Seguridad

No se agregan autenticación ni secretos. El actor es una atribución documental,
no prueba de identidad; ni Git ni SHA-256 sustituyen autorización humana. Se
limita el registro a información necesaria, se evitan tokens y transcripciones
largas, y se revisan rutas para impedir lectura fuera del repo. SEC-001 se
verifica en documentación y fixtures. No hay operaciones destructivas.

# 11. Estrategia de pruebas

| Criterio | Nivel y caso previsto | TDD |
|----------|------------------------|-----|
| AC-001 | Unit/integration: gate con evento y huella válidos | RED/GREEN con `python3 -m unittest discover -s tests` |
| AC-002 | Integración manual: sesión simulada solo con repo y guía | No automatizable por completo; checklist reproducible |
| AC-003 | Unit: cambio de contenido autorizado invalida huella; estado operativo no | RED/GREEN |
| AC-004 | Unit: registro ausente, ruta inválida o resumen atrasado | RED/GREEN para registro; revisión manual del resumen |
| AC-005 | Unit + revisión documental: legado marcado, sin huellas inventadas | RED/GREEN para clasificador; inspección de docs |
| AC-006 | Revisión de fixtures/registros y búsqueda de secretos conocidos | Revisión manual documentada |

Los tests automatizables se escribirán durante `/implement`, se ejecutarán
primero en RED y después en GREEN, con evidencia en `specs/007.../evidence/`.
El comprobador deberá probarse con fixtures temporales, sin modificar el repo
real ni requerir red. Validación final incluye el propio comprobador.

# 12. Observabilidad

La salida del script y la evidencia de RED/GREEN se guardarán en la carpeta de
evidencia. No se añaden logs persistentes ni telemetría.

# 13. Impacto en el repositorio

**CREATE:** `decisions.json` de SPEC-007, guía, comprobador, tests y evidencia.

**MODIFY:** constitución, commands de specify/clarify/plan/tasks/implement/
validate, templates de SPEC/PLAN/TASKS, AGENTS, handoff, índice y quickstart.
`CHANGELOG.md` se actualizará solo si el proceso vigente lo requiere.

**REUSE:** directorios `specs/`, estados SDD, `unittest`, documentación y
evidencia dedicados. **REMOVE:** ninguno.

# 14. Dependencias

Ninguna nueva. Python 3 y su biblioteca estándar son suficientes.

# 15. Configuración

Ninguna variable ni secreto nuevo.

# 16. Migración y compatibilidad

**Breaking changes:** YES para el proceso de aprobación prospectivo: gates
nuevos requerirán registro completo. El legado permanece visible y señalado
como no verificable, sin invalidar retrospectivamente features validadas.
SPEC-007 es la transición: sus aprobaciones previas a la implementación del
protocolo se consignan en el propio artefacto y se reflejarán como transición,
sin fingir que ya cumplieron el comprobador nuevo.

# 17. Manejo de errores

| Escenario | Comportamiento |
|-----------|----------------|
| JSON inválido o campo ausente | Error específico; gate no verificado |
| Huella no coincide | Aprobación no aplicable al contenido actual |
| Dos eventos vigentes contradictorios | Reportar conflicto; detener gate |
| Feature de legado | Advertencia de procedencia, no aprobación inventada |
| Handoff desactualizado | Reportar discrepancia y señalar artefacto fuente |

# 18. Riesgos técnicos

## RISK-001 — Huella auto-referencial

**Impacto:** MEDIUM. **Probabilidad:** MEDIUM.  
**Mitigación:** Normalización de lista cerrada, parser que falla cerrado y
pruebas para cambios permitidos y cambios sustantivos.

## RISK-002 — Falsa certeza de identidad

**Impacto:** MEDIUM. **Probabilidad:** MEDIUM.  
**Mitigación:** Documentar que el registro y la huella acreditan integridad y
trazabilidad interna, no autenticación humana independiente.

# 19. Aclaraciones técnicas

Ninguna bloqueante.

# 20. ADR requeridos

Ninguno: se amplía el workflow documental local sin introducir una tecnología
ni un límite arquitectónico nuevo.

# 21. Orden de implementación

1. Definir y probar el contrato de registro/comprobador en RED/GREEN.
2. Integrar instrucciones, templates y constitución con el contrato.
3. Actualizar guías, índice, handoff y tratamiento del legado.
4. Ejecutar reconstrucción limpia, pruebas y validación final.

# 22. Criterios para avanzar a Tasks

- [x] SPEC aprobada; requisitos MUST cubiertos.
- [x] Contrato, seguridad, impacto y estrategia de pruebas definidos.
- [x] Dependencias, compatibilidad, riesgos y ADR evaluados.
- [x] No hay aclaraciones técnicas bloqueantes.
- [x] Nueva aprobación humana explícita de PLAN-007 versión 0.2.0.

# 23. Estado del plan

**Estado actual:** APPROVED  
**Aprobado por:** Usuario responsable del proyecto  
**Fecha de aprobación:** 2026-09-30  
**Decisión explícita:** "Ok entonces apruebo el plan" tras la explicación de
la revisión 0.2.0.  
**Alcance aprobado:** PLAN-007 versión 0.2.0, incluida la normalización limitada
de campos operativos y el comprobador que falla cerrado.

**Historial:** El usuario aprobó explícitamente PLAN-007 versión 0.1.0 el
2026-09-30 con la respuesta "aprobado" para preparar TASKS. Esa aprobación no
cubre la revisión 0.2.0: se corrigió la huella para distinguir cambios de
estado operativo de cambios al trabajo autorizado.

La aprobación del PLAN no autoriza implementación antes de aprobar TASKS.
