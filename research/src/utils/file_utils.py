import os
import json
import faiss
import numpy as np
import pickle
import pandas as pd
from typing import List, Dict, Any
from src.data_models.paper import Paper
from src.utils.preprocess_utils import remove_missing_references, compute_citation_counts
from src.config.settings import TEST_SET_YEAR


def combine_json_files(input_json_paths: List[str], combined_json_path: str) -> None:
    os.makedirs(os.path.dirname(combined_json_path), exist_ok=True)
    with open(combined_json_path, 'w', encoding="utf-8") as outfile:
        outfile.write("[\n")
        is_first_entry = True

        for input_json_path in input_json_paths:
            with open(input_json_path, 'r', encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if not line or line.startswith('[') or line.endswith(']'):
                        continue

                    if is_first_entry:
                        is_first_entry = False
                    else:
                        outfile.write(",\n")
                    outfile.write(line.strip(','))

        outfile.write("\n]")


def save_papers(papers_path: str, papers: List[Paper]) -> None:
    os.makedirs(os.path.dirname(papers_path), exist_ok=True)
    with open(papers_path, 'w', encoding="utf-8") as file:
        lines = ["[\n"]
        lines.extend(f"{json.dumps(paper.__dict__)},\n" for paper in papers[:-1])
        lines.append(json.dumps(papers[-1].__dict__))
        lines.append("\n]")
        file.writelines(lines)


def read_papers(papers_path: str) -> List[Paper]:
    papers = []
    with open(papers_path, 'r', encoding="utf-8") as file:
        for line in file:
            line = line.strip().strip(',')
            if not line or line.startswith('[') or line.endswith(']'):
                continue

            try:
                papers.append(Paper(**json.loads(line)))
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON on line: {line} -> {e}")
    return papers


def split_dataset(dataset_path: str, train_papers_path: str, test_papers_path: str) -> None:
    papers = read_papers(dataset_path)
    train_papers: List[Paper] = []
    test_papers: List[Paper] = []

    for paper in papers:
        if paper.year >= TEST_SET_YEAR:
            test_papers.append(paper)
        else:
            train_papers.append(paper)

    remove_missing_references(train_papers)
    compute_citation_counts(train_papers)

    train_ids = set(train_paper.id for train_paper in train_papers)
    for test_paper in test_papers:
        test_paper.references = [ref_id for ref_id in test_paper.references if ref_id in train_ids]

    test_papers = [test_paper for test_paper in test_papers if len(test_paper.references) > 0]
    compute_citation_counts(test_papers)

    save_papers(train_papers_path, train_papers)
    save_papers(test_papers_path, test_papers)


def save_embeddings(index_path: str, embeddings: np.ndarray) -> None:
    os.makedirs(os.path.dirname(index_path), exist_ok=True)
    embeddings = embeddings.astype(np.float32)

    # Normalize embeddings for cosine similarity and store in a FAISS index with inner product
    faiss.normalize_L2(embeddings)
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)
    faiss.write_index(index, index_path)


def read_embeddings(index_path: str) -> faiss.Index:
    return faiss.read_index(index_path)


def save_obj(path: str, obj: Any) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as file:
        pickle.dump(obj, file)


def read_obj(path: str) -> Any:
    with open(path, "rb") as file:
        return pickle.load(file)


def save_results(path: str, results: Dict[str, List[float]]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df = pd.DataFrame(results)
    df.to_csv(path, index=False)
