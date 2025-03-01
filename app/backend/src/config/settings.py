# Embedding service constants
TEXT_EMBEDDING_MODEL_DIR = "data/models/specter2/"
BERT_MAX_TOKENS = 512

TEXT_INDEX_PATH = "data/embeddings/v10_train_specter2.faiss"
TEXT_IDS_PATH = "data/embeddings/v10_train_specter2_ids.pkl"

NODE_INDEX_PATH = "data/embeddings/v10_train_node2vec_0.25_4.faiss"
NODE_IDS_PATH = "data/embeddings/v10_train_node2vec_0.25_4_ids.pkl"
NUM_NODE_NEIGHBOURS = 5

FUSION_MODEL_PATH = "data/models/dcca/v10_dcca_specter2_node2vec_0.25_4.pkl"

TOP_K = 10

# Similarity search service constants
FUSED_INDEX_PATH = "data/embeddings/v10_train_dcca_concat_specter2_node2vec_0.25_4.faiss"
FUSED_IDS_PATH = "data/embeddings/v10_train_dcca_concat_specter2_node2vec_0.25_4_ids.pkl"
