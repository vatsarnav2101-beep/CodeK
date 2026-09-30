from collections import defaultdict, deque

from app.core.models import Task, TaskStatus


class TaskGraph:
    """Small directed graph for task dependencies."""

    def __init__(self) -> None:
        self.tasks: dict[str, Task] = {}
        self.edges: dict[str, list[str]] = defaultdict(list)

    def add_task(self, task: Task) -> None:
        if task.id in self.tasks:
            raise ValueError(f"Task already exists: {task.id}")
        self.tasks[task.id] = task

        for dependency in task.depends_on:
            if dependency not in self.tasks:
                raise ValueError(
                    f"Dependency {dependency!r} must be added before {task.id!r}"
                )
            self.edges[dependency].append(task.id)

        if self.has_cycle():
            # Roll back the edge/task if the new task created a cycle.
            for dependency in task.depends_on:
                self.edges[dependency].remove(task.id)
            del self.tasks[task.id]
            raise ValueError("Task graph cannot contain a cycle")

    def ready_tasks(self) -> list[Task]:
        ready = []
        for task in self.tasks.values():
            if task.status != TaskStatus.WAITING:
                continue
            if all(self.tasks[d].status == TaskStatus.DONE for d in task.depends_on):
                task.status = TaskStatus.READY
                ready.append(task)
        return ready

    def has_cycle(self) -> bool:
        state: dict[str, int] = {task_id: 0 for task_id in self.tasks}

        def dfs(node: str) -> bool:
            state[node] = 1
            for child in self.edges[node]:
                if state[child] == 1:
                    return True
                if state[child] == 0 and dfs(child):
                    return True
            state[node] = 2
            return False

        return any(state[node] == 0 and dfs(node) for node in self.tasks)

    def topological_order(self) -> list[str]:
        indegree = {task_id: 0 for task_id in self.tasks}
        for children in self.edges.values():
            for child in children:
                indegree[child] += 1

        queue = deque(task_id for task_id, degree in indegree.items() if degree == 0)
        order: list[str] = []

        while queue:
            node = queue.popleft()
            order.append(node)
            for child in self.edges[node]:
                indegree[child] -= 1
                if indegree[child] == 0:
                    queue.append(child)

        if len(order) != len(self.tasks):
            raise ValueError("Cannot sort a cyclic task graph")
        return order
