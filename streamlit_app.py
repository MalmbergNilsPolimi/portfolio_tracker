import streamlit as st
from datetime import datetime, time as time_obj
from portfolio_tracker.main import PortfolioTracker
from portfolio_tracker.finance_data import get_current_price

def main():
    st.title("Portfolio Tracker")
    tracker = PortfolioTracker()
    
    # Portfolio Selection
    st.sidebar.header("Portfolio Selection")
    portfolio_name = st.sidebar.text_input("Portfolio Name", value="Default Portfolio")
    if st.sidebar.button("Create Portfolio"):
        tracker.create_portfolio(portfolio_name)
        st.sidebar.success(f"Portfolio '{portfolio_name}' created.")

    st.header(f"Portfolio: {portfolio_name}")
    
    # Add Transaction
    st.subheader("Add Transaction")
    with st.form("add_transaction"):
        date = st.date_input("Date", value=datetime.now().date())
        time_input = st.time_input("Time", value=datetime.now().time())
        ticker = st.text_input("Ticker/ISIN")
        amount = st.number_input("Amount Invested", min_value=0.0, format="%.2f")
        submit = st.form_submit_button("Add Transaction")
        if submit:
            date_time = datetime.combine(date, time_input)
            try:
                transaction = tracker.add_transaction(portfolio_name, date_time, ticker, amount)
                st.success(f"Transaction {transaction.transaction_id} added.")
            except ValueError as e:
                st.error(str(e))

    # Portfolio Performance
    st.subheader("Portfolio Performance")
    performance = tracker.calculate_portfolio_performance(portfolio_name)
    if performance:
        st.write(f"**Total Invested:** ${performance['total_invested']:.2f}")
        st.write(f"**Current Value:** ${performance['current_value']:.2f}")
        st.write(f"**Gain/Loss (%):** {performance['gain_loss_percent']:.2f}%")
    
    # Transactions Table
    st.subheader("Transactions")
    transactions = tracker.get_transactions(portfolio_name)
    if transactions:
        data = []
        for t in transactions:
            current_price = get_current_price(t.ticker)
            gain_loss = ((current_price - t.price) / t.price * 100) if t.price else 0
            data.append({
                'Transaction ID': t.transaction_id,
                'Date': t.date.strftime("%Y-%m-%d %H:%M"),
                'Ticker/ISIN': t.ticker,
                'Amount Invested': f"${t.amount:.2f}",
                'Price at Purchase': f"${t.price:.2f}",
                'Current Price': f"${current_price:.2f}",
                'Gain/Loss (%)': f"{gain_loss:.2f}%"
            })
        st.table(data)
    else:
        st.write("No transactions found.")

if __name__ == '__main__':
    import subprocess
    import sys
    import os

    # Check if the script is being run directly or by Streamlit
    if os.getenv('IS_RUNNING_STREAMLIT') == 'true':
        main()
    else:
        # Set an environment variable to prevent recursion
        os.environ['IS_RUNNING_STREAMLIT'] = 'true'
        # Run Streamlit with the current script
        subprocess.run([sys.executable, '-m', 'streamlit', 'run', sys.argv[0]])