from django.db import models


class Meal(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100)
    taste = models.PositiveSmallIntegerField()
    difficulty = models.PositiveSmallIntegerField()
    last_used = models.DateField()
    used_count = models.PositiveIntegerField()
    notes = models.TextField()
