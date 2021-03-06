# Generated by Django 2.1.2 on 2018-11-08 05:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Compitition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='Дата соревнования')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='Организация')),
            ],
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Период проведения')),
                ('begin', models.DateField(max_length=100, verbose_name='Начало соревнований')),
                ('end', models.DateField(max_length=100, verbose_name='Конец соревнований')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fio', models.CharField(db_index=True, max_length=300, verbose_name='ФИО')),
                ('birthday', models.DateField(verbose_name='Дата рождения')),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('address', models.CharField(blank=True, max_length=300, null=True, verbose_name='Адрес')),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200, verbose_name='Наименование')),
            ],
        ),
        migrations.CreateModel(
            name='ResultTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField(db_index=True, verbose_name='Очки')),
                ('place', models.IntegerField(db_index=True, verbose_name='Место')),
                ('compitition', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sport.Compitition', verbose_name='Соревнование')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sport.Department', verbose_name='Организация')),
            ],
        ),
        migrations.CreateModel(
            name='Sport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('лич.', 'Личный'), ('ком.', 'Командный'), ('л.-к.', 'Лично-командный')], db_index=True, max_length=10, verbose_name='Тип спорта')),
                ('name', models.CharField(db_index=True, max_length=200, verbose_name='Вид спорта')),
            ],
        ),
        migrations.CreateModel(
            name='SportsmanResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.IntegerField(verbose_name='Место')),
                ('points', models.DecimalField(decimal_places=2, max_digits=7, max_length=100, verbose_name='Очки')),
                ('compitition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sport.Compitition', verbose_name='Вид Спорта')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('compitition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sport.Compitition', verbose_name='Вид Спорта')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sport.Department', verbose_name='Организация')),
            ],
        ),
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='TeamResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.IntegerField(verbose_name='Место')),
                ('compitition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sport.Compitition', verbose_name='Вид Спорта')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sport.Team', verbose_name='Команда')),
            ],
        ),
        migrations.CreateModel(
            name='Judge',
            fields=[
                ('person_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sport.Person')),
                ('judge_position', models.CharField(choices=[('гл.судья', 'Главный судья'), ('судья', 'Cудья')], max_length=20, verbose_name='Класс судьи')),
            ],
            bases=('sport.person',),
        ),
        migrations.CreateModel(
            name='Organizator',
            fields=[
                ('person_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sport.Person')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            bases=('sport.person',),
        ),
        migrations.AddField(
            model_name='teammember',
            name='sportsman',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sport.Person', verbose_name='Спортсмен'),
        ),
        migrations.AddField(
            model_name='teammember',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sport.Team', verbose_name='Команда'),
        ),
        migrations.AddField(
            model_name='sportsmanresult',
            name='sportsman',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sport.TeamMember', verbose_name='Спортсмен'),
        ),
        migrations.AddField(
            model_name='compitition',
            name='period',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sport.Period', verbose_name='Период проведения'),
        ),
        migrations.AddField(
            model_name='compitition',
            name='place',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sport.Place', verbose_name='Место'),
        ),
        migrations.AddField(
            model_name='compitition',
            name='sport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sport.Sport', verbose_name='Вид Спорта'),
        ),
        migrations.AddField(
            model_name='judge',
            name='compitition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sport.Compitition', verbose_name='Соревнование'),
        ),
        migrations.AddField(
            model_name='judge',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
