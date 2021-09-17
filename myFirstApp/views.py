from django.shortcuts import render
from django.http import HttpResponse
from myFirstApp.stocks import get_data
import time
from .models import Stock
from .models import FollowStocks
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect



def search(request):
    if 'symbol' in request.GET and 'exchange' in request.GET:
        return render(request, 'search.html',{'symbol':request.GET['symbol'].upper(),
        'exchange':request.GET['exchange'].upper()})
    else:
        return render(request, 'search.html')

def addStocks(request):
    followLS = FollowStocks.objects.filter(author = request.user)
    if not followLS:
        followLS = FollowStocks(author = request.user)#create Follow list to the user
        followLS.save()
    else:
        followLS=followLS[0]

    stock = Stock(symbol = str(request.POST['symbol']).upper(),
    screener = str(request.POST['contry']).lower(),
    exchange = str(request.POST['exchange']).lower(),)

    if get_data(stock.symbol, stock.screener, stock.exchange, ["close"], '1d')=={}:
        messages.info(request, 'No such stock was found')
        return False


    stocks = followLS.getList()
    for s1 in stocks:
        if s1["symbol"]==stock.symbol and s1["screener"] == stock.screener and s1["exchange"] == stock.exchange:
            messages.info(request, "".join(['The stock ', stock.symbol ,' is already on the list!']))
            return True

    followLS.addToList(stock)
    return True




def liveStocks(request):
    if not request.user.is_authenticated:
        messages.info(request, 'You most to login first!')
        return redirect('login/')

    if 'symbol' in request.POST and 'contry' in request.POST and 'exchange' in request.POST:
        if not addStocks(request):
            return redirect('liveStocks')
        

    inducators = ["open",
      "change",
      "close",
      "high",
      "low",
      "volume"]

    followLS = FollowStocks.objects.filter(author = request.user)
    if not followLS:
        followLS = FollowStocks(author = request.user)#create Follow list to the user
        followLS.save()
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
            data["exchange"] = exchange
            ls.append(data)
        else:#not legal stock
            followLS.remove(stock)
    
    return render(request , 'liveStocks.html', {'stocks' : ls})
