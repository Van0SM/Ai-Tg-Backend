from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.core.database import get_db
from app.services.user import UserService


async def get_user_service(session: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(session)
