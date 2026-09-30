from pathlib import Path
import subprocess


class WorkspaceError(Exception):
    pass


class Workspace:
    """Local project tools with a simple workspace boundary."""

    ALLOWED_EXTENSIONS = {
        ".py", ".md", ".txt", ".json", ".toml", ".yaml", ".yml",
        ".dart", ".js", ".ts", ".html", ".css"
    }

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root).resolve()

    def _safe_path(self, relative: str) -> Path:
        candidate = (self.root / relative).resolve()
        if candidate != self.root and self.root not in candidate.parents:
            raise WorkspaceError("Path escapes the workspace")
        return candidate

    def list_files(self, limit: int = 80) -> list[str]:
        files = []
        for path in sorted(self.root.rglob("*")):
            if path.is_file() and ".git" not in path.parts and "__pycache__" not in path.parts:
                files.append(str(path.relative_to(self.root)))
            if len(files) >= limit:
                break
        return files

    def read_file(self, relative: str, max_chars: int = 12000) -> str:
        path = self._safe_path(relative)
        if not path.is_file():
            raise WorkspaceError(f"Not a file: {relative}")
        return path.read_text(encoding="utf-8")[:max_chars]

    def search(self, query: str, limit: int = 30) -> list[str]:
        query = query.lower()
        matches = []
        for relative in self.list_files():
            path = self._safe_path(relative)
            if path.suffix.lower() not in self.ALLOWED_EXTENSIONS:
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for line_no, line in enumerate(text.splitlines(), start=1):
                if query in line.lower():
                    matches.append(f"{relative}:{line_no}: {line.strip()}")
                    if len(matches) >= limit:
                        return matches
        return matches

    def run_python_check(self) -> str:
        command = ["python", "-m", "compileall", "-q", "."]
        try:
            completed = subprocess.run(
                command,
                cwd=self.root,
                capture_output=True,
                text=True,
                timeout=15,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise WorkspaceError(f"Python check failed to start: {exc}") from exc

        if completed.returncode != 0:
            raise WorkspaceError(completed.stderr.strip() or "Python check failed")
        return "Python compile check passed"
