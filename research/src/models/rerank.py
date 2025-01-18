import networkx as nx
from typing import Dict
from src.utils.file_utils import read_obj, save_obj
from src.config.settings import PAGERANK_ALPHA


def compute_and_save_rerank_scores(graph_path: str, rerank_scores_path: str) -> None:
    graph: nx.DiGraph = read_obj(graph_path)
    pagerank_scores = compute_pagerank_scores(graph)
    print(f"Saving {len(pagerank_scores)} PageRank scores")
    save_obj(rerank_scores_path, pagerank_scores)


def compute_pagerank_scores(graph: nx.DiGraph, alpha: float = PAGERANK_ALPHA) -> Dict[str, float]:
    return nx.pagerank(graph, alpha=alpha)
