# Generated by Django 2.1.2 on 2019-02-08 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sport', '0004_remove_place_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='name',
            field=models.CharField(default=1, max_length=200, verbose_name='Название'),
            preserve_default=False,
        ),
    ]
