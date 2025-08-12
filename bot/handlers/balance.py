from aiogram import Router, types
from aiogram.filters import Command

from bot.db import queries as q

router = Router()


@router.message(Command('balance'))
async def cmd_balance(msg: types.Message):
    user = await q.get_user_by_tg(msg.from_user.id)
    if not user:
        await msg.answer('Сначала регистрация, команда /start')
        return
    initial = float(user.get('initial_balance') or 0.0)
    spent = await q.get_sum_expenses(msg.from_user.id)
    current = initial - spent
    await msg.answer(f'Ваш баланс: {current}')
