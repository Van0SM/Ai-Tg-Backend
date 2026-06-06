from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="💬 Новый диалог"),
            KeyboardButton(text="📜 История"),
        ],
        [
            KeyboardButton(text="⚙️ Настройки"),
            KeyboardButton(text="ℹ️ Помощь"),
        ],
    ],
    resize_keyboard=True,
)
