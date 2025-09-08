from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.db import queries as q
from bot.filters.balance import BalanceTypeFilter
from bot.states.balance import Balance

router = Router()


@router.message(Command('balance'))
async def cmd_balance(msg: Message):
    balance = await q.get_balance(msg.from_user.id)
    if balance is None:
        await q.create_user(msg.from_user.id, msg.from_user.username)
        balance = 0.0
    await msg.answer(f'Ваш баланс: {balance}')


@router.message(Command('deposit'))
async def cmd_deposit(msg: Message, state: FSMContext):
    await msg.answer('Введите сумму депозита:')

    user_exists = await q.if_exists(msg.from_user.id)
    if not user_exists:
        await q.create_user(msg.from_user.id, msg.from_user.username)

    await state.update_data(type='depo')
    await state.set_state(Balance.amount)


@router.message(Balance.amount, BalanceTypeFilter('depo'))
async def balance_deposit_state(msg: Message, state: FSMContext):
    try:
        amount = float(msg.text.replace(' ', ''))
    except ValueError:
        await msg.answer('Введите корректную сумму:')
        return
    await msg.answer('Успешно добавлено!')
    await q.deposit(msg.from_user.id, amount)
    await state.clear()


@router.message(Command('set'))
async def cmd_set(msg: Message, state: FSMContext):
    await msg.answer('Введите новую сумму вашего баланса:')

    user_exists = await q.if_exists(msg.from_user.id)
    if not user_exists:
        await q.create_user(msg.from_user.id, msg.from_user.username)

    await state.update_data(type='set')
    await state.set_state(Balance.amount)


@router.message(Balance.amount, BalanceTypeFilter('set'))
async def balance_set_state(msg: Message, state: FSMContext):
    try:
        amount = float(msg.text.replace(' ', ''))
    except ValueError:
        await msg.answer('Введите корректную сумму:')
        return
    await msg.answer('Успешно изменено!')
    await q.set_balance(msg.from_user.id, amount)
    await state.clear()
