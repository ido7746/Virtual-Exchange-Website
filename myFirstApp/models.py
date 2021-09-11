from django.db import models
import requests, json, warnings, time
from django.utils import timezone
from django.contrib.auth.models import User
import json


class Stock(models.Model):
    symbol = models.CharField(max_length=10)
    screener = models.CharField(max_length=10)
    exchange = models.CharField(max_length=10)

    def toJson(self):
        a = {}
        a["symbol"] = self.symbol
        a["screener"] = self.screener
        a["exchange"] = self.exchange
        return a

    

class FollowStocks(models.Model):
    listOfStock = models.CharField(max_length=2000000, default = '[]')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def getList(self):
        return json.loads(self.listOfStock)
    
    def addToList(self, stock):
        ls = self.getList()
        ls.append(stock.toJson())
        self.listOfStock = json.dumps(ls)
        self.save()
