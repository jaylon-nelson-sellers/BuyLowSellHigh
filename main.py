!pip install yfinance
import yfinance as yf
from datetime import datetime
tickers = read_ticker_file("t.txt")
stocks = get_stock_info(tickers)
get_closest_prices(stocks)

from array import array
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

def get_closest_prices(stocks):
    # calculate the difference between current price and high/low
    diff_high = {key: round(abs(value[0] - value[2]), 2) for key, value in stocks.items()}
    diff_low = {key: round(abs(value[0] - value[1]), 2) for key, value in stocks.items()}

    # sort the dictionary by the difference to high and low, get top 10
    closest_to_high = sorted(diff_high.items(), key=lambda x: x[1])[:10]
    closest_to_low = sorted(diff_low.items(), key=lambda x: x[1])[:10]

    # prepare the content to write into the text file
    content = "Best Sells:\n"
    content += "\n".join([f"{x[0]} - C: {round(stocks[x[0]][0], 2)}, 52H: {round(stocks[x[0]][2], 2)}, dif: {round(stocks[x[0]][0]- stocks[x[0]][2], 2)}" for x in closest_to_high])

    content += "\n\n Best Buys:\n"
    content += "\n".join([f"{x[0]} - C: {round(stocks[x[0]][0], 2)}, 52L: {round(stocks[x[0]][1], 2)}, dif: {round(stocks[x[0]][0] -stocks[x[0]][1], 2)}"  for x in closest_to_low])

    # write the content into a text file
    current_date = datetime.now().strftime('%Y-%m-%d')
    with open(f'stock_prices_{current_date}.txt', 'w') as f:
        f.write(content)