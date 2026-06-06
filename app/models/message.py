from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, String, func, ForeignKey, Text
from datetime import datetime

from app.core.database import Base


class Message(Base):
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )
    conversation_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
    )
    role: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
    )
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )  # не знаю, сколько символов сделать допустимым
    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=func.now(),
    )
