import logging
from aiogram import F, Router
from aiogram.types import Message, FSInputFile, CallbackQuery

import app.keyboards as kb
import app.database.requests as rq

router = Router()

admins_id = [1774953059, 2026368571, 2079877089]


@router.message(F.text == '⚙️ Админ панель 📄')
async def admin_handler(message: Message):
    user_id = message.from_user.id
    if user_id in admins_id:
        await message.answer('Выберите пункт в Инлайн-клавиатуре ⌨️', reply_markup=kb.admin_keyboard)
    else:
        await message.answer('У вас нет полномочий админа!', reply_markup=kb.main_keyboard(user_id))


@router.callback_query(F.data == 'admin_proposal')
async def admin_proposal_handler(callback: CallbackQuery):
    try:
        user = callback.from_user.id
        if user:
            proposals = await rq.get_all_proposals()
            if proposals:
                await callback.message.answer('Предложения:')
                for proposal in proposals:
                    await callback.message.answer(f'Предложение от пользователя <b>{proposal.username}</b>: \n\n'
                                                  f'{proposal.message}', parse_mode='html')
            else:
                await callback.message.answer('Пока что нет никаких предложений!')
    except Exception as e:
        await callback.answer('Ошибка при отображении предложений!')
        logging.error(f'Ошибка в admin_proposal_handler: {e}')


@router.callback_query(F.data == 'admin_pet')
async def admin_pet_handler(callback: CallbackQuery):
    try:
        user = callback.from_user.id
        if user:
            pets_to_check = await rq.get_show_false()
            if pets_to_check:
                await callback.message.answer('Питомцы на проверку:')
                for pet in pets_to_check:
                    await callback.message.answer_photo(
                        photo=FSInputFile(pet.photo_path),
                        caption=f'Имя: <b>{pet.name}</b>\nПорода: <b>{pet.breed}</b>\n'
                        f'Комментарий: <b>{pet.additionally}</b>\n\n<b>Добавить питомца?</b>',
                        reply_markup=kb.admin_check_pets_keyboard(pet.id), parse_mode='html'
                    )
            else:
                await callback.message.answer('Сейчас нет питомцев на проверку!')
    except Exception as e:
        await callback.message.answer('Ошибка при отображении питомцев, которые должны пройти проверку!')
        logging.error(f'Ошибка в admin_pet_handler: {e}')


@router.callback_query(F.data.startswith('true_'))
async def show_pet_true_handler(callback: CallbackQuery):
    try:
        pet_id = int(callback.data.split('_')[1])
        await rq.change_pet_true(pet_id)
        await callback.answer('Питомец проверен!')
        await callback.message.delete()
    except Exception as e:
        await callback.answer('Ошибка при проверке питомца!')
        logging.error(f'Ошибка в show_pet_true_handler: {e}')


@router.callback_query(F.data.startswith('false_'))
async def show_pet_false_handler(callback: CallbackQuery):
    try:
        pet_id = int(callback.data.split('_')[1])
        await callback.answer('Питомец не прошел проверку!')
        await rq.delete_pet(pet_id)
        await callback.message.delete()
    except Exception as e:
        await callback.answer('Ошибка при отклонении питомца!')
        logging.error(f'Ошибка в show_pet_false_handler: {e}')
