from rest_framework import viewsets

from meals.models import Meal
from meals.serializers import MealSerializer


class MealsViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer