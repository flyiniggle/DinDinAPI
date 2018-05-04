from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """Generate a token whenever a user is created"""
    if created:
        Token.objects.create(user=instance)

class Meal(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100)
    taste = models.PositiveSmallIntegerField()
    difficulty = models.PositiveSmallIntegerField()
    last_used = models.DateField()
    used_count = models.PositiveIntegerField()
    notes = models.TextField()
