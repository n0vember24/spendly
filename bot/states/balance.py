from aiogram.filters.state import State, StatesGroup


class Balance(StatesGroup):
    amount: float = State()
