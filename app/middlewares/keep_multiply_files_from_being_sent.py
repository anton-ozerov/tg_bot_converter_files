from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject
from typing import Callable, Awaitable, Dict, Any

class MediaGroupBlockerMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, Message) and event.media_group_id:
            print(event)
            await event.answer("❗ Отправляйте документы по одному за сообщение")
            return  # Прерываем дальнейшую обработку хэндлеров

        return await handler(event, data)
