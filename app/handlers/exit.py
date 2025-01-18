import logging
from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

router = Router()

@router.callback_query(F.data == 'exit')
async def exit_handler(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.edit_text('Действие отменено!')
        await state.clear()
    except Exception as e:
        logging.error(f'Произошла ошибка при отмене поиска питомца: {e}')