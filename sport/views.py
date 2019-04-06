import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from sport.models import Sport, Period, Team, Place, TeamResult, TeamMember, Person
from django.views.generic.list import ListView
from django.views.generic import TemplateView

from .forms import TeamForm, TeamMember_Form
#from django.contrib.formtools.wizard.views import SessionWizardView

import json
# Create your views here.

def index(request):
    return render(request, 'sport/index.html')


def sport_view(request):
    sports = Sport.objects.all()
    context = {
        'sports': sports
    }
    return render(request, 'sport/competition.html', context)


''' показать все таблицу заявок'''
def teamtable(request):
    teams = Team.objects.all()
    context={
        'teams': teams,
    }
    return render(request, 'sport/teamtable.html', context)


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


'''функции изменения - удаления - добавления Team'''
def form_change_view(request, id):
    team = get_object_or_404(Team, id=id)
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team.competition = form.cleaned_data['competition']
            team.organization = form.cleaned_data['organization']
            team.name = form.cleaned_data['name']
            team.not_resultable = form.cleaned_data['not_resultable']
            team.save()
        return HttpResponseRedirect('/CM/teamtable/') #HttpResponse("good")
    else:
        form = TeamForm()
    return render(request, 'sport/change.html', {'form': TeamForm()})


''' создать заявку'''
'''
def form_create_view(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            try:
                team = form.save()
                for member_id in form.cleaned_data['TeamMembers']:
                    tm = TeamMember()
                    tm.team = team
                    tm.sportsman = Person.objects.get(pk=member_id)
                    tm.save()
            except:
                return HttpResponse('Error')
        return HttpResponseRedirect('/CM/teamtable/') #redirect(reverse('sport:table_input'))
    return render(request, 'sport/teamadding.html', {'form': TeamForm()})
'''


''' удалить команду из заявки'''
def team_remove_view(request, id):
    try:
        team = Team.objects.get(id = id)
    except team.DoesNotExist:
        team = None
    team.delete()

    return HttpResponseRedirect('/CM/teamtable/')


''' Посмотреть участников команды'''

def team_member(request):
    teamMember = TeamMember.objects.all()
    pe = Person.objects.all()

    context={
        'teamMember': teamMember,
        'pe': pe
    }
    return render(request, 'sport/tmembertable.html', context)


'''Добавить спортсмена'''
def member_create_view(request):
    if request.method == 'POST':
        form = TeamMember_Form(request.POST)
        if form.is_valid():
            try:
                form.save()
            except:
                return HttpResponse('Error')
        return HttpResponseRedirect('/CM/tmembertable/')
    return render(request, 'sport/memadd.html', {'form': TeamMember_Form()})


''' удалить спортсмена из списка-команд'''
def member_remove_view(request, id):
    try:
        team = TeamMember.objects.get(id = id)
    except team.DoesNotExist:
        team = None
    team.delete()

    return HttpResponseRedirect('/CM/tmembertable/')


''' редактировать спортсмена'''
def member_change_view(request, id):
    sportsman = TeamMember.objects.get(pk = id)
    teamMemb = get_object_or_404(TeamMember, id=id)
    if request.method == 'POST':
        form = TeamMember_Form(request.POST)
        if form.is_valid():
            teamMemb.team = form.cleaned_data['team']
            teamMemb.sportsman = form.cleaned_data['sportsman']
            teamMemb.comments = form.cleaned_data['comments']

            teamMemb.save()
        return HttpResponseRedirect('/CM/tmembertable/') #HttpResponse("good")
    else:
        form = TeamMember_Form()
    return render(request, 'sport/membChange.html', {'form': TeamMember_Form(instance = sportsman)})

'''
def team_member(request):
    result={"success":True}

    return HttpResponse(json.dumps(result), content_type='application/json')
'''
'''
def team_member(request):
    teamMember = list(TeamMember.objects.all().values())
    data = dict()
    data['teamMember'] = teamMember

    return JsonResponse(data)
'''

def form_create_view(request):

    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():

            try:
                team = form.save()

            except:
                return HttpResponse('Error')
        return HttpResponseRedirect('/CM/teamtable/') #redirect(reverse('sport:table_input'))
    return render(request, 'sport/teamadding.html', {'form': TeamForm()})


# декоратор POST - 1 это обеспечение POST запросов
# декоратор Ajax_require - 2 для совмещения работы Django с Ajax(чтобыне дать Ajax свободы действий)
def ajax_required(f):
   """
   AJAX request required decorator
   use it in your views:

   @ajax_required
   def my_view(request):
       ....

   """

   def wrap(request, *args, **kwargs):
       if not request.is_ajax():
           return HttpResponseBadRequest()
       return f(request, *args, **kwargs)

   wrap.__doc__=f.__doc__
   wrap.__name__=f.__name__
   return wrap

@ajax_required
#@csrf_exempt
def member_team(request):
    if request.method == 'POST':
        answer = dict(teams=[])
        if request.is_ajax():
            team = request.POST.get('team')
            qs = Team.objects.filter(name__contains=team) if team else Team.objects.all()
            for obj in qs:
                members = [{'id': tm.id, 'name': str(tm.sportsman), 'comm': tm.comments} for tm in obj.teammember_set.all()]
                answer['teams'].append({
                    'id': obj.id,
                    'name': obj.name,
                    'members': members,

                })
        return JsonResponse(answer)

    return JsonResponse('team_aj') # возврат данных в Ajax