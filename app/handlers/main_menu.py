from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F

router = Router()


@router.message(CommandStart())
@router.callback_query(F.data == 'cancel')
async def show_main_menu(msg_cbq: Message | CallbackQuery, state: FSMContext = None):
    if state:
        await state.clear()

    if isinstance(msg_cbq, Message):
        start_text = ("Здравствуйте\!\nЭтот бот для объединяет загруженные пользователем файлы в единый PDF, "
                "сжимает его, разделяет на части при превышении размера и формирует сопроводительный документ\.\n\n"
                "Для того, чтобы воспользоваться функционалом:\n1\) Отправьте файлы по порядку, отдельными сообщениями"
                      "\n2\) Нажмите на кнопку "
                "*Указать имя*\n3\) Введите имя нового файла\n\nКоманда /start "
                "всё сбрасывает\n\nДопустимые форматы: `PDF`, `XLS`/`XLSX` \(Excel\), `DOC`/`DOCX`/`RTF` \(Word\), `TXT`, "
                "`PPT`/`PPTX`, `JPG`/`JPEG`/`PNG` \(изображения\)")
        msg = await msg_cbq.answer(start_text, parse_mode="MarkdownV2")
    else:
        cancel_text = ('Данные сброшены\n\nДля того, чтобы воспользоваться функционалом:\n1\) Отправьте файлы по порядку\n2\) Нажмите на кнопку '
                       '*Указать имя*\n3\) Введите имя нового файла')
        msg = await msg_cbq.message.edit_text(cancel_text, parse_mode="MarkdownV2")
    return msg
