import heapq
from dataclasses import dataclass, field

from app.core.models import Task


@dataclass(order=True)
class QueueItem:
    # Negative priority makes a normal min-heap behave like a max-priority queue.
    priority: int
    sequence: int
    task_id: str = field(compare=False)


class PriorityScheduler:
    """Selects ready tasks using a heap."""

    def __init__(self) -> None:
        self._heap: list[QueueItem] = []
        self._sequence = 0

    def add(self, task: Task) -> None:
        self._sequence += 1
        heapq.heappush(
            self._heap,
            QueueItem(-task.priority, self._sequence, task.id),
        )

    def pop(self) -> str | None:
        if not self._heap:
            return None
        return heapq.heappop(self._heap).task_id

    def __bool__(self) -> bool:
        return bool(self._heap)
