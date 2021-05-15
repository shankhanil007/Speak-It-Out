from django.contrib import admin
from django.urls import path, include
from home import views

urlpatterns = [
    path('', views.home, name="home"),
    path('signup', views.handleSignUp, name="handleSignUp"),
    path('login', views.handeLogin, name="handleLogin"),
    path('logout', views.handelLogout, name="handleLogout"),
    path('meet', views.meet, name="meet"),
    path('<slug>/postMessage', views.postMessage, name="postMessage"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('meet/activate', views.meetActivate, name="meetActivate"),
    path('<slug>/newMessages', views.newMessages, name="newMessages"),


    # # path('enter', views.enter, name="enter"),
    # path('message', views.postMessage, name="postMessage"),
    
    # path('meet', views.meet, name="meet"),
    

]
