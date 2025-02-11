from dataclasses import dataclass
from typing import Tuple


@dataclass
class DatasetConfig:
    train_years: Tuple[int, int]
    test_years: Tuple[int, int]
    min_citations_filter: int
    min_references_filter: int
