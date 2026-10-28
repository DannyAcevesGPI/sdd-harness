# FINDING-003 — Fallback debe usar solo diagnóstico del CLI

**Detectado:** 2026-10-27 durante `/validate`  
**Tipo:** IMPLEMENTATION  
**Requisito/AC:** FR-002, BR-001, AC-002; TASK-004; TEST-010

## Descripción

La detección de rechazo de effort examinaba stdout y stderr. Si la salida del
CLI contenía texto de la tarea con una frase parecida a un error de effort,
podía activar un retry aun cuando stderr informara, por ejemplo,
autenticación fallida.

## Evidencia RED

Se añadió `test_effort_phrase_in_stdout_does_not_override_unrelated_stderr`.
`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_run_task.py' -v`
falló: se observaron dos llamadas donde debía haber una. Los otros nueve
tests pasaron.

## Resolución

Limitar el reconocimiento al stderr del CLI, donde se comunica el diagnóstico,
y mantener el código de salida no-cero como precondición. Evidencia GREEN y
reapertura en `evidence/task-004.md`.
