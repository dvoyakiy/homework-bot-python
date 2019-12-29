from aiogram.dispatcher.filters.state import StatesGroup, State


class BotState(StatesGroup):
    waiting = State()

