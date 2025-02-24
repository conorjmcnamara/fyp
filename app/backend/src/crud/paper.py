from sqlalchemy.orm import Session, subqueryload
from uuid import UUID
from typing import List
from src.models.paper import Paper


def get_papers_by_ids(db: Session, ids: List[UUID]) -> List[Paper]:
    return db.query(Paper).filter(Paper.id.in_(ids))\
        .options(
            subqueryload(Paper.venue),
            subqueryload(Paper.authors)
        ).all()
