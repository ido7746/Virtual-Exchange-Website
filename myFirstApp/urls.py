from django.urls import path
from . import views



urlpatterns = [
    path('addStocks', views.addStocks, name = 'addStocks'),
    path('liveStocks', views.liveStocks, name = 'liveStocks')
    ]