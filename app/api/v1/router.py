from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status, HTTPException

from app.schemas.user import UserCreateSchema, UserResponseSchema
from app.api.dependencies.user import get_user_service
from app.core.database import get_db
from app.exceptions.user import UserAlreadyExistsError
from app.services.user import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED
)
async def create_user(
    user: UserCreateSchema, user_service: UserService = Depends(get_user_service)
):

    try:
        return await user_service.create_user_if_not_exists(
            user.telegram_id, user.username
        )
    except UserAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )
