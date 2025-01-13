import logging
from aiogram import F, Router
from aiogram.types import CallbackQuery

import app.keyboards as kb
import app.database.requests as rq

router = Router()


@router.callback_query(F.data.startswith('delete_pet_'))
async def delete_pet_handler(callback: CallbackQuery):
    pet_id = int(callback.data.split('_')[2])
    pet = await rq.update_pet(pet_id)
    await callback.message.edit_caption(
        caption=f'Имя: <b>{pet.name}</b>\nПорода: <b>{pet.breed}</b>\n'
        f'Комментарий: <b>{pet.additionally}</b>\n\n<b>{pet.likes}</b> ❤️\n\n'
        f'<b>Вы уверены, что хотите удалить питомца?</b>',
        reply_markup=kb.delete_pet_check(pet_id), parse_mode='html'
    )


@router.callback_query(F.data.startswith('delete_yes_'))
async def delete_pet_yes_handler(callback: CallbackQuery):
    try:
        pet_id = int(callback.data.split('_')[2])
        await rq.delete_pet(pet_id)
        await callback.answer('Питомец удален!')
        await callback.message.delete()
    except Exception as e:
        await callback.answer('Ошибка при удалении питомца, попробуйте ещё раз позже!')
        logging.error(f'Ошибка в delete_pet_yes_handler: {e}')


@router.callback_query(F.data.startswith('delete_no_'))
async def delete_pet_yes_handler(callback: CallbackQuery):
    pet_id = int(callback.data.split('_')[2])
    pet = await rq.update_pet(pet_id)
    await callback.message.edit_caption(
        caption=f'Имя: <b>{pet.name}</b>\nПорода: <b>{pet.breed}</b>\n'
        f'Комментарий: <b>{pet.additionally}</b>\n\n<b>{pet.likes}</b> ❤️',
        reply_markup=kb.delete_pet(pet_id), parse_mode='html'
    )
