from django.urls import path
from . import views

urlpatterns = [
    path('virtualMarket', views.virtualMarket, name = 'virtualMarket'),
    path('createProtfolio', views.createProtfolio, name = 'createProtfolio'),
    path('protfolio', views.protfolio, name = 'protfolio'),
    ]