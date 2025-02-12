import typing
import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from typing import List
from src.core.database import Base

if typing.TYPE_CHECKING:
    from src.models.paper import Paper


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=True)

    papers: Mapped[List["Paper"]] = relationship(
        "Paper",
        secondary="paper_authors",
        back_populates="authors"
    )
