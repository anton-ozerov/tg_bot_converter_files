from pathlib import Path

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.keyboards.use_as_filename_kb import use_as_filename_kb
from app.states.set_name_to_file_state import NewFileName
from app.utils.clear_folder import async_clear_folder
from app.utils.validate_file_name import is_valid_filename
from app.utils.work_with_pdf import get_convert

router = Router()


# Срабатывает хэндлер на нажатие инлайн-кнопки "Указать имя"
@router.callback_query(F.data == 'set_name')
async def set_name_to_file(callback: CallbackQuery, state: FSMContext):
    res = await callback.message.edit_text('Введите название нового файла')
    await state.set_state(NewFileName.name)
    return res


@router.message(NewFileName.name)  # для состояния ввода имени
async def get_new_file_name_and_send_result(message: Message, state: FSMContext, bot: Bot):
    # Сохраняем имя и вызываем обработчик
    await state.update_data(final_file_name=message.text)
    res = await process_file_with_name(message, state, bot)
    return res


@router.message(F.text)
async def handle_text_name_suggestion(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        return  # Игнорируем, если пользователь уже в каком-то состоянии

    data = await state.get_data()
    if 'files_ids_and_types' not in data or not data['files_ids_and_types']:
        return  # Нет файлов — игнорируем

    await state.update_data(pending_text_as_name=message.text)
    return await message.answer(
        f"Использовать \"{message.text}\" как имя итогового файла?",
        reply_markup=use_as_filename_kb
    )


@router.callback_query(F.data == "use_text_as_filename")
async def confirm_text_as_filename(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    new_name = data.get("pending_text_as_name")

    if not new_name:
        await callback.answer("Нет имени для использования", show_alert=True)
        return

    await callback.message.edit_reply_markup(reply_markup=None)  # убираем клавиатуру

    # Сохраняем имя и переходим в состояние
    await state.update_data(final_file_name=new_name)
    await state.set_state(NewFileName.name)

    # Симулируем обработку имени без отправки нового сообщения
    return await process_file_with_name(callback.message, state, bot)


@router.callback_query(F.data == "cancel_filename_prompt")
async def cancel_text_as_filename(callback: CallbackQuery, state: FSMContext):
    await state.update_data(pending_text_as_name=None)
    return await callback.message.edit_text("Ок, введите другое имя или отправьте ещё файл", reply_markup=None)


async def process_file_with_name(message: Message, state: FSMContext, bot: Bot):
    msg = await message.answer('Ждите ⌛️')
    try:
        data = await state.get_data()
        # Получаем имя из состояния или из текста сообщения
        # из машины состояния - после ввода имени файла БЕЗ нажатия на "Указать имя"
        new_file_name = data["final_file_name"]

        if not is_valid_filename(new_file_name):  # проверка на допустимые файлы и длину
            await msg.delete()
            return await message.answer(
                "❌ Недопустимое имя файла. Убедитесь, что оно не содержит символов:\n"
                r"`\ / : * ? \" < > |` и не слишком длинное.",
                parse_mode='Markdown'
            )

        files_ids_and_types = data['files_ids_and_types']

        files = await get_convert(bot=bot, files_ids_and_types=files_ids_and_types, new_file_name=new_file_name)
        await msg.delete()

        if files[0] == 'Ошибка':
            res = await message.answer(f'❗ Файл {files[1]} поврежден. Замените его и попробуйте еще раз')
            await state.clear()
            return res

        for file in files:
            await message.answer_document(file)
        await state.clear()
        text = ('Для того, чтобы ещё раз воспользоваться функционалом:\n1\) Отправьте файлы по порядку\n2\) '
                'Нажмите на кнопку *Указать имя*\n3\) Введите имя нового файла')
        res = await message.answer(text, parse_mode="MarkdownV2")
        await async_clear_folder("", [file.path for file in files])  # удаление всех временных файлов
        return res
    except Exception as e:
        # Удаляем временные файлы
        await async_clear_folder("",
                                 [str(Path("temp_files") / f"{file[0]}.{file[1]}") for file in files_ids_and_types])
        await async_clear_folder("",
                                 [str(Path("temp_files") / f"{file[0]}.pdf") for file in files_ids_and_types])
        await state.clear()
        await msg.delete()
        res = await message.answer("❗ Какой-то из файлов поврежден. Повторите отправку файлов ещё раз")
        return res
