from django.shortcuts import render
from django.http import HttpResponse
from sport.models import Sport, Period, Team, Place, TeamResult
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from sport.models import Competition
from datetime import datetime, date
from django.core.paginator import Paginator

def index(request):
    args={}
    args['date_now'] = date.today()
    data = Competition.objects.all().order_by("-date")
    args['competition_5'] = data[:5]
    paginator = Paginator(data, 5)
    page = request.GET.get('page')
    args['competition'] = paginator.get_page(page)
    return render(request, 'main.html', args)
