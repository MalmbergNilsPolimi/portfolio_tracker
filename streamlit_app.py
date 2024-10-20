import streamlit as st
from datetime import datetime, time as time_obj
from portfolio_tracker.main import PortfolioTracker
from portfolio_tracker.finance_data import get_current_price
import os

def get_existing_portfolios():
    data_dir = 'data/'
    portfolios = []
    if os.path.exists(data_dir):
        files = os.listdir(data_dir)
        for file in files:
            if file.endswith('.db'):
                portfolio_name = file[:-3]  # Remove .db extension
                portfolios.append(portfolio_name)
    return portfolios

def main():
    st.title("Portfolio Tracker")

    # Initialize session state
    if 'selected_portfolio' not in st.session_state:
        st.session_state.selected_portfolio = None

    # Sidebar for portfolio selection
    st.sidebar.header("Portfolio Selection")

    # Handle new portfolio creation BEFORE the selectbox
    new_portfolio_name = st.sidebar.text_input("New Portfolio Name")
    if st.sidebar.button("Create New Portfolio"):
        if new_portfolio_name:
            existing_portfolios = get_existing_portfolios()
            if new_portfolio_name in existing_portfolios:
                st.sidebar.error("Portfolio already exists.")
            else:
                # Create the new portfolio by initializing it
                tracker = PortfolioTracker(new_portfolio_name)
                tracker.close()  # Close any connections
                # Set the selected portfolio BEFORE the selectbox is instantiated
                st.session_state.selected_portfolio = new_portfolio_name
                st.sidebar.success(f"Portfolio '{new_portfolio_name}' created.")
                st.rerun()  # Force rerun to update the selectbox with the new portfolio
        else:
            st.sidebar.error("Please enter a portfolio name.")

    # Now get the updated list of existing portfolios
    existing_portfolios = get_existing_portfolios()

    # Check if the selected portfolio still exists
    if st.session_state.selected_portfolio not in existing_portfolios:
        st.session_state.selected_portfolio = None

    # Check if there are any portfolios
    if existing_portfolios:
        # Determine the index of the selected portfolio
        if st.session_state.selected_portfolio in existing_portfolios:
            selected_index = existing_portfolios.index(st.session_state.selected_portfolio)
        else:
            selected_index = 0
            st.session_state.selected_portfolio = existing_portfolios[0]

        # Portfolio Selection
        selected_portfolio = st.sidebar.selectbox(
            "Select Portfolio",
            options=existing_portfolios,
            index=selected_index,
            key='selected_portfolio'
        )
        # No need to assign st.session_state.selected_portfolio here; the selectbox handles it
    else:
        st.sidebar.write("No portfolios available. Please create a new portfolio.")
        return

    # Check if a portfolio is selected
    if not st.session_state.selected_portfolio:
        st.info("Please select or create a portfolio from the sidebar.")
        return

    selected_portfolio = st.session_state.selected_portfolio
    tracker = PortfolioTracker(selected_portfolio)
    st.header(f"Portfolio: {selected_portfolio}")

    # Add Transaction
    st.subheader("Add Transaction")
    with st.form("add_transaction"):
        date = st.date_input("Date", value=datetime.now().date())
        time_input = st.time_input("Time", value=datetime.now().time())
        ticker_or_isin = st.text_input("Ticker/ISIN")
        amount = st.number_input("Amount Invested", min_value=0.01, format="%.2f")  # Montant minimal mis à jour
        submit = st.form_submit_button("Add Transaction")
        if submit:
            date_time = datetime.combine(date, time_input)
            try:
                transaction = tracker.add_transaction(date_time, ticker_or_isin, amount)
                st.success(f"Transaction {transaction.transaction_id} added.")
            except ValueError as e:
                st.error(str(e))

    # Portfolio Performance
    st.subheader("Portfolio Performance")
    performance = tracker.calculate_portfolio_performance()
    if performance:
        st.write(f"**Total Invested:** ${performance['total_invested']:.2f}")
        st.write(f"**Current Value:** ${performance['current_value']:.2f}")
        st.write(f"**Gain/Loss (%):** {performance['gain_loss_percent']:.2f}%")

    # Transactions Table
    st.subheader("Transactions")
    transactions = tracker.get_transactions()
    if transactions:
        # Display transactions and provide options to delete them
        data = []
        transaction_ids = []
        for t in transactions:
            current_price = get_current_price(t.ticker)
            gain_loss = ((current_price - t.price) / t.price * 100) if t.price else 0
            data.append({
                'Transaction ID': t.transaction_id,
                'Date': t.date.strftime("%Y-%m-%d %H:%M"),
                'Ticker': t.ticker,
                'Amount Invested': f"${t.amount:.2f}",
                'Price at Purchase': f"${t.price:.2f}",
                'Current Price': f"${current_price:.2f}",
                'Gain/Loss (%)': f"{gain_loss:.2f}%"
            })
            transaction_ids.append(t.transaction_id)
        st.table(data)

        st.subheader("Delete Transactions")
        selected_transactions = st.multiselect("Select Transactions to Delete", options=transaction_ids)
        if st.button("Delete Selected Transactions"):
            if selected_transactions:
                for trans_id in selected_transactions:
                    tracker.delete_transaction(trans_id)
                st.success(f"Deleted transactions: {', '.join(selected_transactions)}")
                st.rerun()
            else:
                st.warning("No transactions selected for deletion.")
    else:
        st.write("No transactions found.")

    # Delete Portfolio
    st.subheader("Delete Portfolio")
    with st.form("delete_portfolio_form"):
        confirm_delete = st.checkbox("Confirm Delete Portfolio", key='confirm_delete_portfolio_main')
        delete_portfolio_button = st.form_submit_button("Delete Portfolio")
        if delete_portfolio_button:
            if confirm_delete:
                tracker = PortfolioTracker(st.session_state.selected_portfolio)
                success = tracker.delete_portfolio()
                del tracker
                if success:
                    st.success(f"Portfolio '{st.session_state.selected_portfolio}' deleted.")
                    st.rerun()
                else:
                    st.error("Failed to delete the portfolio.")
            else:
                st.warning("Please confirm deletion by checking the box.")


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