from aiogram import F
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.keyboards.cancel import cancel_kb
from app.keyboards.set_name_to_file_inline_kb import set_name_kb

router = Router()


@router.message(F.photo)
async def photo_msg(message: Message):
    res = await message.answer("Пожалуйста, отправьте фотографию документом (без сжатия)")
    return res


@router.message(F.document)
async def document_msg(message: Message, state: FSMContext):
    try:
        file_format = message.document.file_name.split('.')[-1].lower()
        if file_format in ('pdf', 'xls', 'xlsx', 'doc', 'docx', 'rtf', 'txt', 'ppt', 'pptx', 'jpg', 'jpeg', 'png'):
            data = await state.get_data()
            if 'files_ids_and_types' in data:
                files_ids_and_types: list = (await state.get_data())['files_ids_and_types']
            else:
                files_ids_and_types = []
            files_ids_and_types.append((message.document.file_id, file_format, message.document.file_name))
            res = await message.answer(f'Принят {len(files_ids_and_types)} документ', reply_markup=set_name_kb)
            await state.update_data(files_ids_and_types=files_ids_and_types)
        else:
            res = await message.answer("❕Извините, но такой формат не поддерживается\n\nДопустимые форматы: `PDF`, "
                                       "`XLS`/`XLSX` (Excel), `DOC`/`DOCX`/`RTF` (Word), `TXT`, `PPT`/`PPTX`, `JPG`/`JPEG`/`PNG` "
                                       "(изображения)", parse_mode='MARKDOWN', reply_markup=cancel_kb)
        return res
    except Exception as e:
        res = await message.answer('❗ Файл поврежден')
        return res
