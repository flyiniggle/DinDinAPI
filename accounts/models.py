from django.db import models


class PendingCollaboration(models.Model):
    owner = models.ForeignKey('auth.User',
                              related_name="pending_collaborations",
                              on_delete=models.CASCADE)
    meal = models.ForeignKey('meals.Meal',
                             related_name="pending_collaborator",
                             on_delete=models.CASCADE)
    collaborator = models.ForeignKey('auth.User',
                                     related_name="new_shared_meals",
                                     on_delete=models.CASCADE)
