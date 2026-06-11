from types import CoroutineType
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
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

    async def save_user_message(self, user: User, content: str):
        active_conv_id = await self.user_repository.get_active_conversation_id(user.id)

        if active_conv_id is None:
            raise ValueError("User have not active conversation")

        await self.message_repository.create_message(
            conversation_id=active_conv_id,
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

        conversation_id = await self.user_repository.get_active_conversation_id(user.id)

        if conversation_id is None:
            raise ValueError("Conversation not found")

        await self.save_user_message(
            user=user,
            content=content,
        )

        return await self.generate_ai_response(
            conversation_id=conversation_id,
            user_id=user.id,
        )
