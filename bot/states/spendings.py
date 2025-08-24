from typing import Literal

from aiogram.fsm.state import State, StatesGroup


class Spending(StatesGroup):
    title: str = State()
    amount: float = State()
    comment: str = State()
    status: Literal['creating', 'updating'] = State()
