import re
from datetime import datetime

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.db import queries as q
from bot.states.planned import Planned

router = Router()


@router.message(Command('plan'))
async def planned_create_state(msg: Message, state: FSMContext):
    await msg.answer('Процесс создания нового расхода с напоминанием.\n'
                     'Пожалуйста, введите заголовок для него:')

    user = await q.get_user(msg.from_user.id)
    if not user:
        await q.create_user(msg.from_user.id, msg.from_user.username)

    await state.update_data(status='creating')
    await state.set_state(Planned.title)


@router.message(Planned.title)
async def planned_title_create_state(msg: Message, state: FSMContext):
    if len(title := msg.text) <= 1:
        await msg.answer('Длина заголовка должна быть больше 1 символа:')
        return
    await msg.answer('Введите сумму денег которых хотите потратить:')
    await state.update_data(title=title)
    await state.set_state(Planned.amount)


@router.message(Planned.amount)
async def planned_amount_create_state(msg: Message, state: FSMContext):
    try:
        amount = float(msg.text.replace(' ', ''))
    except ValueError:
        await msg.answer('Пожалуйста, введите корректное значение числа.\n'
                         'Например: 10 000:')
        return
    await msg.answer('Введите краткое описание текущего расхода\n'
                     'Или введите "`Оставить пустым`" чтобы оставить пустым:')
    await state.update_data(amount=amount)
    await state.set_state(Planned.comment)


@router.message(Planned.comment)
async def planned_comment_create_state(msg: Message, state: FSMContext):
    await msg.answer('Введите дату и время когда вы хотите чтобы я вам напомнил о расходе.\n'
                     'Пример: 2025-01-01 12:00:00:')
    comment = msg.text
    if comment.lower() == 'оставить пустым':
        comment = ''
    await state.update_data(comment=comment)
    await state.set_state(Planned.remind_at)


@router.message(Planned.remind_at)
async def planned_remind_at_create_state(msg: Message, state: FSMContext):
    try:
        reg = re.compile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$')
        if not reg.match(inp := msg.text.strip()):
            await msg.answer('Неверный формат введённых данных!\n'
                             'Пример: 2025-01-01 12:00:00:')
            return
        remint_at = datetime.strptime(inp, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        await msg.answer('Неверная дата!\nПерепроверьте данные и попробуйте ещё раз:')
        return

    user_id = msg.from_user.id
    title = await state.get_value('title')
    amount = float(await state.get_value('amount'))
    comment = await state.get_value('comment')
    await msg.answer('Отлично! Запланированный расход добавлен:\n'
                     f'*Заголовок:* {title}\n*Общ. сумма расхода:* {amount}\n'
                     f'*Комментарий:* {comment}\n*Дата и время напоминания:* {remint_at}')
    await q.add_planned(user_id, title, amount, comment, remint_at)
    await state.clear()


@router.message(Command('planned_list'))
async def cmd_planned_list(msg: Message):
    loading = await msg.answer('Загрузка...')
    lst = await q.get_planned(msg.from_user.id)
    total = ''
    for i in lst:
        total += i.title + '\n'
    await loading.delete()
    await msg.answer(total)
