from src.utils.file_utils import read_parsed_papers_from_json, save_papers_to_json
from src.config.settings import TEST_SET_YEAR


class DatasetSplitter:
    def split_dataset(
        self,
        input_file_path: str,
        train_file_path: str,
        test_file_path: str
    ) -> None:
        papers = read_parsed_papers_from_json(input_file_path)
        train_papers = []
        test_papers = []

        for paper in papers:
            if paper.year >= TEST_SET_YEAR:
                test_papers.append(paper)
            else:
                train_papers.append(paper)

        train_ids = set(train_paper.id for train_paper in train_papers)
        for test_paper in test_papers:
            test_paper.ground_truth_references = [
                ref_id for ref_id in test_paper.references if ref_id in train_ids
            ]

        test_papers = [
            test_paper for test_paper in test_papers if len(test_paper.ground_truth_references) > 0
        ]

        save_papers_to_json(train_file_path, train_papers)
        save_papers_to_json(test_file_path, test_papers)
