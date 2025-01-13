import os
import logging
from sqlalchemy import BigInteger, String, ForeignKey, Integer, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from dotenv import load_dotenv

load_dotenv()

engine = create_async_engine(url=os.getenv('DB_URL'))

async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger, unique=True)
    username: Mapped[str] = mapped_column(String(35))


class Pet(Base):
    __tablename__ = 'pets'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))
    breed: Mapped[str] = mapped_column(String(40))
    additionally: Mapped[str] = mapped_column(String(200))
    likes: Mapped[int] = mapped_column(Integer, default=0)
    photo_path: Mapped[str] = mapped_column(Text)
    user_id = mapped_column(Integer, ForeignKey('users.id'))
    show: Mapped[bool] = mapped_column(Boolean, default=False)


class Like(Base):
    __tablename__ = 'likes'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), index=True)
    pet_id: Mapped[int] = mapped_column(Integer, ForeignKey('pets.id'), index=True)
    liked: Mapped[bool] = mapped_column(Boolean, default=False)


class Favorite(Base):
    __tablename__ = 'favorites'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), index=True)
    pet_id: Mapped[int] = mapped_column(Integer, ForeignKey('pets.id'), index=True)
    favorited: Mapped[bool] = mapped_column(Boolean, default=False)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logging.info('База данных включена!')
