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
