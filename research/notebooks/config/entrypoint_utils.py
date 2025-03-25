import os
import networkx as nx
import numpy as np
from typing import List, Union, Dict, Callable
from src.models.text.text_vectors import train_tfidf, generate_and_save_text_vectors
from src.evaluation.evaluate import evaluate
from src.models.text.text_embeddings import (
    generate_and_save_transformer_embeddings,
    train_doc2vec,
    generate_and_save_doc2vec_embeddings
)
from src.models.graph.graph import generate_and_save_graph
from src.models.graph.node_embeddings import (
    generate_and_save_train_node_embeddings,
    generate_and_save_test_node_embeddings
)
from src.models.fusion.fusion import train_fusion_model, project_embeddings, fuse_embeddings
from src.models.rerank.rerank import compute_and_save_rerank_scores


def run_train_tfidf(curr_dir: str, dataset: str) -> None:
    train_tfidf(
        os.path.join(curr_dir, f"data/embeddings/{dataset}_train_tfidf.pkl"),
        os.path.join(curr_dir, f"data/parsed/{dataset}_train.json")
    )


def run_generate_and_save_text_vectors(curr_dir: str, dataset: str, model: str) -> None:
    def with_split(split: str) -> None:
        generate_and_save_text_vectors(
            os.path.join(curr_dir, f"data/embeddings/{dataset}_{split}_{model}.faiss"),
            os.path.join(curr_dir, f"data/embeddings/{dataset}_{split}_{model}_ids.pkl"),
            os.path.join(curr_dir, f"data/parsed/{dataset}_{split}.json"),
            os.path.join(curr_dir, f"data/embeddings/{dataset}_train_{model}.pkl")
        )

    with_split("test")
    with_split("train")


def run_evaluate(
    curr_dir: str,
    dataset: str,
    model: str,
    k_vals: List[int],
    secondary_model: Union[str, None] = None,
    fusion_model: Union[str, None] = None,
    rerank_model: Union[str, None] = None
) -> None:
    if rerank_model:
        rerank_scores_path = os.path.join(
            curr_dir,
            f"data/embeddings/{dataset}_train_graph_{rerank_model}.pkl"
        )
    else:
        rerank_scores_path = None

    base_model = model.split('_')[0]
    evaluate(
        results_path=os.path.join(
            curr_dir,
            f"data/results/{base_model}/{dataset}{'_' + fusion_model if fusion_model else ''}" +
            f"_{model}{'_' + secondary_model if secondary_model else ''}" +
            f"{'_' + rerank_model if rerank_model else ''}_results.csv"
        ),
        train_index_path=os.path.join(
            curr_dir,
            f"data/embeddings/{dataset}_train{'_' + fusion_model if fusion_model else ''}" +
            f"_{base_model}{'_' + secondary_model if secondary_model else ''}.faiss"
        ),
        test_index_path=os.path.join(
            curr_dir,
            f"data/embeddings/{dataset}_test{'_' + fusion_model if fusion_model else ''}_{model}" +
            f"{'_' + secondary_model if secondary_model else ''}.faiss"
        ),
        train_ids_path=os.path.join(
            curr_dir,
            f"data/embeddings/{dataset}_train{'_' + fusion_model if fusion_model else ''}" +
            f"_{base_model}{'_' + secondary_model if secondary_model else ''}_ids.pkl"
        ),
        test_ids_path=os.path.join(
            curr_dir,
            f"data/embeddings/{dataset}_test{'_' + fusion_model if fusion_model else ''}_{model}" +
            f"{'_' + secondary_model if secondary_model else ''}_ids.pkl"
        ),
        test_papers_path=os.path.join(curr_dir, f"data/parsed/{dataset}_test.json"),
        k_vals=k_vals,
        rerank_scores_path=rerank_scores_path
    )


def run_generate_and_save_transformer_embeddings(
    curr_dir: str,
    dataset: str,
    model: str,
    adapter_config: Union[Dict[str, str], None] = None
) -> None:
    model_path = model.split('/')[-1].split('_')[0]

    def with_split(split: str) -> None:
        generate_and_save_transformer_embeddings(
            os.path.join(curr_dir, f"data/embeddings/{dataset}_{split}_{model_path}.faiss"),
            os.path.join(curr_dir, f"data/embeddings/{dataset}_{split}_{model_path}_ids.pkl"),
            os.path.join(curr_dir, f"data/parsed/{dataset}_{split}.json"),
            model,
            adapter_config
        )

    with_split("test")
    with_split("train")


def run_train_doc2vec(curr_dir: str, dataset: str) -> None:
    train_doc2vec(
        os.path.join(curr_dir, f"data/embeddings/{dataset}_train_doc2vec.model"),
        os.path.join(curr_dir, f"data/parsed/{dataset}_train.json")
    )


def run_generate_and_save_doc2vec_embeddings(curr_dir: str, dataset: str) -> None:
    def with_split(split: str) -> None:
        generate_and_save_doc2vec_embeddings(
            os.path.join(curr_dir, f"data/embeddings/{dataset}_{split}_doc2vec.faiss"),
            os.path.join(curr_dir, f"data/embeddings/{dataset}_{split}_doc2vec_ids.pkl"),
            os.path.join(curr_dir, f"data/parsed/{dataset}_{split}.json"),
            os.path.join(curr_dir, f"data/embeddings/{dataset}_train_doc2vec.model")
        )

    with_split("test")
    with_split("train")


def run_generate_and_save_graph(curr_dir: str, dataset: str) -> None:
    generate_and_save_graph(
        os.path.join(curr_dir, f"data/embeddings/{dataset}_train_graph.pkl"),
        os.path.join(curr_dir, f"data/parsed/{dataset}_train.json")
    )


def run_generate_and_save_train_node_embeddings(
    curr_dir: str,
    dataset: str,
    p: float,
    q: float
) -> None:
    model = f"node2vec_{p}_{q}"

    generate_and_save_train_node_embeddings(
        os.path.join(curr_dir, f"data/embeddings/{dataset}_train_{model}.faiss"),
        os.path.join(curr_dir, f"data/embeddings/{dataset}_train_{model}_ids.pkl"),
        os.path.join(curr_dir, f"data/embeddings/{dataset}_train_graph.pkl"),
        p,
        q
    )


def run_generate_and_save_test_node_embeddings(
    curr_dir: str,
    dataset: str,
    node_model: str,
    text_model: str,
    n_vals: List[int]
) -> None:
    test_node_index_paths = [
        os.path.join(
            curr_dir,
            f"data/embeddings/{dataset}_test_{node_model}_{text_model}_{n}.faiss"
        )
        for n in n_vals
    ]

    generate_and_save_test_node_embeddings(
        test_node_index_paths,
        os.path.join(curr_dir, f"data/embeddings/{dataset}_test_{node_model}_ids.pkl"),
        os.path.join(curr_dir, f"data/embeddings/{dataset}_train_{node_model}.faiss"),
        os.path.join(curr_dir, f"data/embeddings/{dataset}_train_{node_model}_ids.pkl"),
        os.path.join(curr_dir, f"data/embeddings/{dataset}_train_{text_model}.faiss"),
        os.path.join(curr_dir, f"data/embeddings/{dataset}_test_{text_model}.faiss"),
        os.path.join(curr_dir, f"data/embeddings/{dataset}_train_{text_model}_ids.pkl"),
        os.path.join(curr_dir, f"data/embeddings/{dataset}_test_{text_model}_ids.pkl"),
        n_vals
    )


def run_train_fusion_model(
    curr_dir: str,
    dataset: str,
    fusion_model: str,
    fusion_func: Callable[[str, np.ndarray, np.ndarray], None],
    text_model: str,
    node_model: str
) -> None:
    train_fusion_model(
        os.path.join(
            curr_dir,
            f"data/embeddings/{dataset}_{fusion_model}_{text_model}_{node_model}.pkl"
        ),
        fusion_func,
        os.path.join(curr_dir, f"data/embeddings/{dataset}_train_{text_model}.faiss"),
        os.path.join(curr_dir, f"data/embeddings/{dataset}_train_{text_model}_ids.pkl"),
        os.path.join(curr_dir, f"data/embeddings/{dataset}_train_{node_model}.faiss"),
        os.path.join(curr_dir, f"data/embeddings/{dataset}_train_{node_model}_ids.pkl")
    )


def run_project_embeddings(
    curr_dir: str,
    dataset: str,
    fusion_model: str,
    text_model: str,
    node_model: str,
    n_vals: List[int]
) -> None:
    def with_split(train: bool) -> None:
        split = "train" if train else "test"
        base_text_model = text_model.split('_')[0]

        project_embeddings(
            os.path.join(
                curr_dir,
                f"data/embeddings/{dataset}_{split}_{fusion_model}_text_projected_{text_model}" +
                f"_{node_model}.faiss"
            ),
            os.path.join(
                curr_dir,
                f"data/embeddings/{dataset}_{split}_{fusion_model}_text_projected_{text_model}" +
                f"_{node_model}_ids.pkl"
            ),
            os.path.join(
                curr_dir,
                f"data/embeddings/{dataset}_{split}_{fusion_model}_node_projected_{text_model}" +
                f"_{node_model}.faiss"
            ),
            os.path.join(
                curr_dir,
                f"data/embeddings/{dataset}_{split}_{fusion_model}_node_projected_{text_model}" +
                f"_{node_model}_ids.pkl"
            ),
            os.path.join(
                curr_dir,
                f"data/embeddings/{dataset}_{fusion_model}_{base_text_model}_{node_model}.pkl"
            ),
            os.path.join(curr_dir, f"data/embeddings/{dataset}_{split}_{base_text_model}.faiss"),
            os.path.join(curr_dir, f"data/embeddings/{dataset}_{split}_{base_text_model}_ids.pkl"),
            os.path.join(
                curr_dir,
                f"data/embeddings/{dataset}_{split}_{node_model}" +
                f"{'_' + text_model if not train else ''}.faiss"
            ),
            os.path.join(curr_dir, f"data/embeddings/{dataset}_{split}_{node_model}_ids.pkl")
        )

    with_split(True)
    original_text_model = text_model

    for n in n_vals:
        text_model = f"{original_text_model}_{n}"
        with_split(False)


def run_fuse_embeddings(
    curr_dir: str,
    dataset: str,
    fusion_model: str,
    fusion_func: Callable[[np.ndarray, np.ndarray], np.ndarray],
    text_model: str,
    node_model: str,
    n_vals: List[int]
) -> None:
    def with_split(train: bool) -> None:
        split = "train" if train else "test"
        base_text_model = text_model.split('_')[0]

        fuse_embeddings(
            os.path.join(
                curr_dir,
                f"data/embeddings/{dataset}_{split}_{fusion_model}_{text_model}_{node_model}.faiss"
            ),
            os.path.join(
                curr_dir,
                f"data/embeddings/{dataset}_{split}_{fusion_model}_{text_model}_{node_model}_ids" +
                ".pkl"
            ),
            fusion_func,
            os.path.join(curr_dir, f"data/embeddings/{dataset}_{split}_{base_text_model}.faiss"),
            os.path.join(curr_dir, f"data/embeddings/{dataset}_{split}_{base_text_model}_ids.pkl"),
            os.path.join(
                curr_dir,
                f"data/embeddings/{dataset}_{split}_{node_model}" +
                f"{'_' + text_model if not train else ''}.faiss"
            ),
            os.path.join(curr_dir, f"data/embeddings/{dataset}_{split}_{node_model}_ids.pkl")
        )

    with_split(True)
    original_text_model = text_model

    for n in n_vals:
        text_model = f"{original_text_model}_{n}"
        with_split(False)


def run_fuse_embeddings_with_projection(
    curr_dir: str,
    dataset: str,
    fusion_model: str,
    fusion_func: Callable[[np.ndarray, np.ndarray], np.ndarray],
    text_model: str,
    node_model: str,
    n_vals: List[int]
) -> None:
    projection = fusion_model.split('_')[0]

    def with_split(train: bool) -> None:
        split = "train" if train else "test"

        fuse_embeddings(
            os.path.join(
                curr_dir,
                f"data/embeddings/{dataset}_{split}_{fusion_model}_{text_model}_{node_model}.faiss"
            ),
            os.path.join(
                curr_dir,
                f"data/embeddings/{dataset}_{split}_{fusion_model}_{text_model}_{node_model}_ids" +
                ".pkl"
            ),
            fusion_func,
            os.path.join(
                curr_dir,
                f"data/embeddings/{dataset}_{split}_{projection}_text_projected_{text_model}" +
                f"_{node_model}.faiss"
            ),
            os.path.join(
                curr_dir,
                f"data/embeddings/{dataset}_{split}_{projection}_text_projected_{text_model}" +
                f"_{node_model}_ids.pkl"
            ),
            os.path.join(
                curr_dir,
                f"data/embeddings/{dataset}_{split}_{projection}_node_projected_{text_model}" +
                f"_{node_model}.faiss"
            ),
            os.path.join(
                curr_dir,
                f"data/embeddings/{dataset}_{split}_{projection}_node_projected_{text_model}" +
                f"_{node_model}_ids.pkl"
            )
        )

    with_split(True)
    original_text_model = text_model

    for n in n_vals:
        text_model = f"{original_text_model}_{n}"
        with_split(False)


def run_compute_and_save_rerank_scores(
    curr_dir: str,
    dataset: str,
    model: str,
    rerank_func: Callable[[nx.DiGraph], Dict[str, float]]
) -> None:
    compute_and_save_rerank_scores(
        os.path.join(curr_dir, f"data/embeddings/{dataset}_train_graph_{model}.pkl"),
        os.path.join(curr_dir, f"data/embeddings/{dataset}_train_graph.pkl"),
        rerank_func
    )
