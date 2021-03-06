from django import forms
from .models import Team, Sport, Department, Competition, Person, Period, TeamMember, Position, CompetitionJudge, TeamResult,Competition_name, Place
#from django_select2.forms import ModelSelect2MultipleWidget, Select2MultipleWidget, Select2Widget
import datetime
from svfusport import settings

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
    competition = forms.ModelChoiceField(queryset=Competition.objects.filter(date__gte=datetime.date.today()).order_by('date'), empty_label='Выберите соревнование',
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

class datewidget(forms.DateInput):
    input_type = 'date'

class CompetitionForm(forms.ModelForm):
    date = forms.DateField(widget=datewidget(), input_formats = settings.DATE_INPUT_FORMATS)
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
        self.fields['date'].widget.attrs.update({'class': 'form-control', 'id':"date", 'name':"date", 'placeholder':"Дата"})
        self.fields['place'].widget.attrs.update({'class': 'form-control input-form-edit'})
        self.fields['sport'].widget.attrs.update({'class': 'form-control input-form-edit'})
        self.fields['result'].widget.attrs.update({'style':'margin-right: 10px; padding-top: 25px;'})


#форма для добавления вида спорта
class Sport_adding_form(forms.ModelForm):
    class Meta:
        model = Sport
        fields = [
            'name',
            'type'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['type'].widget.attrs.update({'class': 'form-control'})


#форма для добавления места проведения
class Place_adding_form(forms.ModelForm):
    class Meta:
        model = Place
        fields = [
            'name',
            'address'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['address'].widget.attrs.update({'class': 'form-control'})


class JudgeForm(forms.ModelForm):

    class Meta:
        model = CompetitionJudge
        fields =[
            'judge',
            'judge_position'
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

    # sportsman = forms.ModelChoiceField(queryset = Person.objects.all(), empty_label = 'Выберите спортсмена',
    #     widget = forms.Select(attrs = {'id': 'sportsman', 'class': 'form-control', 'aria-describedby': 'manHelp',
    #                                    'placeholder': 'Выберите спортсмена', 'name': 'sportsman'}))
    #
    # comments = forms.CharField(max_length = 100, widget = forms.Select(attrs = {'id':'comments', 'class':'form-control', 'aria-describedby':'commHelp', 'placeholder':'Комментарий', 'name' : 'sportcomment'}))

    class Meta:
        model = TeamMember
        fields = [
            'sportsman',
            'comments'
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sportsman'].widget.attrs.update({'class': 'form-control'})
        self.fields['comments'].widget.attrs.update({'class': 'form-control'})


class TeamResult_form(forms.ModelForm):

    # team = forms.ModelChoiceField(queryset=Team.objects.all(), empty_label='Выберите команду',
    #     widget = forms.Select(attrs = {'id':'team', 'class':'form-control', 'aria-describedby':'teamHelp', 'placeholder':'Выберите команду', 'name' : 'team'}))

    class Meta:
        model = TeamResult
        fields = [
            'team',
            'result',
            'points'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['team'].widget.attrs.update({'class': 'form-control'})
        self.fields['result'].widget.attrs.update({'class': 'form-control'})
        self.fields['points'].widget.attrs.update({'class': 'form-control'})
        self.fields['team'].widget.attrs['disabled'] = True
        self.fields['team'].widget.attrs['required'] = False

class TeamResult_form_competition(forms.ModelForm):
    class Meta:
        model = Competition_name
        fields = [
            'competition'
        ]

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['competition'].widget.attrs.update({'class': 'form-control'})


class Period_for_Table_Form(forms.ModelForm):
    begin = forms.DateField(widget = datewidget(), input_formats = settings.DATE_INPUT_FORMATS)
    end = forms.DateField(widget = datewidget(), input_formats = settings.DATE_INPUT_FORMATS)
    class Meta:
        model = Period
        fields = [
            'begin',
            'end'
        ]

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['begin'].widget.attrs.update({'class': 'form-control'})
            self.fields['end'].widget.attrs.update({'class': 'form-control'})


'''Добавить УЧП форма'''
class Uchp_adding_form(forms.ModelForm):
    class Meta:
        model = Department
        fields = [
            'name',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})