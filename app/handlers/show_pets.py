import logging
from aiogram import F, Router
from aiogram.types import Message, FSInputFile, CallbackQuery, InputMediaPhoto
from aiogram.exceptions import TelegramBadRequest

import app.keyboards as kb
import app.database.requests as rq

router = Router()


@router.message(F.text == '🐱 Смотреть питомцев')
async def show_random_pet_handler(message: Message):
    await message.answer('Выберите действие на Клавиатуре ⌨️', reply_markup=kb.watching_pets)


@router.message(F.text == '🎲 Случайный питомец')
async def show_random_pet_handler(message: Message):
    try:
        pet = await rq.get_random_pet()
        if pet:
            await message.answer_photo(
                photo=FSInputFile(pet.photo_path),
                caption=f'Имя: <b>{pet.name}</b>\nПорода: <b>{pet.breed}</b>\n'
                f'Комментарий: <b>{pet.additionally}</b>\n\n<b>{pet.likes}</b> ❤️',
                reply_markup=kb.pets_keyboard(pet.id), parse_mode='html'
            )
        else:
            await message.answer('Питомцы отсутствуют :(')
    except Exception as e:
        await message.answer('Ошибка при отображении питомцев, попробуйте ещё раз позже!')
        logging.error(f'Ошибка в show_random_pet_handler: {e}')


@router.callback_query(F.data == 'next_pet')
async def next_pet_handler(callback: CallbackQuery):
    try:
        pet = await rq.get_random_pet()
        if pet:
            await callback.message.edit_media(
                InputMediaPhoto(media=FSInputFile(pet.photo_path),
                                caption=f'Имя: <b>{pet.name}</b>\nПорода: <b>{pet.breed}</b>\n'
                                f'Комментарий: <b>{pet.additionally}</b>\n\n<b>{pet.likes}</b> ❤️',
                                parse_mode='html'),
                reply_markup=kb.pets_keyboard(pet.id)
            )
    except TelegramBadRequest:
        await callback.answer('Выпал тот же питомец! Попробуйте еще раз')


@router.message(F.text == '⬅️ В Главное меню')
async def main_menu_handler(message: Message):
    await message.answer('Вы вернулись в Главное меню 📋', reply_markup=kb.main_keyboard(message.from_user.id))
