import typing
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from src.core.database import Base

if typing.TYPE_CHECKING:  # pragma: no cover
    from src.models.paper import Paper


class Venue(Base):
    __tablename__ = "venues"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(nullable=False)

    papers: Mapped[List["Paper"]] = relationship("Paper", back_populates="venue")
