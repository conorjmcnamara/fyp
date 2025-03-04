import pytest
import os
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from typing import Generator
from src.services.recommendation import RecommendationService
from src.app import app


@pytest.fixture()
def mock_create_recommendation_service() -> Generator[MagicMock, None, None]:
    with patch("src.services.factory.create_recommendation_service") as mock:
        mock.return_value = MagicMock(spec=RecommendationService)
        yield mock


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture()
def mock_frontend_url() -> Generator[None, None, None]:
    os.environ["FRONTEND_URL"] = "http://localhost:3000"
    yield
    del os.environ["FRONTEND_URL"]


def test_lifespan_initialization(
    mock_create_recommendation_service: Generator[MagicMock, None, None]
):
    with TestClient(app):
        mock_create_recommendation_service.assert_called_once()
        recommendation_service = app.state.recommendation_service
        assert isinstance(recommendation_service, RecommendationService)


def test_cors_valid(client: TestClient, mock_frontend_url: Generator[None, None, None]):
    response = client.get("/api/health", headers={"Origin": "http://localhost:3000"})

    assert response.status_code == 200
    assert response.headers["Access-Control-Allow-Origin"] == "http://localhost:3000"


def test_cors_invalid(client: TestClient, mock_frontend_url: Generator[None, None, None]):
    response = client.get("/api/health", headers={"Origin": "http://invalid-origin.com"})

    assert response.status_code == 200
    assert "Access-Control-Allow-Origin" not in response.headers
