from django import forms
from .models import Team, Sport, Department, Competition, Person, TeamMember, Position
#from django_select2.forms import ModelSelect2MultipleWidget, Select2MultipleWidget, Select2Widget
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
    competition = forms.ModelChoiceField(queryset=Competition.objects.filter(date__lte=datetime.date.today()).order_by('date'), empty_label='Выберете соревнование',
        widget = forms.Select(attrs = {'id':'sport', 'class':'form-control', 'aria-describedby':'sportHelp', 'placeholder':'Выберете соревнование', 'name' : 'sport'}))

    organization = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label='Выберете УЧП',
        widget = forms.Select(attrs = {'id':'organzation', 'class':'form-control', 'aria-describedby':'orgHelp', 'placeholder':'Введите организацию', 'name' : 'org'}))

    name = forms.CharField(widget=forms.TextInput(attrs = {'id':'team', 'class':'form-control', 'aria-describedby':'teamHelp', 'placeholder':'Введите название комманды', 'name' : 'team'}))

    class Meta:
        model = Team
        fields = [
            'competition',
            'organization',
            'name',
            'not_resultable',

        ]


#
# class TeamMemberWidget(ModelSelect2MultipleWidget):
#     model = Person
#     queryset=Person.objects.all()
#     search_fields = ['fio__contains']

'''Форма добавления спортсмена '''


class TeamMember_Form(forms.ModelForm):
    team = forms.ModelChoiceField(queryset = Team.objects.all(), empty_label = 'Выберите команду')

    sportsman = forms.ModelChoiceField(queryset = Person.objects.all(), empty_label = 'Выберете спортсмена')

    comments = forms.CharField(max_length = 100)

    class Meta:
        model = TeamMember
        fields = [
            'team',
            'sportsman',
            'comments'
        ]


''' добавление Персон в команду '''


# class Person_Form(forms.Form):
#     fio = forms.ModelMultipleChoiceField(queryset = Person.objects.all(),
#         widget = Select2MultipleWidget)
#
#     position = forms.ModelMultipleChoiceField(queryset = Position.objects.all(),
#         widget = Select2MultipleWidget)
#
#     class Meta:
#         model = Person
#         fields = [
#             'fio',
#             'position',
#         ]
