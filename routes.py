from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.runner import AgentRunner
from app.storage.database import RunStore


class RunRequest(BaseModel):
    prompt: str


def build_router(workspace: str | Path, store: RunStore) -> APIRouter:
    router = APIRouter()
    runner = AgentRunner(workspace, store)

    @router.get("/health")
    def health():
        return {"status": "ok", "project": "codeK"}

    @router.post("/run")
    def run(request: RunRequest):
        try:
            result = runner.run(request.prompt)
        except (ValueError, OSError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return {
            "run_id": result.run_id,
            "prompt": result.prompt,
            "plan": result.plan,
            "results": result.results,
        }

    @router.get("/runs")
    def runs():
        return store.all()

    return router
