from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exists, select


from app.models.user import User
from app.models.conversation import Conversation


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(
        self,
        telegram_id: int,
        username: str | None = None,
    ) -> User:

        user = User(
            telegram_id=telegram_id,
            username=username,
        )

        self.session.add(user)

        await self.session.flush()

        return user

    async def get_user_by_tg_id(self, telegram_id: int) -> User | None:
        query = select(User).where(User.telegram_id == telegram_id)

        result = await self.session.execute(query)

        return result.scalar_one_or_none()

    async def exists_by_tg_id(self, telegram_id: int) -> bool:
        query = select(exists().where(User.telegram_id == telegram_id))

        result = await self.session.execute(query)

        return bool(result.scalar())

    async def get_user_by_id(self, user_id: int) -> User | None:
        query = select(User).where(User.id == user_id)

        result = await self.session.execute(query)

        return result.scalar_one_or_none()

    async def set_active_conversation(self, conversation_id: int, user: User) -> None:
        user.active_conversation_id = conversation_id

        self.session.add(user)

        await self.session.flush()

    async def get_active_conversation_id(
        self,
        user_id: int,
    ) -> int | None:
        user = await self.get_user_by_id(user_id)

        if user is None:
            raise ValueError("User not found")

        conv_id = user.active_conversation_id

        return conv_id
