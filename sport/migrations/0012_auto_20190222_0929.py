# Generated by Django 2.1.2 on 2019-02-22 00:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sport', '0011_auto_20190222_0926'),
    ]

    operations = [
        migrations.RenameField(
            model_name='team',
            old_name='compitition',
            new_name='competition',
        ),
        migrations.AddField(
            model_name='compitition',
            name='team_name',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='sport.Team', verbose_name='Команда'),
            preserve_default=False,
        ),
    ]