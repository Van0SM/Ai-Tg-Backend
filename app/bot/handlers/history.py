from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from app.bot.keyboards.history import (
    build_conversations_keyboard,
    ConversationCallback,
    DeleteCallback,
    UpdTitleCallback,
)

from app.repositories.user import UserRepository
from app.services.conversation import ConversationService
from app.repositories.conversation import ConversationRepository

from app.core.database import async_session_maker

router = Router()


async def refresh_history_message(
    message: Message,
    conversation_service: ConversationService,
    telegram_id: int,
):
    conversations = await conversation_service.get_user_conversations(
        telegram_id=telegram_id,
    )

    if not conversations:
        await message.edit_text(text="У вас пока нет бесед")

        return

    await message.edit_text(
        text="Ваши беседы",
        reply_markup=build_conversations_keyboard(conversations),
    )


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


@router.callback_query(DeleteCallback.filter())
async def delete_conversation(
    callback: CallbackQuery,
    callback_data: DeleteCallback,
):
    if not isinstance(callback.message, Message):
        return

    async with async_session_maker() as session:
        conversation_service = ConversationService(session)

        await conversation_service.delete_conversation(
            callback_data.id,
            callback.from_user.id,
        )

        await session.commit()

        await refresh_history_message(
            message=callback.message,
            conversation_service=conversation_service,
            telegram_id=callback.from_user.id,
        )

        await callback.answer("Беседа удалена")
