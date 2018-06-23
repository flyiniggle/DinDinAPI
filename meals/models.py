from django.contrib.postgres.fields import ArrayField
from django.db import models


class Meal(models.Model):
    owner = models.ForeignKey('auth.User',
                              related_name="my_meals",
                              on_delete=models.CASCADE,
                              default=1,
                              editable=False)
    collaborators = models.ManyToManyField('auth.User', related_name="shared_meals")
    name = models.CharField(max_length=100)
    taste = models.PositiveSmallIntegerField()
    difficulty = models.PositiveSmallIntegerField()
    last_used = models.DateField(null=True)
    used_count = models.PositiveSmallIntegerField(blank=True, default=0)
    notes = models.TextField(blank=True, default='')
    ingredients = ArrayField(models.CharField(max_length=100), size=80, default=[])
