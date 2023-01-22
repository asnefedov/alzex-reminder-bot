from aiogram.fsm.state import StatesGroup, State


class GetCSV(StatesGroup):
    waiting_file = State()
