from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

router = Router()

@router.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer(text="Hello")
