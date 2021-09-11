from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from .models import StocksProtfolio
from .models import StockTrade
import json

def virtualMarket(request):
    if not request.user.is_authenticated:
        messages.info(request, 'You most to login first!')
        return redirect('login/')

    p = StocksProtfolio.objects.filter(author = request.user)


    return render(request, "virtualMarket.html", {"protfolios" : p})

def createProtfolio(request):
    if not request.user.is_authenticated:
        messages.info(request, 'You most to login first!')
        return redirect('login/')

    return render(request, 'createProtfolio.html')

def protfolio(request):
    id = -2
    if not request.user.is_authenticated:
        messages.info(request, 'You most to login first!')
        return redirect('login/')

    if "act" in request.POST:
        if request.POST["act"]=="BUY":
            buyStock(request)
        if request.POST["act"]=="SOLD":
            #soldStock(request)
            pass

    if "name" in request.POST and "sum" in request.POST:
        id = newProtfolio(request)
        if id==-1:
            messages.info(request, 'The value most to be positive!')
            return redirect('createProtfolio')
    elif "id" in request.POST:
        id = request.POST["id"]


    protfolio = StocksProtfolio.objects.filter(id = id)
    if not protfolio:
        messages.info(request, 'You need to choise protfolio!')
        return redirect('virtualMarket')
    protfolio = protfolio[0]

    context = {}
    context["name"] = protfolio.name
    context["sum"] = protfolio.sum
    context["stocks"] = protfolio.getStocksList()
    context["id"] = id


    return render(request, 'protfolio.html', context)


def newProtfolio(request):
    context={}

    if float(request.POST["sum"])<=0:
        return -1
    newPro = StocksProtfolio(sum = float(request.POST["sum"]),
                           name =   str(request.POST["name"]),
                           author = request.user
        )
    newPro.save()

    return newPro.id

def buyStock(request):
    #check evreything ok
    buyPrice = -1
    if request.POST['buyPrice']!='':
        buyPrice = float(request.POST["buyPrice"])
    s = StockTrade(symbol = str(request.POST["symbol"]),
                   screener = str(request.POST["screener"]),
                   exchange = str(request.POST["exchange"]),
                   amount = int(request.POST["amount"]),
                   buyPrice = buyPrice
                   )
    protfolio = StocksProtfolio.objects.filter(id = str(request.POST["id"]))
    if not protfolio:
        print("empty protfolio")
        return
    protfolio = protfolio[0]
    protfolio.addStock(s)
    protfolio.save()


