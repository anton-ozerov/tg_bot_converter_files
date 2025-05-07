from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

use_as_filename_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Да", callback_data="use_text_as_filename"),
            InlineKeyboardButton(text="❌ Нет", callback_data="cancel_filename_prompt")
        ]
    ]
)
