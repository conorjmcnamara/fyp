import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List, Tuple
from src.data_models.paper import Paper
from src.utils.file_utils import read_papers, save_embeddings, read_obj, save_obj
from src.config.settings import MIN_DOC_FREQ


def train_tfidf(tfidf_path: str, papers_path: str) -> None:
    papers = read_papers(papers_path)
    papers = preprocess_papers(papers)

    # Fit TF-IDF on the training set
    vectorizer = TfidfVectorizer(
        sublinear_tf=True,
        stop_words="english",
        min_df=MIN_DOC_FREQ,
        lowercase=True
    )
    corpus = [f"{paper.title} {paper.abstract}" for paper in papers]
    vectorizer.fit(corpus)

    print("Saving TF-IDF vectorizer")
    save_obj(tfidf_path, vectorizer)


def generate_and_save_text_vectors(
    index_path: str,
    ids_path: str,
    papers_path: str,
    model_path: str,
) -> None:
    vectorizer: TfidfVectorizer = read_obj(model_path)
    papers = read_papers(papers_path)
    papers = preprocess_papers(papers)

    vectors, ids = generate_text_vectors(papers, vectorizer)
    print(f"Saving {len(vectors)} vectors of dim {vectors.shape[1]}")
    save_embeddings(index_path, vectors)
    save_obj(ids_path, ids)


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


def generate_text_vectors(
    papers: List[Paper],
    vectorizer: TfidfVectorizer
) -> Tuple[np.ndarray, List[str]]:
    corpus = [f"{paper.title} {paper.abstract}" for paper in papers]
    ids = [paper.id for paper in papers]
    vectors = vectorizer.transform(corpus).toarray()
    return vectors, ids
