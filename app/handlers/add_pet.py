from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import app.database.requests as rq

router = Router()


class AddPet(StatesGroup):
    name = State()
    breed = State()
    additionally = State()
    photo = State()


@router.message(F.text == '➕ Добавить питомца')
async def add_pet_start(message: Message, state: FSMContext):
    await state.set_state(AddPet.name)
    await message.answer('Напишите имя питомца: ', reply_markup=kb.exit_pet_add)


@router.message(AddPet.name)
async def add_pet_name(message: Message, state: FSMContext):
    if len(message.text) <= 25:
        await state.update_data(name=message.text)
        await state.set_state(AddPet.breed)
        await message.answer('Напишите породу питомца: ', reply_markup=kb.exit_pet_add)
    else:
        await message.answer('Имя питомца слишком длинное! Оно должно быть не более 25 символов, попробуйте ещё раз!',
                             reply_markup=kb.exit_pet_add)


@router.message(AddPet.breed)
async def add_pet_breed(message: Message, state: FSMContext):
    if len(message.text) <= 40:
        await state.update_data(breed=message.text)
        await state.set_state(AddPet.additionally)
        await message.answer('Напишите комментарий к питомцу: ', reply_markup=kb.exit_pet_add)
    else:
        await message.answer('Порода питомца слишком длинная! Она должно быть не более 40 символов, '
                             'попробуйте ещё раз!', reply_markup=kb.exit_pet_add)


@router.message(AddPet.additionally)
async def add_pet_additionally(message: Message, state: FSMContext):
    if len(message.text) <= 200:
        await state.update_data(additionally=message.text)
        await state.set_state(AddPet.photo)
        await message.answer('Отправьте фотографию питомца: ', reply_markup=kb.exit_pet_add)
    else:
        await message.answer('Комментарий слишком длинный! Он должен быть не более 200 символов, попробуйте ещё раз!',
                             reply_markup=kb.exit_pet_add)


@router.message(AddPet.photo)
async def add_pet_photo(message: Message, state: FSMContext):
    if message.photo:
        photo = message.photo[-1]
        file_id = photo.file_id
        file = await message.bot.get_file(file_id)
        file_path = file.file_path
        local_path = f'pet_photos/{file_id}.jpg'
        await message.bot.download_file(file_path, local_path)

        await state.update_data(photo_path=local_path)
        data = await state.get_data()
        await rq.add_pet(message.from_user.id, data['name'], data['breed'], local_path, data['additionally'], likes=0)
        await state.clear()
        await message.answer(
            'Спасибо за добавление питомца! Он находится на проверке у администраторов! Вы можете проверить '
            'состояние проверки вашего питомца в своем аккаунте!', reply_markup=kb.main_keyboard(message.from_user.id))
    else:
        await message.answer('Отправьте, пожалуйста, ФОТОГРАФИЮ питомца', reply_markup=kb.exit_pet_add)


@router.callback_query(F.data == 'exit_pet_add')
async def exit_pet_add_handler(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.edit_text('Добавление питомца отменено!')
        await state.clear()
    except Exception as e:
        print(f'Произошла ошибка при отмене записи питомца: {e}')
