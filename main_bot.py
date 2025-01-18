import os
import logging
import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from app.handlers import (
    add_pet, admin, commands, delete_pet, exit, delete_favorite, favorite,
    like, my_account, proposal, rating, search_pet, show_pets, secret)
from app.database.models import async_main

load_dotenv()

logging.basicConfig(filename='log.log', level=logging.WARNING,
                    format='%(asctime)s - %(levelname)s - %(module)s - %(message)s')


async def main():
    await async_main()
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    dp.include_routers(
        add_pet.router, admin.router, commands.router, delete_pet.router, delete_favorite.router, exit.router,
        favorite.router, like.router, my_account.router, proposal.router, rating.router, search_pet.router,
        show_pets.router, secret.router
    )
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info('Бот выключен')
