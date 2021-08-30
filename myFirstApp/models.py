from django.db import models

import requests, json, warnings, time




def data1(symbols, interval, indicators):
    """Format TradingView's Scanner Post Data
    Args:
        symbols (list): List of EXCHANGE:SYMBOL (ex: ["NASDAQ:AAPL"] or ["BINANCE:BTCUSDT"])
        interval (string): Time Interval (ex: 1m, 5m, 15m, 1h, 4h, 1d, 1W, 1M)
    Returns:
        string: JSON object as a string.
    """
    if interval == "1m":
        # 1 Minute
        data_interval = "|1"
    elif interval == "5m":
        # 5 Minutes
        data_interval = "|5"
    elif interval == "15m":
        # 15 Minutes
        data_interval = "|15"
    elif interval == "1h":
        # 1 Hour
        data_interval = "|60"
    elif interval == "4h":
        # 4 Hour
        data_interval = "|240"
    elif interval == "1W":
        # 1 Week
        data_interval = "|1W"
    elif interval == "1M":
        # 1 Month
        data_interval = "|1M"
    else:
        if interval != '1d':
            warnings.warn("Interval is empty or not valid, defaulting to 1 day.")
        # Default, 1 Day
        data_interval = ""

    data_json = {"symbols": {"tickers": [symbol.upper() for symbol in symbols], "query": {"types": []}},
                 "columns": [x + data_interval for x in indicators]}

    return data_json


def get_data(symbol, screener, exchange, indicators, interval):

    __version__ = "3.2.7"
    scan_url = "https://scanner.tradingview.com/"
    timeout = None

    exchange_symbol = f"{exchange}:{symbol}"
    data = data1([exchange_symbol], interval, indicators)
    scan_url = f"{scan_url}{screener.lower()}/scan"
    headers = {"User-Agent": "TradeBot/"}
    response = requests.post(scan_url,json=data, headers=headers, timeout=timeout)
    if response.status_code!=200:
        print(response.text)
        print("bad requestes")
        return {}

    result = json.loads(response.text)["data"]
    if result==[]:
        print("empty result")
        return {}

    data = {}
    i=0

    for indicatoe in indicators:
        data[indicatoe] = result[0]['d'][i]
        i+=1
    data["curr"] = data["open"]*(100+data["change"])/100
    data["name"] = symbol

    return data

def start():
    inducators = ["open",
      "change",
      "close",
      "high",
      "low",
      "volume"]
    data = []

    stocks = [("FTAL", "israel", "TASE", inducators, "1d"),
              ("AZRG", "israel", "TASE", inducators, "1d"),
              ("btcusd", "crypto", "bitstamp", inducators, "1d")]


    while True:
        for stock in stocks:
            data = get_data(stock[0],stock[1],stock[2],stock[3],stock[4])
            if data !={}:
                print(stock[0],">>>"

                      , data["curr"] )
        #time.sleep(1)


# Create your models here.
