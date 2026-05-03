import pytest

from src.custom_queue import Queue


def test_fifo_order():
    q = Queue()
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)
    assert q.dequeue() == 1
    assert q.dequeue() == 2
    assert q.dequeue() == 3
    assert q.is_empty()


def test_peek_without_removing():
    q = Queue()
    q.enqueue("a")
    assert q.peek() == "a"
    assert q.size() == 1
    assert q.dequeue() == "a"


def test_empty_dequeue_raises():
    q = Queue()
    with pytest.raises(RuntimeError, match="vacía"):
        q.dequeue()


def test_clear():
    q = Queue()
    for i in range(10):
        q.enqueue(i)
    q.dequeue()
    q.dequeue()
    q.clear()
    assert q.is_empty()
    assert q.size() == 0
