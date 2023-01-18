import datetime

from typing import Union

from sqlalchemy import Column, BigInteger, VARCHAR, Date, select, delete
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError, NoResultFound

from .base import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    user_id = Column(BigInteger, unique=True, nullable=False, primary_key=True)
    username = Column(VARCHAR(32), unique=False, nullable=True)
    fullname = Column(VARCHAR(128), unique=False, nullable=True)
    reg_date = Column(Date, default=datetime.date.today())
    upd_date = Column(Date, onupdate=datetime.date.today())

    def __str__(self):
        return f'<User:{self.user_id}>'


# CREATE
async def create_user(user_id: int, username: str, fullname: str, session_maker: sessionmaker) -> str:
    async with session_maker() as session:
        async with session.begin():
            user = User(
                user_id=user_id,
                username=f'@{username}',
                fullname=fullname
            )
            try:
                session.add(user)
                return 'Вы успешно добавлены в базу данных.'
            except ProgrammingError as error:
                # TODO: log
                return 'Произошла ошибка при добавлении пользователя в базу данных.'


# READ
async def get_user(user_id: int, session_maker: sessionmaker) -> User:
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                select(User).where(User.user_id == user_id)
            )
            return result.scalars().one()


# UPDATE
# TODO: Update functions


# DELETE
async def delete_user(user_id: int, session_maker: sessionmaker) -> Union[None, Exception]:
    async with session_maker() as session:
        async with session.begin():
            try:
                await session.execute(delete(User).where(User.user_id == user_id))
                # TODO: log
            except Exception as error:
                # TODO: log
                return error


# MISC
async def check_user_exists(user_id: int, session_maker: sessionmaker) -> bool:
    try:
        user = await get_user(user_id, session_maker)
        print(user)
        if user:
            return True
    except NoResultFound:
        return False
