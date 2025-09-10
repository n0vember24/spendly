from typing import Union

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot import keyboards as kb
from bot.db import queries as q
from bot.filters.balance import BalanceTypeFilter
from bot.states.balance import Balance

router = Router()


@router.message(Command('balance'))
@router.callback_query(F.data == 'balance')
async def cmd_balance(msg_or_cbq: Union[Message, CallbackQuery]):
    balance = await q.get_balance(msg_or_cbq.from_user.id)
    text = f'Ваш баланс: {balance}'
    if isinstance(msg_or_cbq, Message):
        await msg_or_cbq.answer(text, reply_markup=kb.balance)
    else:
        await msg_or_cbq.message.edit_text(text, reply_markup=kb.balance)


@router.message(Command('deposit'))
async def cmd_deposit(msg: Message, state: FSMContext):
    await msg.answer('Введите сумму депозита:')
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
