from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.db import queries as q
from bot.states.balance import Balance

router = Router()


@router.message(Command('balance'))
async def cmd_balance(msg: Message):
    user = await q.get_user(msg.from_user.id)
    if not user:
        await q.create_user(msg.from_user.id, msg.from_user.username)
        current = 0.0
    else:
        current = user.balance
    await msg.answer(f'Ваш баланс: {current}')


@router.message(Command('deposit'))
async def cmd_deposit(msg: Message, state: FSMContext):
    await msg.answer('Введите сумму депозита:')

    user = await q.get_user(msg.from_user.id)
    if not user:
        await q.create_user(msg.from_user.id, msg.from_user.username)

    await state.set_state(Balance.amount)


@router.message(Balance.amount)
async def balance_deposit_state(msg: Message, state: FSMContext):
    try:
        amount = float(msg.text.replace(' ', ''))
    except ValueError:
        await msg.answer('Введите корректную сумму:')
        return
    await msg.answer('Успешно добавлено!')
    await q.add_balance(msg.from_user.id, amount)
    await state.clear()


@router.message(Command('set'))
async def cmd_set(msg: Message, state: FSMContext):
    await msg.answer('Введите новую сумму вашего баланса:')

    user = await q.get_user(msg.from_user.id)
    if not user:
        await q.create_user(msg.from_user.id, msg.from_user.username)

    await state.set_state(Balance.amount)


@router.message(Balance.amount)
async def balance_set_state(msg: Message, state: FSMContext):
    try:
        amount = float(msg.text.replace(' ', ''))
    except ValueError:
        await msg.answer('Введите корректную сумму:')
        return
    await msg.answer('Успешно изменено!')
    await q.set_balance(msg.from_user.id, amount)
    await state.clear()
