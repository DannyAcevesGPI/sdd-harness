"""Task-based reasoning effort policy."""

from dataclasses import dataclass
import re


_HIGH_IMPACT = re.compile(
    r"\b(?:security|seguridad|auth(?:entication|orization)?|autenticaci[oó]n|"
    r"autorizaci[oó]n|migration|migraci[oó]n|architecture|arquitectura|"
    r"concurrency|concurrencia|complex(?:e|ity)?|complej[oa]|"
    r"multi[- ]component|cross[- ](?:module|service)|several components|"
    r"varios componentes|data loss|p[eé]rdida de datos|integrity|integridad|"
    r"destructive|destructiv[oa])\b",
    re.IGNORECASE,
)
_SMALL_MECHANICAL = re.compile(
    r"\b(?:typo|spelling|format(?:ting)?|rename|renaming|capitalization|"
    r"punctuation|read[- ]only|quick lookup|simple lookup|corrige (?:una )?errata|"
    r"corrige typo|formatea|renombra|consulta simple|revisa ortograf[ií]a|"
    r"explica esta funci[oó]n)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class EffortSelection:
    level: str
    reason: str


def select_effort(task: str) -> EffortSelection:
    """Select a common effort level for a task description."""
    if not task or not task.strip():
        return EffortSelection("medium", "no task details; using medium")
    if _HIGH_IMPACT.search(task):
        return EffortSelection("high", "high-impact work signal detected")
    if _SMALL_MECHANICAL.search(task):
        return EffortSelection("low", "small mechanical task signal detected")
    return EffortSelection("medium", "no decisive complexity signal; using medium")
