# Harness Adoption Guide

Guia para usar este SDD Harness en un proyecto nuevo sin arrastrar historia,
evidencia ni decisiones locales de este repositorio.

## 1. Que copiar

Copia la base del Harness:

```text
.spec/
AGENTS.md
docs/quickstart.md
docs/index.md
docs/tdd.md
docs/agents/
```

Opcionalmente copia `README.md` como referencia editorial, pero adaptalo al
producto real del proyecto destino.

## 2. Que adaptar

Actualiza estos archivos antes de iniciar trabajo real:

- `AGENTS.md`: nombre del repo, rutas, reglas operativas locales y limites de
  lectura.
- `.spec/standards/`: ajusta arquitectura, coding, testing y security al stack
  real.
- `.spec/templates/`: manten la estructura SDD, pero adapta campos si el equipo
  necesita metadatos adicionales.
- `docs/index.md`: conserva el indice, pero reemplaza enlaces que solo existan
  en este repo.
- `README.md`: explica el producto del nuevo proyecto y enlaza el flujo SDD.

El Harness es proceso, no stack. Puede usarse con Python, TypeScript, mobile,
backend, data, infraestructura u otro entorno siempre que PLAN y TASKS reflejen
las herramientas reales.

## 3. Que no copiar como estado propio

No copies como verdad del proyecto destino:

- `handoff.md` con estado vivo de este repo.
- `specs/*` ya ejecutados.
- carpetas `specs/*/evidence/`.
- auditorias, validaciones o findings historicos.
- logs, salidas de comandos, capturas o datos de otro proyecto.
- secretos, tokens, credenciales, llaves privadas o informacion sensible.

Puedes usar esos archivos como ejemplo, pero el nuevo proyecto debe generar su
propio estado, evidencia y validaciones.

## 4. Inicializar un proyecto nuevo

1. Copia la base reusable indicada en la seccion 1.
2. Crea un `handoff.md` nuevo y breve con el estado inicial del proyecto.
3. Deja `specs/` vacio o con un `.gitkeep` si necesitas versionar la carpeta.
4. Revisa `.spec/constitution.md` y confirma que el equipo acepta los gates.
5. Ajusta standards al stack real.
6. Actualiza README e indice documental.
7. Haz un commit base antes de iniciar la primera feature.

`handoff.md` debe funcionar como estado vivo: resumen actual, enlaces a evidencia
y bloqueos activos. El detalle largo debe vivir en `docs/` o en la carpeta de la
feature correspondiente.

## 5. Primera feature desde cero

Para una nueva funcionalidad:

1. Idea o solicitud humana.
2. Ejecuta `/specify` y crea `specs/<feature-id>/spec.md`.
3. Resuelve aclaraciones con `/clarify` si hay ambiguedad.
4. Obtén aprobacion humana de SPEC.
5. Ejecuta `/plan` y crea `plan.md`.
6. Obtén aprobacion humana de PLAN.
7. Ejecuta `/tasks` y crea `tasks.md`.
8. Obtén aprobacion humana de TASKS.
9. Ejecuta `/implement` siguiendo tareas y dependencias.
10. Registra evidencia en `specs/<feature-id>/evidence/`.
11. Cierra TASKS como `COMPLETED`.
12. Ejecuta `/validate` y crea `validation.md`.

La regla operativa se mantiene:

```text
No implementation without an approved SPEC, PLAN and TASKS.
```

Para cambios de comportamiento automatizable, aplica TDD durante `/implement`
después de esos gates. Consulta la [guía TDD](tdd.md) para aplicarlo a tu stack.

## 6. Evidencia por feature

Cada feature debe guardar su evidencia en:

```text
specs/<feature-id>/evidence/
```

Incluye comandos relevantes, resultados, decisiones de ejecucion y enlaces a
archivos modificados. Evita pegar salidas enormes en `handoff.md`; el handoff
solo debe enlazar la evidencia viva.

## 7. Uso con agentes

Al iniciar una sesion en el proyecto destino, el agente debe leer:

1. `AGENTS.md`
2. `.spec/constitution.md`
3. `handoff.md`
4. el command SDD aplicable
5. standards relevantes
6. artefactos de la feature activa

Para subagentes y hooks, conserva las guias en `docs/agents/` y adapta ejemplos
a las herramientas disponibles en el proyecto destino.

## 8. Checklist de adopcion

- [ ] Base reusable copiada.
- [ ] `handoff.md` nuevo creado.
- [ ] Evidencia historica no copiada como estado propio.
- [ ] Standards ajustados al stack.
- [ ] README e indice actualizados.
- [ ] Primer SPEC creado antes de implementar.
- [ ] Secretos y datos sensibles excluidos.
