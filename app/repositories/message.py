from sqlalchemy.ext.asyncio import AsyncSession

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
