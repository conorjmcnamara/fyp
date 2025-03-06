import torch
import numpy as np
import warnings
from transformers import AutoModel, AutoTokenizer
from mvlearn.embed import DCCA
from typing import List, Tuple
from src.utils.file_utils import read_embeddings, read_obj


class EmbeddingService:
    def __init__(
        self,
        text_model_dir: str,
        tokenizer_max_len: int,
        text_index_path: str,
        text_ids_path: str,
        node_index_path: str,
        node_ids_path: str,
        num_node_neighbours: int,
        fusion_model_path: str
    ):
        raise Exception()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.text_model = self._load_text_model(text_model_dir)
        self.tokenizer = AutoTokenizer.from_pretrained(text_model_dir)
        self.tokenizer_max_len = tokenizer_max_len

        self.text_index = read_embeddings(text_index_path)
        self.text_ids: List[str] = read_obj(text_ids_path)
        self.node_index = read_embeddings(node_index_path)
        self.node_ids: List[str] = read_obj(node_ids_path)
        self.num_node_neighbours = num_node_neighbours
        self.node_id_to_idx = {id: idx for idx, id in enumerate(self.node_ids)}
        self.fusion_model: DCCA = read_obj(fusion_model_path)

    def _load_text_model(self, text_model_dir: str) -> AutoModel:
        model = AutoModel.from_pretrained(text_model_dir, torch_dtype=torch.float32)
        model = model.to(self.device)
        model.eval()
        return model

    def embed(self, title: str, abstract: str) -> np.ndarray:
        text_embedding = self._embed_text(title, abstract)
        node_embedding = self._embed_node(text_embedding)
        text_projection, node_projection = self._project_embeddings(text_embedding, node_embedding)
        return self._concat_embeddings(text_projection, node_projection)

    def _embed_text(self, title: str, abstract: str) -> np.ndarray:
        text = f"{title} {abstract}"
        inputs = self.tokenizer(
            text,
            max_length=self.tokenizer_max_len,
            truncation=True,
            return_tensors="pt"
        ).to(self.device)

        with torch.no_grad():
            outputs = self.text_model(**inputs)

        last_hidden_state = outputs.last_hidden_state
        embedding = last_hidden_state.mean(dim=1).cpu().numpy()
        return embedding

    def _embed_node(self, query_text_embedding: np.ndarray) -> np.ndarray:
        _, indices = self.text_index.search(
            query_text_embedding,
            self.num_node_neighbours
        )
        neighbour_text_ids = [self.text_ids[i] for i in indices[0]]

        neighbour_node_embeddings = []
        for neighbour_text_id in neighbour_text_ids:
            node_idx = self.node_id_to_idx[neighbour_text_id]
            neighbour_node_embeddings.append(self.node_index.reconstruct(node_idx))

        return np.expand_dims(np.mean(neighbour_node_embeddings, axis=0), axis=0)

    def _project_embeddings(
        self,
        text_embedding: np.ndarray,
        node_embedding: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=UserWarning, message=".*torch.symeig.*")
            projections = self.fusion_model.transform([
                np.vstack([text_embedding, text_embedding]),
                np.vstack([node_embedding, node_embedding])
            ])

        text_projection, node_projection = projections[0][0], projections[1][0]
        return np.expand_dims(text_projection, axis=0), np.expand_dims(node_projection, axis=0)

    def _concat_embeddings(
        self,
        text_embedding: np.ndarray,
        node_embedding: np.ndarray
    ) -> np.ndarray:
        return np.concatenate((text_embedding, node_embedding), axis=1)
