import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from src.services.recommendation import RecommendationService
from src.app import app

mock_recommendations = [
    {
        "id": "1",
        "title": "Paper 1",
        "year": 2025,
        "abstract": "Abstract for paper 1",
        "venue": "Venue 1",
        "authors": [{"first_name": "John", "last_name": "Doe"}],
        "recommendation_score": 95
    }
]


@pytest.fixture
def mock_service() -> MagicMock:
    mock = MagicMock(spec=RecommendationService)
    mock.recommend.return_value = mock_recommendations
    return mock


@pytest.fixture()
def client(mock_service: MagicMock) -> TestClient:
    app.state.recommendation_service = mock_service
    return TestClient(app)


def test_recommend_papers(client: TestClient, mock_service: MagicMock):
    request_data = {
        "title": "Some title",
        "abstract": "Some abstract"
    }

    response = client.post("/api/v1/recommendations", json=request_data)

    assert response.status_code == 200
    data = response.json()

    assert len(data["papers"]) == 1
    assert data["papers"][0] == mock_recommendations[0]

    mock_service.recommend.assert_called_once_with(
        mock_service.recommend.call_args[0][0],
        request_data["title"],
        request_data["abstract"],
        mock_service.recommend.call_args[0][3]
    )


def test_recommend_papers_invalid_data(client: TestClient):
    request_data = {
        "title": None,
        "abstract": "Some abstract"
    }

    response = client.post("/api/v1/recommendations", json=request_data)
    assert response.status_code == 422


def test_recommend_papers_exception(client: TestClient, mock_service: MagicMock):
    mock_service.recommend.side_effect = Exception("Internal Server Error")
    request_data = {
        "title": "Some title",
        "abstract": "Some abstract"
    }

    response = client.post("/api/v1/recommendations", json=request_data)
    assert response.status_code == 500
