
import yfinance as yf
from datetime import datetime

#import your tickers
def read_ticker_file(text):
 with open(text, 'r') as file:
    data = file.read().splitlines()
    return data

def get_stock_info(tickers):
    data = {}
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1y")
        current_price = hist["Close"][-1]
        low_52_week = min(hist["Low"])
        high_52_week = hist['High'].max()
        data[ticker] = (current_price, low_52_week, high_52_week)
    return data

from datetime import datetime

def get_closest_prices(stocks):
    # calculate the difference between current price and high/low
    diff_high = {key: abs(value[0] / value[2]) for key, value in stocks.items()}

    # sort the dictionary by the difference to high and low, get top 20
    closest_to_high = sorted(diff_high.items(), key=lambda x: x[1])[:10]
    # prepare the content to write into the text file
    content = "Best Buys:\n"
    content += "\n".join([f"{x[0]} - C: {round(stocks[x[0]][0], 2)}, 52H: {round(stocks[x[0]][2], 2)}, discount: {round(1 - (stocks[x[0]][0] / stocks[x[0]][2]), 2)}%" for x in closest_to_high])

    print(content)
    # write the content into a text file
    current_date = datetime.now().strftime('%Y-%m-%d')
    with open(f'stock_prices_{current_date}.txt', 'w') as f:
        f.write(content)

tickers = read_ticker_file("t.txt")
stocks = get_stock_info(tickers)
get_closest_prices(stocks)
