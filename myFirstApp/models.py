from django.db import models
import requests, json, warnings, time
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Stock(models.Model):
    symbol = models.CharField(max_length=10)
    screener = models.CharField(max_length=10)
    exchange = models.CharField(max_length=10)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.symbol


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

    data["symbol"] = symbol.upper()

    return data
