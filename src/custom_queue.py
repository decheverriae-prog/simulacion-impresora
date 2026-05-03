"""Cola FIFO propia para la simulación. La lógica principal depende de esta estructura."""


class Queue:
    """Cola de tipo FIFO implementada con lista y puntero al frente."""

    __slots__ = ("_items", "_start")

    def __init__(self) -> None:
        self._items: list[object] = []
        self._start: int = 0

    def enqueue(self, item: object) -> None:
        self._items.append(item)

    def dequeue(self) -> object:
        if self.is_empty():
            raise RuntimeError("No se puede extraer de una cola vacía.")
        value = self._items[self._start]
        self._start += 1
        self._compact_if_needed()
        return value

    def peek(self) -> object:
        if self.is_empty():
            raise RuntimeError("La cola está vacía.")
        return self._items[self._start]

    def is_empty(self) -> bool:
        return self._start >= len(self._items)

    def size(self) -> int:
        return len(self._items) - self._start

    def clear(self) -> None:
        self._items.clear()
        self._start = 0

    def _compact_if_needed(self) -> None:
        if self._start > 0 and self._start > len(self._items) // 2:
            self._items = self._items[self._start :]
            self._start = 0
