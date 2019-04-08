from django.urls import path
from . import views
from django.views.generic import TemplateView, ListView
from sport.views import Place

app_name="sport"
urlpatterns = [
    path('sport/', views.sport_view, name="sport-view"),
    path('table/', views.table_view, name="table-view"),
    path('competition/', views.competition, name="competition"),
    path('table2/', TemplateView.as_view(template_name="sport/competition.html", extra_context={"name": Place.name})),
    path('competitionedit/<int:competition_id>',views.competitionedit, name="competitionedit"),
    path('competitioncreate', views.competitioncreate, name="competitioncreate"),
    #path('', views.index, name="index"),

]
