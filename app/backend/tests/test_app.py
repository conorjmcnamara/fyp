import pytest
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def mock_env_variables(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "sqlite:///test.db")


@pytest.fixture
def client():
    from src.app import app
    return TestClient(app)

def test_app(client: TestClient):
    assert True
