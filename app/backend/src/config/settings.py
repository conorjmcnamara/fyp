# Schema validation constants
NUM_RECOMMENDATIONS_MIN = 1
NUM_RECOMMENDATIONS_MAX = 50
MAX_TEXT_LENGTH = 1500
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024

# Embedding service constants
TEXT_EMBEDDING_MODEL_DIR = "data/models/specter2/"
BERT_MAX_TOKENS = 512

TEXT_INDEX_PATH = "data/embeddings/v10_train_specter2.faiss"
TEXT_IDS_PATH = "data/embeddings/v10_train_specter2_ids.pkl"

NODE_INDEX_PATH = "data/embeddings/v10_train_node2vec_4_2.faiss"
NODE_IDS_PATH = "data/embeddings/v10_train_node2vec_4_2_ids.pkl"
NUM_NODE_NEIGHBOURS = 5

FUSION_MODEL_PATH = "data/models/dcca/v10_dcca_specter2_node2vec_4_2.pkl"

# Index search service constants
FUSED_INDEX_PATH = "data/embeddings/v10_train_dcca_concat_specter2_node2vec_4_2.faiss"
FUSED_IDS_PATH = "data/embeddings/v10_train_dcca_concat_specter2_node2vec_4_2_ids.pkl"
