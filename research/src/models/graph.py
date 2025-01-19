import networkx as nx
from typing import List
from src.utils.file_utils import read_papers, save_obj
from src.data_models.paper import Paper


def generate_and_save_graph(train_papers_path: str, graph_path: str) -> None:
    train_papers = read_papers(train_papers_path)
    graph = generate_graph(train_papers)

    num_nodes = graph.number_of_nodes()
    num_edges = graph.number_of_edges()
    print(f"Saving training graph with {num_nodes} nodes and {num_edges} edges")
    save_obj(graph_path, graph)


def generate_graph(papers: List[Paper]) -> nx.DiGraph:
    graph = nx.DiGraph()

    for paper in papers:
        paper_id = paper.id
        references = paper.references

        graph.add_node(paper_id)
        for ref_id in references:
            graph.add_edge(paper_id, ref_id)

    return graph
