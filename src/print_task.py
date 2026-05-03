"""Modelo de un trabajo de impresión."""


from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PrintTask:
    """Trabajo con identificador, páginas y momento de llegada (segundos de simulación)."""

    task_id: str
    pages: int
    arrival_time: float
