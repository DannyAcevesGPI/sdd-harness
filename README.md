# SDD Harness

Harness de Spec-Driven Development para proyectos con aprobaciones humanas,
trazabilidad y estado reconstruible sin leer el chat.

## Usar en este repositorio

1. Lee [`AGENTS.md`](AGENTS.md), [la Constitución](.spec/constitution.md) y
   el [handoff vivo](handoff.md).
2. Abre el command de la fase en [el índice](docs/index.md).
3. Antes de implementar, exige SPEC, PLAN y TASKS aprobados con ledger vigente.

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest discover -s tests
python3 src/check_harness_state.py
```

## Usar en otro proyecto

Requiere Python 3 para las herramientas del Harness; no impone el stack de la
aplicación. Desde este repositorio:

```bash
python3 src/adopt_harness.py --list
python3 src/adopt_harness.py /ruta/al/proyecto
```

La CLI copia una base reusable comprobable y crea un handoff e índice limpios.
Consulta la [guía de adopción](docs/adoption.md) antes de ajustar standards y
comenzar la primera feature.

## Referencias

- [Quickstart](docs/quickstart.md)
- [Reconstrucción de estado](docs/state-reconstruction.md)
- [Flujo TDD](docs/tdd.md)
- [Referencia extensa](docs/reference.md)
- [Changelog](CHANGELOG.md)

La historia auditada y la evidencia de features permanecen bajo demanda en
[`docs/index.md`](docs/index.md); no son parte del bootstrap diario.
