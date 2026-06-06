from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message


from app.services.user import UserService
from app.core.database import async_session_maker
from app.bot.keyboards.main_menu import main_menu
from app.bot.texts.welcome import get_welcome_text

start_router = Router()


@start_router.message(CommandStart())
async def bot_start(message: Message):
    tg_user = message.from_user

    if tg_user is None:
        return

    async with async_session_maker() as session:
        user_service = UserService(session)

        user, created = await user_service.get_or_create_user(
            tg_user.id, tg_user.username
        )

        if created:
            await message.answer(
                text=get_welcome_text(created),
                reply_markup=main_menu,
            )  # не придумал нормальные надписи
        else:
            await message.answer(
                text=get_welcome_text(created),
                reply_markup=main_menu,
            )
