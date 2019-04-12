from django.shortcuts import render
from django.http import HttpResponse
from sport.models import Sport, Period, Team, Place, TeamResult
from django.views.generic.list import ListView
from django.views.generic import TemplateView

def index(request):
    return render(request, 'index.html')
