from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey
from app.core.database import Base
from typing import TYPE_CHECKING
from datetime import datetime, timezone
from sqlalchemy import DateTime

if TYPE_CHECKING:
    from app.models.workspaces import Workspace

class Document(Base):
    __tablename__ = 'documents'

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(Text, nullable=True)
    filename: Mapped[str] = mapped_column(String(100))
    file_path: Mapped[str] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    workspace_id: Mapped[int] = mapped_column(ForeignKey('workspaces.id'), index=True)
    workspace: Mapped["Workspace"] = relationship(back_populates="documents")



