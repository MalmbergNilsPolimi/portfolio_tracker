from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class TransactionModel(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    transaction_id = Column(String, unique=True)
    date = Column(DateTime)
    ticker = Column(String)
    amount = Column(Float)
    price = Column(Float)