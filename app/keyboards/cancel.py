from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

cancel_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Сброс', callback_data="cancel"),
    ]
])
