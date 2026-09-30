from fastapi.testclient import TestClient
from app.api.routes import build_router
from app.storage.database import RunStore
from fastapi import FastAPI


def test_health(tmp_path):
    app = FastAPI()
    app.include_router(build_router(tmp_path, RunStore(tmp_path / "test.db")))
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
