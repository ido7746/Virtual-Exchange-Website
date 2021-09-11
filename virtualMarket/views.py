from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from .models import StocksProtfolio

def virtualMarket(request):
    if not request.user.is_authenticated:
        messages.info(request, 'You most to login first!')
        return redirect('login/')

    return render(request, "virtualMarket.html")

def createProtfolio(request):
    if not request.user.is_authenticated:
        messages.info(request, 'You most to login first!')
        return redirect('login/')

    return render(request, 'createProtfolio.html')

def protfolio(request):
    if not request.user.is_authenticated:
        messages.info(request, 'You most to login first!')
        return redirect('login/')

    if "name" in request.POST and "sum" in request.POST:
        id = newProtfolio(request)
        if id==-1:
            messages.info(request, 'The value most to be positive!')
            return redirect('createProtfolio')
    else:
        #take id from user
        print("..")


    #print all the page with protfolioID

    return render(request, 'protfolio.html')


def newProtfolio(request):
    context={}

    if int(request.POST["sum"])<=0:
        return -1
    newPro = StocksProtfolio(sum = int(request.POST["sum"]),
                           name =   str(request.POST["name"]),
                           author = request.user
        )
    newPro.save()

    return newPro.id


