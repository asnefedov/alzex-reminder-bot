from sqlalchemy import Column, Integer, TEXT, DATE, TIME, BOOLEAN

from .base import BaseModel


class Transactions(BaseModel):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    date = Column(DATE)
    time = Column(TIME)
    description = Column(TEXT)
    category = Column(TEXT)
    bank_account = Column(TEXT)
    transaction_status = Column(BOOLEAN)

    def __str__(self):
        return f'<User:{self.user_id}>'
