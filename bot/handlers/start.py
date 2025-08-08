from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command('start'))
async def start(msg: Message):
    await msg.answer(
        'Добро пожаловать в Spendly!\nЭтот бот поможет тебе в управлении с твоими расходами\n/help - для подробностей')
