from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'syslogin'

urlpatterns = [
    path('login/', views.login, name="login"),
    path('logout/', views.logout),
    ]
