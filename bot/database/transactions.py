from sqlalchemy import Column, Integer, TEXT, DATE, TIME, BOOLEAN, ForeignKey, FLOAT
from sqlalchemy.orm import relationship

from .base import BaseModel


class Transactions(BaseModel):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    date = Column(DATE)
    time = Column(TIME)
    amount = Column(FLOAT)
    description = Column(TEXT)
    category = Column(TEXT)
    bank_account = Column(TEXT)
    transaction_status = Column(BOOLEAN)
    user = relationship('User')

    def __str__(self):
        return f'<User:{self.user_id}>'
