from django.db import models
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import json
from myFirstApp.stocks import get_data
import datetime
from myFirstApp.models import Stock



class StockTrade(Stock):
    buyPrice = models.FloatField()
    amount = models.FloatField()
    close = models.FloatField(default = -1)
    changeProfit = models.FloatField(default = -1)
    profit = models.FloatField(default = -1)
    time = models.DateField(("Date"), default=datetime.datetime.now())

    def toJson(self):
        a = super().toJson()
        a["buyPrice"] = self.buyPrice
        a["amount"] = self.amount
        a["close"] = self.close
        a["changeProfit"] = self.changeProfit
        a["profit"] = self.profit
        a["time"] = str(self.time)
        return a


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

        newStock = StockTrade(symbol=symbol, screener=screener, exchange=exchange,
                   amount=amount, buyPrice=price)

        ls = json.loads(self.listOfStock)

        ls.append(newStock.toJson)
        self.listOfStock = json.dumps(ls)

        self.refreshData()


    def refreshData(self):
        sum1 = 0
        ls = json.loads(self.listOfStock)
        for stock in ls:
            data = get_data(stock['symbol'], stock['screener'], stock['exchange'], ["close"], '1d')
            if data != {}:
                stock['profit'] = data['close']*stock['amount']-stock['buyPrice']
                stock['changeProfit'] = ((data['close']*stock['amount'] - stock['buyPrice'])/stock['buyPrice'])*100
                stock['close'] = data['close']
                sum1+=stock['profit']
        self.sum+= sum1
        self.listOfStock = json.dumps(ls)













