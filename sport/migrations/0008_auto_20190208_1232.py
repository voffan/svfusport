# Generated by Django 2.1.2 on 2019-02-08 03:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sport', '0007_auto_20190208_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='compitition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sport.Sport', verbose_name='Вид Спорта'),
        ),
    ]