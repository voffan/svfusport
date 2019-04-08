from django import forms
from .models import Team, Sport, Department, Compitition, Judge, Person, CompetitionJudge
import datetime
from django.forms.models import BaseModelFormSet
from django.forms.formsets import DELETION_FIELD_NAME
'''
class TeamForm(forms.ModelForm):
    competition = forms.ModelChoiceField(queryset=Competition.objects.filter(date__gt=datetime.date.today()).order_by('date'), empty_label='Выберете соревнование')
    organization = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label='Выберете УЧП')
    class Meta:
        model = Team
        fields = [
            'competition',
            'organization',
            'name',
            'not_resultable'
        ]


class ChangeTeamForm(TeamForm):
    pass
'''

class CompetitionForm(forms.ModelForm):
    class Meta:
        model = Compitition
        fields = [
            'date',
            'place',
            'sport'
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].widget.attrs.update({'type': 'date', 'class': 'form-control kostyl', 'id':"date", 'name':"date", 'placeholder':"Дата"})
        self.fields['place'].widget.attrs.update({'class': 'form-control'})
        self.fields['sport'].widget.attrs.update({'class': 'form-control'})

class JudgeForm(forms.ModelForm):

    class Meta():
        model = CompetitionJudge
        fields =[
            'judge',
            'judge_position',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['judge'].widget.attrs.update({'class': 'form-control'})
        self.fields['judge_position'].widget.attrs.update({'class': 'form-control'})
        #self.fields['DELETE'].widget.attrs.update({'class': 'form-check-input'})
