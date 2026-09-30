from app.core.models import Task
from app.dsa.scheduler import PriorityScheduler


def test_high_priority_task_runs_first():
    scheduler = PriorityScheduler()
    scheduler.add(Task("low", "low", "x", priority=1))
    scheduler.add(Task("high", "high", "x", priority=5))
    assert scheduler.pop() == "high"
    assert scheduler.pop() == "low"
