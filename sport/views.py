import datetime

from django.shortcuts import render
from django.http import HttpResponse
from sport.models import Sport, Period, Team, Place, TeamResult
from django.views.generic.list import ListView
from django.views.generic import TemplateView


# Create your views here.

def index(request):
    return render(request, 'sport/competition.html')


def sport_view(request):
    sports = Sport.objects.all()
    context = {
        'sports': sports
    }
    return render(request, 'sport/competition.html', context)

'''
def table_view(request):
    team = Team.objects.all()
    period = Period.objects.all()
    place = Place.objects.all()
    sports = Sport.objects.all()

    context = {
        'sports': sports,
        'team': team,
        'period': period,
        'place': place
    }
    return render(request, 'sport/competition.html', context)
'''

def table_view(request):
    team = Team.objects.all()
    if 'period_id' in request.GET.keys():
        period = Period.objects.get(id=request.GET['period_id'])
    else:
        today = datetime.datetime.now()
        period = Period.objects.get(begin__lte=today, end__gte=today)
    sports = Sport.objects.all()
    results = TeamResult.objects.select_related('Team', 'Department', 'Compitition', 'Place').filter(compitition__date__gte=period.begin, compitition__date__lte=period.end)

    context = {
        'sports': sports,
        'period': period,
        'results':results
    }


    return render(request, 'sport/competition.html', context)

