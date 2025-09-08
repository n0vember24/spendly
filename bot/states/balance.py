from typing import Literal

from aiogram.filters.state import State, StatesGroup


class Balance(StatesGroup):
    amount: float = State()
    type:Literal['depo', 'set'] = State()
