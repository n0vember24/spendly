from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.db import queries as q

router = Router()


@router.message(Command('start'))
async def cmd_start(msg: Message):
    user = await q.get_user_by_tg(msg.from_user.id)
    if not user:
        await q.create_user(msg.from_user.id, msg.from_user.username)
    await msg.answer(
        'Добро пожаловать в Spendly!\n'
        'Этот бот поможет тебе в управлении с твоими расходами\n'
        '/help - для подробностей')


@router.message(Command('help'))
async def cmd_help(msg: Message):
    await msg.answer(
        '/balance - Для просмотра баланса\n'
        '/deposit - Добавить баланс\n'
        '/spend - сохранить расход\n'
        '/plan - Запланировать расход')
