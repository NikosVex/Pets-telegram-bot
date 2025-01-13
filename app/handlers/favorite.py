import os
import logging
from aiogram import F, Router
from aiogram.types import CallbackQuery
from dotenv import load_dotenv

import app.database.requests as rq

router = Router()

load_dotenv()


@router.callback_query(F.data.startswith('favorite_'))
async def favorite_handler(callback: CallbackQuery):
    try:
        pet_id = int(callback.data.split('_')[1])
        user_id = callback.from_user.id
        already_favorited = await rq.check_user_favorited(user_id, pet_id)  # Проверка на избранное от пользователя
        if already_favorited:
            await callback.answer('Вы уже добавили этого питомца в избранное!')
        else:
            await rq.add_favorite(user_id, pet_id)
            await callback.answer('Вы добавили питомца в избранное!')
            count_of_favorites = await rq.count_of_favorites(user_id)
            if count_of_favorites == 10:
                await callback.message.answer(f'🏆 Ачивка!\nВы добавили в избранное 10 питомцев и открыли секретное '
                                              f'слово {os.getenv("SECRET_WORD_3")}!')
    except Exception as e:
        await callback.answer('Ошибка при добавлении питомца в избранное, попробуйте ещё раз позже!')
        logging.error(f'Ошибка в favorite_handler: {e}')
