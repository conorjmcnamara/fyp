import statistics
import matplotlib.pyplot as plt
from collections import defaultdict
from src.utils.file_utils import read_papers
from src.config.settings import TEST_SET_YEAR


def analyse_dataset(papers_path: str) -> None:
    papers = read_papers(papers_path)
    num_papers = len(papers)
    num_duplicates = 0
    ids = set()

    min_year = float("inf")
    max_year = float("-inf")
    num_papers_lt_test_year = 0
    num_papers_gte_test_year = 0
    citation_counts = []
    reference_counts = []

    for paper in papers:
        if paper.id in ids:
            num_duplicates += 1
        ids.add(paper.id)

        year = paper.year
        min_year = min(min_year, year)
        max_year = max(max_year, year)
        if year < TEST_SET_YEAR:
            num_papers_lt_test_year += 1
        else:
            num_papers_gte_test_year += 1

        citation_counts.append(paper.citation_count)
        reference_counts.append(len(paper.references))

    external_reference_count = 0
    num_references_lt_test_year_cite_gte = 0
    num_references_gte_test_year_cite_gte = 0
    paper_map = {paper.id: paper for paper in papers}

    for paper in papers:
        for ref_id in paper.references:
            if ref_id not in ids:
                external_reference_count += 1
            elif paper_map[ref_id].year >= TEST_SET_YEAR:
                if paper.year < TEST_SET_YEAR:
                    num_references_lt_test_year_cite_gte += 1
                else:
                    num_references_gte_test_year_cite_gte += 1

    total_citation_count = sum(citation_counts)
    total_reference_count = sum(reference_counts)

    mean_citation_count = total_citation_count / num_papers
    mean_reference_count = total_reference_count / num_papers

    median_citation_count = statistics.median(citation_counts)
    median_reference_count = statistics.median(reference_counts)

    min_citation_count = min(citation_counts)
    max_citation_count = max(citation_counts)

    min_reference_count = min(reference_counts)
    max_reference_count = max(reference_counts)

    print(f"\n\nDataset statistics for: {papers_path}")
    print(f"Num papers: {num_papers}")
    print(f"Num duplicates: {num_duplicates}")
    print(f"Year range: {min_year} - {max_year}")
    print(f"Num papers with year < {TEST_SET_YEAR}: {num_papers_lt_test_year}")
    print(f"Num papers with year >= {TEST_SET_YEAR}: {num_papers_gte_test_year}")

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
    print(f"Num external references: {external_reference_count}")
    print(
        f"Num references from papers with year < {TEST_SET_YEAR} to papers with year >= "
        f"{TEST_SET_YEAR}: {num_references_lt_test_year_cite_gte}"
    )
    print(
        f"Num references from papers with year >= {TEST_SET_YEAR} to papers with year >= "
        f"{TEST_SET_YEAR}: {num_references_gte_test_year_cite_gte}"
    )


def plot_reference_distribution(papers_path: str) -> None:
    papers = read_papers(papers_path)
    ground_truth_reference_freq = defaultdict(int)

    for paper in papers:
        num_references = len(paper.references)
        ground_truth_reference_freq[num_references] += 1

    plt.figure(figsize=(10, 6))
    plt.bar(list(ground_truth_reference_freq.keys()), list(ground_truth_reference_freq.values()))
    plt.xlabel("Number of Ground Truth References")
    plt.ylabel("Number of Test Papers")
    plt.title("Distribution of Ground Truth References in Test Papers")
    plt.show()
