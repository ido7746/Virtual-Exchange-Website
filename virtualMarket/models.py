from django.db import models
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import json
from myFirstApp.stocks import get_data
import datetime
from myFirstApp.models import Stock



class StockTrade(Stock):
    buyPrice = models.FloatField(default=-1)
    amount = models.FloatField()
    close = models.FloatField(default = -1)
    changeProfit = models.FloatField(default = -1)
    profit = models.FloatField(default = -1)
    time = models.DateField(("Date"), default=timezone.now)

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
    changePer = models.FloatField(default = 0)
    name = models.CharField(max_length=30)
    listOfStock = models.CharField(max_length=2000000, default = '[]')
    value = models.FloatField(default = 1)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


    def getStocksList(self):
        return json.loads(self.listOfStock)



    def addStock(self, stock):#amount: number of stocks to buy
        if stock.buyPrice<=0:
            data = get_data(stock.symbol, stock.screener, stock.exchange, ["close"], '1d')
            if stock.amount<=0 or data == {}:
                return
            stock.buyPrice = data['close']

        stock.buyPrice = stock.buyPrice*stock.amount

        if stock.buyPrice>self.sum:#dont have money for that
            return False

        self.sum-=stock.buyPrice

        ls = json.loads(self.listOfStock)

        ls.append(stock.toJson())
        self.listOfStock = json.dumps(ls)

        self.refreshData()
        return True

    def removeStock(self, stock, price=-1):
        if price<=0:
            data = get_data(stock.symbol, stock.screener, stock.exchange, ["close"], '1d')
            if stock.amount<=0 or data == {}:
                return False
            price = data['close']
        if stock.amount<=0:
            return False
        price = price*stock.amount
        self.sum+=price
        ls = json.loads(self.listOfStock)

        for st in ls:
            if st["symbol"]==stock.symbol and st["screener"]==stock.screener and st["exchange"]==stock.exchange:
                if stock.amount> st["amount"]:
                   stock.amount = st["amount"]
                self.sum += stock.amount*price
                st["amount"]-=stock.amount
                if st["amount"]==0:
                    ls.remove(st)
        self.listOfStock = json.dumps(ls)
        self.refreshData()
        return True




    def refreshData(self):
        sum1 = 0
        ls = json.loads(self.listOfStock)
        for stock in ls:
            data = get_data(stock['symbol'], stock['screener'], stock['exchange'], ["close"], '1d')
            if data != {}:
                stock['profit'] = data['close']*stock['amount']-stock['buyPrice']
                stock['changeProfit'] = ((data['close']*stock['amount'] - stock['buyPrice'])/stock['buyPrice'])*100
                stock['close'] = float("{:.2f}".format(data['close']))
                stock['profit'] = float("{:.2f}".format(stock['profit']))
                stock['changeProfit'] = float("{:.2f}".format(stock['changeProfit']))
                sum1+=stock['profit']
        self.sum+= sum1
        self.listOfStock = json.dumps(ls)

        #calculate the value
        value = self.sum 
        for stock in ls:
            value+=stock["profit"]
        self.value = float("{:.2f}".format(value))

        #calculate the change Percent
        currValueStocks = self.value - self.sum
        buyValue = 0
        for stock in ls:
            buyValue+=stock['buyPrice']
        if buyValue!=0:
            self.changePer = (currValueStocks - buyValue)/buyValue*100
            self.changePer = float("{:.2f}".format(self.changePer))
        self.sum = float("{:.2f}".format(self.sum))

        self.save()














