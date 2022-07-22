from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMUniversalizer(StatesGroup):
    video = State()
    photo = State()