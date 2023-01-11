from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


user_router = Router()


@user_router.message(Command(commands=["start"]))
async def cmd_start(message: Message):
    await message.answer('Привет!')
