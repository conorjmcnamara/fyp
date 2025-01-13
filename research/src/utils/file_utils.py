import json
import faiss
import numpy as np
import pickle
import pandas as pd
from typing import List, Dict
from src.data_models.paper import Paper
from src.config.settings import TEST_SET_YEAR


def combine_json_files(input_json_paths: List[str], output_json_path: str) -> None:
    with open(output_json_path, 'w', encoding="utf-8") as outfile:
        outfile.write("[\n")
        is_first_entry = True

        for input_json_path in input_json_paths:
            with open(input_json_path, 'r', encoding='utf-8') as file:
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


def save_papers(json_path: str, papers: List[Paper]) -> None:
    with open(json_path, 'w', encoding="utf-8") as file:
        lines = ["[\n"]
        lines.extend(f"{json.dumps(paper.__dict__)},\n" for paper in papers[:-1])
        lines.append(json.dumps(papers[-1].__dict__))
        lines.append("\n]")
        file.writelines(lines)


def read_papers(json_path: str) -> List[Paper]:
    papers = []

    with open(json_path, 'r', encoding="utf-8") as file:
        for line in file:
            line = line.strip().strip(',')
            if not line or line.startswith('[') or line.endswith(']'):
                continue

            try:
                papers.append(Paper(**json.loads(line)))
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON on line: {line} -> {e}")

    return papers


def split_dataset(input_json_path: str, train_json_path: str, test_json_path: str) -> None:
    papers = read_papers(input_json_path)
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

    save_papers(train_json_path, train_papers)
    save_papers(test_json_path, test_papers)


def save_embeddings(index_path: str, embeddings: np.ndarray) -> None:
    embeddings = embeddings.astype(np.float32)

    # Normalize embeddings for cosine similarity and store in a FAISS index with inner product
    faiss.normalize_L2(embeddings)
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)
    faiss.write_index(index, index_path)


def save_ids(ids_path: str, ids: List[str]) -> None:
    with open(ids_path, "wb") as file:
        pickle.dump(ids, file)


def read_embeddings(index_path: str) -> faiss.Index:
    return faiss.read_index(index_path)


def read_ids(ids_path: str) -> List[str]:
    with open(ids_path, "rb") as file:
        return pickle.load(file)


def save_results(results_path: str, results: Dict[str, List[float]]) -> None:
    df = pd.DataFrame(results)
    df.to_csv(results_path, index=False)
