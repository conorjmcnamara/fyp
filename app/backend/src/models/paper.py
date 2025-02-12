import typing
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from src.core.database import Base

if typing.TYPE_CHECKING:
    from src.models.venue import Venue
    from src.models.author import Author
    from src.models.citation import Citation


class Paper(Base):
    __tablename__ = "papers"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(nullable=False)
    year: Mapped[int] = mapped_column(nullable=False)
    abstract: Mapped[str] = mapped_column(nullable=False)
    venue_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("venues.id"),
        nullable=False
    )

    venue: Mapped["Venue"] = relationship("Venue", back_populates="papers")
    authors: Mapped[List["Author"]] = relationship(
        "Author",
        secondary="paper_authors",
        back_populates="papers"
    )
    citing_papers: Mapped[List["Citation"]] = relationship(
        "Citation",
        foreign_keys="[Citation.citing_paper_id]",
        back_populates="citing_paper"
    )
    cited_papers: Mapped[List["Citation"]] = relationship(
        "Citation",
        foreign_keys="[Citation.cited_paper_id]",
        back_populates="cited_paper"
    )
