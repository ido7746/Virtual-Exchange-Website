from django.urls import path
from . import views



urlpatterns = [
    path('hello', views.home),
    path('say_hello', views.say_hello)
    ]