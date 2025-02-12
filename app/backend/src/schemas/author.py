from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional
from src.models.paper import Paper


class AuthorBase(BaseModel):
    first_name: str
    last_name: str


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(AuthorBase):
    first_name: Optional[str]
    last_name: Optional[str]


class Author(AuthorBase):
    id: UUID
    papers: List[Paper] = []

    class Config:
        orm_mode = True
