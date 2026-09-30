from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class TaskStatus(str, Enum):
    WAITING = "waiting"
    READY = "ready"
    DONE = "done"
    FAILED = "failed"


@dataclass
class Task:
    id: str
    title: str
    action: str
    priority: int = 1
    depends_on: list[str] = field(default_factory=list)
    status: TaskStatus = TaskStatus.WAITING
    result: Any = None


@dataclass
class RunResult:
    run_id: int
    prompt: str
    plan: list[str]
    results: list[dict[str, Any]]
