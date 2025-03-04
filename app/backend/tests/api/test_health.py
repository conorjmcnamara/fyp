import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)


def test_health_check(client: TestClient):
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
