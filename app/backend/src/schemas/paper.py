from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional
from src.models.author import Author
from src.models.venue import Venue
from src.models.citation import Citation


class PaperBase(BaseModel):
    title: str
    year: int
    abstract: str
    venue_id: UUID


class PaperCreate(PaperBase):
    pass


class PaperUpdate(PaperBase):
    title: Optional[str]
    year: Optional[int]
    abstract: Optional[str]
    venue_id: Optional[UUID]


class Paper(PaperBase):
    id: UUID
    venue: Venue
    authors: List[Author] = []
    citing_papers: List[Citation] = []
    cited_papers: List[Citation] = []

    class Config:
        orm_mode = True
