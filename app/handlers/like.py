import os
import logging
from aiogram import F, Router
from aiogram.types import CallbackQuery
from dotenv import load_dotenv

import app.keyboards as kb
import app.database.requests as rq

router = Router()

load_dotenv()


@router.callback_query(F.data.startswith('like_'))
async def like_handler(callback: CallbackQuery):
    try:
        pet_id = int(callback.data.split('_')[1])
        user_id = callback.from_user.id
        already_liked = await rq.check_user_liked(user_id, pet_id)  # Проверка на наличие лайка от пользователя
        if already_liked:
            await callback.answer('Вы уже лайкнули этого питомца!')
        else:
            await rq.add_like(user_id, pet_id)
            await callback.answer('Вы лайкнули питомца!')
            pet = await rq.update_pet(pet_id)
            if pet:
                await callback.message.edit_caption(
                    caption=f'Имя: <b>{pet.name}</b>\nПорода: <b>{pet.breed}</b>\n'
                    f'Комментарий: <b>{pet.additionally}</b>\n\n<b>{pet.likes}</b> ❤️',
                    reply_markup=kb.pets_keyboard(pet_id), parse_mode='html'
                )
            count_of_likes = await rq.count_of_likes(user_id)
            if count_of_likes == 10:
                await callback.message.answer(f'🏆 Ачивка!\nВы лайкнули 10 питомцев и открыли секретное слово '
                                              f'{os.getenv("SECRET_WORD_2")}!')
    except Exception as e:
        await callback.answer('Ошибка при добавлении лайка, попробуйте ещё раз позже!')
        logging.error(f'Ошибка в like_handler: {e}')
