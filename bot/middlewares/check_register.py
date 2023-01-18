from typing import Callable, Dict, Any, Awaitable, Union

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from bot.database.user import create_user, check_user_exists


class CheckRegister(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: Dict[str, Any]
    ) -> Any:
        session_maker = data['session_maker']
        user = event.from_user

        # Check user in DB and add if user not in DB
        if await check_user_exists(user.id, session_maker) is False:
            result = await create_user(user.id, user.username, user.full_name, session_maker)
            await data['bot'].send_message(event.from_user.id, result)
        return await handler(event, data)
