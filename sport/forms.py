from django import forms
from .models import Team, Sport, Department, Competition, Person, TeamMember, Position, CompetitionJudge, TeamResult,Competition_name
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
    competition = forms.ModelChoiceField(queryset=Competition.objects.filter(date__lte=datetime.date.today()).order_by('date'), empty_label='Выберите соревнование',
        widget = forms.Select(attrs = {'id':'sport', 'class':'form-control', 'aria-describedby':'sportHelp', 'placeholder':'Выберите соревнование', 'name' : 'sport'}))

    organization = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label='Выберете УЧП',
        widget = forms.Select(attrs = {'id':'organzation', 'class':'form-control', 'aria-describedby':'orgHelp', 'placeholder':'Введите организацию', 'name' : 'org'}))

    name = forms.CharField(widget=forms.TextInput(attrs = {'id':'team', 'class':'form-control', 'aria-describedby':'teamHelp', 'placeholder':'Введите название комманды', 'name' : 'team'}))

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


class CompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = [
            'date',
            'place',
            'sport',
            'result'
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


#
# class TeamMemberWidget(ModelSelect2MultipleWidget):
#     model = Person
#     queryset=Person.objects.all()
#     search_fields = ['fio__contains']

#Форма добавления спортсмена


class TeamMember_Form(forms.ModelForm):
    #team = forms.ModelChoiceField(queryset = Team.objects.all(), empty_label = 'Выберите команду')

    sportsman = forms.ModelChoiceField(queryset = Person.objects.all(), empty_label = 'Выберите спортсмена')

    comments = forms.CharField(max_length = 100)

    class Meta:
        model = TeamMember
        fields = [
            'sportsman',
            'comments'
        ]


class TeamResult_form(forms.ModelForm):

    team = forms.ModelChoiceField(queryset=Team.objects.all(), empty_label='Выберите команду',
        widget = forms.Select(attrs = {'id':'team', 'class':'form-control', 'aria-describedby':'teamHelp', 'placeholder':'Выберите команду', 'name' : 'team'}))

    class Meta:
        model = TeamResult
        fields = [
            'team',
            'result',
            'points'
        ]


class TeamResult_form_competition(forms.ModelForm):
    class Meta:
        model = Competition_name
        fields = [
            'competition'
        ]

#добавление Персон в команду

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
#             'position'
#         ]
