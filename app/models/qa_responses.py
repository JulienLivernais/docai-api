from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, ForeignKey
from app.core.database import Base
from typing import TYPE_CHECKING
from datetime import datetime, timezone
from sqlalchemy import DateTime


if TYPE_CHECKING:
    from app.models.workspaces import Workspace


class QAResponse(Base):
    __tablename__ = 'qa_responses'

    id: Mapped[int] = mapped_column(primary_key=True)
    question: Mapped[str] = mapped_column(Text)
    answer: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    workspace_id: Mapped[int] = mapped_column(ForeignKey('workspaces.id'), index=True)
    workspace: Mapped["Workspace"] = relationship(back_populates="qa_responses")



