from dataclasses import dataclass, field
from typing import List


@dataclass
class Paper:
    id: str = ""
    title: str = ""
    authors: List[str] = field(default_factory=list)
    year: int = 0
    abstract: str = ""
    venue: str = ""
    references: List[str] = field(default_factory=list)
    citation_count: int = 0

    def is_populated(self) -> bool:
        return (
            bool(
                self.id and
                self.title and
                self.authors and
                self.year != 0 and
                self.abstract and
                self.venue and
                self.references
            )
        )
