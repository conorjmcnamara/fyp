import typing
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base

if typing.TYPE_CHECKING:  # pragma: no cover
    from src.models.paper import Paper
    from src.models.author import Author


class PaperAuthor(Base):
    __tablename__ = "paper_authors"

    paper_id: Mapped[UUID] = mapped_column(ForeignKey("papers.id"), primary_key=True)
    author_id: Mapped[UUID] = mapped_column(ForeignKey("authors.id"), primary_key=True)

    paper: Mapped["Paper"] = relationship("Paper", overlaps="authors,papers")
    author: Mapped["Author"] = relationship("Author", overlaps="authors,papers")
