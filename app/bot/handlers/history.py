from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from app.bot.keyboards.history import build_conversations_keyboard, ConversationCallback

from app.services.conversation import ConversationService
from app.repositories.conversation import ConversationRepository

from app.core.database import async_session_maker

router = Router()


@router.message(F.text == "📜 История")
async def get_history(message: Message):
    tg_user = message.from_user

    if tg_user is None:
        return

    async with async_session_maker() as session:
        conversation_service = ConversationService(session)

        conversations = await conversation_service.get_user_conversations(tg_user.id)

        if not conversations:
            await message.answer(
                text="У вас пока нет бесед",
            )
            return

        kb = build_conversations_keyboard(conversations)

        await message.answer(text="Ваши беседы: ", reply_markup=kb)


@router.callback_query(ConversationCallback.filter())
async def select_conversation(
    callback: CallbackQuery,
    callback_data: ConversationCallback,
):
    async with async_session_maker() as session:
        conversation_service = ConversationService(session)

        conversation = await conversation_service.select_conversation(
            conversation_id=callback_data.id,
            telegram_id=callback.from_user.id,
        )

        if conversation is None:
            await callback.answer("Беседа не найдена")
            return

        await callback.answer(
            text=f"Вы выбрали беседу: {callback_data.id}. {conversation.title}"
        )
