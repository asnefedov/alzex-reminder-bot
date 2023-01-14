from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.keyboards.reply import ReplyKB


user_router = Router()


@user_router.message(Command(commands=['start']))
async def cmd_start(message: Message):
    await message.answer('Привет!')


@user_router.message(Command(commands=['menu']))
async def show_user_menu(message: Message):
    await message.answer('Вы зашли в пользовательское меню', reply_markup=ReplyKB.userMenuMain)
