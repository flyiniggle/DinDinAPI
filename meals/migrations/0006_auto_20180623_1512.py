# Generated by Django 2.0.3 on 2018-06-23 19:12

import django.contrib.postgres.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('meals', '0005_auto_20180519_1615'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='ingredients',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), default=[],
                                                            size=80),
        ),
        migrations.AlterField(
            model_name='meal',
            name='owner',
            field=models.ForeignKey(default=1, editable=False, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='my_meals', to=settings.AUTH_USER_MODEL),
        ),
    ]
