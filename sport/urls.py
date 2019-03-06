from django.urls import path
from . import views
from django.views.generic import TemplateView, ListView
from sport.views import Place

app_name = 'sport'
urlpatterns = [
    path('index/', views.index, name="index"),
    #path('declaration/', views.index, name="declaration.html"),
    path('sport/', views.sport_view, name="sport-view"),
    path('table/', views.table_view, name="table-view"),

    path('create/', views.form_create_view, name="create"),
    path('table_input', views.table_input, name="table_input"),
]
