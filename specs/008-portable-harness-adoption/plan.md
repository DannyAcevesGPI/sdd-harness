# Plan Técnico: Adopción portable del Harness

**ID:** PLAN-008  
**SPEC relacionada:** SPEC-008 v0.2.0  
**Estado:** APPROVED  
**Versión:** 0.1.0  
**Fecha:** 2026-09-30

---

# 1. Precondiciones

- [x] SPEC-008 v0.2.0 está `APPROVED`; DECISION-003 y huella pasan el comprobador.
- [x] No hay aclaraciones bloqueantes; los requisitos MUST tienen AC.
- [x] La excepción transitoria solo permite ledger y proyecciones de
  estado/enlaces antes de `/implement`.

# 2. Resumen técnico

Unificar el contrato de metadata por fase, hacer explícito y ejecutable el
paquete de adopción, probarlo en aislamiento, añadir un chequeo CI local al
repo y ampliar el diagnóstico de estado al handoff/índice. El README será una
entrada breve; el detalle educativo permanecerá en documentación bajo demanda.

# 3. Requisitos cubiertos

| Requisito | Cobertura técnica |
|-----------|-------------------|
| FR-001, BR-001 | Reglas de mutación para ledger y proyecciones, sin autoaprobación |
| FR-002, NFR-002, BR-002 | Lista reusable única y adopción segura; legado local no copiado |
| FR-003 | Prueba con repo temporal y aprobaciones sintéticas etiquetadas |
| FR-004 | Workflow CI con suite y comprobador, sin gates humanos automáticos |
| FR-005 | Estado estructurado compacto y comprobación de handoff/índice |
| FR-006, NFR-001 | README breve, quickstart e índice; referencia larga enlazada |
| SEC-001 | Allowlist de copia, destino confinado y fixtures sin secretos |

# 4. Contexto técnico existente

- Repositorio de documentación SDD con Python 3 estándar en `src/` y
  `unittest` en `tests/`; sin framework, base de datos ni package manager.
- `src/check_harness_state.py` ya verifica ledgers/huellas y excluye seis
  carpetas históricas exactas, pero no handoff/índice.
- `docs/adoption.md` enumera una base incompleta: omite checker, tests y guía
  de reconstrucción. `docs/state-reconstruction.md` aún contiene referencias
  locales de la transición SPEC-007.
- `AGENTS.md` tiene 171 líneas, `handoff.md` 150 aprox. y README 1,285.
- No hay workflow CI ni instalador; `origin` apunta a GitHub. No hay ADR
  aplicables.

# 5. Decisiones técnicas

## DEC-001 — Metadata operativa permitida por fase

**Decisión:** Actualizar `AGENTS.md` y commands de SPEC/clarificación/PLAN/TASKS
para permitir solo `decisions.json` de la feature y cambios de estado/enlaces
en `handoff.md`/`docs/index.md` antes de `/implement`. Mantener prohibidos
código, pruebas y cambios sustantivos. El registro vacío se crea con la SPEC;
la aprobación humana se registra después de recibirse y antes del gate siguiente.

**Justificación:** FR-001/FR-005 y AC-001 eliminan la contradicción actual.
**Alternativas:** Aplazar el ledger hasta `/implement` (rompe gates); permitir
cualquier documentación (demasiado amplio).  
**Consecuencias:** Las proyecciones deberán mantenerse tras cada transición.
**ADR:** NO.

## DEC-002 — Adopción con allowlist y CLI local

**Decisión:** Añadir un comando Python estándar de adopción que copie solo la
base reusable declarada a un destino elegido, rechace colisiones/symlinks
inseguros y genere handoff/índice iniciales sin historia. El mismo catálogo
de rutas alimentará listado, copia y prueba; `docs/adoption.md` documentará
requisitos Python, adaptación de standards y ejecución local. No copiar el
README ni validaciones históricas como estado. El workflow CI de GitHub será
opcional para destinos GitHub, no parte del núcleo agnóstico al proveedor.

**Justificación:** FR-002/SEC-001; reduce omisiones manuales y deriva la guía
de una base comprobable.  
**Alternativas:** Lista solo en Markdown (puede divergir); paquete externo
(dependencia y publicación innecesarias).  
**Consecuencias:** Una utilidad local adicional, sin runtime de aplicación
impuesto salvo Python para herramientas del Harness.  
**ADR:** NO.

## DEC-003 — Diagnóstico de proyecciones

**Decisión:** Reutilizar `src/check_harness_state.py` y añadir un bloque JSON
pequeño de estado operativo en `handoff.md`, parseado estructuralmente. El
checker derivará features activas, fase, siguiente gate y features validadas
desde SPEC/PLAN/TASKS/validation; comparará el bloque y los enlaces del índice.
Un bloque ausente, malformado o discordante será FAIL con archivo/causa. El
checker seguirá siendo de solo lectura y no escribirá aprobaciones ni resúmenes.

**Justificación:** FR-005/AC-005; evita interpretar prosa libre como estado
canónico.  
**Alternativas:** Regex sobre todo el handoff (frágil); nuevo servicio de
estado (excesivo).  
**Consecuencias:** Cada proyecto adoptado necesita un bloque inicial válido;
DEC-002 lo genera. Se revisará compatibilidad con las validaciones legadas de
formato variable.  
**ADR:** NO.

## DEC-004 — CI del repositorio fuente

**Decisión:** Añadir un workflow de GitHub Actions que instale Python para las
herramientas, ejecute `unittest` (incluida la prueba de adopción) y el checker
en pull requests y pushes relevantes. El workflow usará permisos mínimos,
sin secretos ni autoescritura. Versiones concretas de acciones oficiales se
verificarán al implementar.

**Justificación:** FR-004/AC-004 y remoto GitHub real.  
**Alternativas:** Hook local obligatorio (fácil de omitir); plataforma nueva
(sin necesidad).  
**Consecuencias:** CI informa PASS/FAIL técnico, no aprobación humana ni
`FEATURE STATUS: VALIDATED`.  
**ADR:** NO.

## DEC-005 — Documentación de entrada corta

**Decisión:** Reducir README a oferta literal, comandos de inicio y enlaces;
trasladar el detalle largo vigente a referencia dedicada bajo `docs/`,
revisando enlaces y eliminando duplicación. Mantener `docs/quickstart.md` como
bootstrap de agente y `docs/adoption.md` como procedimiento de proyecto nuevo.

**Justificación:** FR-006/NFR-001, sin perder información útil.  
**Alternativas:** Borrar detalle (pierde referencia); mantener 1,285 líneas
como entrada principal (dificulta navegación).  
**Consecuencias:** Enlaces internos deberán comprobarse.  
**ADR:** NO.

# 6. Arquitectura propuesta

| Componente | Responsabilidad | Cambio |
|------------|-----------------|--------|
| `src/check_harness_state.py` | Ledger y consistencia de proyecciones | MODIFY |
| `src/adopt_harness.py` | Lista/copia segura de base reusable | CREATE |
| `tests/test_check_harness_state.py` | Casos de estado obsoleto/legado | MODIFY |
| `tests/test_adopt_harness.py` | Instalación aislada y casos negativos | CREATE |
| `.github/workflows/harness.yml` | Ejecutar controles existentes | CREATE |
| `handoff.md`, `docs/index.md` | Proyecciones compactas | MODIFY |
| Commands, AGENTS, guías | Instrucciones coherentes | MODIFY |
| `README.md`, `docs/reference.md` | Entrada y referencia | MODIFY/CREATE |

Flujo: source repo -> allowlist -> destino aislado + handoff/índice iniciales
-> primera SPEC + ledger vacío -> decisión humana -> gate registrado -> checker
-> siguiente fase. CI solo ejecuta pruebas y checker sobre el repo fuente.

# 7. Modelo de datos

Sin base de datos ni migraciones. El ledger conserva el contrato JSON actual.
El bloque del handoff será un objeto JSON de versión conocida con lista de
features activas (ID, fase, siguiente acción) y lista de IDs validados. El
detalle/evidencia permanece en `specs/`; el bloque es proyección, no autoridad.
Las carpetas `specs/` del destino comienzan vacías. Cambio destructivo: NO.

# 8. Interfaces y contratos

- CLI de adopción: listar base reusable y copiar a destino explícito; salida
  clara ante colisión, ruta insegura o falta de archivo fuente.
- CLI de diagnóstico existente: `python3 src/check_harness_state.py` conserva
  exit 0/1 y añade códigos para bloque/índice/estado discordante.
- CI: ejecuta la misma suite y diagnóstico local; no consume credenciales.
- Handoff: bloque JSON versionado y visible, más enlaces humanos compactos.
- Índice: enlaces de feature bajo convención estable, comparados con `specs/`.

# 9. Validación de entradas

El adoptador valida destino, colisiones y symlinks antes de copiar; usa solo
rutas de allowlist. El checker valida forma del bloque, IDs, estados, rutas y
enlaces antes de comparar; un dato ambiguo falla cerrado. No ejecuta contenido
del repo destino. Datos de prueba sintéticos quedan en directorios temporales.

# 10. Seguridad

SEC-001: no leer/copiar `specs/` históricos, handoff local, secretos, logs ni
auditorías. El destino no se sobrescribe parcialmente si hay colisión conocida;
el plan de copia se valida antes de mutar. Symlinks fuera de raíz se rechazan.
No hay autenticación, autorización externa, red ni operación destructiva.
GitHub Actions con permisos de lectura y sin secretos de aplicación.

# 11. Estrategia de pruebas y TDD

| AC | Nivel / caso previsto | TDD |
|----|-----------------------|-----|
| AC-001 | Unit/documental: ledger vacío permitido y gates posteriores | RED/GREEN para checker; revisión de commands |
| AC-002 | Integration: copiar base y ejecutar bootstrap con feature 001 nueva | RED/GREEN, `unittest` |
| AC-003 | Integration: repo temporal, gate sintético, registro malo y salida | RED/GREEN, `unittest` |
| AC-004 | CI/static: workflow invoca suite y checker; fallo negativo | Prueba estática/ejecución local; YAML de CI no tiene RED productivo independiente |
| AC-005 | Unit: handoff/índice ausente, corrupto, atrasado y válido | RED/GREEN, `unittest` |
| AC-006 | Revisión documental y conteo de líneas | Sin TDD; verificación de enlaces/lectura |
| AC-007 | Integration/security: allowlist excluye historia y symlinks | RED/GREEN, `unittest` |

Comando previsto: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m
unittest discover -s tests`, más `python3 src/check_harness_state.py`. Guardar
RED/GREEN por TEST en `specs/008.../evidence/`; fixtures sintéticos no son
decisiones humanas. La regresión incluye los 25 tests actuales y checker
SPEC-007/008.

# 12. Observabilidad

Salida de CLI/CI con código de fallo, ruta y causa. Evidencia detallada por
feature; sin logs persistentes ni datos sensibles en handoff.

# 13. Impacto en el repositorio

**CREATE:** `src/adopt_harness.py`, `tests/test_adopt_harness.py`,
`.github/workflows/harness.yml`, `docs/reference.md`, evidencia SPEC-008.

**MODIFY:** `src/check_harness_state.py`, su test, `AGENTS.md`, commands de
SPEC/clarify/plan/tasks/implement/validate cuando aplique, templates afectados,
`docs/adoption.md`, `docs/state-reconstruction.md`, `docs/quickstart.md`,
`docs/index.md`, `handoff.md`, `README.md`, `CHANGELOG.md` y artefactos de estado
de SPEC-008. No tocar código de la feature de prueba.

**REUSE:** `.spec/`, Python estándar, `unittest`, ledger SPEC-007/008.  
**REMOVE:** ninguno; la referencia larga cambia de lugar, no se pierde.

# 14. Dependencias y configuración

No hay dependencia de paquete nueva. Python 3 (versión compatible con sintaxis
existente) es requisito de herramientas, no del stack de aplicación. GitHub
Actions usa acciones oficiales de checkout/setup-python; versiones se fijan y
verifican en implementación. Sin variables secretas ni configuración nueva de
aplicación.

# 15. Migración y compatibilidad

**Breaking change:** YES en el formato operativo de `handoff.md`: requiere un
bloque estructurado que el adoptador genera y el checker exige. Se migra el
handoff de este repo y se documenta el formato. No se reescriben aprobaciones
legadas. Una feature en DRAFT puede tener ledger vacío; las aprobaciones siguen
siendo humanas. Evaluar impacto sobre SPEC-007 y repetir pruebas/validaciones
afectadas antes de cerrar SPEC-008.

# 16. Manejo de errores

| Escenario | Resultado |
|-----------|-----------|
| Destino con colisión o symlink inseguro | Adoptador falla antes de copiar |
| Fuente reusable faltante | Error con ruta, sin paquete parcial |
| Handoff/índice sin bloque o desactualizado | Checker FAIL con causa/ruta |
| Ledger vacío en DRAFT | Válido, no concede gate |
| Gate aprobado sin evento vigente | Checker FAIL |
| CI no disponible | No se informa como PASS; ejecutar local y reportar límite |

# 17. Riesgos técnicos

## RISK-001 — Proyección de estado frágil

**Impacto:** MEDIUM. **Probabilidad:** MEDIUM.  
**Mitigación:** Bloque JSON versionado, parser estructurado y fixtures para
estados válidos/obsoletos; prosa fuera del contrato no decide gates.

## RISK-002 — Copia accidental de historia o datos sensibles

**Impacto:** HIGH. **Probabilidad:** LOW.  
**Mitigación:** Allowlist única, rechazo de symlinks y prueba de no contaminación
en destino aislado.

# 18. Aclaraciones técnicas y ADR

Ninguna aclaración bloqueante. No se requiere ADR: son herramientas y
convenciones locales, sin nuevo servicio ni cambio de arquitectura de app.

# 19. Orden de implementación

1. Contrato de metadata por fase y documentación de adopción/estado.
2. Adoptador y pruebas RED/GREEN en destino temporal.
3. Checker de handoff/índice y pruebas RED/GREEN; migrar proyecciones.
4. Workflow CI y verificación de ejecución/seguridad.
5. README/referencia, enlaces, regresión y evidencia final.

# 20. Criterios para avanzar a Tasks

- [x] SPEC aprobada y requisitos MUST cubiertos.
- [x] Diseño, contratos, seguridad, pruebas e impacto definidos.
- [x] Compatibilidad, riesgos y ADR evaluados; sin aclaraciones bloqueantes.
- [x] Aprobación humana explícita de PLAN-008.

# 21. Estado del plan

**Estado actual:** APPROVED  
**Aprobado por:** Usuario responsable del proyecto  
**Fecha de aprobación:** 2026-09-30  
**Registro durable:** DECISION-004 en `decisions.json`.

La aprobación humana fue "Listo aprobado" en respuesta al PLAN-008 v0.1.0.
Autoriza preparar TASKS; no autoriza implementación antes de aprobar TASKS.
