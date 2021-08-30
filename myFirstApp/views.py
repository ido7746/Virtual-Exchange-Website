from django.shortcuts import render
from django.http import HttpResponse
from myFirstApp.models import get_data
import time



def home(request):
    return render(request, "home.html")


def say_hello(request):
    inducators = ["open",
      "change",
      "close",
      "high",
      "low",
      "volume"]

    symbol = str(request.GET['symbol'])
    contry = str(request.GET['contry'])
    exchange = str(request.GET['exchange'])

    data = get_data(symbol, contry, exchange, inducators, "1d")
    
    
    if(data["change"]<0):
        data["colorChange"] = "red"
    if(data["change"]>0):
        data["colorChange"] = "green"


    return render(request , 'liveStocks.html', data)
