from django.urls import path
from . import views



urlpatterns = [
    path('search', views.home, name = 'search'),
    path('liveStocks', views.liveStocks)
    ]