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
    profit = models.FloatField(default = 0)
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
        dics = json.loads(self.listOfStock)
        for dic in dics:
            dic["buyPrice"] = float(dic["buyPrice"])
            dic["amount"] = float(dic["amount"])
            dic["close"] = float(dic["close"])
            dic["changeProfit"] = float(dic["changeProfit"])
            dic["profit"] = float(dic["profit"])
        return dics



    def addStock(self, stock):#amount: number of stocks to buy
        if stock.buyPrice<=0:
            data = get_data(stock.symbol, stock.screener, stock.exchange, ["close"], '1d')
            if stock.amount<=0 or data == {}:
                return False
            stock.buyPrice = data['close']

        stock.buyPrice = stock.buyPrice*stock.amount

        if stock.buyPrice>self.sum:#dont have money for that
            return False

        self.sum-=stock.buyPrice

        ls = json.loads(self.listOfStock)
        stock.symbol = stock.symbol.upper()
        stock.screener = stock.screener.upper()
        stock.exchange = stock.exchange.upper()
        for st in ls:
            if st['symbol']==stock.symbol and st['screener']==stock.screener and st['exchange']==stock.exchange:
                price1 = st['buyPrice']
                price2 = stock.buyPrice*stock.amount
                per1 = price1*100/(price1+price2)
                per2 = price2*100/(price1+price2)
                st['amount']+=stock.amount
                st['buyPrice'] = ((price1*per1/100)+(price2*per2/100))*st['amount']
                self.listOfStock = json.dumps(ls)
                self.refreshData()
                return True
            
        ls.append(stock.toJson())
        self.listOfStock = json.dumps(ls)

        self.refreshData()
        return True

    def removeStock(self, stock, price):
        if price<=0:
            data = get_data(stock.symbol, stock.screener, stock.exchange, ["close"], '1d')
            if data == {}:
                print("data == {}")
                return False
            price = data['close']
        if stock.amount<=0:
            print("stock.amount<=0")
            return False
        
        ls = json.loads(self.listOfStock)

        for st in ls:
            if st["symbol"]==stock.symbol.upper() and st["screener"]==stock.screener.upper() and st["exchange"]==stock.exchange.upper():
                if stock.amount> st["amount"]:
                   stock.amount = st["amount"]#SOLD all the stocks
                st["amount"]-=stock.amount
                price = price*stock.amount
                self.sum=self.sum + price
                if st["amount"]==0:
                    ls.remove(st)

                self.listOfStock = json.dumps(ls)
                self.refreshData()
                return True




    def refreshData(self):
        profits = 0
        ls = json.loads(self.listOfStock)
        for stock in ls:
            data = get_data(stock['symbol'], stock['screener'], stock['exchange'], ["close"], '1d')
            if data != {}:
                stock['profit'] = data['close']*stock['amount']-stock['buyPrice']
                stock['profit'] = float("{:.2f}".format(stock['profit']))
                stock['changeProfit'] = ((data['close']*stock['amount'] - stock['buyPrice'])/stock['buyPrice'])*100
                stock['changeProfit'] = float("{:.2f}".format(stock['changeProfit']))
                stock['close'] = data['close']
                stock['changeProfit'] = stock['changeProfit']
                if(stock['changeProfit']<0):
                    stock['color']='red'
                if(stock['changeProfit']>0):
                    stock['color']='green'
                profits=profits+stock['profit']+stock['buyPrice']
        self.listOfStock = json.dumps(ls)

        #calculate the value
        self.value = profits + self.sum
        self.value = float("{:.2f}".format(self.value))
        
        #calculate the change Percent
        buyValue = 0
        for stock in ls:
            buyValue=buyValue+stock['buyPrice']
        buyValue = buyValue + self.sum
        if buyValue!=0:
            self.changePer = (self.value - buyValue)/buyValue*100
            self.changePer = float("{:.2f}".format(self.changePer))

        self.save()














