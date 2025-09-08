from typing import Literal

from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


class BalanceTypeFilter(BaseFilter):
    def __init__(self, type: Literal['depo', 'set']):
        self.type = type

    async def __call__(self, msg: Message, state: FSMContext):
        data = await state.get_data()
        return data.get('type') == self.type
