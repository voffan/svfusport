from django import forms
from .models import Team, Sport, Department, Competition
import datetime

'''
class SportName(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s"%obj.name


class TeamForm(forms.ModelForm):
    sport = SportName(label = 'Вид спорта', queryset = Sport.objects.order_by('name'))
    org = SportName(label = 'Организация', queryset = Department.objects.order_by('name'))
    name = forms.CharField(label = 'Команда', max_length = 100)
'''


    #not_res = forms.BooleanField()

class TeamForm(forms.ModelForm):
    competition = forms.ModelChoiceField(queryset=Competition.objects.filter(date__lte=datetime.date.today()).order_by('date'), empty_label='Выберете соревнование')
    organization = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label='Выберете УЧП')
    class Meta:
        model = Team
        fields = [
            'competition',
            'organization',
            'name',
            'not_resultable'
        ]

'''
class TeamChangeForm(forms.ModelForm):
    competition = 
'''