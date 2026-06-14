from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.bot.keyboards.history import (
    build_conversations_keyboard,
    ConversationCallback,
    DeleteCallback,
    UpdTitleCallback,
)

from app.services.conversation import ConversationService

from app.core.database import async_session_maker

router = Router()


class UpdateTitleState(StatesGroup):
    waiting_for_title = State()


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


@router.callback_query(UpdTitleCallback.filter())
async def process_title(
    callback: CallbackQuery,
    callback_data: DeleteCallback,
    state: FSMContext,
) -> None:
    await state.update_data(conversation_id=callback_data.id)

    await state.set_state(UpdateTitleState.waiting_for_title)

    await callback.answer(text="Введите новое название")


@router.message(UpdateTitleState.waiting_for_title)
async def update_title(
    message: Message,
    state: FSMContext,
) -> None:
    tg_user = message.from_user

    if tg_user is None:
        return

    async with async_session_maker() as session:
        conversation_service = ConversationService(
            session=session,
        )

        data = await state.get_data()

        conversation_id = data.get("conversation_id")

        if conversation_id is None:
            return

        new_title = message.text

        if new_title is None:
            return

        _ = await conversation_service.update_title(
            conversation_id=conversation_id,
            telegram_id=tg_user.id,
            new_title=new_title,
        )

        await refresh_history_message(
            message=message,
            conversation_service=conversation_service,
            telegram_id=tg_user.id,
        )

        await state.clear()
