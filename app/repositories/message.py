from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from typing import Sequence

from app.models.message import Message


class MessageRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_message(
        self,
        conversation_id: int,
        role: str,
        content: str,
        user_id: int,
    ) -> Message:

        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            user_id=user_id,
        )

        self.session.add(message)

        await self.session.flush()

        return message

    async def get_conversation_messages(
        self, conversation_id: int, limit: int = 50
    ) -> list[Message]:

        query = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
        )

        result = await self.session.execute(query)

        messages = list(result.scalars().all())
        messages.reverse()

        return messages
