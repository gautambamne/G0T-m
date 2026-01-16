from sqlalchemy import String, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.config.base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey, text
import uuid

class ChatSessionSource(Base):
    __tablename__ = "chat_session_sources"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("get_random_uuid()")
    )

    message_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("chat_session_messages.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    source_type: Mapper[str] = mapped_column(
        String(50),
        nullable=False,
    )

    source_name: Mapper[str] = mapped_column(
        String(255),
    )

    chunk_id: Mapper[str | None] = mapped_column(
        String(255),
    )

    source_metadata: Mapper[dict | None] = mapped_column(
        JSON,
    )

    message: Mapped["ChatSessionMessage"] = relationship(
        "ChatSessionMessage",
        back_populates="sources",
    )