import statistics
import matplotlib.pyplot as plt
from collections import defaultdict
from typing import List
from src.data_models.dataset_config import DatasetConfig
from src.utils.file_utils import read_papers


def analyse_dataset(papers_path: str, config: DatasetConfig) -> None:
    papers = read_papers(papers_path)
    ids = set()

    num_papers = len(papers)
    num_duplicates = 0
    min_year = float("inf")
    max_year = float("-inf")

    test_start_year = config.test_years[0]
    num_papers_lt_test_year = 0
    num_papers_gte_test_year = 0

    citation_counts = []
    reference_counts = []
    external_reference_count = 0
    num_references_lt_test_year_cite_gte = 0
    num_references_gte_test_year_cite_gte = 0
    paper_map = {paper.id: paper for paper in papers}

    for paper in papers:
        if paper.id in ids:
            num_duplicates += 1
            continue
        ids.add(paper.id)

        year = paper.year
        min_year = min(min_year, year)
        max_year = max(max_year, year)
        if year < test_start_year:
            num_papers_lt_test_year += 1
        else:
            num_papers_gte_test_year += 1

        citation_counts.append(paper.citation_count)
        reference_counts.append(len(paper.references))
    
        for ref_id in paper.references:
            if ref_id not in paper_map:
                external_reference_count += 1
            elif paper_map[ref_id].year >= test_start_year:
                if paper.year < test_start_year:
                    num_references_lt_test_year_cite_gte += 1
                else:
                    num_references_gte_test_year_cite_gte += 1

    print(f"\n\nDataset statistics for: {papers_path}")
    print(f"Num papers: {num_papers}")
    print(f"Num duplicates: {num_duplicates}")
    print(f"Year range: {min_year} - {max_year}")
    print(f"Num papers with year < {test_start_year}: {num_papers_lt_test_year}")
    print(f"Num papers with year >= {test_start_year}: {num_papers_gte_test_year}")

    compute_reference_stats(citation_counts, reference_counts, num_papers)

    print(f"\nNum external references: {external_reference_count}")
    print(
        f"Num references from papers with year < {test_start_year} to papers with year >= "
        f"{test_start_year}: {num_references_lt_test_year_cite_gte}"
    )
    print(
        f"Num references from papers with year >= {test_start_year} to papers with year >= "
        f"{test_start_year}: {num_references_gte_test_year_cite_gte}"
    )


def compute_reference_stats(
    citation_counts: List[int],
    reference_counts: List[int],
    num_papers: int
) -> None:
    total_citation_count = sum(citation_counts)
    mean_citation_count = total_citation_count / num_papers
    median_citation_count = statistics.median(citation_counts)
    min_citation_count = min(citation_counts)
    max_citation_count = max(citation_counts)

    print(f"\nTotal citation count: {total_citation_count}")
    print(f"Mean citation count: {mean_citation_count:.2f}")
    print(f"Median citation count: {median_citation_count}")
    print(f"Min citation count: {min_citation_count}")
    print(f"Max citation count: {max_citation_count}")

    total_reference_count = sum(reference_counts)
    mean_reference_count = total_reference_count / num_papers
    median_reference_count = statistics.median(reference_counts)
    min_reference_count = min(reference_counts)
    max_reference_count = max(reference_counts)

    print(f"\nTotal reference count: {total_reference_count}")
    print(f"Mean reference count: {mean_reference_count:.2f}")
    print(f"Median reference count: {median_reference_count}")
    print(f"Min reference count: {min_reference_count}")
    print(f"Max reference count: {max_reference_count}")


def plot_reference_distribution(papers_path: str) -> None:
    papers = read_papers(papers_path)
    reference_freq = defaultdict(int)

    for paper in papers:
        num_references = len(paper.references)
        reference_freq[num_references] += 1

    plt.figure(figsize=(10, 6))
    plt.bar(list(reference_freq.keys()), list(reference_freq.values()))
    plt.xlabel("Number of References")
    plt.ylabel("Number of Papers")
    plt.title("Distribution of Reference Counts")
    plt.show()
