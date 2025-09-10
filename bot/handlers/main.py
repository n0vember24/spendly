from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from bot import keyboards as kb

router = Router()


@router.message(Command('start'))
async def cmd_start(msg: Message):
    await msg.answer('Добро пожаловать в Spendly!\n'
                     'Этот бот поможет тебе в управлении с твоими расходами\n'
                     '/help - для подробностей', reply_markup=kb.main)


@router.callback_query(F.data == 'home')
async def cbq_main(cbq: CallbackQuery):
    await cbq.message.edit_text('Выберите опции ниже:', reply_markup=kb.main)


@router.message(Command('help'))
async def cmd_help(msg: Message):
    await msg.answer(
        '/balance - Для просмотра баланса\n'
        '/deposit - Добавить баланс\n'
        '/set - Изменить баланс\n'
        '/spend - сохранить расход\n'
        '/spendings\\_list - список расходов\n'
        '/plan - Запланировать расход\n'
        '/planned\\_list - список расходов\n')
