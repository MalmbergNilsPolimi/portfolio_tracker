# Portfolio Tracker

Portfolio Tracker is a Python module to manage your investment portfolio in stocks, ETFs, and cryptocurrencies. It allows you to track your investments, calculate gains and losses, and visualize your portfolio performance with a clean and professional interface using Streamlit.

## Features

- **Transaction Tracking**: Input transactions with date, time, ISIN or ticker, and amount. The module updates your portfolio by fetching the necessary data (product price at the date and time of purchase) using Yahoo Finance tools.

- **Real-time Updates**: Visualize your portfolio at any time, see the list of transactions (with invested amount and percentage gain/loss since investment), the total amount invested in each ISIN (with total gain/loss).

- **Gain/Loss Calculation per Transaction**: For multiple transactions on the same asset at different dates, the module calculates the total invested and cumulative gains/losses. It also indicates the gains/losses associated with each specific transaction. Each transaction has a unique identifier for easy retrieval.

- **Integrated Database**: Includes a database to store all information, with the ability to export and import data in .csv files. Manage one or more portfolios separately.

- **Graphical Interface**: An intuitive interface using Streamlit to follow your portfolio performance.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/portfolio_tracker.git

## Usage

### Running the Streamlit App

You can now start the Streamlit interface by simply running:

```bash
python streamlit_app.py
