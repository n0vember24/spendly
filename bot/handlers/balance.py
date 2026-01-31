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
@router.callback_query(F.data=='deposit')
async def cmd_deposit(msg_or_cbq: Union[Message, CallbackQuery], state: FSMContext):
    deposit_text = 'Введите сумму депозита:'
    if isinstance(msg_or_cbq, Message):
        await msg_or_cbq.answer(deposit_text, reply_markup=kb.cancel)
    else:
        await msg_or_cbq.message.edit_text(deposit_text, reply_markup=kb.cancel)
    await state.update_data(type='depo')
    await state.set_state(Balance.amount)


@router.message(Command('cancel'))
@router.callback_query(F.data=='cancel')
async def state_cancel(msg_or_cbq:Union[Message, CallbackQuery], state: FSMContext):
    cancel_text = 'Операция была отменена.'
    if isinstance(msg_or_cbq, Message):
        await msg_or_cbq.answer(cancel_text, reply_markup=kb.balance_or_home)
    else:
        await msg_or_cbq.message.edit_text(cancel_text, reply_markup=kb.balance_or_home)
    await state.clear()

@router.message(Balance.amount, BalanceTypeFilter('depo'))
async def balance_deposit_state(msg: Message, state: FSMContext):
    try:
        amount = float(msg.text.replace(' ', ''))
    except ValueError:
        await msg.answer('Введите корректную сумму:')
        return
    await msg.answer('Успешно добавлено!', reply_markup=kb.balance_or_home)
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
    await msg.answer('Успешно изменено!', reply_markup=kb.balance_or_home)
    await q.set_balance(msg.from_user.id, amount)
    await state.clear()
