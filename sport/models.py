# Create your models here.
from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
SportType = (
    ('лич.', 'Личный'),
    ('ком.', 'Командный'),
    ('л.-к.', 'Лично-командный')
           )


JudesType = (
    ('гл.судья', 'Главный судья'),
    ('судья', 'Cудья')
            )

'''начало организации мероприятий'''


class Place(models.Model):
    name = models.CharField(verbose_name="Название", max_length=200)
    address = models.CharField(verbose_name="Адрес", max_length=300)

    def __str__(self):
        return self.address


class Sport(models.Model):
    type = models.CharField(choices=SportType, verbose_name="Тип спорта", max_length=10)
    name = models.CharField(verbose_name="Вид спорта", max_length=200, db_index=True)

    class Meta:
        ordering = ['name']
        verbose_name = "вид спорта"
        verbose_name_plural = "виды спорта"

    def __str__(self):
        return self.name


class Period(models.Model):
    begin = models.DateField(max_length=100, verbose_name="Начало соревнований")
    end = models.DateField(max_length=100, verbose_name="Конец соревнований")

    def __str__(self):
        return str(self.begin)+"-"+str(self.end)


class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name="Организация", db_index=True)

    def __str__(self):
        return self.name


class Competition(models.Model):
    date = models.DateField(verbose_name = "Дата соревнования", default=datetime.date.today())
    place = models.ForeignKey(Place, verbose_name = "Место проведения", null = True, blank = True, on_delete = models.CASCADE)
    sport = models.ForeignKey(Sport, verbose_name = "Вид Спорта", db_index = True, on_delete = models.CASCADE)
    result = models.BooleanField(verbose_name="Проведено", default = False)

    def __str__(self):
        return self.sport.name + '(' + str(self.date) + ')'


class Competition_name(models.Model):
    competition = models.ForeignKey(Competition, verbose_name = "Соревнование", null = True, blank = True, on_delete = models.CASCADE)


class Team(models.Model):
    competition = models.ForeignKey(Competition, verbose_name="Соревнование", db_index=True, on_delete=models.CASCADE)
    organization = models.ForeignKey(Department, verbose_name="Организация", db_index=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name= "Название команды", db_index=True)
    not_resultable = models.BooleanField(verbose_name='В зачете', default=False)

    def __str__(self):
        return self.organization.name + ' : команда -- : ' + self.name


'''class ResultTable(models.Model):
    points = models.IntegerField(verbose_name="Очки", db_index=True)
    result = models.PositiveIntegerField(verbose_name= "Место", db_index=True)
    department = models.ForeignKey(Department, verbose_name="Организация", db_index=True)
    compitition = models.ForeignKey(Competition, verbose_name="Соревнование", db_index=True)
    team = models.ForeignKey(Team, verbose_name = "Команда", db_index=True)

    def __str__(self):
       return self.compitition.place.name'''


class TeamResult(models.Model):
    points = models.PositiveIntegerField(verbose_name = "Очки", null=True, blank=True)
    competition = models.ForeignKey(Competition, verbose_name = "Соревнование", db_index = True, on_delete=models.CASCADE)
    result = models.PositiveIntegerField(verbose_name= "Место", null=True, blank=True)
    team = models.ForeignKey(Team, verbose_name="Команда", db_index=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.team.organization.name


class Position(models.Model):
    name = models.CharField(max_length=200, verbose_name="Наименование", db_index=True)

    def __str__(self):
        return self.name


class Person(models.Model):
    fio = models.CharField(max_length=300, verbose_name="ФИО", db_index=True)
    position = models.ForeignKey(Position, default=None, verbose_name='Должность', on_delete=models.CASCADE)

    def __str__(self):
        return self.fio


class TeamMember(models.Model):
    team = models.ForeignKey(Team, verbose_name="Команда", db_index=True, on_delete=models.CASCADE)
    sportsman = models.ForeignKey(Person, verbose_name="Спортсмен", db_index=True, on_delete=models.CASCADE)
    comments = models.CharField(verbose_name = 'Комментарии', max_length = 512, blank = True, null = True)

    def __str__(self):
        return self.sportsman.fio


class SportsmanResult(models.Model):
    competition = models.ForeignKey(Competition, verbose_name= "Вид Спорта", db_index=True, null=True, on_delete=models.CASCADE)
    place = models.IntegerField(verbose_name="Место")
    points = models.DecimalField(verbose_name="Очки", max_length=100, max_digits=7, decimal_places=2)
    sportsman = models.OneToOneField(TeamMember, verbose_name="Спортсмен", db_index=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.sportsman.name + ' ' + str(self.place)


class Organizator(Person):

    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)

    def __str__(self):
        return self.fio


class Judge(Person):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)

    def __str__(self):
        return self.fio

class CompetitionJudge(models.Model):
    judge = models.ForeignKey(Judge, verbose_name='Судья', on_delete=models.CASCADE)
    judge_position = models.CharField(max_length=20, choices=JudesType, verbose_name="Класс судьи", blank=False)
    competition = models.ForeignKey(Competition, verbose_name="Соревнование", null=True, db_index=True, on_delete=models.CASCADE)


class ResultDepart(models.Model):
    competition = models.ForeignKey(Competition, verbose_name = "Соревнование", null = True, db_index = True,
        on_delete = models.CASCADE)
    department = models.ForeignKey(Department, verbose_name = "Организация", db_index = True,
        on_delete = models.CASCADE)
    total = models.IntegerField(verbose_name = "Итог")
    points = models.IntegerField(verbose_name = "Место")