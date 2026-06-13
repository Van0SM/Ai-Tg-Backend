from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from collections.abc import Sequence

from app.models.conversation import Conversation


class ConversationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_conversation(self, title: str, user_id: int) -> Conversation:
        conversation = Conversation(title=title, user_id=user_id)

        self.session.add(conversation)

        await self.session.flush()

        return conversation

    async def delete_conversation(self, conversation: Conversation) -> None:
        await self.session.delete(conversation)

        await self.session.flush()

    async def get_conversation_by_id(self, conversation_id: int) -> Conversation | None:
        query = select(Conversation).where(Conversation.id == conversation_id)

        result = await self.session.execute(query)

        return result.scalar_one_or_none()

    async def get_users_conversations(self, user_id: int) -> Sequence[Conversation]:
        query = select(Conversation).where(Conversation.user_id == user_id)

        result = await self.session.execute(query)

        return result.scalars().all()
