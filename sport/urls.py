from django.urls import path
from . import views
from django.views.generic import TemplateView, ListView
#from sport.views import Place

app_name = 'sport'

urlpatterns = [
    path('index/', views.index, name="index"),
    #path('declaration/', views.index, name="declaration.html"),
    path('sport/', views.sport_view, name="sport-view"),
    path('table/', views.table_view, name="table-view"),

    path('create/', views.form_create_view, name="form-create-view"),
    path('create/memberTeam/', views.member_team, name='member-team'),
    path('create/memberTeam/', views.member_team, name='member-team'),

    path('teamtable/', views.teamtable, name='team_table'), # Таблица: список-заявок
    path('teamtable/<int:id>/change/', views.form_change_view, name="form-change-view"),
    path('teamtable/<int:id>/teamremove/', views.team_remove_view, name="form-change-view"),

    path('tmembertable/', views.team_member, name='team_member'), # Таблица: список-участников-команд
    path('tmembertable/<int:id>/membChange/', views.member_change_view, name="member_change_view"),
    path('tmembertable/<int:id>/membremove/', views.member_remove_view, name="member_remove_view"),
    path('membercreate/', views.member_create_view, name="member_create_view"),
    #path('team_member_process', views.team_member, name='team_member'),
    #path('change/<int:id>/chan/', views.changelink, name="change-link"),
]
