from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.db import queries as q

router = Router()


@router.message(Command('balance'))
async def cmd_balance(msg: Message):
    user = await q.get_user_by_tg(msg.from_user.id)
    if not user:
        await msg.answer('Сначала регистрация, команда /start')
        return
    initial = float(user.balance or 0.0)
    spent = await q.get_sum_expenses(msg.from_user.id)
    current = initial - spent
    await msg.answer(f'Ваш баланс: {current}')


@router.message(Command('deposit'))
async def deposit(msg: Message):
    amount = msg.text.split(maxsplit=1)
    if len(amount) < 2:
        await msg.answer('Укажите корректную сумму для депозита, пример: /deposit 25000')
        return
    try:
        amount = float(amount[1])
    except ValueError:
        await msg.answer('Сумма должна быть числом')
        return
    await q.add_balance(msg.from_user.id, amount)
    await msg.answer(f'Успешно добавлено в баланс {amount}')
