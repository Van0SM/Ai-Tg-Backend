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

    async def create_new_conversation(self, title: str, user_id: int) -> Conversation:
        conversation = await self.conversation_repository.create_conversation(
            title=title,
            user_id=user_id,
        )

        user = await self.user_repository.get_user_by_id(user_id)

        if user is None:
            raise ValueError("user not found")

        await self.user_repository.set_active_conversation(user, conversation.id)

        await self.session.commit()

        return conversation
