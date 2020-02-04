from aiogram.dispatcher.filters.state import StatesGroup, State


class States(StatesGroup):
    subject_list = State()
    subject_task = State()
    waiting = State()

