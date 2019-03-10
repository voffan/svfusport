import datetime

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from sport.models import Sport, Period, Team, Place, TeamResult
from django.views.generic.list import ListView
from django.views.generic import TemplateView

from .forms import TeamForm, ChangeTeamForm
#from django.contrib.formtools.wizard.views import SessionWizardView
# Create your views here.
'''
FORMS = [
    ('team', TeamForm),
    ('changeTeam', ChangeTeamForm)
]

TEMPLATES = {
    'team': 'declaration.html',
    'changeTeam': 'table_input.html'
}

class AddTeamWizard():


'''
def index(request):
    return render(request, 'sport/declaration.html')


def sport_view(request):
    sports = Sport.objects.all()
    context = {
        'sports': sports
    }
    return render(request, 'sport/competition.html', context)


def teamtable(request):
    teams = Team.objects.all()
    context={
        'teams': teams,
    }
    return render(request, 'sport/teamtable.html', context)


def form_create_view(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except:
                return HttpResponse('Error')
       # return HttpResponse('Success') #redirect(reverse('sport:table_input'))
    return render(request, 'sport/declaration.html', {'form': TeamForm()})


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

'''
проверочнафункция
def changelink(request, id):

    if request.method == 'GET':
        org = request.GET.get('t.id')
        res = Team.objects.all().get(id=org)
        return HttpResponse(res)
'''

def change_link(request):

    if request.method == 'GET':
        org = request.GET.get('t.id')
        res = Team.objects.all().get(id=org)
        return HttpResponse(res)