import sys
from pathlib import Path

from fastapi import FastAPI

from app.api.routes import build_router
from app.storage.database import RunStore


BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "codek.db"

app = FastAPI(title="CodeK", version="0.1.0")
store = RunStore(DB_PATH)
app.include_router(build_router(BASE_DIR, store))


def main() -> None:
    prompt = " ".join(sys.argv[1:]).strip()
    if not prompt:
        print("Usage: python -m app.main \"inspect this project\"")
        return

    from app.core.runner import AgentRunner
    result = AgentRunner(BASE_DIR, store).run(prompt)
    print("\nPlan:")
    for step in result.plan:
        print(f"- {step}")
    print("\nResults:")
    for item in result.results:
        print(f"[{item['status']}] {item['task']}: {item['result']}")


if __name__ == "__main__":
    main()
