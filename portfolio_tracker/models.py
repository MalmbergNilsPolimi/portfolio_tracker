from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class PortfolioModel(Base):
    __tablename__ = 'portfolios'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    transactions = relationship('TransactionModel', back_populates='portfolio')

class TransactionModel(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    transaction_id = Column(String, unique=True)
    date = Column(DateTime)
    ticker = Column(String)
    amount = Column(Float)
    price = Column(Float)
    portfolio_id = Column(Integer, ForeignKey('portfolios.id'))
    portfolio = relationship('PortfolioModel', back_populates='transactions')