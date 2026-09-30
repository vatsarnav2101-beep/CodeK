import sqlite3
from pathlib import Path


class RunStore:
    def __init__(self, path: str | Path = "codek.db") -> None:
        self.path = str(path)
        with self._connect() as db:
            db.execute(
                """CREATE TABLE IF NOT EXISTS runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prompt TEXT NOT NULL,
                    result TEXT NOT NULL
                )"""
            )

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.path)

    def save(self, prompt: str, result: str) -> int:
        with self._connect() as db:
            cursor = db.execute(
                "INSERT INTO runs(prompt, result) VALUES (?, ?)",
                (prompt, result),
            )
            return int(cursor.lastrowid)

    def all(self) -> list[dict]:
        with self._connect() as db:
            rows = db.execute(
                "SELECT id, prompt, result FROM runs ORDER BY id DESC"
            ).fetchall()
        return [{"id": row[0], "prompt": row[1], "result": row[2]} for row in rows]
