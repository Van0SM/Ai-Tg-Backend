from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.conversation import ConversationRepository
from app.models.conversation import Conversation
from app.models.user import User
from app.repositories.user import UserRepository


class ConversationService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.conversation_repository = ConversationRepository(self.session)
        self.user_repository = UserRepository(self.session)

    async def create_new_conversation(
        self,
        title: str,
        user_id: int,
    ) -> Conversation:
        conversation = await self.conversation_repository.create_conversation(
            title=title,
            user_id=user_id,
        )

        user = await self.user_repository.get_user_by_id(user_id)

        if user is None:
            raise ValueError("User not found")

        await self.user_repository.set_active_conversation(conversation.id, user)

        await self.session.commit()

        return conversation

    async def start_new_dialog(
        self,
        telegram_id: int,
    ) -> Conversation | None:
        user = await self.user_repository.get_user_by_tg_id(telegram_id)

        if user is None:
            return None

        conversation = await self.create_new_conversation(
            title="Новый диалог",
            user_id=user.id,
        )

        return conversation

    async def get_user_conversations(self, telegram_id: int) -> list[Conversation]:
        user = await self.user_repository.get_user_by_tg_id(telegram_id)

        if user is None:
            raise ValueError("User not found")

        conversations = await self.conversation_repository.get_users_conversations(
            user.id
        )

        return list(conversations)

    async def build_conversations_list(self, telegram_id: int) -> str:
        conversations = await self.get_user_conversations(telegram_id)

        lines = []

        for index, conv in enumerate(conversations, start=1):
            lines.append(f"{index}. {conv.title}")

        return "\n".join(lines) if conversations else "У вас пока нет бесед."

    async def select_conversation(
        self, conversation_id: int, telegram_id: int
    ) -> Conversation:
        user = await self.user_repository.get_user_by_tg_id(telegram_id)

        if user is None:
            raise ValueError("User not found")

        conversation = await self.conversation_repository.get_conversation_by_id(
            conversation_id
        )

        if conversation is None:
            raise ValueError("Conversation not found")

        if conversation.user_id != user.id:
            raise ValueError(f"Conversation does not belong to user")

        await self.user_repository.set_active_conversation(conversation_id, user)

        await self.session.commit()

        return conversation
