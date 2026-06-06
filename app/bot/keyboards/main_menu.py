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
            KeyboardButton(text="🤖 О боте"),
        ],
    ],
    resize_keyboard=True,
)
