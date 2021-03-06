# Generated by Django 2.1.2 on 2019-02-08 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sport', '0005_place_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='address',
            field=models.CharField(blank=True, default=1, max_length=300, verbose_name='Адрес'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='teamresult',
            name='place',
            field=models.PositiveIntegerField(verbose_name='Место'),
        ),
    ]
