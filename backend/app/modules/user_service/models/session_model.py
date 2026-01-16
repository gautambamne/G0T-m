from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, DateTime, ForeignKey, func
from datetime import datetime
from app.config.base import Base
import uuid
from app.modules.user_service.models.user_model import User

class Session(Base):
    __tablename__="sessions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )

    refresh_token: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),  # CASCADE : If the parent deleted then delete all the children
        nullable=False,
        index=True,
    )

    user_agent: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
    )

    ip_address: Mapped[str] = mapped_column(
        String(45),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        back_populates="sessions",
    )