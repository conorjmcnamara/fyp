import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from typing import Generator
from src.services.recommendation import RecommendationService
from src.app import app
from src.config.settings import NUM_RECOMMENDATIONS_MIN, NUM_RECOMMENDATIONS_MAX


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
def mock_recommendation_service() -> Generator[RecommendationService, None, None]:
    with patch.object(
        RecommendationService,
        "recommend",
        return_value=mock_recommendations
    ):
        yield RecommendationService


@pytest.fixture()
def client(mock_recommendation_service: RecommendationService) -> TestClient:
    app.state.recommendation_service = mock_recommendation_service
    return TestClient(app)


def test_recommend_papers(client: TestClient, mock_recommendation_service: RecommendationService):
    request_data = {
        "title": "Example title",
        "abstract": "Example abstract",
        "numRecommendations": 10
    }

    response = client.post("/api/v1/recommendations", json=request_data)

    assert response.status_code == 200
    data = response.json()

    assert len(data["papers"]) == 1
    assert data["papers"][0] == mock_recommendations[0]

    mock_recommendation_service.recommend.assert_called_once_with(
        mock_recommendation_service.recommend.call_args[0][0],
        request_data["title"],
        request_data["abstract"],
        mock_recommendation_service.recommend.call_args[0][3]
    )


def test_recommend_papers_invalid_types(client: TestClient):
    request_data = {
        "title": None,
        "abstract": "Example abstract",
        "numRecommendations": 10
    }

    response = client.post("/api/v1/recommendations", json=request_data)
    assert response.status_code == 422


def test_recommend_papers_num_recommendations_less_than_min(client: TestClient):
    request_data = {
        "title": "Example title",
        "abstract": "Example abstract",
        "numRecommendations": NUM_RECOMMENDATIONS_MIN - 1
    }

    response = client.post("/api/v1/recommendations", json=request_data)
    assert response.status_code == 422

    data = response.json()
    assert data["detail"][0]["msg"] == (
        "Value error, numRecommendations must be between " +
        f"{NUM_RECOMMENDATIONS_MIN} and {NUM_RECOMMENDATIONS_MAX}"
    )


def test_recommend_papers_num_recommendations_greater_than_max(client: TestClient):
    request_data = {
        "title": "Example title",
        "abstract": "Example abstract",
        "numRecommendations": NUM_RECOMMENDATIONS_MAX + 1
    }

    response = client.post("/api/v1/recommendations", json=request_data)
    assert response.status_code == 422

    data = response.json()
    assert data["detail"][0]["msg"] == (
        "Value error, numRecommendations must be between " +
        f"{NUM_RECOMMENDATIONS_MIN} and {NUM_RECOMMENDATIONS_MAX}"
    )


def test_recommend_papers_exception(
    client: TestClient,
    mock_recommendation_service: RecommendationService
):
    mock_recommendation_service.recommend.side_effect = Exception("Internal Server Error")
    request_data = {
        "title": "Example title",
        "abstract": "Example abstract",
        "numRecommendations": 10
    }

    response = client.post("/api/v1/recommendations", json=request_data)
    assert response.status_code == 500
