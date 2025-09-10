from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton

main = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Создать расход', callback_data='spend'),
        InlineKeyboardButton(text='Запланировать расход', callback_data='plan'),
    ],
    [
        InlineKeyboardButton(text='Мои расходы', callback_data='my_spendings'),
        InlineKeyboardButton(text='Мои запланированные', callback_data='my_planned'),
    ],
    [InlineKeyboardButton(text='Мой баланс', callback_data='balance'),
     InlineKeyboardButton(text='Тест', switch_inline_query_current_chat='АХАХАХА НУ ТЫ И ЛОШАРА')]
])

balance = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text='Депозит', callback_data='deposit'),
    InlineKeyboardButton(text='Изменить', callback_data='set_balance'),
    InlineKeyboardButton(text='Домой', callback_data='home')
]])
