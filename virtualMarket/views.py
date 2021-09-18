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

    protfolios = StocksProtfolio.objects.filter(author = request.user)

    for p in protfolios:
        p.refreshData()

    return render(request, "virtualMarket.html", {"protfolios" : protfolios})




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

    if "id" in request.POST:
        id = request.POST["id"]

    if "name" in request.POST and "sum" in request.POST:
        id = newProtfolio(request)
        if id==-1:
            messages.info(request, 'The value most to be positive!')
            return redirect('createProtfolio')

    protfolio = StocksProtfolio.objects.filter(id = id)
    if not protfolio:
        messages.info(request, 'You need to choise protfolio!')
        return redirect('virtualMarket')
    protfolio = protfolio[0]
    if protfolio.author != request.user:
        return redirect('virtualMarket')

    if "act" in request.POST:
        if request.POST["act"]=="BUY":
            buyStock(request, protfolio)

        if request.POST["act"]=="SOLD":
            soldStock(request, protfolio)

        if request.POST["act"]=="DELETE":
            protfolio.delete()
            return redirect('virtualMarket')
    protfolio.refreshData()
    context = {}
    context["name"] = protfolio.name
    context["sum"] = protfolio.sum
    context["stocks"] = protfolio.getStocksList()
    context["value"] = protfolio.value
    context["changePer"] = protfolio.changePer
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

def buyStock(request, protfolio):
    #check evreything ok
    buyPrice = -1
    if request.POST['price']!='':
        buyPrice = float(request.POST["price"])
    s = StockTrade(symbol = str(request.POST["symbol"].upper()),
                   screener = str(request.POST["screener"]),
                   exchange = str(request.POST["exchange"]),
                   amount = int(request.POST["amount"]),
                   buyPrice = buyPrice,
                   profit = 0
                   )

    if not protfolio.addStock(s):
        messages.info(request, 'You need more money to buy this stock!')
    protfolio.save()

def soldStock(request, protfolio):
    soldPrice = -1
    if request.POST['price']!='':
        soldPrice = float(request.POST["price"])
    s = StockTrade(symbol = str(request.POST["symbol"]),
                   screener = str(request.POST["screener"]),
                   exchange = str(request.POST["exchange"]),
                   amount = int(request.POST["amount"])
                   )
    if not protfolio.removeStock(stock = s,price = soldPrice):
        messages.info(request, 'Some of the details is wrong!')
