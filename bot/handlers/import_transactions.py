import os

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.orm import sessionmaker

from bot.database.transactions import import_transactions
from bot.misc.states import GetCSV
from bot.utils.csv_reader import CsvReader

import_router = Router()


@import_router.message(F.text == '📥 Импортировать транзакции')
async def request_csv_file(message: Message, state: FSMContext):
    await message.answer('Загрузите файл')
    await state.set_state(GetCSV.waiting_file)


@import_router.message(GetCSV.waiting_file)
async def get_file(message: Message, bot: Bot, state: FSMContext, session_maker: sessionmaker):
    # Download file
    file = await bot.get_file(message.document.file_id)
    await bot.download_file(file.file_path, f'bot/utils/temp_{message.from_user.id}.csv')
    await message.answer('Файл успешно получен')

    try:
        # Read file
        reader = CsvReader(f'bot/utils/temp_{message.from_user.id}.csv')
        df = reader.read_csv_file()
        await message.answer('Файл успешно прочитан')

        headers = reader.get_headers(df)
        await message.answer('Заголовки получены')

        check = reader.check_keys(headers)
        if check is not None:
            return await message.answer(f'Произошла ошибка при проверке файла. Колонка {check} не найдена.')
        await message.answer('Все колонки проверены.')

        filtered = reader.filtered_df_by_datetime(df)
        data = reader.df_to_dict(filtered)
        await message.answer('Транзакции отфильтрованы и успешно извлечены.')

        # Import data in database
        await import_transactions(message.from_user.id, data, session_maker)
        await message.answer('Транзакции успешно загружены в базу данных.')

    except Exception as error:
        await message.answer(f'Произошла ошибка при чтении файла: {error}\n Обратитесь в поддержку.')
    finally:
        # Clear state and delete temp file
        await state.clear()
        os.remove(f'bot/utils/temp_{message.from_user.id}.csv')
