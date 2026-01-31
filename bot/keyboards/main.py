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
    [InlineKeyboardButton(text='Мой баланс', callback_data='balance')]
])

balance = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text='Депозит', callback_data='deposit'),
    InlineKeyboardButton(text='Изменить', callback_data='set_balance'),
    InlineKeyboardButton(text='Домой', callback_data='home')
]])

balance_or_home = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text='Баланс', callback_data='balance'),
    InlineKeyboardButton(text='Домой', callback_data='home')
]])

cancel = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Отмена', callback_data='cancel')]])
