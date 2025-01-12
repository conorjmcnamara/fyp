import statistics
import matplotlib.pyplot as plt
from collections import defaultdict
from typing import Dict
from src.utils.file_utils import read_parsed_papers_from_json


class DatasetAnalyser:
    def analyse(self, file_path: str) -> None:
        paper_ids = set()
        duplicate_count = 0
        min_year = float("inf")
        max_year = float("-inf")
        citation_counts = []
        reference_counts = []

        papers = read_parsed_papers_from_json(file_path)
        paper_count = len(papers)

        for paper in papers:
            if paper.id in paper_ids:
                duplicate_count += 1
            paper_ids.add(paper.id)

            year = paper.year
            min_year = min(min_year, year)
            max_year = max(max_year, year)

            citation_counts.append(paper.citation_count)
            reference_counts.append(len(paper.references))

        total_citation_count = sum(citation_counts)
        total_reference_count = sum(reference_counts)

        mean_citation_count = total_citation_count / paper_count
        mean_reference_count = total_reference_count / paper_count

        median_citation_count = statistics.median(citation_counts)
        median_reference_count = statistics.median(reference_counts)

        min_citation_count = min(citation_counts)
        max_citation_count = max(citation_counts)

        min_reference_count = min(reference_counts)
        max_reference_count = max(reference_counts)

        print(f"\nDataset statistics for: {file_path}")
        print(f"Num papers: {paper_count}")
        print(f"Num duplicates: {duplicate_count}")
        print(f"Year range: {min_year} - {max_year}")

        print(f"\nTotal citation count: {total_citation_count}")
        print(f"Mean citation count: {mean_citation_count:.2f}")
        print(f"Median citation count: {median_citation_count}")
        print(f"Min citation count: {min_citation_count}")
        print(f"Max citation count: {max_citation_count}")

        print(f"\nTotal reference count: {total_reference_count}")
        print(f"Mean reference count: {mean_reference_count:.2f}")
        print(f"Median reference count: {median_reference_count}")
        print(f"Min reference count: {min_reference_count}")
        print(f"Max reference count: {max_reference_count}")

    def analyse_test_set(self, file_path: str) -> None:
        ground_truth_reference_counts = []
        ground_truth_reference_frequencies = defaultdict(int)

        papers = read_parsed_papers_from_json(file_path)
        paper_count = len(papers)

        for paper in papers:
            num_references = len(paper.ground_truth_references)
            ground_truth_reference_counts.append(num_references)
            ground_truth_reference_frequencies[num_references] += 1

        total_ground_truth_count = sum(ground_truth_reference_counts)
        mean_ground_truth_count = total_ground_truth_count / paper_count
        median_ground_truth_count = statistics.median(ground_truth_reference_counts)
        min_ground_truth_count = min(ground_truth_reference_counts)
        max_ground_truth_count = max(ground_truth_reference_counts)

        print(f"\nTest dataset statistics for: {file_path}")
        print(f"Num papers: {paper_count}")
        print(f"Total ground truth references: {total_ground_truth_count}")
        print(f"Mean ground truth references: {mean_ground_truth_count:.2f}")
        print(f"Median ground truth references: {median_ground_truth_count}")
        print(f"Min ground truth references: {min_ground_truth_count}")
        print(f"Max ground truth references: {max_ground_truth_count}")

        self._plot_ground_truth_reference_distribution(ground_truth_reference_frequencies)

    def _plot_ground_truth_reference_distribution(self, frequencies: Dict[int, int]) -> None:
        reference_counts = list(frequencies.keys())

        plt.figure(figsize=(10, 6))
        plt.bar(reference_counts, list(frequencies.values()))
        plt.xlabel("Number of Ground Truth References")
        plt.ylabel("Number of Test Papers")
        plt.title("Distribution of Ground Truth References in Test Papers")
        plt.show()
