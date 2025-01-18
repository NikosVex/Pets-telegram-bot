import logging
from aiogram import F, Router
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import app.database.requests as rq

router = Router()


class SeacrhPet(StatesGroup):
    username = State()
    petname = State()


@router.message(F.text == '🔎 Поиск питомца')
async def search_pet_handler(message: Message):
    await message.answer('Выберите тип поиска на Клавиатуре ⌨️', reply_markup=kb.search_pet_keyboard)


@router.message(F.text == '👤 По имени пользователя')
async def search_pet_username_handler(message: Message, state: FSMContext):
    await state.set_state(SeacrhPet.username)
    await message.answer('Введите имя пользователя, у которого хотите посмотреть питомцев',
                         reply_markup=kb.exit_button)


@router.message(SeacrhPet.username)
async def show_pets_username_handler(message: Message, state: FSMContext):
    try:
        username = message.text
        pets = await rq.get_pet_by_username(username)
        if pets:
            await message.answer(f'Все результаты по запросу: <b>{username}</b>', parse_mode='html')
            for pet in pets:
                await message.answer_photo(
                    photo=FSInputFile(pet.photo_path),
                    caption=f'Имя: <b>{pet.name}</b>\nПорода: <b>{pet.breed}</b>\n'
                    f'Комментарий: <b>{pet.additionally}</b>\n\n<b>{pet.likes}</b> ❤️',
                    reply_markup=kb.pets_keyboard_without_next(pet.id), parse_mode='html'
                )
        else:
            await message.answer('У этого пользователя пока нет питомцев или этого пользователя не существует')
        await state.clear()
    except Exception as e:
        await message.answer('Ошибка при поиске питомцев, попробуйте ещё раз позже!')
        logging.error(f'Ошибка в show_pets_by_username_handler: {e}')


@router.message(F.text == '🐱 По имени питомца')
async def search_pet_petname_handler(message: Message, state: FSMContext):
    await state.set_state(SeacrhPet.petname)
    await message.answer('Введите имя питомца: ', reply_markup=kb.exit_button)


@router.message(SeacrhPet.petname)
async def show_pets_username_handler(message: Message, state: FSMContext):
    try:
        petname = message.text
        pets = await rq.get_pet_by_petname(petname)
        if pets:
            await message.answer(f'Все результаты по запросу: <b>{petname}</b>', parse_mode='html')
            for pet in pets:
                await message.answer_photo(
                    photo=FSInputFile(pet.photo_path),
                    caption=f'Имя: <b>{pet.name}</b>\nПорода: <b>{pet.breed}</b>\n'
                    f'Комментарий: <b>{pet.additionally}</b>\n\n<b>{pet.likes}</b> ❤️',
                    reply_markup=kb.pets_keyboard_without_next(pet.id), parse_mode='html'
                )
        else:
            await message.answer('Не найдено питомцев с таким именем!')
        await state.clear()
    except Exception as e:
        await message.answer('Ошибка при поиске питомцев, попробуйте ещё раз позже!')
        logging.error(f'Ошибка в show_pets_by_username_handler: {e}')


@router.message(F.text == '⬅️ Назад')
async def back_to_watching_pets_handler(message: Message):
    await message.answer('Вы вернулись назад', reply_markup=kb.watching_pets)
