# Estado reconstruible sin chat

El chat transmite decisiones; los archivos del repositorio conservan su
resultado. Una sesion nueva no necesita leer conversaciones anteriores para
decidir el siguiente paso. El registro no autentica criptograficamente a una
persona ni sustituye la aprobacion humana explicita.

## Bootstrap de una sesion nueva

1. Leer `AGENTS.md`, `.spec/constitution.md` y `handoff.md`.
2. Consultar `docs/index.md` para localizar la feature activa y las validadas.
3. Ejecutar `git status --short --branch`: el worktree puede contener estado
   posterior al ultimo commit. Para otro clon, primero deben versionarse los
   artefactos; nunca se hace un commit automatico.
4. Leer `spec.md`, `plan.md`, `tasks.md` y `decisions.json` de la feature activa,
   mas `validation.md` si existe. Abrir `evidence/` solo bajo demanda.
5. Ejecutar `python3 src/check_harness_state.py`. Ante FAIL, no inferir
   autorizacion desde el chat, un commit o un campo `APPROVED`; resolver el
   conflicto en el nivel dueno.
6. Determinar fase, gate vigente, bloqueos y proxima accion. Leer completo el
   command de esa fase y los standards relevantes.

`handoff.md` solo indica estado vivo y enlaces. Si discrepa con los artefactos,
reportar la discrepancia y corregir el indice; no avanzar silenciosamente.

## Registro por feature

Desde SPEC-007, cada feature tiene `specs/<feature-id>/decisions.json`:

```json
{
  "schema_version": 1,
  "events": [
    {
      "id": "DECISION-001",
      "kind": "APPROVAL",
      "actor": "Responsable humano",
      "date": "2026-09-30",
      "decision": "Aprobado SPEC-008",
      "scope": "SPEC-008 version 0.1.0",
      "artifact": "specs/008-example/spec.md",
      "artifact_sha256": "<64 caracteres hexadecimales calculados>",
      "source": "Decision humana explicita recibida y registrada"
    }
  ]
}
```

El ejemplo ilustra la forma; no es una aprobacion real. Los campos de texto
deben contener el resultado y alcance concretos, no solo "en esta
conversacion". `artifact` apunta a `spec.md`, `plan.md` o `tasks.md` de la misma
feature. Fechas en ISO `YYYY-MM-DD`; IDs unicos en orden, sin borrar eventos.
Crear el ledger con `"events": []` al crear una feature nueva, aun si su SPEC
esta en DRAFT; agregar eventos solo tras una decision humana real.
`APPROVAL` habilita un gate solo tras una decision humana explicita. Para
reemplazarlo, el nuevo evento lleva `supersedes` con el ID activo; `REVOCATION`
lo retira. `DECISION` conserva aclaraciones, sin crear gate. Una sustitucion
de contenido autorizado requiere reevaluar dependientes y nueva aprobacion.

## Huella del contenido autorizado

La huella es SHA-256 de `canonical_bytes(artifact)` en
`src/check_harness_state.py`. Se registra fuera del artefacto. Para calcularla:

```bash
PYTHONPATH=src python3 -c 'from pathlib import Path; from hashlib import sha256; from check_harness_state import canonical_bytes; print(sha256(canonical_bytes(Path("specs/008-example/spec.md"))).hexdigest())'
```

Cambiar la ruta del ejemplo por el artefacto real. El algoritmo conserva texto,
orden y estructura. Solo normaliza estados de encabezado, estados de TASK,
`Estado actual` en seccion de estado y, en `tasks.md`, marcas de checklists y
estado de la tabla de orden. Evidencia nueva va en `evidence/`, no en texto
libre dentro de TASKS. Un cambio de requisito, titulo, dependencia, prueba o
alcance cambia la huella. Formatos desconocidos deben fallar cerrado.

Secuencia de gate: obtener aprobacion humana explicita; actualizar solo
metadata de estado/aprobacion; calcular huella; agregar evento; ejecutar el
comprobador; avanzar unicamente con PASS. Una decision ambigua requiere
aclaracion. El hash detecta cambios de contenido, no demuestra identidad.

## Legado y transicion

SPEC-001 a SPEC-006 conservan sus estados y validaciones, pero las
aprobaciones cuya unica prueba depende del chat son **legado no verificable**.
No se reconstruyen huellas historicas ni se inventan aprobaciones. SPEC-007
documento sus aprobaciones humanas en sus propios artefactos durante la
transicion; su ledger se completa en TASK-004 y se comprueba antes de validar.
Desde la siguiente feature, cada gate exige el registro completo antes de
continuar.

## Errores y secretos

`MISSING_LEDGER`, `MISSING_APPROVAL`, `HASH_MISMATCH`, `INVALID_EVENT` y
`INVALID_SUPERSESSION` bloquean el gate afectado. Una ruta o feature enlazada
fuera del repo tambien falla. Resolver en SPEC/PLAN/TASKS
segun la decision duena. No registrar tokens, credenciales, datos sensibles
innecesarios ni transcripciones largas en el ledger o la evidencia.
