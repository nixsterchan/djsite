# Generated by Django 2.1.5 on 2019-04-01 06:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20190401_0617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutorial',
            name='tutorial_published',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 1, 6, 17, 51, 705591), verbose_name='date published'),
        ),
    ]
