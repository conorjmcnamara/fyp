import networkx as nx
import numpy as np
from node2vec import Node2Vec
from typing import Tuple, List
from src.utils.file_utils import save_obj, read_obj, save_embeddings, read_embeddings
from src.config.settings import (
    NODE2VEC_DIM,
    NODE2VEC_WALK_LEN,
    NODE2VEC_NUM_WALKS,
    NUM_WORKERS,
    NODE2VEC_WINDOW,
    NODE2VEC_MIN_COUNT,
    NODE2VEC_BATCH_WORDS
)


def generate_and_save_train_embeddings(index_path: str, ids_path: str, graph_path: str) -> None:
    graph: nx.DiGraph = read_obj(graph_path)
    embeddings, ids = generate_train_embeddings(graph)
    print(f"Saving {len(embeddings)} training embeddings of size {embeddings.shape[1]}")
    save_embeddings(index_path, embeddings)
    save_obj(ids_path, ids)


def generate_train_embeddings(graph: nx.DiGraph) -> Tuple[np.ndarray, List[str]]:
    node2vec = Node2Vec(
        graph,
        dimensions=NODE2VEC_DIM,
        walk_length=NODE2VEC_WALK_LEN,
        num_walks=NODE2VEC_NUM_WALKS,
        workers=NUM_WORKERS
    )

    # Fit Node2vec model
    model = node2vec.fit(
        window=NODE2VEC_WINDOW,
        min_count=NODE2VEC_MIN_COUNT,
        batch_words=NODE2VEC_BATCH_WORDS
    )

    ids = list(graph.nodes)
    embeddings = np.array([model.wv[id] for id in ids])
    return embeddings, ids


def generate_and_save_test_embeddings(
    test_node_index_path: str,
    test_node_ids_path: str,
    train_node_index_path: str,
    train_node_ids_path: str,
    train_text_index_path: str,
    test_text_index_path: str,
    train_text_ids_path: str,
    test_text_ids_path: str,
    n: int
) -> None:
    embeddings, ids = generate_test_embeddings(
        train_node_index_path,
        train_node_ids_path,
        train_text_index_path,
        test_text_index_path,
        train_text_ids_path,
        test_text_ids_path,
        n
    )
    print(f"Saving {len(embeddings)} testing embeddings of size {embeddings.shape[1]}")
    save_embeddings(test_node_index_path, embeddings)
    save_obj(test_node_ids_path, ids)


def generate_test_embeddings(
    train_node_index_path: str,
    train_node_ids_path: str,
    train_text_index_path: str,
    test_text_index_path: str,
    train_text_ids_path: str,
    test_text_ids_path: str,
    n: int
) -> Tuple[np.ndarray, List[str]]:
    train_node_index = read_embeddings(train_node_index_path)
    train_node_ids: List[str] = read_obj(train_node_ids_path)
    train_text_index = read_embeddings(train_text_index_path)
    test_text_index = read_embeddings(test_text_index_path)
    train_text_ids: List[str] = read_obj(train_text_ids_path)
    test_text_ids: List[str] = read_obj(test_text_ids_path)

    train_node_id_to_idx = {id: idx for idx, id in enumerate(train_node_ids)}
    test_node_embeddings = []
    test_node_ids = []

    for i, test_id in enumerate(test_text_ids):
        test_text_vector = test_text_index.reconstruct(i)

        # Retrieve top-N training text neighbours
        _, indices = train_text_index.search(np.expand_dims(test_text_vector, axis=0), n)
        neighbour_text_ids = [train_text_ids[j] for j in indices[0]]

        neighbour_node_embeddings = []
        for neighbour_text_id in neighbour_text_ids:
            node_idx = train_node_id_to_idx[neighbour_text_id]
            neighbour_node_embeddings.append(train_node_index.reconstruct(node_idx))

        # Average neighbour node embeddings
        avg_node_embedding = np.mean(neighbour_node_embeddings, axis=0)
        test_node_embeddings.append(avg_node_embedding)
        test_node_ids.append(test_id)

    return np.array(test_node_embeddings), test_node_ids
