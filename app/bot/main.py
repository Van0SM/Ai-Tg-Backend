import asyncio

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.core.config import settings
from app.bot.handlers.start import start_router
from app.bot.handlers.dialog import router as dialog_router
from app.bot.handlers.history import router as history_router

bot = Bot(
    token=settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


async def main():
    dp.include_router(start_router)
    dp.include_router(history_router)
    dp.include_router(dialog_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
