import os
from datetime import datetime
from portfolio_tracker.database import get_engine, get_session
from portfolio_tracker.models import TransactionModel
from portfolio_tracker.finance_data import get_price_at, get_current_price, get_ticker_from_input
from portfolio_tracker.utils import generate_transaction_id

class PortfolioTracker:
    def __init__(self, portfolio_name):
        self.portfolio_name = portfolio_name
        db_filename = f"{portfolio_name}.db"
        db_path = f"sqlite:///data/{db_filename}"
        self.engine = get_engine(db_path)
        self.session = get_session(self.engine)

    def add_transaction(self, date_time, input_ticker_or_isin, amount):
        # Vérifier que le montant est strictement positif
        if amount <= 0:
            raise ValueError("The amount invested must be strictly positive.")
        
        ticker = get_ticker_from_input(input_ticker_or_isin)
        if not ticker:
            raise ValueError("Ticker or ISIN not found.")
        price = get_price_at(ticker, date_time)
        if price is None:
            raise ValueError("Price data not available for the given date and time.")
        transaction_id = generate_transaction_id(ticker, date_time.date())
        transaction = TransactionModel(
            transaction_id=transaction_id,
            date=date_time,
            ticker=ticker,
            amount=amount,
            price=price
        )
        self.session.add(transaction)
        self.session.commit()
        return transaction

    def get_transactions(self):
        return self.session.query(TransactionModel).all()

    def calculate_portfolio_performance(self):
        transactions = self.get_transactions()
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

    def delete_transaction(self, transaction_id):
        transaction = self.session.query(TransactionModel).filter_by(transaction_id=transaction_id).first()
        if transaction:
            self.session.delete(transaction)
            self.session.commit()
            return True
        else:
            return False

    def delete_portfolio(self):
        # Fermer la session et l'engine
        self.session.close()
        self.engine.dispose()

        # Supprimer les références
        del self.session
        del self.engine

        # Forcer le garbage collector
        import gc
        gc.collect()

        # Supprimer le fichier de base de données
        db_filename = f"{self.portfolio_name}.db"
        db_path = os.path.join('data', db_filename)

        if os.path.exists(db_path):
            try:
                os.remove(db_path)
                return True
            except Exception as e:
                print(f"Erreur lors de la suppression du fichier de base de données : {e}")
                return False
        else:
            print("Le fichier de base de données n'existe pas.")
            return False



    def close(self):
        self.session.close()
        self.engine.dispose()