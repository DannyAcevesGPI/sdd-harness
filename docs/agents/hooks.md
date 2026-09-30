# Hooks Guide

Esta guía prepara el Harness para hooks futuros sin crear hooks ejecutables en esta feature.

## Rol

Los hooks pueden apoyar verificaciones repetibles, pero no son autoridad del proceso SDD.

Un hook futuro puede ayudar a:

- Contar líneas o validar formato documental.
- Detectar marcadores pendientes.
- Ejecutar pruebas configuradas.
- Revisar patrones obvios de secretos.
- Recordar gates antes de commits o pushes.

## Límites

Un hook no sustituye:

- SPEC aprobada.
- PLAN aprobado.
- TASKS aprobadas.
- Aprobación humana.
- Revisión de seguridad.
- `/validate` y su resultado final.

Los hooks no deben declarar una feature `VALIDATED`.

## Seguridad

Todo hook futuro debe:

- Evitar imprimir secretos, tokens o credenciales.
- Tratar entradas externas como no confiables.
- No escribir secretos en logs, evidencia ni documentación.
- Fallar de forma explícita cuando no pueda verificar una condición crítica.
- Documentar si depende de red, reloj, entorno o estado externo.

## Diseño Recomendado

Antes de crear un hook ejecutable debe existir trabajo SDD aprobado que defina:

- Propósito del hook.
- Evento de ejecución.
- Archivos que lee o escribe.
- Comandos que ejecuta.
- Evidencia que produce.
- Modo de fallo.
- Impacto en desarrolladores y agentes.

Preferir hooks pequeños, deterministas y sin dependencias nuevas. Si una dependencia es necesaria, debe justificarse en PLAN.

## Evidencia

Cuando un hook se use como evidencia, registrar:

- Comando o evento que lo ejecutó.
- Resultado.
- Versión o contenido relevante del hook.
- Límites conocidos.

Un PASS de hook es evidencia parcial; la validación SDD decide cumplimiento final.
