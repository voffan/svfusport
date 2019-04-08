import datetime
from django.template.context_processors import csrf
from django.db.models import Q
from django.contrib import auth
from django.shortcuts import render, redirect
from django.http import HttpResponse
from sport.models import Sport, Period, Team, Place, TeamResult, Compitition, Judge, Person, CompetitionJudge
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.template.context_processors import csrf
from .forms import CompetitionForm, JudgeForm
from django.forms import modelformset_factory, inlineformset_factory, formset_factory
from django import forms
import json
from django.utils.safestring import mark_safe

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
        'results':resultsr
    }
    return render(request, 'sport/competition.html', context)

def competition(request):
    competition = Compitition.objects.all()
    json_collection=[]
    for i, item in enumerate(competition):
        json_collection.append({
        "competition_id": str(item.id),
        "id": str(i+1),
        "sport": item.sport.name,
        "date": str(item.date),
        "place":item.place.name
        })
    args={}
    data=mark_safe(json.dumps(json_collection, ensure_ascii=False))
    args['json_collection'] = data
    '''
    if 'q' in request.GET.keys():
        args={}
        query = request.GET.get('q')
        founded_values = Compitition.objects.filter(
            Q(sport__name__icontains = query)|
            Q(place__name__icontains = query)
        )
        args['competition'] = founded_values
        args['search_values'] = 'Результаты поиска: ' + str(founded_values.count()) + ' результатов по запросу "' + str(query) + '"'
        return render(request, 'sport/competitiond.html', args)'''
    return render(request, 'sport/competitiond.html', args)


def competitionedit(request, competition_id):
    competition = Compitition.objects.get(pk = competition_id)
    judge = CompetitionJudge.objects.filter(compitition__id = competition_id).first()
    form_judge = modelformset_factory(CompetitionJudge, form = JudgeForm, can_delete=True, extra=10)
    formset = form_judge(queryset=CompetitionJudge.objects.filter(compitition__id = competition_id))
    if request.method == 'POST':
        args={}
        form = CompetitionForm(request.POST, instance=competition)
        if request.POST['button']=='save':
            if form.is_valid():
                try:
                    new_competition = form.save()
                    form.save()
                    formj = form_judge(request.POST)
                    if formj.is_valid():
                        instances = formj.save(commit=False)
                        for instance in instances:
                            instance.compitition = new_competition
                            instance.save()
                        for obj in formj.deleted_objects:
                            obj.delete()
                except Exception as e:
                    args['save_error']=str(e)
                    return  render(request, 'sport/competitiondEdit.html', args)
            return redirect("sport:competition")
        if request.POST['button']=='delete':
            Compitition.objects.filter(id=competition_id).delete()
            return redirect("sport:competition")
    return render(request, 'sport/competitiondEdit.html', {
        'form': CompetitionForm(instance = competition),
        'formset': formset,
        })

'''
def competitionedit(request, competition_id):
    competition = Compitition.objects.get(pk = competition_id)
    judge = CompetitionJudge.objects.filter(compititi   on__id = competition_id).first()
    form_judge = inlineformset_factory(Compitition, CompetitionJudge, fields=('judge','judge_position'))
    if request.method == 'POST':
        form = CompetitionForm(request.POST, instance=competition)
        formset = form_judge(request.POST, instance = competition)
        args={}
        if request.POST['button']=='save':
            if form.is_valid():
                try:
                    form.save()
                    formset.instance.compitition = form.instance
                    formset.save()
                except Exception as e:
                    args['save_error']=str(e)
                    return  render(request, 'sport/competitiondEdit.html', args)
            return redirect("sport:competition")
        if request.POST['button']=='delete':
            Compitition.objects.filter(id=competition_id).delete()
            return redirect("sport:competition")
    formset = form_judge(instance = competition)
    return render(request, 'sport/competitiondEdit.html', {
        'form': CompetitionForm(instance = competition),
        'formset': form_judge
        })
'''

def competitioncreate(request):
    args={}
    args['create'] = 'true'
    form_judge = modelformset_factory(CompetitionJudge, form = JudgeForm, can_delete=True, extra=10)
    formset = form_judge(queryset=CompetitionJudge.objects.none())
    if request.method == 'POST':
        form = CompetitionForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                new_competition = form.instance
                formj = form_judge(request.POST)
                if formj.is_valid():
                    instances = formj.save(commit=False)
                    for instance in instances:
                        instance.compitition = new_competition
                        instance.save()
                    for obj in formj.deleted_objects:
                        obj.delete()
            except:
                args['save_error']=str(e)
                return  render(request, 'sport/competitiondEdit.html', args)
        return redirect("sport:competition")
    return render(request, 'sport/competitiondEdit.html', {
        'form': CompetitionForm(),
        'formset': formset,
        'create': 'create'
        })
