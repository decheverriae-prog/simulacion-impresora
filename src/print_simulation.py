"""
Simulación de llegadas, cola FIFO y un solo servidor (impresora).
Toda la espera y atención pasa por la clase Queue.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .custom_queue import Queue
from .print_task import PrintTask
from .printer import Printer


@dataclass(frozen=True, slots=True)
class CompletedJob:
    task: PrintTask
    wait_time: float
    service_start: float
    service_end: float


@dataclass(frozen=True, slots=True)
class SimulationMetrics:
    total_processed: int
    average_wait_time: float
    max_wait_time: float
    task_id_max_wait: str | None
    max_queue_size: int


@dataclass
class SimulationResult:
    metrics: SimulationMetrics
    completed: list[CompletedJob] = field(default_factory=list)
    rejected: list[str] = field(default_factory=list)


def _validate_task(task: PrintTask) -> str | None:
    if not str(task.task_id).strip():
        return "Identificador de trabajo vacío."
    if task.pages <= 0:
        return f"Trabajo '{task.task_id}': la cantidad de páginas debe ser positiva."
    if task.arrival_time < 0:
        return f"Trabajo '{task.task_id}': el tiempo de llegada no puede ser negativo."
    return None


class PrintSimulation:
    """Orquesta cola + impresora y calcula métricas."""

    def __init__(self, seconds_per_page: float) -> None:
        if seconds_per_page <= 0:
            raise ValueError("seconds_per_page debe ser positivo.")
        self.seconds_per_page = seconds_per_page

    def run(self, tasks: list[PrintTask]) -> SimulationResult:
        queue: Queue = Queue()
        printer = Printer(self.seconds_per_page)

        rejected: list[str] = []
        valid: list[PrintTask] = []
        for t in tasks:
            err = _validate_task(t)
            if err is not None:
                rejected.append(err)
            else:
                valid.append(t)

        valid.sort(key=lambda x: (x.arrival_time, x.task_id))
        n = len(valid)
        ptr = 0
        current_time = 0.0
        max_queue_size = 0
        completed: list[CompletedJob] = []

        while ptr < n or not queue.is_empty() or printer.is_busy(current_time):
            while ptr < n and valid[ptr].arrival_time <= current_time:
                queue.enqueue(valid[ptr])
                ptr += 1
                max_queue_size = max(max_queue_size, queue.size())

            if printer.is_idle(current_time) and not queue.is_empty():
                task = queue.dequeue()
                wait_time = current_time - task.arrival_time
                service_start = current_time
                service_end = printer.start_job(task, service_start)
                completed.append(
                    CompletedJob(
                        task=task,
                        wait_time=wait_time,
                        service_start=service_start,
                        service_end=service_end,
                    )
                )
                continue

            next_arrival = valid[ptr].arrival_time if ptr < n else float("inf")
            if printer.is_busy(current_time):
                if next_arrival < printer.busy_until:
                    current_time = next_arrival
                else:
                    current_time = printer.busy_until
            else:
                if ptr < n:
                    current_time = next_arrival
                else:
                    break

        metrics = _build_metrics(completed, max_queue_size)
        return SimulationResult(metrics=metrics, completed=completed, rejected=rejected)


def _build_metrics(completed: list[CompletedJob], max_queue_size: int) -> SimulationMetrics:
    total = len(completed)
    if total == 0:
        return SimulationMetrics(
            total_processed=0,
            average_wait_time=0.0,
            max_wait_time=0.0,
            task_id_max_wait=None,
            max_queue_size=max_queue_size,
        )
    waits = [c.wait_time for c in completed]
    max_w = max(waits)
    idx = waits.index(max_w)
    max_id = completed[idx].task.task_id
    avg = sum(waits) / total
    return SimulationMetrics(
        total_processed=total,
        average_wait_time=avg,
        max_wait_time=max_w,
        task_id_max_wait=max_id,
        max_queue_size=max_queue_size,
    )
