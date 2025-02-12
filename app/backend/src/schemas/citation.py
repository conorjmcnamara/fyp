from pydantic import BaseModel
from uuid import UUID
from src.models.paper import Paper


class CitationBase(BaseModel):
    citing_paper_id: UUID
    cited_paper_id: UUID


class CitationCreate(CitationBase):
    pass


class Citation(CitationBase):
    citing_paper: Paper
    cited_paper: Paper

    class Config:
        orm_mode = True
