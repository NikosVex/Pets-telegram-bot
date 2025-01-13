from aiogram import F, Router
from aiogram.types import Message

import app.database.requests as rq

router = Router()


@router.message(F.text == '🏅 Рейтинг')
async def raiting_handler(message: Message):
    top_pets = await rq.get_top_pets()
    if top_pets:
        text = 'Топ-10 питомцев по лайкам:\n\n'
        medals = ['🥇', '🥈', '🥉']
        for i, pet in enumerate(top_pets):
            medal = medals[i] if i < len(medals) else str(i + 1)
            text += f'{medal} - <b>{pet.name} {pet.likes}</b> ❤️\n'
        await message.answer(text, parse_mode='html')
    else:
        await message.answer('Питомцы отсутствуют :(')
