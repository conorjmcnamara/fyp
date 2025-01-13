import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List, Tuple
from src.utils.file_utils import read_parsed_papers_from_json
from src.config.settings import MAX_FEATURES, MIN_DOC_FREQ
from src.data_models.paper import Paper
from src.models.text_embeddings import save_embeddings


def normalize_text(text: str) -> str:
    # Remove non-alphabetic, non-space characters
    normalized_text = re.sub(r"[^a-zA-Z\s]", ' ', text)

    # Remove extra spaces
    return re.sub(r"\s+", ' ', normalized_text).strip()


def preprocess_papers(papers: List[Paper]) -> List[Paper]:
    for paper in papers:
        paper.title = normalize_text(paper.title)
        paper.abstract = normalize_text(paper.abstract)
    return papers


def generate_vectors(
    papers: List[Paper],
    vectorizer: TfidfVectorizer
) -> Tuple[np.ndarray, List[str]]:
    corpus = [f"{paper.title} {paper.abstract}" for paper in papers]
    ids = [paper.id for paper in papers]
    vectors = vectorizer.transform(corpus).toarray()
    return vectors, ids


def generate_and_save_vectors(
    input_train_path: str,
    input_test_path: str,
    output_train_path: str,
    output_test_path: str
) -> None:
    train_papers = read_parsed_papers_from_json(input_train_path)
    train_papers = preprocess_papers(train_papers)

    # Fit a TF-IDF vectorizer on the training corpus
    vectorizer = TfidfVectorizer(
        max_features=MAX_FEATURES,
        sublinear_tf=True,
        stop_words="english",
        min_df=MIN_DOC_FREQ,
        lowercase=True
    )
    train_corpus = [f"{paper.title} {paper.abstract}" for paper in train_papers]
    vectorizer.fit(train_corpus)
    print("Fitted vectorizer")

    train_vectors, train_ids = generate_vectors(train_papers, vectorizer)
    print(f"Saving {len(train_vectors)} training vectors of size {train_vectors.shape[1]}")
    save_embeddings(output_train_path, train_vectors, train_ids)

    test_papers = read_parsed_papers_from_json(input_test_path)
    test_papers = preprocess_papers(test_papers)
    test_vectors, test_ids = generate_vectors(test_papers, vectorizer)
    print(f"Saving {len(test_vectors)} training vectors of size {test_vectors.shape[1]}")
    save_embeddings(output_test_path, test_vectors, test_ids)
