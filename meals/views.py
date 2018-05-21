from itertools import chain
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from meals.models import Meal
from meals.serializers import MealSerializer


class MealList(generics.ListCreateAPIView):
    '''
    get:
    Return a list of meals owned by the logged in user.

    post:
    Create a new meal and associate it with the logged in user.
    '''
    serializer_class = MealSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        my_meals = user.my_meals.all()
        shared_meals = user.shared_meals.all()
        meals = list(chain(my_meals, shared_meals))
        return meals

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