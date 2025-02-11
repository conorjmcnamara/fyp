from src.data_models.dataset_config import DatasetConfig

# Environment constants
NUM_WORKERS = 2

# Dataset parser constants
DBLP_V10_CONFIG = DatasetConfig((1968, 2013), (2014, 2017), 15, 20)

# Text embedding constants
MIN_DOC_FREQ = 5

BERT_MAX_TOKENS = 512
TEXT_EMBEDDING_BATCH_SIZE = 32
DOC2VEC_DIM = 300
DOC2VEC_WINDOW = 5

# Node embedding constants
NODE2VEC_DIM = 128
NODE2VEC_WALK_LEN = 80
NODE2VEC_NUM_WALKS = 200
WORD2VEC_WINDOW = 10
WORD2VEC_MIN_COUNT = 1
WORD2VEC_BATCH_WORDS = 4

# Fusion constants
CCA_DIM = 128

DCCA_TEXT_HIDDEN_LAYERS = [512, 256, 128]
DCCA_NODE_HIDDEN_LAYERS = [128]
DCCA_EPOCHS = 10
DCCA_BATCH_SIZE = 1024

# Rerank constants
PAGERANK_ALPHA = 0.85

HITS_MAX_ITER = 100
HITS_TOLERANCE = 1.0e-8
