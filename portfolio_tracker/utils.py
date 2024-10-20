import uuid

def generate_transaction_id(ticker, date):
    return f"{ticker}-{date.strftime('%Y%m%d')}-{uuid.uuid4().hex[:6]}"