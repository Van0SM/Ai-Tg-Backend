from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.conversation import ConversationRepository
from app.repositories.message import MessageRepository

from app.repositories.user import UserRepository

FIELDS = ("role", "content")


class MessageService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_user_message(self, telegram_id: int, content: str):
        conversation_repository = ConversationRepository(self.session)
        message_repository = MessageRepository(self.session)
        user_repository = UserRepository(self.session)

        user = await user_repository.get_user_by_tg_id(telegram_id)

        if user is None:
            return

        last_conv = await conversation_repository.get_last_conversation(user.id)

        if last_conv is None:
            return

        new_message = await message_repository.create_message(
            conversation_id=last_conv.id,
            role="user",
            content=content,
            user_id=user.id,
        )

        await self.session.commit()

    async def build_conversation_context(
        self, conversation_id: int
    ) -> list[dict[str, str]]:
        message_repository = MessageRepository(self.session)

        messages = await message_repository.get_conversation_messages(conversation_id)

        context = []

        for message in messages:
            context.append({field: getattr(message, field) for field in FIELDS})

        return context
