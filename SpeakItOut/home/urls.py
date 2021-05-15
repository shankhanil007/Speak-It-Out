from django.contrib import admin
from django.urls import path, include
from home import views

urlpatterns = [
    path('', views.home, name="home"),
    path('enter', views.enter, name="enter"),
    path('message', views.postMessage, name="postMessage"),
    path('dashboard', views.dashboard, name="dashboard"),
]
