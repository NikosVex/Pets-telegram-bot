import logging
from aiogram import F, Router
from aiogram.types import CallbackQuery

import app.keyboards as kb
import app.database.requests as rq

router = Router()


@router.callback_query(F.data.startswith('delete_favorite_'))
async def delete_pet_handler(callback: CallbackQuery):
    pet_id = int(callback.data.split('_')[2])
    pet = await rq.update_pet(pet_id)
    await callback.message.edit_caption(
        caption=f'Имя: <b>{pet.name}</b>\nПорода: <b>{pet.breed}</b>\n'
        f'Комментарий: <b>{pet.additionally}</b>\n\n<b>{pet.likes}</b> ❤️\n\n'
        f'<b>Вы уверены, что хотите удалить питомца из избранного?</b>',
        reply_markup=kb.delete_favorite_check(pet_id), parse_mode='html'
    )


@router.callback_query(F.data.startswith('delfavorite_yes_'))
async def delete_pet_yes_handler(callback: CallbackQuery):
    try:
        user_id = callback.from_user.id
        pet_id = int(callback.data.split('_')[2])
        await rq.delete_favorite_pet(pet_id, user_id)
        await callback.answer('Питомец удален из избранного!')
        await callback.message.delete()
    except Exception as e:
        await callback.answer('Ошибка при удалении питомца из избранного, попробуйте ещё раз позже!')
        logging.error(f'Ошибка в delete_pet_yes_handler: {e}')


@router.callback_query(F.data.startswith('delfavorite_no_'))
async def delete_pet_yes_handler(callback: CallbackQuery):
    pet_id = int(callback.data.split('_')[2])
    pet = await rq.update_pet(pet_id)
    await callback.message.edit_caption(
        caption=f'Имя: <b>{pet.name}</b>\nПорода: <b>{pet.breed}</b>\n'
        f'Комментарий: <b>{pet.additionally}</b>\n\n<b>{pet.likes}</b> ❤️',
        reply_markup=kb.delete_favorite(pet_id), parse_mode='html'
    )
