import asyncio
import logging

from aiogram import Bot, Dispatcher
from app.data.config import BOT_TOKEN
from app.handlers import main_menu, get_files, set_name_to_file_handler
from app.middlewares.delete_old_reply_markup import RemoveReplyMarkupMiddleware
from app.middlewares.keep_multiply_files_from_being_sent import MediaGroupBlockerMiddleware
from app.middlewares.reset_states_to_commands import ResetStateMiddleware


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def main():
    logging.basicConfig(level=logging.INFO)

    dp.update.middleware(ResetStateMiddleware())  # удаление состояний при вводе команд
    dp.update.middleware(RemoveReplyMarkupMiddleware())  # удаление инлайн клавиатур у Message при новом Message
    # dp.message.middleware(MediaGroupBlockerMiddleware())  # блокировка отправки сгруппированных файлов

    dp.include_routers(main_menu.router, get_files.router, set_name_to_file_handler.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('EXIT')