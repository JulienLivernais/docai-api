from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from app.core.database import Base
from typing import TYPE_CHECKING
from datetime import datetime, timezone
from sqlalchemy import DateTime


if TYPE_CHECKING:
    from app.models.users import User
    from app.models.documents import Document
    from app.models.qa_responses import QAResponse


class Workspace(Base):
    __tablename__ = 'workspaces'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    pinecone_namespace: Mapped[str] = mapped_column(String(255), unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    user: Mapped["User"] = relationship(back_populates="workspaces")

    documents: Mapped[list["Document"]] = relationship(
        back_populates="workspace",
        cascade="all, delete, delete-orphan",
    )
    qa_responses: Mapped[list["QAResponse"]] = relationship(
        back_populates="workspace",
        cascade="all, delete, delete-orphan",
    )

