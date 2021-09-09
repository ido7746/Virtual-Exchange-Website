from django.shortcuts import render
from django.http import HttpResponse
from myFirstApp.models import get_data
import time
from .models import Stock
from django.contrib.auth.models import User





def search(request):
    if not 'symbol' in request.GET:
        return render(request, "home.html")
    stock = Stock(symbol = str(request.GET['symbol']).upper(),
    screener = str(request.GET['contry']).lower(),
    exchange = str(request.GET['exchange']).lower(),
    author = request.user )
    stocks = Stock.objects.filter(author = request.user)
    for s1 in stocks:
        if s1.symbol==stock.symbol and s1.screener == stock.screener and s1.exchange == stock.exchange:
            return render(request, "home.html")
    stock.save()
    return render(request, "home.html")




def liveStocks(request):
    inducators = ["open",
      "change",
      "close",
      "high",
      "low",
      "volume"]

    stocks = Stock.objects.filter(author = request.user)

    
    
    ls = []

    for stock in stocks:
        symbol = stock.symbol
        contry = stock.screener
        exchange = stock.exchange
        data = get_data(symbol, contry, exchange, inducators, "1d")
        if data != {}:
            if(data["change"]<0):
                data["colorChange"] = "red"
            if(data["change"]>0):
                data["colorChange"] = "green"
            ls.append(data)
    
    return render(request , 'liveStocks.html', {'stocks' : ls})
