from rest_framework import generics
from meals.models import Meal
from meals.serializers import MealSerializer


class MealList(generics.ListAPIView):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

class MealDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
