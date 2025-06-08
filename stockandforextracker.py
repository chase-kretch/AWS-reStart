
### Simple stock market and forex checker using Alpha Vantage API
### By Chase Kretschmar

import requests
from datetime import datetime, timezone, date
import asyncio
import json

# with open("data.json", "r") as f:
#    gainers = json.load(f)
# I used this to test without overusing my api key

api_key = "" ## Yes I know you should not have your API key on github haha
# Rate limit is only 25 requests per day

class myAlphaVAPI:
    def __init__(self, api_key):
        self.url = f"https://www.alphavantage.co/query"
        self.api_key = api_key

    def getForex(self, currFrom, currTo):

        params = {
            'function': 'CURRENCY_EXCHANGE_RATE',
            'from_currency': currFrom,
            'to_currency': currTo,
            'apikey': api_key,

        }

        response = requests.get(self.url, params=params)
        data = response.json()

        exchange_data = data['Realtime Currency Exchange Rate']
        from_curr = exchange_data['1. From_Currency Code']
        to_curr = exchange_data['3. To_Currency Code']
        rate = exchange_data['5. Exchange Rate']
        last_updated = exchange_data['6. Last Refreshed']


        print(f"\n{from_curr} → {to_curr}")
        print(f"Rate: {float(rate):.4f}")
        print(f"Last Updated: {last_updated}")
        main()

    def getDailyStockValue(self, symbol):
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': symbol,
            'apikey': self.api_key,
        }
        response = requests.get(self.url, params=params)
        data = response.json()
        tsd = data['Time Series (Daily)']
        most_recent_date = list(tsd.keys())[0]
        daily_data = tsd[most_recent_date]
        print(f"\nStock Data for {symbol} for {most_recent_date}\n")
        open_price = float(daily_data['1. open'])
        high_price = float(daily_data['2. high'])
        low_price = float(daily_data['3. low'])
        close_price = float(daily_data['4. close'])
        volume = int(daily_data['5. volume'])

        print(f"Open: ${open_price:.2f}")
        print(f"High: ${high_price:.2f}")
        print(f"Low: ${low_price:.2f}")
        print(f"Close: ${close_price:.2f}")
        print(f"Volume: {volume:,}")

    def getTopGainersAndLosers(self):
        params = {
            'function': 'TOP_GAINERS_LOSERS',
            'apikey': self.api_key,
        }
        response = requests.get(self.url, params=params)
        data = response.json()
        print("\nTop Gainers")
        print("=========================================")
        for stock in data['top_gainers']:
            print(
                f"Ticker: {stock['ticker']}, Price: {stock['price']}, Change: {stock['change_percentage']}, Volume: {stock['volume']}")
        print("=========================================\n")
        print("Top Losers")
        for stock in data['top_losers']:
            print(
                f"Ticker: {stock['ticker']}, Price: {stock['price']}, Change: {stock['change_percentage']}, Volume: {stock['volume']}")
def main():
    API = myAlphaVAPI(api_key)
    while True:

        print("\n=================================")
        print("Stocks and Forex using AlphaVantage API")
        print("=================================\n")
        function = input("Please enter the number of what you would like to do:"
                         "\n1: Exit"
                         "\n2: Foreign Exchange"
                         "\n3: Daily Stock Value"
                         "\n4: Top Gainers and Losers\n")
        if function == "1":
            print("Exiting...")

            exit()
        if function == "2":
            currFrom = input("Please enter the first currency e.g USD: ")
            currTo = input("Please enter the second currency e.g NZD: ")
            API.getForex(currFrom, currTo)
        if function == "3":
            symbol = input("Please enter the stock symbol e.g IBM: ")
            API.getDailyStockValue(symbol)
        if function == "4":
            API.getTopGainersAndLosers()


if __name__ == "__main__":
    main()
