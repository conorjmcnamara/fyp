import typing
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey
from src.core.database import Base

if typing.TYPE_CHECKING:  # pragma: no cover
    from src.models.paper import Paper


class Citation(Base):
    __tablename__ = "citations"

    citing_paper_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("papers.id"),
        primary_key=True
    )
    cited_paper_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("papers.id"),
        primary_key=True
    )

    citing_paper: Mapped["Paper"] = relationship(
        "Paper",
        foreign_keys=[citing_paper_id],
        back_populates="citing_papers"
    )
    cited_paper: Mapped["Paper"] = relationship(
        "Paper",
        foreign_keys=[cited_paper_id],
        back_populates="cited_papers"
    )
