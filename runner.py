from pathlib import Path

from app.agents.planner import Planner
from app.core.graph import TaskGraph
from app.core.models import RunResult, TaskStatus
from app.dsa.scheduler import PriorityScheduler
from app.storage.database import RunStore
from app.tools.workspace import Workspace


class AgentRunner:
    def __init__(self, workspace: str | Path, store: RunStore | None = None) -> None:
        self.workspace = Workspace(workspace)
        self.planner = Planner()
        self.store = store

    def run(self, prompt: str) -> RunResult:
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty")

        tasks = self.planner.plan(prompt)
        graph = TaskGraph()
        for task in tasks:
            graph.add_task(task)

        scheduler = PriorityScheduler()
        results: list[dict] = []

        while True:
            for task in graph.ready_tasks():
                scheduler.add(task)

            task_id = scheduler.pop()
            if task_id is None:
                break

            task = graph.tasks[task_id]
            try:
                value = self._execute(task.action, prompt)
                task.result = value
                task.status = TaskStatus.DONE
                results.append({
                    "task": task.title,
                    "status": "done",
                    "result": value,
                })
            except Exception as exc:
                task.status = TaskStatus.FAILED
                results.append({
                    "task": task.title,
                    "status": "failed",
                    "result": str(exc),
                })
                break

        summary = self._make_summary(prompt, results)
        results.append({"task": "Run summary", "status": "done", "result": summary})

        run_id = self.store.save(prompt, summary) if self.store else 0
        return RunResult(
            run_id=run_id,
            prompt=prompt,
            plan=[task.title for task in tasks],
            results=results,
        )

    def _execute(self, action: str, prompt: str):
        if action == "list_files":
            return self.workspace.list_files()

        if action == "search_files":
            words = [
                word.strip(".,!?()[]{}")
                for word in prompt.split()
                if len(word.strip(".,!?()[]{}")) >= 4
            ]
            query = words[0] if words else "def"
            return self.workspace.search(query)

        if action == "run_check":
            return self.workspace.run_python_check()

        if action == "summarize":
            return "Collected workspace information and completed the planned checks."

        raise ValueError(f"Unknown action: {action}")

    @staticmethod
    def _make_summary(prompt: str, results: list[dict]) -> str:
        completed = sum(item["status"] == "done" for item in results)
        failed = sum(item["status"] == "failed" for item in results)
        return (
            f"Task: {prompt}\n"
            f"Steps completed: {completed}\n"
            f"Steps failed: {failed}\n"
            "Mode: deterministic demo planner"
        )
