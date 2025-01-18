import numpy as np
from typing import List, Tuple, Dict
from src.utils.file_utils import read_embeddings, read_obj, read_papers, save_results


def evaluate(
    train_index_path: str,
    test_index_path: str,
    train_ids_path: str,
    test_ids_path: str,
    test_json_path: str,
    k_vals: List[int],
    results_path: str,
    rerank_scores_path: str = None
) -> None:
    train_index = read_embeddings(train_index_path)
    test_index = read_embeddings(test_index_path)
    train_ids: List[str] = read_obj(train_ids_path)
    test_ids: List[str] = read_obj(test_ids_path)
    test_papers = read_papers(test_json_path)

    rerank_scores = None
    if rerank_scores_path:
        rerank_scores: Dict[str, float] = read_obj(rerank_scores_path)

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
            top_k_recommendations = recommended_ids[:k]

            # Rerank recommendations
            if rerank_scores:
                top_k_recommendations = rerank_recommendations(top_k_recommendations, rerank_scores)
            
            precision, recall, ap = compute_metrics(top_k_recommendations, ground_truth)
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


def rerank_recommendations(
    recommended_ids: List[str],
    rerank_scores: Dict[str, float]
) -> List[str]:
    reranked_recommendations = sorted(
        recommended_ids, key=lambda id: rerank_scores.get(id, 0), reverse=True
    )
    return reranked_recommendations


def compute_metrics(
    recommended_ids: List[str],
    ground_truth: List[str]
) -> Tuple[float, float, float]:
    recommended_set = set(recommended_ids)
    relevant_set = set(ground_truth)

    # Precision at K
    precision = len(recommended_set & relevant_set) / len(recommended_ids)

    # Recall at K
    recall = len(recommended_set & relevant_set) / len(relevant_set)

    # Average Precision at K
    ap = 0
    relevant_count = 0
    for i, rec_id in enumerate(recommended_ids):
        if rec_id in relevant_set:
            relevant_count += 1
            ap += relevant_count / (i + 1)
    ap /= len(relevant_set)

    return precision, recall, ap
