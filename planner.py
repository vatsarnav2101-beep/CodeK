from app.core.models import Task


class Planner:
    """Creates a small deterministic plan from a coding request.

    This is intentionally not presented as an LLM. It is the default demo
    planner so CodeK works without an API key.
    """

    def plan(self, prompt: str) -> list[Task]:
        text = prompt.lower()
        tasks = [
            Task("inspect", "Inspect the workspace", "list_files", priority=3),
            Task(
                "understand",
                "Search for relevant code",
                "search_files",
                priority=2,
                depends_on=["inspect"],
            ),
        ]

        if any(word in text for word in ("run", "test", "check", "bug", "error")):
            tasks.append(
                Task(
                    "check",
                    "Run a small Python check",
                    "run_check",
                    priority=3,
                    depends_on=["understand"],
                )
            )

        tasks.append(
            Task(
                "summary",
                "Summarize what was found",
                "summarize",
                priority=1,
                depends_on=[tasks[-1].id],
            )
        )
        return tasks
