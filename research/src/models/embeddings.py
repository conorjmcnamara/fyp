import torch
import faiss
import numpy as np
import os
import pickle
from torch.utils.data import DataLoader
from transformers import AutoTokenizer, AutoModel
from tqdm import tqdm
from typing import Tuple, List
from src.utils.file_utils import read_parsed_papers_from_json
from src.models.text_dataset import TextDataset
from src.config.settings import BATCH_SIZE, NUM_WORKERS


def generate_embeddings(
    model: torch.nn.Module,
    data_loader: DataLoader,
    device: torch.device
) -> Tuple[np.ndarray, List[str]]:
    embeddings = []
    ids = []
    model.eval()

    with torch.no_grad():
        for batch in tqdm(data_loader, desc="Generating embeddings"):
            # Move inputs to device
            input_ids = batch["input_ids"].squeeze(1).to(device)
            attention_mask = batch["attention_mask"].squeeze(1).to(device)

            # Forward pass through the model
            outputs = model(input_ids, attention_mask=attention_mask)

            # Average token embeddings to generate a single embedding per input
            last_hidden_state = outputs.last_hidden_state
            batch_embeddings = last_hidden_state.mean(dim=1)
            embeddings.append(batch_embeddings.cpu())

            paper_ids = batch["id"]
            ids.extend(paper_ids)

    return torch.cat(embeddings, dim=0).numpy(), ids


def save_embeddings(file_path: str, embeddings: np.ndarray, ids: List[str]):
    # Normalize embeddings for cosine similarity and store in a FAISS index with inner product
    faiss.normalize_L2(embeddings)
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)
    faiss.write_index(index, file_path)

    base_name = os.path.splitext(file_path)[0]
    ids_file_path = base_name + "_ids.pkl"
    with open(ids_file_path, "wb") as file:
        pickle.dump(ids, file)


def generate_and_save_embeddings(
    input_file_path: str,
    model_name: str,
    output_file_path: str
) -> None:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name).to(device)

    papers = read_parsed_papers_from_json(input_file_path)
    dataset = TextDataset(
        [paper.title for paper in papers],
        [paper.abstract for paper in papers],
        [paper.id for paper in papers],
        tokenizer
    )

    data_loader = DataLoader(
        dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=NUM_WORKERS,
        pin_memory=True
    )

    embeddings, ids = generate_embeddings(model, data_loader, device)
    print(f"Saving {len(embeddings)} embeddings")
    save_embeddings(output_file_path, embeddings, ids)
