from datetime import datetime
from typing import Literal

from aiogram.filters.state import State, StatesGroup


class Planned(StatesGroup):
    title: str = State()
    amount: float = State()
    comment: str = State()
    remind_at: datetime = State()
    status: Literal['creating', 'updating'] = State()
