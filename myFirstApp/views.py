from django.shortcuts import render
from django.http import HttpResponse
from myFirstApp.stocks import get_data
import time
from .models import Stock
from .models import FollowStocks
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect



def addStocks(request):
    if not request.user.is_authenticated:
        messages.info(request, 'You most to login first!')
        return redirect('login/')

    if not 'symbol' in request.POST:
        return render(request, "addStocks.html")

    followLS = FollowStocks.objects.filter(author = request.user)
    if not followLS:
        followLS = FollowStocks(author = request.user)
        followLS.save()
    else:
        followLS=followLS[0]

    stock = Stock(symbol = str(request.POST['symbol']).upper(),
    screener = str(request.POST['contry']).lower(),
    exchange = str(request.POST['exchange']).lower(),)

    print(str(request.POST['symbol']) , str(request.POST['contry']), str(request.POST['exchange']))

    stocks = followLS.getList()
    for s1 in stocks:
        if s1["symbol"]==stock.symbol and s1["screener"] == stock.screener and s1["exchange"] == stock.exchange:
            return redirect('liveStocks')

    followLS.addToList(stock)
    return redirect('liveStocks')




def liveStocks(request):
    if not request.user.is_authenticated:
        messages.info(request, 'You most to login first!')
        return redirect('login/')

    inducators = ["open",
      "change",
      "close",
      "high",
      "low",
      "volume"]

    followLS = FollowStocks.objects.filter(author = request.user)
    if not followLS:
        messages.info(request, 'You most to add stocks first!')
        return redirect('addStocks')
    else:
        followLS=followLS[0]

    stocks = followLS.getList()

    ls = []

    for stock in stocks:
        symbol = stock["symbol"]
        contry = stock["screener"]
        exchange = stock["exchange"]
        data = get_data(symbol, contry, exchange, inducators, "1d")
        if data != {}:
            if(data["change"]<0):
                data["colorChange"] = "red"
            if(data["change"]>0):
                data["colorChange"] = "green"
            ls.append(data)
    
    return render(request , 'liveStocks.html', {'stocks' : ls})
