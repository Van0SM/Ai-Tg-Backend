from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, String, func, ForeignKey
from datetime import datetime

from app.core.database import Base


class Conversation(Base):
    __tablename__ = "conversations"
    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id"),
        ondelete="CASCADE",
        nullable=False,
    )
    title: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=func.now(),
    )
