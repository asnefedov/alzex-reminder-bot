from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove


class ReplyKB:
    userMenuMain = ReplyKeyboardMarkup(
        keyboard=[
            [
              KeyboardButton(text='📥 Импортировать транзакции')
            ],
            [
                KeyboardButton(text='📊 Текущие транзакции')
            ],
            [
                KeyboardButton(text='⚙️ Настройки'),
                KeyboardButton(text='🇬🇧 Сменить язык')
            ],
            [
                KeyboardButton(text='📕 Справочная информация'),
                KeyboardButton(text='🦸🏻‍♂️ Поддержка')
            ],
            [
                KeyboardButton(text='⬇️ Убрать меню')
            ]
        ],
        resize_keyboard=True, one_time_keyboard=True
    )

    transactionsMenu = ReplyKeyboardMarkup(
        [
            [
                KeyboardButton(text='Удалить одну транзакцию')
            ],
            [
                KeyboardButton(text='Удалить список транзакций')
            ],
            [
                KeyboardButton(text='Удалить все транзакции')
            ],
            [
                KeyboardButton(text='⬅️ Вернуться')
            ]
        ],
        resize_keyboard=True, one_time_keyboard=True
    )

    settingsMenu = ReplyKeyboardMarkup(
        [
            [
                KeyboardButton(text='🔔 Настройка напоминаний')
            ],
            [
                KeyboardButton(text='🗑 Удалить аккаунт')
            ]
        ]
    )

    remove = ReplyKeyboardRemove()
