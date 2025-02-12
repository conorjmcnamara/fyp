from pydantic import BaseModel
from uuid import UUID
from src.models.paper import Paper
from src.models.author import Author


class PaperAuthorBase(BaseModel):
    paper_id: UUID
    author_id: UUID


class PaperAuthorCreate(PaperAuthorBase):
    pass


class PaperAuthor(PaperAuthorBase):
    paper: Paper
    author: Author

    class Config:
        orm_mode = True
