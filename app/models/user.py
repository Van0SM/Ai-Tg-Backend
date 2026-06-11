from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, String, func, ForeignKey
from datetime import datetime


from app.core.database import Base

from app.models.conversation import Conversation


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )
    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        nullable=False,
    )
    username: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=func.now(),
    )
    active_conversation_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("conversations.id"),
        nullable=True,
    )
