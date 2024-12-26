from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_get_message():
    response = client.get("/api/v1/message")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello"}
