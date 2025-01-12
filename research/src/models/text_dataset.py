from torch.utils.data import Dataset
from transformers import PreTrainedTokenizer
from typing import List
from src.config.settings import MAX_TOKENS


class TextDataset(Dataset):
    def __init__(
        self,
        titles: List[str],
        abstracts: List[str],
        ids: List[str],
        tokenizer: PreTrainedTokenizer,
        max_len: int = MAX_TOKENS
    ):
        self.titles = titles
        self.abstracts = abstracts
        self.ids = ids
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self) -> int:
        return len(self.titles)

    def __getitem__(self, idx: int) -> dict:
        title = self.titles[idx]
        abstract = self.abstracts[idx]
        text = f"{title} {abstract}"
        id = self.ids[idx]

        encoding = self.tokenizer(
            text,
            add_special_tokens=True,
            max_length=self.max_len,
            truncation=True,
            padding="max_length",
            return_attention_mask=True,
            return_tensors="pt"
        )

        encoding["id"] = id
        return encoding
