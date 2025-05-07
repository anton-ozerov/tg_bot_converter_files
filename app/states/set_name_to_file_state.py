from aiogram.fsm.state import StatesGroup, State


class NewFileName(StatesGroup):
    name = State()
