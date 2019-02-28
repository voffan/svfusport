from django.urls import path
from . import views
from django.views.generic import TemplateView, ListView
from sport.views import Place

urlpatterns = [
    path('', views.index, name="index"),
    path('sport/', views.sport_view, name="sport-view"),
    path('table/', views.table_view, name="table-view"),
    path('table2/', TemplateView.as_view(template_name="sport/competition.html", extra_context={"name": Place.name}))

]
