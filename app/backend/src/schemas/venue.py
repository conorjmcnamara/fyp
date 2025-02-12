from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional
from src.models.paper import Paper


class VenueBase(BaseModel):
    name: str


class VenueCreate(VenueBase):
    pass


class VenueUpdate(VenueBase):
    name: Optional[str]


class Venue(VenueBase):
    id: UUID
    papers: List[Paper] = []

    class Config:
        orm_mode = True
