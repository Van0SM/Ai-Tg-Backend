from types import CoroutineType
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.conversation import ConversationRepository
from app.repositories.message import MessageRepository

from app.repositories.user import UserRepository

from app.integrations.fake_ai import FakeAI

FIELDS = ("role", "content")


class MessageService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.conversation_repository = ConversationRepository(self.session)
        self.message_repository = MessageRepository(self.session)
        self.user_repository = UserRepository(self.session)

    async def save_user_message(self, telegram_id: int, content: str):

        user = await self.user_repository.get_user_by_tg_id(telegram_id)

        if user is None:
            return

        last_conv = await self.conversation_repository.get_last_conversation(user.id)

        if last_conv is None:
            return

        await self.message_repository.create_message(
            conversation_id=last_conv.id,
            role="user",
            content=content,
            user_id=user.id,
        )

        await self.session.commit()

    async def build_conversation_context(
        self, conversation_id: int
    ) -> list[dict[str, str]]:
        messages = await self.message_repository.get_conversation_messages(
            conversation_id
        )

        context = []

        for message in messages:
            context.append({field: getattr(message, field) for field in FIELDS})

        return context

    async def generate_ai_response(self, conversation_id: int, user_id: int) -> str:
        conversation = await self.conversation_repository.get_conversation_by_id(
            conversation_id
        )

        if conversation is None:
            raise ValueError("Conversation not found")

        context = await self.build_conversation_context(conversation_id)

        fake_ai = FakeAI()

        response = await fake_ai.create_response(context)

        await self.message_repository.create_message(
            conversation_id=conversation_id,
            role="assistant",
            content=response,
            user_id=user_id,
        )

        await self.session.commit()

        return response

    async def process_user_message(
        self,
        telegram_id: int,
        content: str,
    ) -> str:
        user = await self.user_repository.get_user_by_tg_id(telegram_id)

        if user is None:
            raise ValueError("User Not found")

        user_id = user.id

        conversation = await self.conversation_repository.get_last_conversation(user_id)

        if conversation is None:
            raise ValueError("Conversations not found")

        await self.save_user_message(
            telegram_id=telegram_id,
            content=content,
        )

        return await self.generate_ai_response(
            conversation_id=conversation.id,
            user_id=user_id,
        )
