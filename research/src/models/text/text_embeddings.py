import torch
import numpy as np
from transformers import AutoTokenizer, AutoModel
from adapters import AutoAdapterModel
from torch.utils.data import DataLoader
from tqdm import tqdm
from typing import Union, Dict, Tuple, List
from src.models.text.text_dataset import TextDataset
from src.utils.file_utils import read_papers, save_embeddings, save_obj
from src.config.settings import TEXT_EMBEDDING_BATCH_SIZE, NUM_WORKERS


def generate_and_save_text_embeddings(
    index_path: str,
    ids_path: str,
    papers_path: str,
    model_name: str,
    adapter_config: Union[Dict[str, str], None] = None
) -> None:
    if adapter_config:
        model = AutoAdapterModel.from_pretrained(model_name)
        model.load_adapter(
            model_name.split('_')[0],
            source=adapter_config.get("source"),
            load_as=adapter_config.get("load_as"),
            set_active=True
        )
    else:
        model = AutoModel.from_pretrained(model_name)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    papers = read_papers(papers_path)
    dataset = TextDataset(
        [paper.title for paper in papers],
        [paper.abstract for paper in papers],
        [paper.id for paper in papers],
        tokenizer
    )

    data_loader = DataLoader(
        dataset,
        batch_size=TEXT_EMBEDDING_BATCH_SIZE,
        shuffle=False,
        num_workers=NUM_WORKERS,
        pin_memory=True
    )

    embeddings, ids = generate_text_embeddings(model, data_loader, device)
    print(f"Saving {len(embeddings)} embeddings of dim {embeddings.shape[1]}")
    save_embeddings(index_path, embeddings)
    save_obj(ids_path, ids)


def generate_text_embeddings(
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

            ids.extend(batch["id"])

    return torch.cat(embeddings, dim=0).numpy(), ids
