from sqlalchemy.ext.asyncio import AsyncSession


from app.repositories.user import UserRepository
from app.models.user import User


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

        self.user_repository = UserRepository(session)

    async def get_or_create_user(self, telegram_id: int, username: str | None = None) -> tuple[User, bool]:
        user = await self.user_repository.get_user_by_tg_id(telegram_id)

        if user is not None:
            return (user, False)

        user = await self.user_repository.create_user(telegram_id, username)

        await self.session.commit()

        return (user, True)