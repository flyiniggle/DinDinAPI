# Generated by Django 2.0.3 on 2018-05-19 20:15

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meals', '0004_auto_20180514_1954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='collaborators',
            field=models.ManyToManyField(related_name='shared_meals', to=settings.AUTH_USER_MODEL),
        ),
    ]
