import asyncio
from loguru import logger
from aiogram import Bot, Dispatcher

from sqlalchemy.engine import URL

from bot.config import load_config
# from bot.models import BaseModel, create_async_engine, get_session_maker
from bot.handlers.user import user_router
# from bot.middlewares.checking_registrants import CheckingRegistrants


async def on_startup():
    pass


# def register_all_middlewares(dp: Dispatcher):
#     dp.message.outer_middleware(CheckingRegistrants())
#     dp.callback_query.outer_middleware(CheckingRegistrants())
#
#     dp.message.middleware(CheckingRegistrants())
#     dp.callback_query.middleware(CheckingRegistrants())


async def main() -> None:
    logger.info('Bot launched')
    config = load_config()
    bot = Bot(token=config.bot.token, parse_mode='HTML')
    dp = Dispatcher()

    # Register routers
    # for router in [
    #     start_router
    # ]:
    dp.include_router(user_router)

    # On startup
    # await on_startup()

    # Database
    # postgres_url = URL.create(
    #     'postgresql+asyncpg',
    #     username=config.db.user,
    #     password=config.db.password,
    #     host=config.db.host,
    #     database=config.db.database,
    #     port=config.db.port
    # )
    # async_engine = create_async_engine(postgres_url)
    # session_maker = get_session_maker(async_engine)
    # await proceed_schemas(async_engine, BaseModel.metadata)

    # Register Middlewares
    # register_all_middlewares(dp)
    # dp.message.middleware(CheckingRegistrants())
    # dp.callback_query.middleware(CheckingRegistrants())

    await dp.start_polling(bot)
    # await dp.start_polling(bot, session_maker=session_maker)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped')
