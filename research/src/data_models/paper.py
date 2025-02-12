from dataclasses import dataclass, field
from typing import List


@dataclass
class Paper:
    id: str = ""
    title: str = ""
    year: int = 0
    authors: List[str] = field(default_factory=list)
    abstract: str = ""
    venue: str = ""
    references: List[str] = field(default_factory=list)
    citation_count: int = 0
