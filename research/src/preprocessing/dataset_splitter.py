import json
from models.paper import Paper
from utils.file_utils import save_papers_to_json
from config.settings import TEST_SET_YEAR


class DatasetSplitter:
    def split_dataset(
        self,
        input_file_path: str,
        train_file_path: str,
        test_file_path: str
    ) -> None:
        train_papers = []
        test_papers = []

        with open(input_file_path, 'r', encoding="utf-8") as file:
            for line in file:
                try:
                    paper = Paper(**json.loads(line))

                    if paper.year >= TEST_SET_YEAR:
                        test_papers.append(paper)
                    else:
                        train_papers.append(paper)

                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON on line: {line} -> {e}")

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
