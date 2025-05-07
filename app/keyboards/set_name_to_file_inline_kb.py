from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

set_name_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Указать имя', callback_data="set_name")
    ],
    [
        InlineKeyboardButton(text='Сброс', callback_data="cancel"),
    ]
])
