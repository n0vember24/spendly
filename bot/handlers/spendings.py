from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.db import queries as q
from bot.states.spendings import Spending

router = Router()


@router.message(Command('spend'))
async def spending_create_state(msg: Message, state: FSMContext):
    await msg.answer('Процесс создания нового расхода.\n'
                     'Пожалуйста, введите заголовок для него:')
    user = await q.get_user(msg.from_user.id)
    if not user:
        await q.create_user(msg.from_user.id, msg.from_user.username)

    await state.update_data(status='creating')
    await state.set_state(Spending.title)


@router.message(Spending.title)
async def spending_title_create_state(msg: Message, state: FSMContext):
    if len(title := msg.text) <= 1:
        await msg.answer('Длина заголовка должна быть больше 1 символа:')
        return
    await msg.answer('Введите сумму денег которых хотите потратить:')
    await state.update_data(title=title)
    await state.set_state(Spending.amount)


@router.message(Spending.amount)
async def spending_amount_create_state(msg: Message, state: FSMContext):
    try:
        amount = float(msg.text.replace(' ', ''))
    except ValueError:
        await msg.answer('Пожалуйста, введите корректное значение числа.\n'
                         'Например: 10 000:')
        return
    await msg.answer('Введите краткое описание текущего расхода\n'
                     'Или введите "`Оставить пустым`" чтобы оставить пустым:')
    await state.update_data(amount=amount)
    await state.set_state(Spending.comment)


@router.message(Spending.comment)
async def spending_comment_create_state(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    title = await state.get_value('title')
    amount = float(await state.get_value('amount'))
    comment = msg.text
    if comment.lower() == 'оставить пустым':
        comment = ''
    await msg.answer('Отлично! Расходы добавлены:\n'
                     f'*Заголовок:* {title}\n*Общ. сумма расхода:* {amount}\n*Комментарий:* {comment}')
    await q.add_spending(user_id, title, amount, comment)
    await state.clear()


@router.message(Command('spendings_list'))
async def cmd_spendings_list(msg: Message):
    loading = await msg.answer('Загрузка...')
    total = ''
    lst = await q.get_spendings(msg.from_user.id)
    for i in lst:
        total += i.title + '\n'
    await loading.delete()
    await msg.answer(total)
