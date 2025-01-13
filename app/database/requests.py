import os
import logging

from sqlalchemy import select, func, update
from app.database.models import async_session, User, Pet, Like, Favorite


async def set_user(tg_id, username):
    """Функция записи пользователя в базу данных"""
    async with async_session() as session:
        try:
            existing_user = await session.scalar(select(User).where(User.tg_id == tg_id))  # type: ignore
            if not existing_user:
                session.add(User(tg_id=tg_id, username=username))
                await session.commit()
                logging.info(f'Пользователь с ID {tg_id} и username {username} добавлен')
        except Exception as e:
            logging.error(f'Ошибка при добавлении пользователя: {e}')


async def add_pet(tg_id, name, breed, photo_path, additionally, likes):
    """Функция добавления питомца в базу данных"""
    async with async_session() as session:
        try:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))  # type: ignore
            if user:
                session.add(Pet(user_id=user.id, name=name, breed=breed, photo_path=photo_path,
                                additionally=additionally, likes=likes, show=False))
                await session.commit()
                logging.info(f'Питомец с ID {name} пользователя с ID {tg_id} добавлен!')
            else:
                logging.warning(f'Пользователь с tg_id {tg_id} не найден')
        except Exception as e:
            logging.error(f'Ошибка при добавлении питомца: {e}')


async def get_random_pet():
    """Функция получения рандомного питомца из базы данных"""
    async with async_session() as session:
        random_pet = await session.execute(select(Pet).filter(Pet.show == True).order_by(func.random()))
        return random_pet.scalars().first()


async def add_like(tg_id, pet_id):
    """Функция добавления лайка в базу данных"""
    async with async_session() as session:
        try:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))  # type: ignore
            existing_like = await session.scalar(select(Like).where(Like.user_id == user.id, Like.pet_id == pet_id))
            if not existing_like:
                session.add(Like(user_id=user.id, pet_id=pet_id, liked=True))
                await session.execute(update(Pet).where(Pet.id == pet_id).values(likes=Pet.likes + 1))
                await session.commit()
                logging.info(f'Пользователь с ID {user.id} лайкнул питомца с ID {pet_id}')
        except Exception as e:
            logging.error(f'Ошибка при добавлении лайка: {e}')


async def check_user_liked(tg_id, pet_id):
    """Проверка на лайк от пользователя"""
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))  # type: ignore
        result = await session.scalar(select(Like).where(Like.user_id == user.id, Like.pet_id == pet_id))
        return result is not None


async def add_favorite(tg_id, pet_id):
    """Функция добавления питомца в избранное"""
    async with async_session() as session:
        try:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))  # type: ignore
            existing_favorite = await session.scalar(select(Favorite).where(Favorite.user_id == user.id,
                                                                            Favorite.pet_id == pet_id))
            if not existing_favorite:
                session.add(Favorite(user_id=user.id, pet_id=pet_id, favorited=True))
                await session.commit()
                logging.info(f'Пользователь с ID {user.id} добавил в избранное питомца с ID {pet_id}')
        except Exception as e:
            logging.error(f'Ошибка при добавлении лайка: {e}')


async def check_user_favorited(tg_id, pet_id):
    """Проверка на избранное от пользователя"""
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))  # type: ignore
        result = await session.scalar(select(Favorite).where(Favorite.user_id == user.id, Favorite.pet_id == pet_id))
        return result is not None


async def get_my_pets(tg_id):
    """Возвращает список питомцев пользователя"""
    async with async_session() as session:
        try:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))  # type: ignore
            if user:
                pet_of_user = await session.execute(select(Pet).where(Pet.user_id == user.id))  # type: ignore
                pets = pet_of_user.scalars().all()
                return pets
        except Exception as e:
            logging.error(f'Ошибка при получении питомцев пользователя: {e}')


async def get_user_favorite_pets(tg_id):
    """Возвращает список избранных питомцев пользователя"""
    async with async_session() as session:
        try:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))  # type: ignore
            if user:
                favorites = await session.execute(select(Pet).join(Favorite).where(Favorite.user_id == user.id,
                                                                                   Favorite.favorited))
                pets = favorites.scalars().all()
                return pets
        except Exception as e:
            logging.error(f'Ошибка при получении питомцев пользователя: {e}')


async def get_pet_by_username(username):
    """Возвращает список питомцев по имени пользователя"""
    async with async_session() as session:
        try:
            user = await session.scalar(select(User).where(User.username.ilike(f'%{username}%')))
            if user:
                pet = await session.execute(
                    select(Pet).filter(Pet.show == True).where(Pet.user_id == user.id))  # type: ignore
                pets = pet.scalars().all()
                return pets
        except Exception as e:
            logging.error(f'Ошибка при получении питомцев пользователя: {e}')


async def get_pet_by_petname(petname):
    """Возвращает список питомцев по имени"""
    async with async_session() as session:
        try:
            pets = await session.execute(select(Pet).filter(Pet.show == True).where(Pet.name.ilike(f'%{petname}%')))
            return pets.scalars().all()
        except Exception as e:
            logging.error(f"Ошибка при получении питомцев по имени: {e}")


async def update_pet(pet_id):
    """Функция для обновления питомца"""
    async with async_session() as session:
        pet = await session.execute(select(Pet).where(Pet.id == pet_id))
        return pet.scalars().first()


async def get_top_pets(limit=10):
    """Функция получения топ-10 питомцев по лайкам"""
    async with async_session() as session:
        top_pets = await session.execute(select(Pet).filter(Pet.show == True).order_by(Pet.likes.desc()).limit(limit))
        return top_pets.scalars().all()


async def delete_pet(pet_id):
    """Функция удаления питомца и связанных с ним лайков из базы данных"""
    async with async_session() as session:
        try:
            likes_to_delete = await session.scalars(select(Like).where(Like.pet_id == pet_id))
            for like in likes_to_delete:
                await session.delete(like)

            favorites_to_delete = await session.scalars(select(Favorite).where(Favorite.pet_id == pet_id))
            for favorite in favorites_to_delete:
                await session.delete(favorite)

            pet_to_delete = await session.get(Pet, pet_id)
            if pet_to_delete:
                photo_path = pet_to_delete.photo_path
                if photo_path and os.path.exists(photo_path):  # Проверка на существование файла
                    os.remove(photo_path)
                await session.delete(pet_to_delete)
                await session.commit()
                logging.info(f'Питомец с ID {pet_id} удален.')
            else:
                logging.warning(f'Питомец с ID {pet_id} не найден.')
        except Exception as e:
            logging.error(f'Ошибка при удалении питомца: {e}')
            await session.rollback()


async def delete_favorite_pet(pet_id, tg_id):
    """Функция удаления питомца из избранного"""
    async with async_session() as session:
        try:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))  # type: ignore
            if user:
                favorite_to_delete = await session.scalar(select(Favorite).where(Favorite.user_id == user.id,
                                                                                 Favorite.pet_id == pet_id))
                await session.delete(favorite_to_delete)
                await session.commit()
                logging.info(f'Питомец с ID {pet_id} удален из избранного пользователя {user.username}.')
            else:
                logging.warning(f'Питомец с ID {pet_id} не найден.')
        except Exception as e:
            logging.error(f'Ошибка при удалении питомца из избранного: {e}')
            await session.rollback()


async def count_of_likes(tg_id):
    """Функция подсчета количества лайков пользователя"""
    async with async_session() as session:
        try:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))  # type: ignore
            if user:
                count = await session.scalar(select(func.count(Like.id)).where(Like.user_id == user.id))
                return count.scalar_one()
        except Exception as e:
            logging.error(f'Ошибка при подсчете лайков пользователя: {e}')


async def count_of_favorites(tg_id):
    """Функция подсчета количества избранных у пользователя"""
    async with async_session() as session:
        try:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))  # type: ignore
            if user:
                count = await session.execute(select(func.count(Favorite.id)).where(Favorite.user_id == user.id))
                return count.scalar_one()
        except Exception as e:
            logging.error(f'Ошибка при подсчете лайков пользователя: {e}')


async def get_show_false():
    """Выводит всех питомцев с show = False"""
    async with async_session() as session:
        pets_false = await session.execute(select(Pet).filter(Pet.show == False))
        return pets_false.scalars().all()


async def change_pet_true(pet_id):
    """Изменяет Pet.show на True"""
    async with async_session() as session:
        try:
            await session.execute(update(Pet).where(Pet.id == pet_id).values(show=True))
            await session.commit()
            logging.info(f"Значение show для питомца с ID {pet_id} изменено на True.")
        except Exception as e:
            await session.rollback()
            logging.error(f"Ошибка при изменении значения show для питомца с ID {pet_id}: {e}")
