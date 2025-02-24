import faiss
import pickle
from typing import Any


def read_embeddings(index_path: str) -> faiss.Index:
    return faiss.read_index(index_path)


def read_obj(path: str) -> Any:
    with open(path, "rb") as file:
        return pickle.load(file)
