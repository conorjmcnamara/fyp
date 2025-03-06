import pytest
from unittest.mock import patch, MagicMock
from typing import Generator
from src.services.factory import create_recommendation_service
from src.services.recommendation import RecommendationService


@pytest.fixture
def mock_embedding_service() -> Generator[MagicMock, None, None]:
    with patch("src.services.factory.EmbeddingService") as mock_embedding_service:
        mock_instance = MagicMock(spec=mock_embedding_service)
        mock_embedding_service.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_search_service() -> Generator[MagicMock, None, None]:
    with patch("src.services.factory.IndexSearchService") as mock_search_service:
        mock_instance = MagicMock(spec=mock_search_service)
        mock_search_service.return_value = mock_instance
        yield mock_instance


def test_create_recommendation_service(
    mock_embedding_service: MagicMock,
    mock_search_service: MagicMock
):
    recommendation_service = create_recommendation_service()

    assert isinstance(recommendation_service, RecommendationService)
    assert recommendation_service.embedding_service == mock_embedding_service
    assert recommendation_service.search_service == mock_search_service
