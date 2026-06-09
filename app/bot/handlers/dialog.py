from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message


from app.services.conversation import ConversationService
from app.services.message import MessageService

from app.repositories.conversation import ConversationRepository
from app.repositories.user import UserRepository

from app.core.database import async_session_maker
from app.bot.keyboards.main_menu import main_menu

router = Router()


@router.message(F.text == "💬 Новый диалог")
async def new_dialog(message: Message):
    tg_user = message.from_user

    if tg_user is None:
        return

    async with async_session_maker() as session:
        conversation_service = ConversationService(session)

        conversation = await conversation_service.start_new_dialog(tg_user.id)

        if conversation is None:
            await message.answer(text="Произошла ошибка. Попробуйте /start")

            return

        await message.answer(text="Новый диалог создан", reply_markup=main_menu)


@router.message(F.text)
async def save_message(message: Message):
    tg_user = message.from_user

    if tg_user is None:
        return

    content = message.text

    if content is None:
        return

    async with async_session_maker() as session:
        message_service = MessageService(session)

        response = await message_service.process_user_message(
            telegram_id=tg_user.id,
            content=content,
        )

        await message.answer(response)
