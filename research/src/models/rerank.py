import networkx as nx
from typing import Dict
from src.utils.file_utils import read_obj, save_obj
from src.config.settings import PAGERANK_ALPHA, HITS_MAX_ITER, HITS_TOLERANCE


def compute_and_save_pagerank_scores(rerank_scores_path: str, graph_path: str) -> None:
    graph: nx.DiGraph = read_obj(graph_path)
    pagerank_scores = compute_pagerank_scores(graph)
    print(f"Saving {len(pagerank_scores)} PageRank scores")
    save_obj(rerank_scores_path, pagerank_scores)


def compute_pagerank_scores(graph: nx.DiGraph) -> Dict[str, float]:
    return nx.pagerank(graph, alpha=PAGERANK_ALPHA)


def compute_and_save_hits_scores(rerank_scores_path: str, graph_path: str) -> None:
    graph: nx.DiGraph = read_obj(graph_path)
    authority_scores = compute_hits_scores(graph)
    print(f"Saving {len(authority_scores)} HITS authority scores")
    save_obj(rerank_scores_path, authority_scores)


def compute_hits_scores(graph: nx.DiGraph) -> Dict[str, float]:
    _, authority_scores = nx.hits(graph, max_iter=HITS_MAX_ITER, tol=HITS_TOLERANCE)
    return authority_scores
