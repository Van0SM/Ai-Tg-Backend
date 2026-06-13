from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData

from app.models.conversation import Conversation


class ConversationCallback(CallbackData, prefix="conversation"):
    id: int


class DeleteCallback(CallbackData, prefix="del_conv"):
    id: int


class UpdTitleCallback(CallbackData, prefix="upd_conv_title"):
    id: int


def build_conversations_keyboard(
    conversations: list[Conversation],
) -> InlineKeyboardMarkup:
    buttons = []

    for conv in conversations:
        conv_button = InlineKeyboardButton(
            text=conv.title,
            callback_data=ConversationCallback(id=conv.id).pack(),
        )

        delete_button = InlineKeyboardButton(
            text="Удалить",
            callback_data=DeleteCallback(id=conv.id).pack(),
        )

        upd_title_btn = InlineKeyboardButton(
            text="Изменить название",
            callback_data=UpdTitleCallback(id=conv.id).pack(),
        )

        buttons.append([conv_button, delete_button, upd_title_btn])

    kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    return kb
