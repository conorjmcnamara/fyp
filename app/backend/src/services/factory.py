from src.services.embedding import EmbeddingService
from src.services.similarity_search import SimilaritySearchService
from src.services.recommendation import RecommendationService
from src.config.settings import (
    TEXT_EMBEDDING_MODEL_DIR,
    BERT_MAX_TOKENS,
    TEXT_INDEX_PATH,
    TEXT_IDS_PATH,
    NODE_INDEX_PATH,
    NODE_IDS_PATH,
    NUM_NODE_NEIGHBOURS,
    FUSION_MODEL_PATH,
    FUSED_INDEX_PATH,
    FUSED_IDS_PATH
)


def create_recommendation_service() -> RecommendationService:
    embedding_service = EmbeddingService(
        TEXT_EMBEDDING_MODEL_DIR,
        BERT_MAX_TOKENS,
        TEXT_INDEX_PATH,
        TEXT_IDS_PATH,
        NODE_INDEX_PATH,
        NODE_IDS_PATH,
        NUM_NODE_NEIGHBOURS,
        FUSION_MODEL_PATH
    )
    search_service = SimilaritySearchService(FUSED_INDEX_PATH, FUSED_IDS_PATH)
    return RecommendationService(embedding_service, search_service)
