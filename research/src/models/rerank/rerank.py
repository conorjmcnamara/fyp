import networkx as nx
from typing import Callable, Dict
from src.utils.file_utils import read_obj, save_obj
from src.config.settings import PAGERANK_ALPHA, HITS_MAX_ITER, HITS_TOLERANCE


def compute_and_save_rerank_scores(
    rerank_scores_path: str,
    graph_path: str,
    rerank_func: Callable[[nx.DiGraph], Dict[str, float]]
) -> None:
    graph: nx.DiGraph = read_obj(graph_path)
    scores = rerank_func(graph)
    print(f"Saving {len(scores)} scores")
    save_obj(rerank_scores_path, scores)


def compute_pagerank_scores(graph: nx.DiGraph) -> Dict[str, float]:
    return nx.pagerank(graph, alpha=PAGERANK_ALPHA)


def compute_hits_scores(graph: nx.DiGraph) -> Dict[str, float]:
    _, authority_scores = nx.hits(graph, max_iter=HITS_MAX_ITER, tol=HITS_TOLERANCE)
    return authority_scores
