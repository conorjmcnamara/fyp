import numpy as np
from sklearn.cross_decomposition import CCA
from typing import Callable, List
from src.utils.file_utils import read_embeddings, save_embeddings, read_obj, save_obj
from src.utils.preprocess_utils import extract_embeddings_from_index, align_embeddings
from src.config.settings import CCA_DIM


def train_fusion_model(
    fusion_model_path: str,
    fusion_func: Callable[[str, np.ndarray, np.ndarray], None],
    text_index_path: str,
    text_ids_path: str,
    node_index_path: str,
    node_ids_path: str,
) -> None:
    text_index = read_embeddings(text_index_path)
    text_ids: List[str] = read_obj(text_ids_path)
    node_index = read_embeddings(node_index_path)
    node_ids: List[str] = read_obj(node_ids_path)

    text_embeddings = extract_embeddings_from_index(text_index)
    node_embeddings = extract_embeddings_from_index(node_index)

    aligned_node_embeddings, _ = align_embeddings(
        text_ids,
        node_embeddings,
        node_ids
    )

    fusion_func(fusion_model_path, text_embeddings, aligned_node_embeddings)


def train_cca(cca_path: str, text_embeddings: np.ndarray, node_embeddings: np.ndarray) -> None:
    # Fit CCA on the training set, learning text and node projection matrices
    cca = CCA(n_components=CCA_DIM)
    cca.fit(text_embeddings, node_embeddings)

    print("Saving CCA")
    save_obj(cca_path, cca)


def project_embeddings(
    projected_text_index_path: str,
    projected_text_ids_path: str,
    projected_node_index_path: str,
    projected_node_ids_path: str,
    fusion_model_path: str,
    text_index_path: str,
    text_ids_path: str,
    node_index_path: str,
    node_ids_path: str
) -> None:
    fusion_model: CCA = read_obj(fusion_model_path)
    text_index = read_embeddings(text_index_path)
    text_ids: List[str] = read_obj(text_ids_path)
    node_index = read_embeddings(node_index_path)
    node_ids: List[str] = read_obj(node_ids_path)

    text_embeddings = extract_embeddings_from_index(text_index)
    node_embeddings = extract_embeddings_from_index(node_index)

    # Project text and node embeddings into the shared space
    text_projections, node_projections = fusion_model.transform(text_embeddings, node_embeddings)

    print(
        f"Saving {len(text_projections)} projected text embeddings of dim " +
        str(text_projections.shape[1])
    )
    save_embeddings(projected_text_index_path, text_projections)
    save_obj(projected_text_ids_path, text_ids)

    print(
        f"Saving {len(node_projections)} projected text embeddings of dim " +
        str(node_projections.shape[1])
    )
    save_embeddings(projected_node_index_path, node_projections)
    save_obj(projected_node_ids_path, node_ids)


def fuse_embeddings(
    fused_index_path: str,
    fused_ids_path: str,
    fusion_func: Callable[[np.ndarray, np.ndarray], np.ndarray],
    text_index_path: str,
    text_ids_path: str,
    node_index_path: str,
    node_ids_path: str
) -> None:
    text_index = read_embeddings(text_index_path)
    text_ids: List[str] = read_obj(text_ids_path)
    node_index = read_embeddings(node_index_path)
    node_ids: List[str] = read_obj(node_ids_path)

    text_embeddings = extract_embeddings_from_index(text_index)
    node_embeddings = extract_embeddings_from_index(node_index)

    aligned_node_embeddings, _ = align_embeddings(
        text_ids,
        node_embeddings,
        node_ids
    )

    fused_embeddings = fusion_func(text_embeddings, aligned_node_embeddings)
    print(f"Saving {len(fused_embeddings)} fused embeddings of dim {fused_embeddings.shape[1]}")
    save_embeddings(fused_index_path, fused_embeddings)
    save_obj(fused_ids_path, text_ids)


def concat_embeddings(text_embeddings: np.ndarray, node_embeddings: np.ndarray) -> np.ndarray:
    return np.concatenate((text_embeddings, node_embeddings), axis=1)


def create_linear_combiner(alpha: float) -> Callable[[np.ndarray, np.ndarray], np.ndarray]:
    def linearly_combine_embeddings(
        text_embeddings: np.ndarray,
        node_embeddings: np.ndarray
    ) -> np.ndarray:
        return alpha * text_embeddings + (1 - alpha) * node_embeddings
    return linearly_combine_embeddings
