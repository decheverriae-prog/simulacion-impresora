"""Procesamiento de trabajos, métricas básicas y uso de Queue vía simulación."""

import pytest

from src.print_simulation import PrintSimulation
from src.print_task import PrintTask


def test_single_job_no_wait():
    sim = PrintSimulation(seconds_per_page=1.0)
    tasks = [PrintTask("A", pages=3, arrival_time=0.0)]
    r = sim.run(tasks)
    assert r.metrics.total_processed == 1
    assert r.metrics.average_wait_time == 0.0
    assert r.metrics.max_wait_time == 0.0
    assert r.metrics.task_id_max_wait == "A"
    assert r.metrics.max_queue_size >= 1
    assert len(r.completed) == 1
    assert r.completed[0].service_end == 3.0


def test_second_job_waits_until_first_finishes():
    # Llegan juntos pero uno primero en cola: primero imprime 2 páginas (=2s), segundo espera 2s con spp=1
    sim = PrintSimulation(seconds_per_page=1.0)
    tasks = [
        PrintTask("first", pages=2, arrival_time=0.0),
        PrintTask("second", pages=1, arrival_time=0.0),
    ]
    r = sim.run(tasks)
    assert r.metrics.total_processed == 2
    waits = {c.task.task_id: c.wait_time for c in r.completed}
    assert waits["first"] == 0.0
    assert waits["second"] == pytest.approx(2.0)
    assert r.metrics.max_wait_time == pytest.approx(2.0)
    assert r.metrics.max_queue_size == 2


def test_invalid_tasks_rejected_not_processed():
    sim = PrintSimulation(seconds_per_page=2.0)
    tasks = [
        PrintTask("ok", pages=1, arrival_time=0.0),
        PrintTask("", pages=1, arrival_time=0.0),
        PrintTask("bad_pages", pages=0, arrival_time=0.0),
        PrintTask("bad_time", pages=2, arrival_time=-1.0),
    ]
    r = sim.run(tasks)
    assert r.metrics.total_processed == 1
    assert len(r.rejected) == 3


def test_empty_job_list():
    sim = PrintSimulation(seconds_per_page=5.0)
    r = sim.run([])
    assert r.metrics.total_processed == 0
    assert r.metrics.average_wait_time == 0.0
    assert r.metrics.task_id_max_wait is None
    assert r.metrics.max_queue_size == 0


def test_metrics_average_wait():
    sim = PrintSimulation(seconds_per_page=10.0)
    tasks = [
        PrintTask("t1", pages=1, arrival_time=0.0),
        PrintTask("t2", pages=1, arrival_time=0.0),
    ]
    r = sim.run(tasks)
    assert r.metrics.average_wait_time == pytest.approx(5.0)
