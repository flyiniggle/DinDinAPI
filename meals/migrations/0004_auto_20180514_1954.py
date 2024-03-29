# Generated by Django 2.0.3 on 2018-05-14 23:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meals', '0003_auto_20180506_1526'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='collaborators',
            field=models.ManyToManyField(null=True, related_name='shared_meals', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='meal',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='my_meals', to=settings.AUTH_USER_MODEL),
        ),
    ]
