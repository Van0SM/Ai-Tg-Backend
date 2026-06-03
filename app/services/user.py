from sqlalchemy.ext.asyncio import AsyncSession


from app.repositories.user import UserRepository
from app.models.user import User


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

        self.user_repository = UserRepository(session)

    async def create_user_if_not_exists(
        self,
        telegram_id: int,
        username: str | None = None,
    ) -> User:
        user = await self.user_repository.get_user_by_tg_id(telegram_id)
        if user is not None:
            return user

        user = await self.user_repository.create_user(telegram_id, username)
        return user
