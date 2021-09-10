from django.db import models
import requests, json, warnings, time
from django.utils import timezone
from django.contrib.auth.models import User

class Stock(models.Model):
    symbol = models.CharField(max_length=10)
    screener = models.CharField(max_length=10)
    exchange = models.CharField(max_length=10)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.symbol
