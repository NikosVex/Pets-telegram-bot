import os
import logging
import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from app.handlers import (
    add_pet, admin, commands, delete_pet, delete_favorite, favorite,
    like, my_account, rating, search_pet, show_pets, secret)
from app.database.models import async_main

load_dotenv()

logging.basicConfig(filename='log.log', level=logging.WARNING,
                    format='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

admins_id = [1774953059, 2026368571, 2079877089]


async def main():
    await async_main()
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    dp.include_routers(
        add_pet.router, admin.router, commands.router, delete_pet.router, delete_favorite.router, favorite.router,
        like.router, my_account.router, rating.router, search_pet.router, show_pets.router, secret.router
    )
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info('Бот выключен')
