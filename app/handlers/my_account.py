import logging
from aiogram import F, Router
from aiogram.types import Message, FSInputFile, CallbackQuery

import app.keyboards as kb
import app.database.requests as rq

router = Router()


@router.message(F.text == '👤 Мой аккаунт')
async def my_account_handler(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    await message.answer(f'Аккаунт пользователя @{username}\nВаш Telegram ID: <b>{user_id}</b>',
                         reply_markup=kb.my_account_keyboard(user_id), parse_mode='html')


@router.callback_query(F.data.startswith('my_pets_'))
async def my_pets_handler(callback: CallbackQuery):
    try:
        user_id = callback.from_user.id
        pets = await rq.get_my_pets(user_id)
        if pets:
            await callback.message.answer('Ваши питомцы:')
            for pet in pets:
                if pet.show:
                    status = 'Проверен ✅'
                else:
                    status = 'Не проверен ❌'
                await callback.message.answer_photo(
                    photo=FSInputFile(pet.photo_path),
                    caption=f'Имя: <b>{pet.name}</b>\nПорода: <b>{pet.breed}</b>\n'
                    f'Комментарий: <b>{pet.additionally}</b>\nСтатус: <b>{status}</b>\n\n<b>{pet.likes}</b> ❤️',
                    reply_markup=kb.delete_pet(pet.id), parse_mode='html'
                )
        else:
            await callback.answer('У вас пока нет питомцев. Добавьте своего!')
    except Exception as e:
        await callback.answer('Ошибка при отображении ваших питомцев, попробуйте ещё раз позже!')
        logging.error(f'Ошибка в my_pets_handler: {e}')


@router.callback_query(F.data.startswith('my_favorites_'))
async def my_favorites_pets_handler(callback: CallbackQuery):
    try:
        user_id = callback.from_user.id
        pets = await rq.get_user_favorite_pets(user_id)
        if pets:
            await callback.message.answer('Ваши избранные питомцы:')
            for pet in pets:
                await callback.message.answer_photo(
                    photo=FSInputFile(pet.photo_path),
                    caption=f'Имя: <b>{pet.name}</b>\nПорода: <b>{pet.breed}</b>\n'
                    f'Комментарий: <b>{pet.additionally}</b>\n\n<b>{pet.likes}</b> ❤️',
                    reply_markup=kb.delete_favorite(pet.id), parse_mode='html'
                )
        else:
            await callback.answer('У вас пока нет питомцев в избранном!')
    except Exception as e:
        await callback.answer('Ошибка при отображении избранных питомцев, попробуйте ещё раз позже!')
        logging.error(f'Ошибка в my_favorites_pets_handler: {e}')
