from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

import app.keyboards as kb
import app.database.requests as rq

router = Router()


@router.message(CommandStart())
async def cmd_start_handler(message: Message):
    username = message.from_user.username
    tg_id = message.from_user.id
    if username:
        await rq.set_user(tg_id, username)
    else:
        await rq.set_user(tg_id, 'Отсутствует')
    await message.answer('Привет! Здесь вы можете посмотреть питомцев и добавить своего!\n/help - помощь',
                         reply_markup=kb.main_keyboard(tg_id))


@router.message(Command('help'))
async def cmd_help_handler(message: Message):
    await message.reply(
        'Все функции и команды бота <b>Pets</b>:\n\n/start - Перезапуск бота.\n/info - Информация о боте.\n\n'
        'Кнопка <b>"🐱 Смотреть питомца"</b> - После нажатия на эту кнопку вы попадаете в Меню выбора просмотра питомцев:\n\n'
        '1. Кнопка <b>"🎲 Случайный питомец"</b> - Выдает рандомного питомца, которого добавил другой пользователь.\n'
        '2. Кнопка <b>"🔎 Поиск питомца"</b> - После нажатия на эту кнопку вы можете выбрать тип поиска: '
        'поиск по имени пользователя, который добавил питомца, либо по имени питомца, для того, '
        'чтобы вернуться в Меню просмотра питомцев нажмите кнопку <b>"⬅️ Назад"</b>.\n'
        '3. Кнопка <b>"⬅️ В Главное меню"</b> - Вы возвращайтесь в Главное меню.\n\n'
        'Кнопка <b>"➕ Добавить питомца"</b> - Дает возможность добавить своего питомца, которого смогут увидеть '
        'другие пользователи.'
        ' Вас попросят ввести информацию о вашем питомце и затем загрузить фотографию, '
        'после этого питомец должен пройти проверку администраторов, чтобы стать доступным другим пользователям!\n\n'
        'Кнопка <b>"🏅 Рейтинг"</b> - Показывает топ-10 питомцев по количеству ❤️\n\n'
        'Кнопка <b>"👤 Мой аккаунт"</b> - Вы попадаете в свой аккаунт, где можете посмотреть своих питомцев, '
        'которых вы загрузили, с помощью кнопки <b>"Мои питомцы"</b> и питомцев, '
        'которых вы добавили в избранное с помощью кнопки <b>"💛 Моё избранное"</b>.',
        parse_mode='html'
    )


@router.message(Command('info'))
async def cmd_info_handler(message: Message):
    await message.reply(
        'Информация о боте:\n\nЭтот бот создан в рамках <b>индивидуального проекта студента 1 курса ФСПО ГУАП</b>\n\n'
        'Основная цель бота - дать возможность пользователям делиться своими питомцами и '
        'смотреть питомцев других пользователей!\n\nАктуальная версия бота - <b>beta 1.13</b>',
        reply_markup=kb.link_button, parse_mode='html'
    )
