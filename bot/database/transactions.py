import datetime as dt

from sqlalchemy import Column, Integer, BigInteger, Text, Date, Time, Boolean, ForeignKey, Float, select, and_, delete
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import relationship, sessionmaker

from .base import BaseModel


class Transactions(BaseModel):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    date = Column(Date)
    time = Column(Time)
    amount = Column(Float)
    description = Column(Text)
    category = Column(Text)
    bank_account = Column(Text)
    user = relationship('User')

    def __str__(self):
        return f'<User:{self.user_id}>'


# CREATE
async def import_transaction(
        user_id: int,
        date: dt,
        time: dt,
        amount: float,
        description: str,
        category: str,
        bank_account: str,
        session_maker: sessionmaker) -> None:
    async with session_maker() as session:
        async with session.begin():
            transaction = Transactions(
                user_id=user_id,
                date=date,
                time=time,
                amount=amount,
                description=description,
                category=category,
                bank_account=bank_account,
            )
            try:
                session.add(transaction)
                # TODO: log
            except ProgrammingError as error:
                # TODO: log
                print(error)


async def import_transactions(user_id: int, transactions: list, session_maker: sessionmaker) -> None:
    for transaction in transactions:
        await import_transaction(
            user_id=user_id,
            date=dt.datetime.strptime(transaction.get('Дата'), '%d/%m/%y'),
            time=dt.datetime.strptime(transaction.get('Время'), '%H:%M'),
            amount=transaction.get('Сумма'),
            description=transaction.get('Описание'),
            category=transaction.get('Категория'),
            bank_account=transaction.get('Счет'),
            session_maker=session_maker
        )


# READ
async def get_all_transactions(user_id: int, session_maker: sessionmaker) -> Transactions:
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                select(Transactions).where(Transactions.user_id == user_id)
            )
            return result.scalars()


async def get_transactions_filtered_by_datetime(user_id: int, session_maker: sessionmaker) -> Transactions:
    async with session_maker() as session:
        async with session.begin():
            datetime_now = dt.datetime.now()
            date_now = datetime_now.date()
            time_now = datetime_now.time()
            result = await session.execute(
                select(Transactions).filter(and_(
                    Transactions.user_id == user_id,
                    Transactions.date >= date_now,
                    Transactions.time >= time_now)
                )
            )
            return result.scalars()


async def get_one_transaction(user_id: int, transaction_id: int, session_maker: sessionmaker) -> Transactions:
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                select(Transactions).where(and_(
                    Transactions.user_id == user_id,
                    Transactions.id == transaction_id
                ))
            )
            return result.scalars().one()


# DELETE
async def delete_transaction(user_id: int, transaction_id: int, session_maker: sessionmaker) -> None:
    async with session_maker() as session:
        async with session.begin():
            await session.execute(delete(Transactions).filter_by(user_id=user_id, id=transaction_id))


async def delete_all_transaction(user_id: int, session_maker: sessionmaker) -> None:
    async with session_maker() as session:
        async with session.begin():
            await session.execute(delete(Transactions).where(Transactions.user_id == user_id))
