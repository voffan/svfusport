from django.db import models
from django.contrib.auth.models import User

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
    name = models.CharField(verbose_name="Название", max_length=200, blank=False)
    address = models.CharField(verbose_name="Адрес", max_length=300, null=True, blank=True)


class Sport(models.Model):
    type = models.CharField(choices=SportType, verbose_name="Тип спорта", max_length=10, blank=False)
    name = models.CharField(verbose_name="Вид спорта", max_length=200, db_index=True, blank=False)
    def __str__(self):
        return self.name

class Period(models.Model):
    name = models.CharField(max_length=100, verbose_name="Период проведения", blank=False)


class Compitition(models.Model):
    date = models.DateTimeField(verbose_name="Дата соревнования", blank=False, null=False)
    name = models.CharField(max_length=200, verbose_name="Наименование соревнования", blank=False)
    '''связи с классами'''
    place = models.ForeignKey(Place, verbose_name="Место", db_index=True, null=True, blank=True, on_delete=models.CASCADE)
    sport = models.ForeignKey(Sport, verbose_name="Вид Спорта", db_index=True, on_delete=models.CASCADE)
    period = models.ForeignKey(Period, verbose_name="Период проведения", db_index=True, on_delete=models.CASCADE)


class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name="Организация", db_index=True)


class ResultTable(models.Model):
    points = models.IntegerField(verbose_name="Очки", db_index=True)
    place = models.IntegerField(verbose_name="Место", db_index=True)
    period = models.ForeignKey(Period, verbose_name="Период проведения", db_index=True, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, verbose_name="Организация", db_index=True, on_delete=models.CASCADE)


class Team(models.Model):
    compitition = models.ForeignKey(Compitition, verbose_name="Вид Спорта", db_index=True, on_delete=models.CASCADE)
    organization = models.ForeignKey(Department, verbose_name="Организация", db_index=True, on_delete=models.CASCADE)


class TeamResult(models.Model):
    compitition = models.ForeignKey(Compitition, verbose_name="Вид Спорта", db_index=True, on_delete=models.CASCADE)
    place = models.IntegerField(verbose_name="Место", null=False)
    team = models.ForeignKey(Team, verbose_name="Команда", db_index=True, on_delete=models.CASCADE)


class Sportsman(models.Model):
    fio = models.CharField(max_length=300, verbose_name="ФИО", db_index=True)
    birthday = models.DateField(verbose_name="Дата рождения", blank=False)
    position = models.ForeignKey('Position', verbose_name="Должность", db_index=True, null=True, blank=True, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, verbose_name="Команда", db_index=True, on_delete=models.CASCADE)
    ''''''


class Position(models.Model):
    name = models.CharField(max_length=200, verbose_name="Наименование", db_index=True)


class SportsmanResult(models.Model):
    compitition = models.ForeignKey(Compitition, verbose_name="Вид Спорта", db_index=True, on_delete=models.CASCADE)
    place = models.IntegerField(verbose_name="Место")
    points = models.DecimalField(verbose_name="Очки", max_length=100, max_digits=7, decimal_places=2)
    sportsman = models.OneToOneField(Sportsman, verbose_name="Спортсмен", db_index=True, on_delete=models.CASCADE)


class Organizator(models.Model):
    fio = models.CharField(verbose_name="ФИО", max_length=300, unique=True, blank=False)
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)


class Judge(models.Model):
    fio = models.CharField(max_length=100, verbose_name="ФИО", blank=False)
    position = models.CharField(max_length=20, choices=JudesType, verbose_name="Класс судьи", blank=False)
    compitition = models.ForeignKey(Compitition, verbose_name="Соревнование", db_index=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)