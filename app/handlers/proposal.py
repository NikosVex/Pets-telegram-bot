import logging
from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import app.database.requests as rq

router = Router()


class AddProposal(StatesGroup):
    proposal = State()


@router.message(F.text == '🗳 Предложка')
async def add_proposal_handler_start(message: Message, state: FSMContext):
    await state.set_state(AddProposal.proposal)
    await message.answer('Введите предложение для улучшения бота, его прочитает разработчик! (не более 400 символов)',
                         reply_markup=kb.exit_button)


@router.message(AddProposal.proposal)
async def add_proposal_handler_end(message: Message, state: FSMContext):
    try:
        if len(message.text) <= 400:
            await state.update_data(proposal=message.text)
            data = await state.get_data()
            await rq.add_proposal(message.from_user.id, data['proposal'])
            await state.clear()
            await message.answer('Спасибо за предложение! Оно будет рассмотрено разработчиком :)',
                                 reply_markup=kb.main_keyboard(message.from_user.id))
            logging.info(f'Пользователь {message.from_user.username} добавил предложение!')
        else:
            await message.answer(
                'Предложение слишком длинное! Попробуйте еще раз, оно должно быть не более 400 символов',
                reply_markup=kb.exit_button
            )
    except Exception as e:
        await message.answer('Произошла ошибка при добавлении предложения, попробуйте еще раз позже!')
        logging.error(f'Произошла ошибка в add_proposal_handler_end: {e}')
