from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from bot.db.queries import get_spendings

async def spending_create(user_id:int):
    spendings_list = await get_spendings(user_id)
        