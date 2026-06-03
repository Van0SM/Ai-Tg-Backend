from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, APIRouter, Depends

from app.schemas.user import UserCreateSchema, UserResponseSchema
from app.services.user import UserService
from app.core.database import get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponseSchema)
async def create_user(user: UserCreateSchema, session: AsyncSession = Depends(get_db)):
    user_service = UserService(session)

    return await user_service.create_user_if_not_exists(user.telegram_id, user.username)
