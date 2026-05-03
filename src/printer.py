"""Impresora: duración de impresión, ocupación y avance de tiempo de servicio."""


from __future__ import annotations

from .print_task import PrintTask


class Printer:
    """
    Simula una impresora que atiende un trabajo a la vez.
    `busy_until` es el instante (tiempo de simulación) en que quedará libre.
    """

    __slots__ = ("seconds_per_page", "busy_until")

    def __init__(self, seconds_per_page: float) -> None:
        if seconds_per_page <= 0:
            raise ValueError("seconds_per_page debe ser positivo.")
        self.seconds_per_page = seconds_per_page
        self.busy_until: float = 0.0

    def is_busy(self, at_time: float) -> bool:
        return at_time < self.busy_until

    def is_idle(self, at_time: float) -> bool:
        return not self.is_busy(at_time)

    def print_duration_seconds(self, task: PrintTask) -> float:
        return task.pages * self.seconds_per_page

    def start_job(self, task: PrintTask, start_time: float) -> float:
        """
        Asigna el trabajo en `start_time` y devuelve el instante en que termina.
        Actualiza `busy_until`.
        """
        duration = self.print_duration_seconds(task)
        self.busy_until = start_time + duration
        return self.busy_until

    def reset(self) -> None:
        self.busy_until = 0.0
