from app.core.database import async_session_maker
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from app.services.user import UserService
from app.exceptions.user import UserAlreadyExistsError

router = Router()



@router.message(CommandStart())
async def command_start_handler(message: Message):
    user = message.from_user

    if user is None:
        return 

    async with async_session_maker() as session:
        user_service = UserService(session)
        try:
            await user_service.create_user_if_not_exists(
                telegram_id=user.id,
                username=user.username,
                )
        except UserAlreadyExistsError:
            await message.answer(text="Такой пользователь уже существует")
            return

        await session.commit()

        await message.answer(text="Регистрация успешна")