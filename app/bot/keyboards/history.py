from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData

from app.models.conversation import Conversation


class ConversationCallback(CallbackData, prefix="conversation"):
    id: int


def build_conversations_keyboard(
    conversations: list[Conversation],
) -> InlineKeyboardMarkup:
    buttons = []

    for conv in conversations:
        button = InlineKeyboardButton(
            text=conv.title,
            callback_data=ConversationCallback(id=conv.id).pack(),
        )

        buttons.append([button])

    kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    return kb
