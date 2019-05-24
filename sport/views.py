import datetime
from django.template.context_processors import csrf
from django.db import IntegrityError
from django.contrib import auth
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from sport.models import Sport, Period, Team, Place, TeamResult, Competition, Judge, Person, CompetitionJudge, TeamMember, Competition_name, Department
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from .forms import CompetitionForm, JudgeForm, TeamForm, TeamMember_Form, TeamResult_form, TeamResult_form_competition, Sport_adding_form, Place_adding_form, Period_for_Table_Form, Uchp_adding_form
from django.forms import modelformset_factory, inlineformset_factory, formset_factory, modelform_factory
from django import forms
import json
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required


# Create your views here.

def index(request):
    return render(request, 'sport/competition.html')


def sport_view(request):
    sports = Sport.objects.all()
    context = {
        'sports': sports
    }
    return render(request, 'sport/competition.html', context)


''' показать все таблицу заявок'''
def teamtable(request):

    teams = Team.objects.all().order_by('competition')
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
    results = TeamResult.objects.select_related('Team', 'Department', 'Competition', 'Place').filter(competition__date__gte=period.begin, competition__date__lte=period.end)

    context = {
        'sports': sports,
        'period': period,
        'results':results
    }
    return render(request, 'sport/competition.html', context)


#действия со списком соревнований
@login_required()
@permission_required("sport.delete_competition")
def competition(request):
    def json_filling():
        competition = Competition.objects.all()
        json_collection=[]
        for i, item in enumerate(competition):
            json_collection.append({
            "competition_id": str(item.id),
            "url": reverse('sport:competitionedit', args=[item.id]),
            "id": str(i+1),
            "sport": item.sport.name,
            "date": str(item.date),
            "place":item.place.name
            })
        return json_collection
    args={}
    if request.method == 'GET':
        data=mark_safe(json.dumps(json_filling(), ensure_ascii=False))
        args['json_collection'] = data
        return render(request, 'sport/competitiond.html', args)
    args.update(csrf(request))
    if request.POST:
        data = json.loads(request.POST.get('datajson'))
        if request.POST["operation"]=="delete-competition":
            for item in data:
                Competition.objects.filter(id=item).delete()
        if request.POST["operation"]=="copy-competition":
            for item in data:
                competition_data = Competition.objects.get(id=item)
                competition_save = Competition(
                    date = competition_data.date,
                    place = competition_data.place,
                    sport = competition_data.sport,
                    result = False
                )
                competition_save.save()
        if request.POST["operation"]=="close-competition":
            for item in data:
                competition_data = Competition.objects.get(id=item)
                competition_data.result = True
                competition_data.save()
                print("OK")
            #return render(request, 'sport/competitiond.html', args)
        #data_json=mark_safe(json.dumps(json_filling(), ensure_ascii=False))
        #args['json_collection'] = data_json
        #return render(request, 'sport/competitiond.html', args)
        #return redirect("sport:competition")




#редактирование соревнования
@login_required()
@permission_required("sport.delete_competition")
def competitionedit(request, competition_id):
    competition = Competition.objects.get(pk = competition_id)
    name = competition.sport.name + "(" + str(competition.date) + ")"
    judge = CompetitionJudge.objects.filter(competition__id = competition_id).first()
    form_judge = modelformset_factory(CompetitionJudge, form = JudgeForm, can_delete=True, extra=1)
    formset = form_judge(queryset=CompetitionJudge.objects.filter(competition__id = competition_id))
    if request.method == 'POST':
        args={}
        form = CompetitionForm(request.POST, instance=competition)
        if request.POST['button']=='save':
            if form.is_valid():
                try:
                    new_competition = form.save()
                    formj = form_judge(request.POST)
                    if formj.is_valid():
                        instances = formj.save(commit=False)
                        print(instances)
                        for instance in instances:
                            instance.competition = new_competition
                            instance.save()
                        for obj in formj.deleted_objects:
                            obj.delete()
                    else:
                        print(formj.errors)
                        return HttpResponse("lol")
                except Exception as e:
                    args['save_error']=str(e)
                    return  render(request, 'sport/competitiondEdit.html', args)
            return redirect("sport:competition")
        if request.POST['button']=='copy':
            if form.is_valid():
                try:
                    copy_competition = form.save(commit=False)
                    copy_competition.pk = None
                    copy_competition.save()
                    return redirect (reverse('sport:competitionedit', args=[copy_competition.pk]), {
                        'form': CompetitionForm(instance = copy_competition),
                        'formset': formset,
                        'copy': 'редактирование копии'
                        })
                except Exception as e:
                    args['save_error']=str(e)
                    return  render(request, 'sport/competitiondEdit.html', args)
        if request.POST['button']=='delete':
            Competition.objects.filter(id=competition_id).delete()
            return redirect("sport:competition")
    return render(request, 'sport/competitiondEdit.html', {
        'form': CompetitionForm(instance = competition),
        'formset': formset,
        'name': name,
        'competition_id': str(competition.id)
        })


#создание соревнования
@login_required()
@permission_required("sport.delete_competition")
def competitioncreate(request):
    args={}
    args['create'] = 'true'
    form_judge = modelformset_factory(CompetitionJudge, form = JudgeForm, can_delete=True)
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
                        instance.competition = new_competition
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


#добавление витда спорта
@login_required()
@permission_required("sport.delete_competition")
def sport_adding(request):
    request_url = request.GET.get("next")
    form = Sport_adding_form()
    if request.POST:
        forms = Sport_adding_form(request.POST)
        forms.save()
        return redirect(request_url)
    return render(request, "sport/addform.html", {
        'form':form,
        'whatweadding':'вида спорта'
    })

#добавление места проведения
@login_required()
@permission_required("sport.delete_competition")
def place_adding(request):
    request_url = request.GET.get("next")
    form = Place_adding_form()
    if request.POST:
        forms = Place_adding_form(request.POST)
        forms.save()
        return redirect(request_url)
    return render(request, "sport/addform.html", {
        'form':form,
        'whatweadding':'места проведения'
    })

#результаы соревнования
def result_team(request, competition_id):
    print("test")
    teamRes = TeamResult.objects.filter(competition__id = competition_id).order_by('result')
    teamresult ={}
    teamresult['teamresult'] = teamRes
    competition_name = Competition.objects.get(id = competition_id)
    if any(teamresult['teamresult']):
        print("yes")
        context = {
            'teamRes': teamresult,
            'competition_name': competition_name
        }
    else:
        print("no")
        context = {
            'is_empty': True,
            'competition_name': competition_name
        }
    return render(request, 'sport/ResultTeam.html', context)


'''функции изменения Team'''
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
    context={
        'teamMember': teamMember,
    }
    return render(request, 'sport/tmembertable.html', context)


'''Добавить спортсмена'''
# def member_create_view(request):
#     if request.method == 'POST':
#         form = TeamMember_Form(request.POST)
#         if form.is_valid():
#             try:
#                 form.save()
#             except:
#                 return HttpResponse('Error')
#         return HttpResponseRedirect('/CM/tmembertable/')
#     return render(request, 'sport/memadd.html', {'form': TeamMember_Form()})


''' удалить спортсмена из списка-команд'''
def member_remove_view(request, id):
    try:
        team = TeamMember.objects.get(id = id)
    except team.DoesNotExist:
        team = None
    team.delete()

    return HttpResponseRedirect('/CM/tmembertable/')


'''редактировать Team'''
def form_change_view(request, id):
    team_instance = Team.objects.get(pk = id)

    change_mamber = modelformset_factory(TeamMember, TeamMember_Form, can_delete = True, extra = 1)
    formset = change_mamber(queryset = TeamMember.objects.filter(team__id=id))
    if request.method == 'POST':
        form = TeamForm(request.POST)

        formset = change_mamber(request.POST)
        if form.is_valid() and formset.is_valid():
                try:
                    team_instance.competition = form.cleaned_data['competition']
                    team_instance.organization = form.cleaned_data['organization']
                    team_instance.name = form.cleaned_data['name']
                    team_instance.not_resultable = form.cleaned_data['not_resultable']

                    objects = formset.save(commit = False)
                    for mem in objects:
                        mem.save
                except IntegrityError:
                    team_instance.name = form.cleaned_data['name']
        team_instance.save()
        return HttpResponseRedirect('/CM/teamtable/') #HttpResponse("good")
    return render(request, 'sport/change.html', {'form': TeamForm(instance = team_instance), 'formset': formset})


''' редактировать спортсмена'''
def member_change_view(request, id):
    sportsman = TeamMember.objects.get(pk = id)
    teamMemb = get_object_or_404(TeamMember, id=id)

    context = {}
    form2 = TeamMember_Form(request.POST)
    change_member = modelformset_factory(TeamMember, form=TeamMember_Form, can_delete = True, extra = 0)
    formset = change_member(queryset = TeamMember.objects.none)
    if request.method == 'POST':
        form2 = TeamMember_Form(request.POST)
        if form2.is_valid() and formset.is_valid():
            try:
                # teamMemb.team = form.cleaned_data['team']
                teamMemb.sportsman = form2.cleaned_data['sportsman']
                teamMemb.comments = form2.cleaned_data['comments']

                teamMemb.save()
            except:
                return HttpResponse('error!!!')
        return HttpResponseRedirect('/CM/tmembertable/') #HttpResponse("good")
    else:
        form = TeamMember_Form()
    return render(request, 'sport/membChange.html', {'form': TeamMember_Form(instance = sportsman)})

'''
def team_member(request):
result={"success":True}

return HttpResponse(json.dumps(result), content_type='application/json')
def team_member(request):
teamMember = list(TeamMember.objects.all().values())
data = dict()
data['teamMember'] = teamMember

return JsonResponse(data)

 создать заявку team
def form_create_view(request):
    form_member = modelformset_factory(TeamMember, form = TeamMember_Form, can_delete = True, extra = 3)
    formset = form_member(queryset = TeamMember.objects.none())
    if request.method == 'POST':
        form = TeamForm(request.POST)
        formset = form_member(request.POST)
        if form.is_valid() and formset.is_valid():
            try:
                team = form.save()'''
def member_create_view(request):
    context = {}
    #team = TeamMember.objects.get(pk = id)
    #Smemberteam = TeamMember.objects.filter(team_id = id).first()
    form1 = TeamMember_Form(request.POST)
    form_member = modelformset_factory(TeamMember, form = TeamMember_Form, can_delete=True, extra=6)
    formset = form_member(queryset = TeamMember.objects.none())
    if request.method == 'POST':
        formset = form_member(request.POST)
        if form1.is_valid() and formset.is_valid():
            try:
                member = form1.save(commit = False)
                member.save()

                for memb in formset:
                    data = memb.save(commit=False)
                    data.member = member
                    data.save()
                # new_team = form1.save()
                # form1.save()
                # form_m = form_member(request.POST)
                # if form_m.is_valid():
                #     instances = form_m.save(commit=False)
                #     for instance in instances:
                #         instance.team = new_team
                #         instance.save()
            except:
                return HttpResponse('Error')
            return HttpResponseRedirect('/CM/tmembertable/') # redirect(reverse('sport:table_input'))
    context['form1'] = form1
    context['formset'] = formset


    return render(request, 'sport/teamadding.html', context)


''' создать заявку'''
def form_create_view(request):
    form_member = modelformset_factory(TeamMember, form = TeamMember_Form, can_delete = True, extra = 3)
    formset = form_member(queryset = TeamMember.objects.none())
    if request.method == 'POST':
        form = TeamForm(request.POST)
        formset = form_member(request.POST)
        if form.is_valid() and formset.is_valid():
            try:
                team=form.save()
                objects = formset.save(commit = False)
                for mem in objects:
                    mem.team = team
                    mem.save()

            except:
                return HttpResponse('Error')
        return HttpResponseRedirect('/CM/teamtable/') #redirect(reverse('sport:table_input'))
    return render(request, 'sport/teamadding.html', {'form': TeamForm(),'formset': formset})


'''Добавить спортсмена'''
def member_create_view(request):
    context = {}
    form1 = TeamMember_Form(request.POST)
    form_member = modelformset_factory(TeamMember, form = TeamMember_Form, can_delete=True, extra=3)
    formset = form_member(queryset = TeamMember.objects.none())
    if request.method == 'POST':
        formset = form_member(request.POST)
        if form1.is_valid() and formset.is_valid():
            try:
                member = form1.save(commit = False)
                member.save()

                for memb in formset:
                    data = memb.save(commit=False)
                    data.member = member
                    data.save()
            except:
                return HttpResponse('Error')
            return HttpResponseRedirect('/CM/tmembertable/') # redirect(reverse('sport:table_input'))
    context['form1'] = form1
    context['formset'] = formset


    return render(request, 'sport/teamadding.html', context)


''' Результаты соревнования
def result_team(request, competition_id):

    teamRes = TeamResult.objects.filter(competition__id = competition_id).order_by('result')

    context = {
        'teamRes': teamRes,
    }
    return render(request, 'sport/ResultTeam.html', context)
'''

''' Результаты соревнования все'''
def result_other(request):

    zachot = Team.objects.filter(not_resultable = 1)
    #print(zachot)
    teamRes = TeamResult.objects.filter(team__in = zachot).order_by('competition')

    context = {
        'teamRes': teamRes,
    }
    return render(request, 'sport/ResultTeam.html', context)


''' Задать результаты'''
def create_result_team(request):
    context = {}
    form = TeamResult_form_competition()
    form_team = modelformset_factory(TeamResult, form = TeamResult_form, extra = 2)
    formset = form_team(queryset = TeamResult.objects.none())
    if request.method == 'POST':
        form_c = TeamResult_form_competition(request.POST)
        competition_id = form_c.save(commit = False)
        if form_c.is_valid():
            form_r = form_team(request.POST)
            if form_r.is_valid():
                instances = form_r.save(commit=False)
                for instance in instances:
                    instance.competition = competition_id.competition
                    instance.save()
                '''
                for t in formset:
                    data = t.save(commit = False)
                    data.team = team
                    data.save()'''

        return HttpResponseRedirect('/CM/teamresult/')
    context['form_competition'] = form
    context['formset'] = formset
    return render(request, 'sport/createResult.html', context)


def table_referee(request, competition_id):
    comp = Competition.objects.get(pk=competition_id)
    team = Team.objects.filter(competition__exact = competition_id)
    team_results = TeamResult.objects.filter(competition__id=comp.id)

    print(team.count())
    print(len(team_results))

    if len(team_results) < len(team):
        teams = set(team.values_list('id', flat=True)) - set(team_results.values_list('team__id', flat=True))
        for t in Team.objects.filter(id__in=teams):
            tr = TeamResult()
            tr.competition = comp
            tr.team = t
            tr.points = 0
            tr.result = 0
            tr.save()
        team_results = TeamResult.objects.filter(competition__id=comp.id)

    team_name = modelformset_factory(TeamResult, form = TeamResult_form, extra=0)
    formset = team_name(queryset=team_results)
    print(team)
    print(comp)
    context = {}
    if request.method == 'POST':
        formset = team_name(request.POST)
        if formset.is_valid():
            try:
                for item in formset:

                    result = item.save(commit = False)
                    print(result.points)
                    print(result.result)
                    result.result = result.points
                    result = item.save()

                    if result.points == 0:
                        result.points = team.count()
                        result.result = result.points
                        result = item.save()
            except:
                return HttpResponse('Errorss!!')
        return HttpResponseRedirect('/CM/teamresult/')
    context['formset'] = formset
    context['competition'] = comp
    return render(request, 'sport/Results.html', context)


'''все-общая таблица результатов соревнования'''
def grand_table(request):
    if 'begin' in request.GET:
        begin = request.GET['begin']
        end = request.GET['end']
    else:
        period = Period.objects.all().latest('end')
        begin = period.begin
        end = period.end
    table = {}
    competitions = Competition.objects.select_related('sport').filter(date__range=[begin, end], result=True).order_by('date')
    deps = Department.objects.all()
    for d in deps:
        s = 0
        table[d.name] = []
        team_results = dict(TeamResult.objects.filter(team__organization__id=d.id, team__not_resultable=True).values_list('competition__id', 'result'))
        for comp in competitions:
            table[d.name].append(team_results[comp.id] if comp.id in team_results.keys() else len(TeamResult.objects.filter(competition__id=comp.id)) + 1)
            s += table[d.name][-1]
        table[d.name].append(s)
    table = sorted(table.items(), key=lambda x: x[1][-1])
    place = 0
    prev = 0
    for item in table:
        if item[1][-1] > prev:
            place += 1
        prev = item[1][-1]
        item[1].append(place)
    return render(request, 'sport/grandTable2.html', {'form': Period_for_Table_Form(), 'grand_table': dict(table), 'daten': competitions})


'''Добавить УЧП'''
def uchp_add(request):
    request_url = request.GET.get("next")
    form = Uchp_adding_form()
    if request.POST:
        forms = Uchp_adding_form(request.POST)
        forms.save()
        return redirect(request_url)
    return render(request, "sport/uchp.html", {
        'form':form,
        'whatweadding': 'УЧП'
    })

# декоратор POST - 1 это обеспечение POST запросов
# декоратор Ajax_require - 2 для совмещения работы Django с Ajax(чтобыне дать Ajax свободы действий)

def ajax_required(f):
    def wrap(request, *args, **kwargs):
       if not request.is_ajax():
           return HttpResponseBadRequest()
       return f(request, *args, **kwargs)

    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__
    return wrap
#@ajax_required
#@csrf_exempt
def member_team(request):
    if request.method == 'POST':
        answer = dict(teams=[])
        if request.is_ajax():

            if Team.objects.filter(name__contains=request.POST.get('team')):
                answer['teams'].append('true')

            else:
                answer['teams'].append('false')
            # print(type(team))
            # print(type(qs))
            # team = request.POST.get('team')
            # qs = Team.objects.filter(name__contains='wolfes')
            # for obj in qs:
            #     members = [{'id': tm.id, 'name': str(tm.sportsman), 'comm': tm.comments} for tm in obj.teammember_set.all()]
            #     answer['teams'].append({
            #         'id': obj.id,
            #         'name': obj.name,
            #         'members': members,
            #
            #     })
        return JsonResponse(answer)
    return JsonResponse('team_aj') # возврат данных в Ajax


# def grand_t(request):
#
#
#
#     if request.method == 'POST':
#
#         answer = dict(teams=[])
#         if request.is_ajax():
#             begin = request.POST.get('begin')
#
#             if
#             qs = Team.objects.filter(name__contains=team) if team else Team.objects.all()
#             for obj in qs:
#                 members = [{'id': tm.id, 'name': str(tm.sportsman)} for tm in obj.teammember_set.all()]
#                 answer['teams'].append({
#                     'id': obj.id,
#                     'name': obj.name,
#                     'members': members,
#                 })
#         return JsonResponse(answer)
#
#     return JsonResponse('team_aj')
