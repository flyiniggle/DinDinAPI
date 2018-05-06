from rest_framework import generics, permissions
from meals.models import Meal
from meals.serializers import MealSerializer


class MealList(generics.ListCreateAPIView):
    serializer_class = MealSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Meal.objects.filter(owner=user)

class MealDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
