import numpy as np
from typing import List, Tuple
from src.utils.file_utils import read_embeddings, read_ids, read_papers, save_results


def evaluate(
    train_index_path: str,
    test_index_path: str,
    train_ids_path: str,
    test_ids_path: str,
    test_json_path: str,
    k_vals: List[int],
    results_path: str
) -> None:
    train_index = read_embeddings(train_index_path)
    test_index = read_embeddings(test_index_path)
    train_ids = read_ids(train_ids_path)
    test_ids = read_ids(test_ids_path)

    test_papers = read_papers(test_json_path)
    ground_truth_references_map = {
        paper.id: paper.ground_truth_references for paper in test_papers
    }

    precision_at_k = {k: [] for k in k_vals}
    recall_at_k = {k: [] for k in k_vals}
    avg_precision_at_k = {k: [] for k in k_vals}

    for i, test_id in enumerate(test_ids):
        ground_truth = ground_truth_references_map[test_id]
        if not ground_truth:
            continue

        test_vector = test_index.reconstruct(i)
        max_k = max(k_vals)

        # Retrieve top-N neighbours (max K)
        _, indices = train_index.search(np.expand_dims(test_vector, axis=0), max_k)
        recommended_ids = [train_ids[idx] for idx in indices[0]]

        for k in k_vals:
            precision, recall, ap = compute_metrics_at_k(recommended_ids, ground_truth, k)
            precision_at_k[k].append(precision)
            recall_at_k[k].append(recall)
            avg_precision_at_k[k].append(ap)

    results = {
        "K": k_vals,
        "P@K": [round(np.mean(precision_at_k[k]), 4) for k in k_vals],
        "R@K": [round(np.mean(recall_at_k[k]), 4) for k in k_vals],
        "MAP@K": [round(np.mean(avg_precision_at_k[k]), 4) for k in k_vals]
    }

    print("Saving results")
    save_results(results_path, results)


def compute_metrics_at_k(
    recommended_ids: List[str],
    ground_truth: List[str],
    k: int
) -> Tuple[float, float, float]:
    recommended_at_k = recommended_ids[:k]
    recommended_set = set(recommended_at_k)
    relevant_set = set(ground_truth)

    # Precision at K
    precision = len(recommended_set & relevant_set) / k

    # Recall at K
    recall = len(recommended_set & relevant_set) / len(relevant_set)

    # Average Precision
    ap = 0
    relevant_count = 0

    for i, rec_id in enumerate(recommended_at_k):
        if rec_id in relevant_set:
            relevant_count += 1
            ap += relevant_count / (i + 1)

    ap /= len(relevant_set)

    return precision, recall, ap
