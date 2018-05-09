from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from meals.models import Meal
from meals.serializers import MealSerializer


class MealList(generics.ListCreateAPIView):
    serializer_class = MealSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Meal.objects.filter(owner=user)

    def get_object(self):
        key = self.kwargs["pk"]
        obj = get_object_or_404(self.get_queryset(), pk=key)
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MealDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MealSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        key = self.kwargs["pk"]
        return Meal.objects.filter(pk=key)

    def get_object(self):
        user = self.request.user
        obj = get_object_or_404(self.get_queryset(), owner=user)
        self.check_object_permissions(self.request, obj)
        return obj