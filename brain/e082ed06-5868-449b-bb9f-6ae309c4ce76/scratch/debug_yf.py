import yfinance as yf
import datetime

TICKERS = ["V", "JNJ", "WMT", "PG", "MA"]
data = yf.download(TICKERS, period="5d", interval="1d", group_by='ticker', progress=False)
print("Data columns:", data.columns)
print("Data head:\n", data.head())

for ticker in TICKERS:
    ticker_data = data[ticker]
    print(f"\n{ticker} data length: {len(ticker_data)}")
    if len(ticker_data) >= 2:
        last_close = ticker_data['Close'].iloc[-1]
        prev_close = ticker_data['Close'].iloc[-2]
        print(f"{ticker}: Prev={prev_close}, Last={last_close}")
    else:
        print(f"{ticker}: Not enough data")
