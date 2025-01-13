import os
from aiogram import F, Router
from aiogram.types import Message, FSInputFile
from dotenv import load_dotenv

router = Router()

load_dotenv()


@router.message(F.text == os.getenv('SECRET_WORD_1'))
async def secret_n1_handler(message: Message):
    await message.answer_photo(photo=FSInputFile(os.getenv('SECRET_PATH_1')), caption=os.getenv('SECRET_CAPTION_1'))


@router.message(F.text == os.getenv('SECRET_WORD_2'))
async def secret_n2_handler(message: Message):
    await message.answer_photo(photo=FSInputFile(os.getenv('SECRET_PATH_2')), caption=os.getenv('SECRET_CAPTION_2'))


@router.message(F.text == os.getenv('SECRET_WORD_3'))
async def secret_n2_handler(message: Message):
    await message.answer_photo(photo=FSInputFile(os.getenv('SECRET_PATH_3')), caption=os.getenv('SECRET_CAPTION_3'))


@router.message()
async def all_messages_handler(message: Message):
    await message.answer('Данное сообщение не является командой или ключевым словом!')