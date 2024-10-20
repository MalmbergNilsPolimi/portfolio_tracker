import yfinance as yf
from datetime import datetime, timedelta

def get_price_at(ticker, date_time):
    # Fetch historical data using yfinance
    date_str = date_time.strftime('%Y-%m-%d')
    data = yf.Ticker(ticker)
    hist = data.history(start=date_str, end=(date_time + timedelta(days=1)).strftime('%Y-%m-%d'), interval="1h")
    price = None
    if not hist.empty:
        hist = hist.reset_index()
        hist['Datetime'] = hist['Datetime'].dt.tz_localize(None)
        hist['TimeDiff'] = (hist['Datetime'] - date_time).abs()
        closest = hist.loc[hist['TimeDiff'].idxmin()]
        price = closest['Close']
    return price

def get_current_price(ticker):
    data = yf.Ticker(ticker)
    price = data.history(period='1d')['Close'].iloc[-1]
    return price