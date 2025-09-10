from typing import Callable, Union, Dict, Any

from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import Message, CallbackQuery

from bot.db.queries import if_exists, create_user


class UserCheckMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable, event: Union[Message, CallbackQuery], data: Dict[str, Any]) -> Any:
        is_exist = await if_exists(tg_id := event.from_user.id)
        if not is_exist:
            await create_user(tg_id, event.from_user.username)

        return await handler(event, data)


def register_middlewares(dp: Dispatcher):
    dp.message.middleware(UserCheckMiddleware())
