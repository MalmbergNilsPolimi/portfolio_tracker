from datetime import datetime
from .database import get_engine, get_session
from .models import PortfolioModel, TransactionModel
from .finance_data import get_price_at, get_current_price
from .utils import generate_transaction_id

class PortfolioTracker:
    def __init__(self, db_path='sqlite:///data/portfolios.db'):
        self.engine = get_engine(db_path)
        self.session = get_session(self.engine)

    def create_portfolio(self, name):
        portfolio = PortfolioModel(name=name)
        self.session.add(portfolio)
        self.session.commit()
        return portfolio

    def get_portfolio(self, name):
        return self.session.query(PortfolioModel).filter_by(name=name).first()

    def add_transaction(self, portfolio_name, date_time, ticker, amount):
        portfolio = self.get_portfolio(portfolio_name)
        if not portfolio:
            portfolio = self.create_portfolio(portfolio_name)
        
        price = get_price_at(ticker, date_time)
        if price is None:
            raise ValueError("Price data not available for the given date and time.")
        
        transaction_id = generate_transaction_id(ticker, date_time.date())
        transaction = TransactionModel(
            transaction_id=transaction_id,
            date=date_time,
            ticker=ticker,
            amount=amount,
            price=price,
            portfolio=portfolio
        )
        self.session.add(transaction)
        self.session.commit()
        return transaction

    def get_transactions(self, portfolio_name):
        portfolio = self.get_portfolio(portfolio_name)
        if not portfolio:
            return []
        return portfolio.transactions

    def calculate_portfolio_performance(self, portfolio_name):
        transactions = self.get_transactions(portfolio_name)
        total_invested = sum(t.amount for t in transactions)
        current_value = 0
        for t in transactions:
            current_price = get_current_price(t.ticker)
            current_value += (t.amount / t.price) * current_price
        gain_loss = ((current_value - total_invested) / total_invested * 100) if total_invested > 0 else 0
        return {
            'total_invested': total_invested,
            'current_value': current_value,
            'gain_loss_percent': gain_loss
        }