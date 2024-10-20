# Portfolio Tracker

Portfolio Tracker is a Python-based module designed to help you manage and track your investments in ETFs, stocks, and cryptocurrencies. The tool provides a detailed transaction history, real-time portfolio updates, and calculates gains and losses for each investment. It includes an intuitive graphical interface built using Streamlit, making it easy to monitor the performance of your portfolio over time.

## Features

- **Transaction Tracking**: 
  - Add and manage transactions with details like date, time, asset ticker/ISIN, and investment amount.
  - Automatically fetch the historical price of assets at the time of the transaction using Yahoo Finance.
  
- **Real-Time Portfolio Updates**: 
  - View the current status of your portfolio, including the total invested amount and gains/losses per asset.
  - Track each transaction's performance and cumulative gains/losses across all transactions for the same asset.

- **Database Management**: 
  - Store all transaction data in an integrated SQLite database.
  - Import/export transaction data in CSV format.
  - Manage multiple portfolios separately within the application.

- **Intuitive Interface**:
  - An easy-to-use Streamlit interface for adding, viewing, and managing your portfolios and transactions.
  - Visualize the performance of your portfolio in real-time.

## Project Structure

```
portfolio_tracker/
│   .gitignore
│   README.md
│   requirements.txt
│   streamlit_app.py
│
├── data/
│   └── Portfolio databases (*.db)
│
└── portfolio_tracker/
    ├── database.py
    ├── finance_data.py
    ├── main.py
    ├── models.py
    ├── utils.py
    └── __init__.py
```

- **`streamlit_app.py`**: The main file that runs the Streamlit application, providing the user interface.
- **`portfolio_tracker/database.py`**: Handles database connections and setup using SQLAlchemy.
- **`portfolio_tracker/finance_data.py`**: Fetches financial data from Yahoo Finance.
- **`portfolio_tracker/main.py`**: The core logic for managing portfolios and transactions.
- **`portfolio_tracker/models.py`**: Defines the SQLAlchemy models for the database.
- **`portfolio_tracker/utils.py`**: Provides utility functions like generating unique transaction IDs.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/MalmbergNilsPolimi/portfolio_tracker.git
   cd portfolio_tracker
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit application:

   ```bash
   python streamlit_app.py
   ```

## Usage

### 1. Create a Portfolio
- Enter a name for your portfolio in the Streamlit sidebar and click "Create New Portfolio".
  
### 2. Add Transactions
- Enter the date, time, ticker (or ISIN), and the amount for each transaction. The system will automatically fetch the price at the specified date and time.

### 3. View Portfolio
- Once transactions are added, view the real-time value of your portfolio, including the gain/loss for each transaction.

### 4. Delete Transactions/Portfolios
- Manage your portfolio by removing transactions or entire portfolios from the interface.

## Requirements

- Python 3.7 or higher
- Streamlit
- yfinance
- YahooQuery
- SQLAlchemy

For a complete list of dependencies, refer to `requirements.txt`.

## Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue if you have suggestions or find bugs.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- This project makes use of the [Yahoo Finance](https://pypi.org/project/yfinance/) and [YahooQuery](https://pypi.org/project/yahooquery/) APIs for fetching financial data.