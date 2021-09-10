from django.db import models
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import json
from myFirstApp.stocks import get_data
import datetime

class StocksProtfolio(models.Model):
    sum = models.FloatField()
    name = models.CharField(max_length=30)
    listOfStock = models.CharField(max_length=2000000, default = '[]')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def addStock(self, symbol, screener, exchange, amount, price=-1):#amount: number of stocks to buy
        if price==-1:
            data = get_data(symbol, screener, exchange, ["close"], '1d')
            if amount<=0 or data == {}:
                return
            price = data['close']

        price = price*amount

        if price>self.sum:#dont have money for that
            return

        self.sum-=price

        ls = json.loads(self.listOfStock)
        dic = {}
        dic['symbol'] = symbol
        dic['screener'] = screener
        dic['exchange'] = exchange
        dic['amount'] = amount
        dic['price'] = price #summary original price
        dic['close'] = -1
        dic['changeProfit'] = -1
        dic['profit'] = -1 
        dic['time'] = str(datetime.datetime.now())
        ls.append(dic)
        self.listOfStock = json.dumps(ls)
        self.refreshData()


    def refreshData(self):
        sum1 = 0
        ls = json.loads(self.listOfStock)
        for stock in ls:
            data = get_data(stock['symbol'], stock['screener'], stock['exchange'], ["close"], '1d')
            if data != {}:
                stock['profit'] = data['close']*stock['amount']-stock['price']
                stock['changeProfit'] = ((data['close']*stock['amount'] - stock['price'])/stock['price'])*100
                stock['close'] = data['close']
                sum1+=stock['profit']
        self.sum+= sum1
        self.listOfStock = json.dumps(ls)













