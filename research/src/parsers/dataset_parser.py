import json
from abc import ABC, abstractmethod
from typing import Callable, Dict, Any, List
from src.data_models.dataset_config import DatasetConfig
from src.data_models.paper import Paper
from src.utils.preprocess_utils import remove_missing_references, compute_citation_counts
from src.utils.file_utils import read_papers, save_papers


class DatasetParser(ABC):
    def __init__(self, config: DatasetConfig):
        self.config = config

    @abstractmethod
    def parse_and_transform(self, input_path: str, output_json_path: str) -> None:
        pass

    @abstractmethod
    def is_paper_populated(self, paper: Paper) -> bool:
        pass

    def read_json(
        self,
        json_path: str,
        parse_func: Callable[[Dict[str, Any]], Paper]
    ) -> Dict[str, Paper]:
        papers = {}

        with open(json_path, 'r', encoding="utf-8") as file:
            for line in file:
                line = line.strip().strip(',')
                if not line or line.startswith('[') or line.endswith(']'):
                    continue

                try:
                    paper = parse_func(json.loads(line))
                    if self.is_paper_populated(paper):
                        papers[paper.id] = paper

                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON on line: {line} -> {e}")

        return papers

    def filter_papers(self, papers: Dict[str, Paper]) -> Dict[str, Paper]:
        # Remove references to papers with missing metadata
        remove_missing_references(list(papers.values()))
        compute_citation_counts(list(papers.values()))

        papers = {
            id: paper for id, paper in papers.items()
            if (
                paper.citation_count >= self.config.min_citations_filter and
                len(paper.references) >= self.config.min_references_filter
            )
        }

        # Remove references to filtered papers
        remove_missing_references(list(papers.values()))
        compute_citation_counts(list(papers.values()))

        return papers

    def split_dataset(
        self,
        dataset_path: str,
        train_papers_path: str,
        test_papers_path: str
    ) -> None:
        papers = read_papers(dataset_path)
        train_papers: List[Paper] = []
        test_papers: List[Paper] = []

        for paper in papers:
            if self.config.train_years[0] <= paper.year <= self.config.train_years[1]:
                train_papers.append(paper)
            elif self.config.test_years[0] <= paper.year <= self.config.test_years[1]:
                test_papers.append(paper)

        remove_missing_references(train_papers)
        compute_citation_counts(train_papers)

        train_ids = set(train_paper.id for train_paper in train_papers)
        for test_paper in test_papers:
            test_paper.references = [
                ref_id for ref_id in test_paper.references if ref_id in train_ids
            ]

        test_papers = [test_paper for test_paper in test_papers if len(test_paper.references) > 0]
        compute_citation_counts(test_papers)

        save_papers(train_papers_path, train_papers)
        save_papers(test_papers_path, test_papers)
