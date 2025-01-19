import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List, Tuple
from src.utils.file_utils import read_papers, save_embeddings, save_obj
from src.config.settings import MIN_DOC_FREQ
from src.data_models.paper import Paper


def generate_and_save_vectors(
    train_index_path: str,
    test_index_path: str,
    train_ids_path: str,
    test_ids_path: str,
    train_papers_path: str,
    test_papers_path: str
) -> None:
    # Process training papers
    train_papers = read_papers(train_papers_path)
    train_papers = preprocess_papers(train_papers)

    # Fit TF-IDF vectorizer on the training corpus
    vectorizer = TfidfVectorizer(
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
    save_embeddings(train_index_path, train_vectors)
    save_obj(train_ids_path, train_ids)

    # Process testing papers
    test_papers = read_papers(test_papers_path)
    test_papers = preprocess_papers(test_papers)
    test_vectors, test_ids = generate_vectors(test_papers, vectorizer)
    print(f"Saving {len(test_vectors)} testing vectors of size {test_vectors.shape[1]}")
    save_embeddings(test_index_path, test_vectors)
    save_obj(test_ids_path, test_ids)


def preprocess_papers(papers: List[Paper]) -> List[Paper]:
    for paper in papers:
        paper.title = normalize_text(paper.title)
        paper.abstract = normalize_text(paper.abstract)
    return papers


def normalize_text(text: str) -> str:
    # Remove non-alphabetic, non-space characters
    normalized_text = re.sub(r"[^a-zA-Z\s]", ' ', text)

    # Remove extra spaces
    return re.sub(r"\s+", ' ', normalized_text).strip()


def generate_vectors(
    papers: List[Paper],
    vectorizer: TfidfVectorizer
) -> Tuple[np.ndarray, List[str]]:
    corpus = [f"{paper.title} {paper.abstract}" for paper in papers]
    ids = [paper.id for paper in papers]
    vectors = vectorizer.transform(corpus).toarray()
    return vectors, ids
